# Product views
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import Product, Category, Favorite

def product_list(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

# def shop_view(request):
#     products = Product.objects.filter(is_active=True).order_by('-created_at')
#     return render(request, 'products/shop.html', {'products': products})

def shop_view(request):
    products = Product.objects.prefetch_related('images', 'size_variants').filter(is_active=True)
    categories = Category.objects.all()
    # Подробная отладочная информация
    print("Categories fetched in shop_view:", categories)
    print("Category IDs and Names:", [(cat.id, cat.name) for cat in categories])
    print("Number of categories:", categories.count())
    favorites = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True) if request.user.is_authenticated else []
    context = {
        'products': products,
        'categories': categories,
        'favorites': favorites,
    }
    print("Context being passed to template:", context)
    return render(request, 'products/shop.html', context)


@csrf_exempt  # Временно для отладки, в продакшене лучше использовать CSRF-токен
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
