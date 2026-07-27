from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from .forms import ProductForm
from .models import Product, Category


def get_categories():
    return Category.objects.annotate(product_count=Count('products')).filter(product_count__gt=0)


def home(request):
    products = Product.objects.filter(available=True).order_by('price')
    categories = get_categories()
    return render(request, 'home.html', {'products': products, 'categories': categories})


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(available=True).order_by('price')
    categories = get_categories()
    return render(request, 'category_products.html', {'category': category, 'products': products, 'categories': categories})


def sale_products(request):
    products = Product.objects.filter(available=True, is_on_sale=True).order_by('price')
    categories = get_categories()
    return render(request, 'sale.html', {'products': products, 'categories': categories})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    categories = get_categories()
    return render(request, 'product_detail.html', {'product': product, 'categories': categories})


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
        'categories': get_categories(),
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
        'categories': get_categories(),
        'title': 'Update Product',
        'submit_label': 'Save changes',
    })


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('store:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_categories()
        return context
