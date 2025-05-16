from apps.products.models import Product

def get_cart_items(request):
    session_cart = request.session.get('cart', {})
    items = []
    for product_id, data in session_cart.items():
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            continue  # безопасно пропускаем удалённые товары

        items.append({
            'product': product,
            'size': data.get('size'),
            'quantity': data.get('quantity', 1),
        })
    return items
