# Cart models
from django.conf import settings
from django.db import models

from apps.products.models import Product


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=20, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product", "size")

    def get_total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"
