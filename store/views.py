from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from .forms import ProductForm
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
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product_detail.html', {'product': product})


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('store:product_detail', slug=product.slug)
    else:
        form = ProductForm()

    return render(request, 'product_form.html', {
        'form': form,
        'title': 'Add Product',
        'submit_label': 'Add product',
    })


def product_update(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            return redirect('store:product_detail', slug=product.slug)
    else:
        form = ProductForm(instance=product)

    return render(request, 'product_form.html', {
        'form': form,
        'product': product,
        'title': 'Update Product',
        'submit_label': 'Save changes',
    })


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('store:home')
