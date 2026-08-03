from django.db.models import Count

from .models import Category, Product


def shop_context(request):
    return {
        'categories': Category.objects.annotate(product_count=Count('products')).filter(product_count__gt=0),
        'latest_products': Product.objects.order_by('-created')[:5],
    }
