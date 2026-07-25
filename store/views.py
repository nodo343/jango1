from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Product, Category


def home(request):
    products = Product.objects.filter(available=True).order_by('price')
    categories = Category.objects.annotate(product_count=Count('products')).filter(product_count__gt=0)
    return render(request, 'home.html', {'products': products, 'categories': categories})


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(available=True).order_by('price')
    categories = Category.objects.annotate(product_count=Count('products')).filter(product_count__gt=0)
    return render(request, 'category_products.html', {'category': category, 'products': products, 'categories': categories})


def sale_products(request):
    products = Product.objects.filter(available=True, is_on_sale=True).order_by('price')
    categories = Category.objects.annotate(product_count=Count('products')).filter(product_count__gt=0)
    return render(request, 'sale.html', {'products': products, 'categories': categories})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    categories = Category.objects.annotate(product_count=Count('products')).filter(product_count__gt=0)
    return render(request, 'product_detail.html', {'product': product, 'categories': categories})
