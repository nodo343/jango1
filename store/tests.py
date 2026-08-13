from django.test import TestCase
from django.urls import reverse

from .models import Category, Product


class ProductFilteringTests(TestCase):
    def setUp(self):
        electronics = Category.objects.create(name='Electronics', slug='electronics')
        books = Category.objects.create(name='Books', slug='books')

        Product.objects.create(
            category=electronics,
            name='Laptop',
            slug='laptop',
            description='Portable work computer',
            price='1200.00',
            available=True,
        )
        Product.objects.create(
            category=electronics,
            name='Headphones',
            slug='headphones',
            description='Wireless audio',
            price='200.00',
            discount_price='150.00',
            is_on_sale=True,
            available=True,
        )
        Product.objects.create(
            category=books,
            name='Django Book',
            slug='django-book',
            description='Web framework guide',
            price='45.00',
            available=True,
        )

    def product_names(self, response):
        return [product.name for product in response.context['products']]

    def test_search_category_sale_filter_and_sort_work_together(self):
        response = self.client.get(reverse('store:home'), {
            'q': 'audio',
            'category': 'electronics',
            'sale': 'on',
            'sort': 'price_desc',
        })

        self.assertEqual(self.product_names(response), ['Headphones'])
        self.assertContains(response, 'value="audio"')
        self.assertContains(response, 'value="electronics" selected')
        self.assertContains(response, 'value="price_desc" selected')
        self.assertContains(response, 'name="sale" value="on" checked')

    def test_sort_uses_discount_price_when_present(self):
        response = self.client.get(reverse('store:home'), {'sort': 'price_desc'})

        self.assertEqual(self.product_names(response), ['Laptop', 'Headphones', 'Django Book'])

    def test_sale_page_keeps_sale_filter_forced_with_search_and_category(self):
        response = self.client.get(reverse('store:sale_products'), {
            'q': 'wireless',
            'category': 'electronics',
            'sort': 'name_asc',
        })

        self.assertEqual(self.product_names(response), ['Headphones'])
        self.assertNotContains(response, 'id="sale-filter"')

    def test_category_page_searches_and_sorts_inside_current_category(self):
        response = self.client.get(reverse('store:category_products', args=['electronics']), {
            'q': 'computer',
            'sort': 'name_desc',
        })

        self.assertEqual(self.product_names(response), ['Laptop'])
        self.assertNotContains(response, 'id="category-filter"')
