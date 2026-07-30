from __future__ import annotations

from django.db import models
from django.conf import settings
from apps.common.models import TimeStampedModel
from apps.products.models import Product


class Favorite(TimeStampedModel):
    """
    Favorite products for authenticated users.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Пользователь"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="favorited_by", verbose_name="Товар")

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные товары"
        unique_together = ("user", "product")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.user} -> {self.product.name}"
