from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<slug:slug>/', views.CategoryProductsView.as_view(), name='category_products'),
    path('sale/', views.SaleProductsView.as_view(), name='sale_products'),
    path('product/add/', views.ProductCreateView.as_view(), name='product_create'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product/<slug:slug>/edit/', views.ProductUpdateView.as_view(), name='product_update'),
    path('product/<slug:slug>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
]
