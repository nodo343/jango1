from django.db.models import Case, DecimalField, F, Q, When
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Product, Category


SORT_OPTIONS = (
    ('price_asc', 'Price: low to high'),
    ('price_desc', 'Price: high to low'),
    ('name_asc', 'Name: A to Z'),
    ('name_desc', 'Name: Z to A'),
    ('newest', 'Newest first'),
    ('oldest', 'Oldest first'),
)

SORT_FIELDS = {
    'price_asc': 'display_price',
    'price_desc': '-display_price',
    'name_asc': 'name',
    'name_desc': '-name',
    'newest': '-created',
    'oldest': 'created',
}


def filter_and_sort_products(request, products, *, force_sale=False, allow_category_filter=True):
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    sale_only = force_sale or request.GET.get('sale') == 'on'
    sort = request.GET.get('sort', 'price_asc')

    products = products.annotate(
        display_price=Case(
            When(is_on_sale=True, discount_price__isnull=False, then=F('discount_price')),
            default=F('price'),
            output_field=DecimalField(max_digits=10, decimal_places=2),
        )
    )

    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(category__name__icontains=query)
        )

    if allow_category_filter and category_slug:
        products = products.filter(category__slug=category_slug)

    if sale_only:
        products = products.filter(is_on_sale=True)

    if sort not in SORT_FIELDS:
        sort = 'price_asc'

    return products.order_by(SORT_FIELDS[sort], 'name'), {
        'query': query,
        'category_slug': category_slug if allow_category_filter else '',
        'sale_only': sale_only,
        'force_sale': force_sale,
        'sort': sort,
        'sort_options': SORT_OPTIONS,
        'allow_category_filter': allow_category_filter,
    }


def home(request):
    products, filters = filter_and_sort_products(
        request,
        Product.objects.filter(available=True),
    )
    return render(request, 'home.html', {'products': products, 'filters': filters})


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products, filters = filter_and_sort_products(
        request,
        category.products.filter(available=True),
        allow_category_filter=False,
    )
    return render(request, 'category_products.html', {
        'category': category,
        'products': products,
        'filters': filters,
    })


def sale_products(request):
    products, filters = filter_and_sort_products(
        request,
        Product.objects.filter(available=True),
        force_sale=True,
    )
    return render(request, 'sale.html', {'products': products, 'filters': filters})


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


def product_delete(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        product.delete()
        return redirect('store:home')

    return render(request, 'product_confirm_delete.html', {'object': product})
