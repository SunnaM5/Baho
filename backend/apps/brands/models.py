from __future__ import annotations

from django.db import models
from apps.common.models import TimeStampedModel, SEOFields


class Brand(TimeStampedModel, SEOFields):
    """
    Brand model for electronics manufacturers (e.g. Apple, Samsung, Xiaomi).
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Название бренда")
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL Slug")
    logo = models.ImageField(upload_to="brands/logos/", blank=True, null=True, verbose_name="Логотип")
    description = models.TextField(blank=True, verbose_name="Описание бренда")
    description_ru = models.TextField(blank=True, verbose_name="Описание (RU)")
    description_uz = models.TextField(blank=True, verbose_name="Описание (UZ)")
    description_en = models.TextField(blank=True, verbose_name="Описание (EN)")
    country = models.CharField(max_length=100, blank=True, verbose_name="Страна бренда")
    is_active = models.BooleanField(default=True, db_index=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
