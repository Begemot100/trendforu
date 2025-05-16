# products/admin.py
from django.contrib import admin
from .models import Product, ProductSize, Category, ProductImage

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1
    min_num = 1

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'slug']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'stock', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['title']
    inlines = [ProductImageInline, ProductSizeInline]

admin.site.register(ProductSize)
