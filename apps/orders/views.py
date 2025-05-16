# Order views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Order, OrderItem
from apps.cart.cart import get_cart_items  # предполагается, будет реализован
from django.db import transaction

@login_required
def create_order(request):
    cart_items = get_cart_items(request)
    if not cart_items:
        return redirect('cart_view')

    if request.method == 'POST':
        with transaction.atomic():
            order = Order.objects.create(user=request.user)
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    size=item['size'],
                    quantity=item['quantity'],
                    price=item['product'].price,
                )
        # Очистка корзины — предполагается отдельная реализация
        request.session['cart'] = {}
        return redirect('order_success')

    return render(request, 'orders/confirm_order.html', {'cart_items': cart_items})
