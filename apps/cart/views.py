# apps/cart/views.py
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseServerError
from apps.products.models import Product
from .models import CartItem
import logging

from ..products.models import ProductSize

logger = logging.getLogger(__name__)

def cart_view(request):
    try:
        items = []
        total = 0
        if request.user.is_authenticated:
            logger.info(f"Загрузка корзины для пользователя: {request.user.email}")
            cart_items = CartItem.objects.filter(user=request.user).select_related('product')
            logger.info(f"Найдено элементов корзины: {cart_items.count()}, IDs: {[item.id for item in cart_items]}")
            for item in cart_items:
                if not item.product:
                    logger.warning(f"Элемент корзины без продукта: ID {item.id}")
                    continue
                try:
                    items.append({
                        'id': item.id,
                        'product': item.product,
                        'size': item.size,
                        'quantity': item.quantity,
                        'total_price': item.get_total_price()
                    })
                    total += item.get_total_price()
                except Exception as e:
                    logger.warning(f"Ошибка в элементе корзины {item.id}: {e}")
        else:
            logger.info("Загрузка корзины для гостя")
            session_cart = request.session.get('cart', [])
            for entry in session_cart:
                try:
                    product = Product.objects.get(pk=entry['product_id'])
                    item_total = product.price * entry['quantity']
                    items.append({
                        'id': None,  # Для гостей нет ID
                        'product': product,
                        'size': entry['size'],
                        'quantity': entry['quantity'],
                        'total_price': item_total
                    })
                    total += item_total
                except Product.DoesNotExist:
                    logger.warning(f"Продукт {entry['product_id']} не найден")
                    continue
            logger.info(f"Найдено элементов корзины для гостя: {len(items)}")

        return render(request, 'cart/cart.html', {
            'items': items,
            'total': total
        })
    except Exception as e:
        logger.exception(f"Ошибка в cart_view: {e}")
        return HttpResponseServerError("Ошибка при загрузке корзины")

@require_POST
@login_required
def cart_update(request, item_id):
    try:
        data = request.POST or json.loads(request.body)
        quantity = int(data.get("quantity", 1))
        item = get_object_or_404(CartItem, id=item_id, user=request.user)
        item.quantity = quantity
        item.save()
        return JsonResponse({"success": True})
    except Exception as e:
        logger.exception("Ошибка в cart_update")
        return JsonResponse({"success": False, "error": str(e)}, status=500)





@require_POST
def add_to_cart(request, product_id):
    """
    Add an item to the cart for both authenticated and guest users.
    Replaces the problematic add_to_cart and cart_add views.
    """
    try:
        data = json.loads(request.body) if request.body else request.POST
        size = data.get('size')
        quantity = int(data.get('quantity', 1))

        product = get_object_or_404(Product, pk=product_id)

        # Validate stock if size is provided
        if size:
            try:
                product_size = ProductSize.objects.get(product=product, size=size)
                if quantity > product_size.stock:
                    return JsonResponse({
                        'success': False,
                        'error': f'Only {product_size.stock} items available'
                    }, status=400)
            except ProductSize.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Selected size not available'
                }, status=400)

        if request.user.is_authenticated:
            logger.info(f"Adding to cart for user {request.user.email}: product {product_id}, size {size}, qty {quantity}")
            item, created = CartItem.objects.get_or_create(
                user=request.user,
                product=product,
                size=size if size else None,
                defaults={'quantity': quantity}
            )
            if not created:
                new_quantity = item.quantity + quantity
                if size and new_quantity > product_size.stock:
                    return JsonResponse({
                        'success': False,
                        'error': f'Only {product_size.stock} items available'
                    }, status=400)
                item.quantity = new_quantity
                item.save()
            logger.debug(f"Cart item {'created' if created else 'updated'}: ID {item.id}")
        else:
            logger.info(f"Adding to guest cart: product {product_id}, size {size}, qty {quantity}")
            session_cart = request.session.get('cart', [])
            for entry in session_cart:
                if entry['product_id'] == product_id and entry['size'] == size:
                    new_quantity = entry['quantity'] + quantity
                    if size and new_quantity > product_size.stock:
                        return JsonResponse({
                            'success': False,
                            'error': f'Only {product_size.stock} items available'
                        }, status=400)
                    entry['quantity'] = new_quantity
                    break
            else:
                session_cart.append({
                    'product_id': product_id,
                    'size': size,
                    'quantity': quantity
                })
            request.session['cart'] = session_cart
            request.session.modified = True
            logger.debug(f"Updated guest cart: {session_cart}")

        return JsonResponse({
            'success': True,
            'quantity': quantity,
            'total_items': sum(item.quantity for item in CartItem.objects.filter(user=request.user)) if request.user.is_authenticated else sum(entry['quantity'] for entry in session_cart)
        })
    except Product.DoesNotExist:
        logger.warning(f"Product {product_id} not found")
        return JsonResponse({'success': False, 'error': 'Product not found'}, status=404)
    except Exception as e:
        logger.exception(f"Error in add_to_cart: {e}")
        return JsonResponse({'success': False, 'error': 'An error occurred'}, status=500)

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, user=request.user)
    item.delete()
    return redirect('cart_view')

def create_order_guest(request):
    session_cart = request.session.get('cart', [])
    items = []
    total = 0

    for entry in session_cart:
        try:
            product = Product.objects.get(pk=entry['product_id'])
            item = {
                'product': product,
                'size': entry['size'],
                'quantity': entry['quantity'],
                'total_price': product.price * entry['quantity']
            }
            total += item['total_price']
            items.append(item)
        except Product.DoesNotExist:
            continue

    return render(request, 'orders/guest_checkout.html', {
        'items': items,
        'total': total
    })

@login_required
def cart_add(request, product_id):
    try:
        product = get_object_or_404(Product, pk=product_id)
        item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1}
        )
        if not created:
            item.quantity += 1
            item.save()

        return JsonResponse({'success': True, 'quantity': item.quantity})
    except Exception as e:
        import traceback
        traceback.print_exc()  # 🔥 покажет точную ошибку в Railway log
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
def update_cart(request, item_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            quantity = int(data.get('quantity', 1))
            item = get_object_or_404(CartItem, id=item_id, user=request.user)
            item.quantity = quantity
            item.save()
            print(f"[update_cart] Updated item {item_id} to qty={quantity} for user={request.user}")
            return JsonResponse({'success': True})
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=400)
@login_required
def cart_decrease(request, product_id):
    item = get_object_or_404(CartItem, user=request.user, product__id=product_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('profile')

@require_POST
@login_required
def cart_delete(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('profile')


# AJAX версии (без перезагрузки)
@require_POST
@login_required
def cart_increase(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.quantity += 1
    item.save()
    return JsonResponse({'status': 'ok'})

@require_POST
@login_required
def cart_decrease_ajax(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    return JsonResponse({'status': 'ok'})

@require_POST
@login_required
def cart_delete_ajax(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return JsonResponse({'status': 'ok'})
