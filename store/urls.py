from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('sale/', views.sale_products, name='sale_products'),
    path('product/add/', views.product_create, name='product_create'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product/<slug:slug>/edit/', views.product_update, name='product_update'),
    path('product/<slug:slug>/delete/', views.product_delete, name='product_delete'),
]
