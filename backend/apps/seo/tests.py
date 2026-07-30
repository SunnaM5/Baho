from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient

from apps.categories.models import Category
from apps.brands.models import Brand
from apps.products.models import Product


class EnterpriseSeoTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Смартфоны", slug="smartphones")
        self.brand = Brand.objects.create(name="Apple", slug="apple")

        self.product = Product.objects.create(
            name="iPhone 16 Pro",
            slug="iphone-16-pro",
            sku="IP16P-128",
            category=self.category,
            brand=self.brand,
            base_price=Decimal("14000000.00"),
            stock=5,
            is_active=True
        )

    def test_robots_txt_view(self):
        res = self.client.get("/robots.txt")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res["Content-Type"], "text/plain")
        self.assertIn("User-agent: *", res.content.decode("utf-8"))
        self.assertIn("Sitemap:", res.content.decode("utf-8"))

    def test_sitemap_xml_view(self):
        res = self.client.get("/sitemap.xml")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res["Content-Type"], "application/xml")
        content = res.content.decode("utf-8")
        self.assertIn("<?xml version=", content)
        self.assertIn("/category/smartphones", content)
        self.assertIn("/product/iphone-16-pro", content)
        self.assertIn("hreflang=\"ru\"", content)

    def test_seo_meta_api_view(self):
        res = self.client.get(f"/api/v1/seo/meta/?entity_type=product&slug={self.product.slug}")
        self.assertEqual(res.status_code, 200)
        self.assertIn("canonical", res.data)
        self.assertIn("json_ld", res.data)
        self.assertEqual(len(res.data["json_ld"]), 3)  # Organization, Product, BreadcrumbList
