# apps/users/templatetags/template_filters.py
from django import template

register = template.Library()


@register.filter
def replace(value, arg):
    """Заменяет подстроку в значении. Аргумент: 'old:new'"""
    try:
        # Разделяем только по первому двоеточию, чтобы избежать проблем с URL-ами
        old, new = arg.split(":", 1)
        return value.replace(old, new)
    except ValueError as e:
        # Логируем ошибку, но возвращаем исходное значение, чтобы избежать сбоя
        from django.utils.log import getLogger

        logger = getLogger(__name__)
        logger.warning(f"Ошибка в фильтре replace с аргументом '{arg}': {e}")
        return value
