from __future__ import annotations

from django.db import models
from django.conf import settings
from apps.common.models import TimeStampedModel
from apps.products.models import Product


class ProductComparison(TimeStampedModel):
    """
    User/Guest Product Comparison list.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="comparisons")
    session_key = models.CharField(max_length=100, blank=True, db_index=True, verbose_name="Сессия гостя")
    products = models.ManyToManyField(Product, related_name="compared_in", verbose_name="Товары в сравнении")

    class Meta:
        verbose_name = "Сравнение товаров"
        verbose_name_plural = "Списки сравнения"
        indexes = [
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["session_key", "created_at"]),
        ]

    def __str__(self) -> str:
        owner = self.user.phone if self.user else f"Guest ({self.session_key})"
        return f"Comparison list: {owner}"


class RecentlyViewedProduct(TimeStampedModel):
    """
    User/Guest Recently Viewed Products history.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="recently_viewed")
    session_key = models.CharField(max_length=100, blank=True, db_index=True, verbose_name="Сессия гостя")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="recent_views")

    class Meta:
        verbose_name = "Недавно просмотренный товар"
        verbose_name_plural = "История просмотров товаров"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["session_key", "created_at"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["user", "product"], condition=models.Q(user__isnull=False), name="unique_user_recent_product"),
            models.UniqueConstraint(fields=["session_key", "product"], condition=models.Q(user__isnull=True), name="unique_session_recent_product"),
        ]

    def __str__(self) -> str:
        return f"{self.product.name} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class StockNotificationRequest(TimeStampedModel):
    """
    Back-in-stock notification subscription when product stock returns > 0.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="stock_notifications")
    email = models.EmailField(blank=True, verbose_name="Email для уведомления")
    phone = models.CharField(max_length=50, blank=True, verbose_name="Телефон для уведомления")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stock_subscribers")
    is_notified = models.BooleanField(default=False, db_index=True, verbose_name="Уведомлен")

    class Meta:
        verbose_name = "Запрос уведомления о поступлении"
        verbose_name_plural = "Запросы уведомлений о поступлении"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["product", "is_notified"]),
            models.Index(fields=["user", "created_at"]),
        ]

    def __str__(self) -> str:
        contact = self.email or self.phone or (self.user.phone if self.user else "Anonymous")
        return f"Stock notification for {self.product.name} -> {contact}"
