# apps/core/views.py
from django.shortcuts import render


def home_view(request):
    return render(request, "core/home.html", {"image_range": range(1, 21)})
