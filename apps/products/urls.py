from django.urls import path

from .views import product_detail, product_list, shop_view

urlpatterns = [
    path("", product_list, name="product_list"),  # ← именно этот URL
    path("shop/", product_list, name="shop"),  # ← добавь этот путь
    path("<int:pk>/", product_detail, name="product_detail"),
    path("", shop_view, name="shop"),
]
