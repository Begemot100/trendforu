from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.products.views import toggle_favorite

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("apps.users.urls")),
    path("products/", include("apps.products.urls")),
    path("orders/", include("apps.orders.urls")),
    path("cart/", include("apps.cart.urls")),
    path("", include("apps.core.urls")),
    path("shop/", include("apps.products.urls")),
    path("favorite/<int:product_id>/", toggle_favorite, name="toggle_favorite"),
    path("cart/", include("apps.cart.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Обслуживание медиафайлов в режиме DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# URL configuration here
