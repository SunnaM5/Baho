from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient

from apps.categories.models import Category
from apps.brands.models import Brand
from apps.products.models import Product, ProductColor, ProductMemoryVariant


class MultilingualArchitectureTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Смартфоны",
            name_ru="Смартфоны",
            name_uz="Smartfonlar",
            name_en="Smartphones",
            slug="smartphones"
        )
        self.brand = Brand.objects.create(name="Apple", slug="apple")
        
        self.product = Product.objects.create(
            name="iPhone 15 Pro Max",
            name_ru="iPhone 15 Pro Max (RU)",
            name_uz="iPhone 15 Pro Max (UZ)",
            name_en="iPhone 15 Pro Max (EN)",
            slug="iphone-15-pro-max",
            sku="IP15PM-256",
            category=self.category,
            brand=self.brand,
            short_description_ru="Отличный смартфон",
            short_description_uz="Ajoyib smartfon",
            short_description_en="Great smartphone",
            base_price=Decimal("15000000.00"),
            stock=10
        )
        self.client = APIClient()

    def test_api_returns_russian_by_default(self):
        response = self.client.get(f"/api/v1/products/{self.product.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "iPhone 15 Pro Max (RU)")
        self.assertEqual(response.data["short_description"], "Отличный смартфон")

    def test_api_returns_uzbek_via_query_param(self):
        response = self.client.get(f"/api/v1/products/{self.product.slug}/?lang=uz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "iPhone 15 Pro Max (UZ)")
        self.assertEqual(response.data["short_description"], "Ajoyib smartfon")

    def test_api_returns_english_via_accept_language_header(self):
        response = self.client.get(f"/api/v1/products/{self.product.slug}/", HTTP_ACCEPT_LANGUAGE="en-US,en;q=0.9")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "iPhone 15 Pro Max (EN)")
        self.assertEqual(response.data["short_description"], "Great smartphone")

    def test_translation_fallback_chain(self):
        # Product with only RU translation available
        p_fallback = Product.objects.create(
            name="AirPods Pro",
            name_ru="AirPods Pro (RU)",
            slug="airpods-pro",
            sku="APP-002",
            category=self.category,
            base_price=Decimal("3000000.00"),
            stock=5
        )
        response = self.client.get(f"/api/v1/products/{p_fallback.slug}/?lang=uz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "AirPods Pro (RU)", "Must fallback to RU when UZ translation is missing")

    def test_multilingual_search(self):
        response_uz = self.client.get("/api/v1/products/?search=Ajoyib")
        self.assertEqual(response_uz.status_code, 200)
        self.assertEqual(len(response_uz.data["results"]), 1)


from apps.products.models import ProductSimVariant, ProductVariant
from apps.cart.services import CartService
from apps.cart.models import Cart
from apps.orders.services import OrderService
from django.db import IntegrityError


class ProductVariantMatrixTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Смартфоны", slug="smartphones")
        self.brand = Brand.objects.create(name="Apple", slug="apple")
        self.product = Product.objects.create(
            name="iPhone 17 Pro Max",
            slug="iphone-17-pro-max",
            sku="IPH17PM-BASE",
            category=self.category,
            brand=self.brand,
            base_price=Decimal("17000000.00"),
            stock=20
        )
        self.mem_256 = ProductMemoryVariant.objects.create(product=self.product, capacity="256GB")
        self.mem_512 = ProductMemoryVariant.objects.create(product=self.product, capacity="512GB")
        self.sim_esim = ProductSimVariant.objects.create(product=self.product, sim_type="ESIM")
        self.sim_single = ProductSimVariant.objects.create(product=self.product, sim_type="SINGLE")
        self.color_orange = ProductColor.objects.create(product=self.product, name="Cosmic Orange", hex_code="#FF9500")
        self.color_blue = ProductColor.objects.create(product=self.product, name="Deep Blue", hex_code="#0000FF")

        self.variant_1 = ProductVariant.objects.create(
            product=self.product,
            memory=self.mem_256,
            sim=self.sim_esim,
            color=self.color_orange,
            price=Decimal("18500000.00"),
            old_price=Decimal("19500000.00"),
            stock=5,
            sku="IPH17PM-256-ESIM-ORANGE"
        )
        self.variant_2 = ProductVariant.objects.create(
            product=self.product,
            memory=self.mem_512,
            sim=self.sim_single,
            color=self.color_blue,
            price=Decimal("21000000.00"),
            stock=3,
            sku="IPH17PM-512-SIM-BLUE"
        )
        self.client = APIClient()

    def test_variant_creation_and_fields(self):
        self.assertEqual(self.variant_1.price, Decimal("18500000.00"))
        self.assertEqual(self.variant_1.stock, 5)
        self.assertTrue(self.variant_1.is_active)

    def test_duplicate_combination_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            ProductVariant.objects.create(
                product=self.product,
                memory=self.mem_256,
                sim=self.sim_esim,
                color=self.color_orange,
                price=Decimal("18500000.00"),
                stock=2
            )

    def test_product_detail_api_returns_variants(self):
        response = self.client.get(f"/api/v1/products/{self.product.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("variants", response.data)
        variants = response.data["variants"]
        self.assertEqual(len(variants), 2)
        
        var1 = next(v for v in variants if v["sku"] == "IPH17PM-256-ESIM-ORANGE")
        self.assertEqual(Decimal(str(var1["price"])), Decimal("18500000.00"))
        self.assertEqual(var1["storage"], "256GB")
        self.assertEqual(var1["sim_type"], "ESIM")
        self.assertEqual(var1["color_name"], "Cosmic Orange")

    def test_cart_accepts_variant_id_and_locks_variant_price(self):
        session = self.client.session
        session.create()
        cart, _ = Cart.objects.get_or_create(session_key=session.session_key)

        item = CartService.add_to_cart(
            cart=cart,
            product_id=str(self.product.id),
            quantity=1,
            variant_id=str(self.variant_1.id)
        )
        self.assertEqual(item.variant, self.variant_1)
        self.assertEqual(item.unit_price, Decimal("18500000.00"))

    def test_order_deducts_variant_stock_and_stores_variant_snapshot(self):
        order = OrderService.create_order(
            full_name="Тестовый Покупатель",
            phone_number="+998901234567",
            delivery_address="г. Ташкент",
            items_data=[{
                "product_id": str(self.product.id),
                "variant_id": str(self.variant_1.id),
                "quantity": 2,
                "expected_price": "18500000.00"
            }]
        )
        self.variant_1.refresh_from_db()
        self.assertEqual(self.variant_1.stock, 3)
        order_item = order.items.first()
        self.assertEqual(order_item.price, Decimal("18500000.00"))
        self.assertEqual(order_item.variant, self.variant_1)
        self.assertEqual(order_item.sku_snapshot, "IPH17PM-256-ESIM-ORANGE")
