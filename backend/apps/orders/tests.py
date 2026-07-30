from decimal import Decimal
from unittest.mock import patch
from django.test import TestCase, TransactionTestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient

from apps.categories.models import Category
from apps.brands.models import Brand
from apps.products.models import Product, ProductColor, ProductMemoryVariant
from apps.cart.models import Cart, CartItem
from apps.cart.services import CartService
from apps.favorites.models import Favorite
from apps.orders.models import Order
from apps.orders.services import OrderService

from rest_framework.exceptions import ValidationError as DRFValidationError

User = get_user_model()


class ComprehensivePhase3VerificationTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user(phone_number="+998901111111", password="password123")
        self.user_b = User.objects.create_user(phone_number="+998902222222", password="password123")
        
        self.category = Category.objects.create(name="Электроника", slug="electronics")
        self.brand = Brand.objects.create(name="Samsung", slug="samsung")
        
        self.product = Product.objects.create(
            name="Galaxy S24 Ultra",
            slug="galaxy-s24-ultra",
            sku="GS24U-512",
            category=self.category,
            brand=self.brand,
            base_price=Decimal("12000000.00"),
            stock=5
        )
        self.color = ProductColor.objects.create(product=self.product, name="Titanium Gray")
        self.memory = ProductMemoryVariant.objects.create(product=self.product, capacity="512GB", price_override=Decimal("13000000.00"))

        self.client_a = APIClient()
        self.client_a.force_authenticate(user=self.user_a)

        self.client_b = APIClient()
        self.client_b.force_authenticate(user=self.user_b)

    # 1. IDEMPOTENCY TEST
    @patch("apps.orders.services.send_telegram_message_task.delay")
    def test_idempotency_prevents_duplicate_orders(self, mock_telegram):
        items_data = [{"product_id": str(self.product.id), "quantity": 1}]
        
        order1 = OrderService.create_order(
            full_name="Тест Идемпотентности",
            phone_number="+998901111111",
            delivery_address="Ташкент",
            items_data=items_data,
            idempotency_key="KEY-ABC-123"
        )
        
        order2 = OrderService.create_order(
            full_name="Тест Идемпотентности",
            phone_number="+998901111111",
            delivery_address="Ташкент",
            items_data=items_data,
            idempotency_key="KEY-ABC-123"
        )

        self.assertEqual(Order.objects.count(), 1, "Must not create a duplicate order with the same Idempotency-Key")
        self.assertEqual(order1.id, order2.id)
        self.assertEqual(self.product.refresh_from_db() or self.product.stock, 4, "Stock must only be decremented once")

    # 2. CART PRICE CHANGE NOTIFICATION TEST
    def test_cart_price_change_detection(self):
        # Client expected price is 10,000,000, but product current_price is 12,000,000
        items_data = [{"product_id": str(self.product.id), "quantity": 1, "expected_price": Decimal("10000000.00")}]
        
        with self.assertRaises(ValidationError) as ctx:
            OrderService.create_order(
                full_name="Покупатель",
                phone_number="+998901111111",
                delivery_address="Ташкент",
                items_data=items_data
            )
        
        self.assertIn("PRICE_CHANGED", str(ctx.exception))

    # 3. TRANSACTION ROLLBACK TEST
    def test_checkout_transaction_rollback_on_failure(self):
        initial_stock = self.product.stock
        # Invalid product_id will trigger ValidationError inside loop
        items_data = [
            {"product_id": str(self.product.id), "quantity": 1},
            {"product_id": "00000000-0000-0000-0000-000000000000", "quantity": 1}
        ]

        with self.assertRaises(ValidationError):
            OrderService.create_order(
                full_name="Тест Отката",
                phone_number="+998901111111",
                delivery_address="Ташкент",
                items_data=items_data
            )

        self.assertEqual(Order.objects.count(), 0, "Order must be rolled back completely")
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, initial_stock, "Stock must be fully restored upon rollback")

    # 4. CART & FAVORITES IDOR AUTHORIZATION TEST
    def test_cart_and_favorites_idor_security(self):
        cart_b = CartService.get_or_create_cart(type("Req", (), {"user": self.user_b})())
        item_b = CartService.add_to_cart(cart_b, str(self.product.id), quantity=1)

        # User A attempts to update User B's cart item via REST endpoint
        response = self.client_a.patch(f"/api/v1/cart/cart/items/{item_b.id}/", {"quantity": 5})
        self.assertEqual(response.status_code, 404, "User A must not be able to access or modify User B's cart item")

    # 5. GUEST CART MERGE TEST
    def test_guest_cart_merge_quantities(self):
        guest_cart = Cart.objects.create(session_key="guest_sess_999")
        CartItem.objects.create(cart=guest_cart, product=self.product, quantity=2)

        user_cart = CartService.get_or_create_cart(type("Req", (), {"user": self.user_a})())
        CartItem.objects.create(cart=user_cart, product=self.product, quantity=1)

        merged_cart = CartService.merge_guest_cart(self.user_a, "guest_sess_999")
        item = merged_cart.items.get(product=self.product)
        self.assertEqual(item.quantity, 3, "Merged cart must sum quantities (2 + 1 = 3)")

    # 6. FAVORITES TOGGLE TEST
    def test_favorites_toggle(self):
        response1 = self.client_a.post("/api/v1/favorites/toggle/", {"product_id": str(self.product.id)})
        self.assertEqual(response1.status_code, 201)
        self.assertTrue(Favorite.objects.filter(user=self.user_a, product=self.product).exists())

        response2 = self.client_a.post("/api/v1/favorites/toggle/", {"product_id": str(self.product.id)})
        self.assertEqual(response2.status_code, 200)
        self.assertFalse(Favorite.objects.filter(user=self.user_a, product=self.product).exists())

    # 7. QUANTITY VALIDATION TEST
    def test_invalid_quantity_rejected(self):
        cart = CartService.get_or_create_cart(type("Req", (), {"user": self.user_a})())
        with self.assertRaises((ValidationError, DRFValidationError)):
            CartService.add_to_cart(cart, str(self.product.id), quantity=0)
        with self.assertRaises((ValidationError, DRFValidationError)):
            CartService.add_to_cart(cart, str(self.product.id), quantity=-5)
