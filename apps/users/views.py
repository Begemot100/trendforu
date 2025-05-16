import logging
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseServerError, JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

from .forms import UserRegistrationForm, UserLoginForm, ProfileForm

from apps.orders.models import Order
from apps.cart.models import CartItem
from apps.users.models import Profile
from ..products.models import Favorite, Product


logger = logging.getLogger(__name__)

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('home')
            form.add_error(None, 'Неверный email или пароль')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def profile_view(request):
    try:
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)
        logger.info(f"Профиль для {user.email}: создан={created}, аватар={profile.avatar.url if profile.avatar else 'нет'}")
        form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
        if request.method == 'POST':
            logger.info(f"POST данные: {request.POST}, Файлы: {request.FILES}")
            if form.is_valid():
                form.save()
                logger.info(f"Аватар сохранен: {profile.avatar.url if profile.avatar else 'нет'}")
                return redirect('profile')
            else:
                logger.warning(f"Ошибки формы: {form.errors}")
        favorites = Favorite.objects.filter(user=user).select_related('product')
        cart_items_raw = CartItem.objects.filter(user=user).select_related('product')
        safe_items = []
        cart_total = 0
        for item in cart_items_raw:
            if not item.product:
                logger.warning(f"Элемент корзины без продукта: ID {item.id}")
                continue
            try:
                item_total = item.product.price * item.quantity
                cart_total += item_total
                safe_items.append(item)
            except Exception as e:
                logger.warning(f"Ошибка в элементе корзины {item.id}: {e}")
        orders = Order.objects.filter(user=user)
        return render(request, 'users/profile.html', {
            'form': form,
            'profile': profile,
            'cart_items': safe_items,
            'cart_total': cart_total,
            'orders': orders,
            'favorites': favorites,
        })
    except Exception as e:
        logger.exception(f"Ошибка в profile_view: {e}")
        return HttpResponseServerError("Ошибка при загрузке профиля")
def logout_view(request):
    logout(request)
    return redirect('login')


@csrf_exempt  
@login_required
def toggle_favorite(request, product_id):
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=product_id)
            favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
            if not created:
                favorite.delete()
                action = 'removed'
            else:
                action = 'added'
            likes_count = product.liked_by.count()
            return JsonResponse({
                'success': True,
                'action': action,
                'likes_count': likes_count
            })
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Товар не найден'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Неверный метод'}, status=405)


@login_required
def favorite_status(request, product_id):
    if request.method == 'GET':
        try:
            product = Product.objects.get(id=product_id)
            is_favorited = Favorite.objects.filter(user=request.user, product=product).exists()
            likes_count = product.liked_by.count()
            return JsonResponse({
                'success': True,
                'is_favorited': is_favorited,
                'likes_count': likes_count
            })
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Товар не найден'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Неверный метод'}, status=405)

def shop(request):
    try:
        products = Product.objects.all().prefetch_related('images', 'size_variants')
        favorites = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True) if request.user.is_authenticated else []
        return render(request, 'users/shop.html', {
            'products': products,
            'favorites': favorites,
            'csrf_token': request.META.get('CSRF_COOKIE', ''),
        })
    except Exception as e:
        logger.exception("Ошибка в shop_view")
        return HttpResponseServerError("Ошибка при загрузке магазина")
