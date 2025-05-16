from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ['email', 'username', 'is_staff', 'is_active']
    search_fields = ['email', 'username']
    ordering = ['email']
    # ❗ НЕ добавляй повторно email в fieldsets → уже унаследован

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'phone']
    search_fields = ['user__email', 'address', 'phone']
