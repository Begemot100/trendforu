from django.urls import path
from . import views
from apps.cart import views as cart_views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('favorite/<int:product_id>/', views.toggle_favorite, name='toggle_favorite'),

    # Корзина — используем views из apps.cart

]
