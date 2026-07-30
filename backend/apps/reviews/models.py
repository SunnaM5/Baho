from __future__ import annotations

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from apps.common.models import TimeStampedModel
from apps.products.models import Product


class Review(TimeStampedModel):
    """
    Product reviews with ratings, pros, cons, and admin moderation status.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Товар"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Пользователь"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оценка (1-5)"
    )
    title = models.CharField(max_length=255, blank=True, verbose_name="Заголовок отзыва")
    comment = models.TextField(verbose_name="Текст отзыва")
    pros = models.TextField(blank=True, verbose_name="Достоинства")
    cons = models.TextField(blank=True, verbose_name="Недостатки")
    
    is_approved = models.BooleanField(default=False, db_index=True, verbose_name="Одобрен админом")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]
        unique_together = ("product", "user")

    def __str__(self) -> str:
        return f"Review ({self.rating}/5) for {self.product.name} by {self.user}"
