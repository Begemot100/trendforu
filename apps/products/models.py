# Product models
from django.db import models
from cloudinary.models import CloudinaryField
from django.conf import settings
from apps.users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # ← просто хранение локально
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    size_string = models.CharField(max_length=100, help_text="Comma-separated sizes like: S,M,L")
    stock = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# products/models.py

class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image')
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.product.title} image"

class ProductSize(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='size_variants',  # ← новое имя
        on_delete=models.CASCADE
    )
    size = models.CharField(
        max_length=10,
        choices=[('XXS', 'XXS'), ('XS', 'XS'), ('S', 'S'),
                 ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL')]
    )
    stock = models.PositiveIntegerField(default=0)


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='liked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')