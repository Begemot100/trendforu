from django.urls import path

from . import views

urlpatterns = [
    path("", views.cart_view, name="cart"),
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/guest/", views.create_order_guest, name="create_order_guest"),
    path("increase/<int:item_id>/", views.cart_increase, name="cart_increase"),
    path("decrease/<int:item_id>/", views.cart_decrease, name="cart_decrease"),
    path("delete/<int:item_id>/", views.cart_delete, name="cart_delete"),
    path("update/<int:item_id>/", views.cart_update, name="cart_update"),
]
