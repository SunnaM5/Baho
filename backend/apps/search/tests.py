from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient

from apps.categories.models import Category
from apps.brands.models import Brand
from apps.products.models import Product
from apps.search.models import SearchSynonym, PopularSearchQuery, SearchHistory


class EnterpriseSearchTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(
            name="Смартфоны",
            name_ru="Смартфоны",
            name_uz="Smartfonlar",
            name_en="Smartphones",
            slug="smartphones"
        )
        self.brand = Brand.objects.create(name="Apple", slug="apple")

        self.product1 = Product.objects.create(
            name="iPhone 16 Pro Max",
            name_ru="iPhone 16 Pro Max",
            name_uz="iPhone 16 Pro Max",
            name_en="iPhone 16 Pro Max",
            slug="iphone-16-pro-max",
            sku="IP16PM-512",
            category=self.category,
            brand=self.brand,
            base_price=Decimal("18000000.00"),
            rating=4.9,
            stock=15
        )

        self.product2 = Product.objects.create(
            name="Samsung Galaxy S24 Ultra",
            name_ru="Samsung Galaxy S24 Ultra",
            name_uz="Samsung Galaxy S24 Ultra",
            slug="samsung-s24-ultra",
            sku="SM-S24U",
            category=self.category,
            base_price=Decimal("16000000.00"),
            rating=4.8,
            stock=8
        )

        # Create active synonym mapping
        SearchSynonym.objects.create(
            source_term="айфон",
            target_terms="iphone"
        )
        SearchSynonym.objects.create(
            source_term="самсунг",
            target_terms="samsung"
        )

    def test_search_by_russian_synonym(self):
        response = self.client.get("/api/v1/search/?q=айфон")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["sku"], "IP16PM-512")

    def test_search_by_sku_exact_match(self):
        response = self.client.get("/api/v1/search/?q=SM-S24U")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], "Samsung Galaxy S24 Ultra")

    def test_search_by_uzbek_category(self):
        response = self.client.get("/api/v1/search/?q=Smartfonlar")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

    def test_search_suggestions_autocomplete(self):
        response = self.client.get("/api/v1/search/suggestions/?q=iph")
        self.assertEqual(response.status_code, 200)
        self.assertIn("products", response.data)
        self.assertIn("categories", response.data)
        self.assertIn("brands", response.data)
        self.assertEqual(len(response.data["products"]), 1)

    def test_popular_queries_tracking(self):
        self.client.get("/api/v1/search/?q=айфон")
        self.client.get("/api/v1/search/?q=айфон")
        
        pop = PopularSearchQuery.objects.get(query="айфон")
        self.assertEqual(pop.search_count, 2)

    def test_search_history_management(self):
        self.client.get("/api/v1/search/?q=samsung")
        hist_response = self.client.get("/api/v1/search/history/")
        self.assertEqual(hist_response.status_code, 200)
        self.assertEqual(len(hist_response.data), 1)

        # Clear history
        del_response = self.client.delete("/api/v1/search/history/")
        self.assertEqual(del_response.status_code, 204)
