from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from apps.categories.models import Category
from apps.brands.models import Brand
from apps.products.models import Product
from apps.cart.models import Cart, CartItem
from apps.cart.services import CartService

User = get_user_model()


class CartServiceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(phone_number="+998901112233", password="password123")
        self.category = Category.objects.create(name="Ноутбуки", slug="laptops")
        self.brand = Brand.objects.create(name="Apple", slug="apple")
        self.product = Product.objects.create(
            name="MacBook Pro 14",
            slug="macbook-pro-14",
            sku="MBP14-2026",
            category=self.category,
            brand=self.brand,
            base_price=Decimal("20000000.00"),
            stock=5
        )

    def test_cart_item_creation_and_subtotal(self):
        cart = CartService.get_or_create_cart(type("Req", (), {"user": self.user})())
        item = CartService.add_to_cart(cart, str(self.product.id), quantity=2)

        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(item.subtotal, Decimal("40000000.00"))
        self.assertEqual(cart.total, Decimal("40000000.00"))

    def test_cannot_add_exceeding_stock(self):
        cart = CartService.get_or_create_cart(type("Req", (), {"user": self.user})())
        with self.assertRaises(ValidationError):
            CartService.add_to_cart(cart, str(self.product.id), quantity=10)

    def test_guest_cart_merging(self):
        guest_cart = Cart.objects.create(session_key="guest_session_123")
        CartItem.objects.create(cart=guest_cart, product=self.product, quantity=1)

        merged_cart = CartService.merge_guest_cart(self.user, "guest_session_123")
        self.assertEqual(merged_cart.items.count(), 1)
        self.assertEqual(merged_cart.items.first().quantity, 1)
        self.assertFalse(Cart.objects.filter(session_key="guest_session_123").exists())
