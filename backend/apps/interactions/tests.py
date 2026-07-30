from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient

from apps.categories.models import Category
from apps.brands.models import Brand
from apps.products.models import Product
from apps.interactions.models import ProductComparison, RecentlyViewedProduct, StockNotificationRequest
from apps.interactions.services import process_stock_notifications


class UXInteractionsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Смартфоны", slug="smartphones")
        self.other_category = Category.objects.create(name="Телевизоры", slug="tv")
        self.brand = Brand.objects.create(name="Apple", slug="apple")

        self.product1 = Product.objects.create(
            name="iPhone 16 Pro",
            slug="iphone-16-pro",
            sku="IP16P-128",
            category=self.category,
            brand=self.brand,
            base_price=Decimal("14000000.00"),
            stock=5,
            is_active=True
        )

        self.product2 = Product.objects.create(
            name="iPhone 16 Pro Max",
            slug="iphone-16-pro-max",
            sku="IP16PM-256",
            category=self.category,
            brand=self.brand,
            base_price=Decimal("17000000.00"),
            stock=0,
            is_active=True
        )

        self.tv_product = Product.objects.create(
            name="Samsung TV 65",
            slug="samsung-tv-65",
            sku="SAM-TV-65",
            category=self.other_category,
            brand=self.brand,
            base_price=Decimal("10000000.00"),
            stock=3,
            is_active=True
        )

    def test_product_comparison_flow_and_category_limit_enforcement(self):
        # 1. Add product1
        add_res = self.client.post("/api/v1/interactions/comparison/", {"product_id": self.product1.id})
        self.assertEqual(add_res.status_code, 201)

        # 2. Reject adding product from different category (TV vs Smartphone)
        diff_cat_res = self.client.post("/api/v1/interactions/comparison/", {"product_id": self.tv_product.id})
        self.assertEqual(diff_cat_res.status_code, 400)
        self.assertIn("error", diff_cat_res.data)

    def test_recently_viewed_history(self):
        self.client.post("/api/v1/interactions/recently-viewed/", {"product_id": self.product1.id})
        res = self.client.get("/api/v1/interactions/recently-viewed/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)

    def test_recommendations_endpoint(self):
        url = f"/api/v1/interactions/recommendations/?product_id={self.product1.id}"
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIn("similar_products", res.data)
        self.assertIn("frequently_bought_together", res.data)
        self.assertEqual(len(res.data["similar_products"]), 1)

    def test_stock_notification_and_automated_dispatch(self):
        # 1. Subscribe
        sub_res = self.client.post("/api/v1/interactions/stock-notification/", {
            "product_id": self.product2.id,
            "email": "customer@baho.uz",
            "phone": "+998901112233"
        })
        self.assertEqual(sub_res.status_code, 201)
        self.assertEqual(StockNotificationRequest.objects.count(), 1)

        # 2. Simulate stock return > 0
        self.product2.stock = 10
        self.product2.save()

        # 3. Process notifications & verify idempotency
        dispatched = process_stock_notifications(self.product2)
        self.assertEqual(dispatched, 1)

        # 4. Verify second attempt dispatches 0 (idempotent)
        second_dispatch = process_stock_notifications(self.product2)
        self.assertEqual(second_dispatch, 0)
