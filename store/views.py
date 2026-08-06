from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ProductForm
from .models import Product, Category


class HomeView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(available=True).order_by('price')


class CategoryProductsView(ListView):
    template_name = 'category_products.html'
    context_object_name = 'products'

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, slug=kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.category.products.filter(available=True).order_by('price')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class SaleProductsView(ListView):
    model = Product
    template_name = 'sale.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(available=True, is_on_sale=True).order_by('price')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Product'
        context['submit_label'] = 'Add product'
        return context

    def get_success_url(self):
        return reverse_lazy('store:product_detail', kwargs={'slug': self.object.slug})


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Product'
        context['submit_label'] = 'Save changes'
        return context

    def get_success_url(self):
        return reverse_lazy('store:product_detail', kwargs={'slug': self.object.slug})


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('store:home')
