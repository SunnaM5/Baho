from __future__ import annotations

from decimal import Decimal
from django.db import models
from django.conf import settings
from apps.common.models import TimeStampedModel
from apps.products.models import Product, ProductColor, ProductMemoryVariant, ProductVariant


class Cart(TimeStampedModel):
    """
    Production Cart model supporting both authenticated users and guest sessions.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
        blank=True,
        null=True,
        verbose_name="Пользователь"
    )
    session_key = models.CharField(max_length=40, blank=True, null=True, db_index=True, verbose_name="Ключ сессии")

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self) -> str:
        return f"Cart ({self.user or self.session_key})"

    @property
    def items_count(self) -> int:
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self) -> Decimal:
        return sum((item.unit_price * item.quantity for item in self.items.all()), Decimal("0.00"))

    @property
    def total(self) -> Decimal:
        return self.subtotal


class CartItem(TimeStampedModel):
    """
    Individual items inside a cart with variant tracking.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", verbose_name="Корзина")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Конкретная комбинация SKU")
    color = models.ForeignKey(ProductColor, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Цвет")
    memory_variant = models.ForeignKey(ProductMemoryVariant, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Память")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"
        unique_together = ("cart", "product", "variant", "color", "memory_variant")

    def __str__(self) -> str:
        return f"{self.quantity}x {self.product.name}"

    @property
    def unit_price(self) -> Decimal:
        if self.variant and self.variant.price:
            return self.variant.price
        if self.memory_variant and self.memory_variant.price_override:
            return self.memory_variant.price_override
        return self.product.current_price

    @property
    def subtotal(self) -> Decimal:
        return self.unit_price * self.quantity
