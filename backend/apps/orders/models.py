from __future__ import annotations

import random
import string
from decimal import Decimal
from django.db import models
from django.conf import settings
from apps.common.models import TimeStampedModel
from apps.products.models import Product, ProductColor, ProductMemoryVariant


def generate_order_number() -> str:
    prefix = "BM"
    random_str = "".join(random.choices(string.digits, k=8))
    return f"{prefix}-{random_str}"


class Order(TimeStampedModel):
    """
    Enterprise Order Model with status tracking, history, and full audit details.
    """
    class Status(models.TextChoices):
        NEW = "NEW", "Новый"
        PROCESSING = "PROCESSING", "В обработке"
        CONFIRMED = "CONFIRMED", "Подтвержден"
        SHIPPED = "SHIPPED", "В пути"
        DELIVERED = "DELIVERED", "Доставлен"
        CANCELLED = "CANCELLED", "Отменен"

    class PaymentMethod(models.TextChoices):
        CASH = "CASH", "Наличными при получении"
        CARD_UPON_RECEIPT = "CARD_UPON_RECEIPT", "Картой при получении"
        CLICK = "CLICK", "Click"
        PAYME = "PAYME", "Payme"

    class DeliveryMethod(models.TextChoices):
        COURIER = "COURIER", "Курьерская доставка"
        PICKUP = "PICKUP", "Самовывоз"

    order_number = models.CharField(
        max_length=50,
        unique=True,
        default=generate_order_number,
        db_index=True,
        verbose_name="Номер заказа"
    )
    idempotency_key = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
        verbose_name="Ключ идемпотентности"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="orders",
        verbose_name="Пользователь"
    )
    
    # Customer Details
    full_name = models.CharField(max_length=255, verbose_name="Имя и Фамилия клиента")
    phone_number = models.CharField(max_length=20, verbose_name="Телефон клиента")
    email = models.EmailField(blank=True, verbose_name="Email")
    
    # Delivery Info
    delivery_method = models.CharField(
        max_length=20,
        choices=DeliveryMethod.choices,
        default=DeliveryMethod.COURIER,
        verbose_name="Способ доставки"
    )
    delivery_address = models.TextField(verbose_name="Адрес доставки")
    comment = models.TextField(blank=True, verbose_name="Комментарий к заказу")
    
    # Payment & Financials
    payment_method = models.CharField(
        max_length=30,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH,
        verbose_name="Способ оплаты"
    )
    is_paid = models.BooleanField(default=False, verbose_name="Оплачен")
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Итоговая сумма"
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        db_index=True,
        verbose_name="Статус заказа"
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Order #{self.order_number} ({self.get_status_display()})"


from apps.products.models import Product, ProductColor, ProductMemoryVariant, ProductVariant


class OrderItem(TimeStampedModel):
    """
    Items included in an order with price snapshot at purchase time.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Товар")
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Вариант SKU")
    product_name = models.CharField(max_length=255, verbose_name="Название товара (снапшот)")
    color_name = models.CharField(max_length=50, blank=True, verbose_name="Цвет (снапшот)")
    memory_capacity = models.CharField(max_length=50, blank=True, verbose_name="Память (снапшот)")
    sim_type = models.CharField(max_length=100, blank=True, verbose_name="SIM (снапшот)")
    sku_snapshot = models.CharField(max_length=100, blank=True, verbose_name="SKU (снапшот)")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Цена за unit")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказах"

    def __str__(self) -> str:
        return f"{self.quantity}x {self.product_name}"

    @property
    def total_price(self) -> Decimal:
        return self.price * self.quantity


class OrderHistory(TimeStampedModel):
    """
    Audit log of order status transitions.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="history", verbose_name="Заказ")
    old_status = models.CharField(max_length=20, choices=Order.Status.choices, verbose_name="Старый статус")
    new_status = models.CharField(max_length=20, choices=Order.Status.choices, verbose_name="Новый статус")
    comment = models.TextField(blank=True, verbose_name="Причина / Комментарий")

    class Meta:
        verbose_name = "История заказа"
        verbose_name_plural = "История заказов"
        ordering = ["-created_at"]
