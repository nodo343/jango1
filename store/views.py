from django.shortcuts import get_object_or_404, render

from .models import Product, Category


def home(request):
    products = Product.objects.filter(available=True).order_by('price')
    return render(request, 'home.html', {'products': products})


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(available=True).order_by('price')
    return render(request, 'category_products.html', {'category': category, 'products': products})


def sale_products(request):
    products = Product.objects.filter(available=True, is_on_sale=True).order_by('price')
    return render(request, 'sale.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'product_detail.html', {'product': product})
