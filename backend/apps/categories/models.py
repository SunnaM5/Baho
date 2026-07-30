from __future__ import annotations

from django.db import models
from apps.common.models import TimeStampedModel, SEOFields


class Category(TimeStampedModel, SEOFields):
    """
    Hierarchical Categories for electronics catalog with SEO & Media support.
    """
    name = models.CharField(max_length=255, verbose_name="Название категории (Основное)")
    name_ru = models.CharField(max_length=255, blank=True, verbose_name="Название (RU)")
    name_uz = models.CharField(max_length=255, blank=True, verbose_name="Название (UZ)")
    name_en = models.CharField(max_length=255, blank=True, verbose_name="Название (EN)")

    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL Slug")
    
    description = models.TextField(blank=True, verbose_name="Описание (Основное)")
    description_ru = models.TextField(blank=True, verbose_name="Описание (RU)")
    description_uz = models.TextField(blank=True, verbose_name="Описание (UZ)")
    description_en = models.TextField(blank=True, verbose_name="Описание (EN)")
    icon = models.ImageField(upload_to="categories/icons/", blank=True, null=True, verbose_name="Иконка")
    image = models.ImageField(upload_to="categories/images/", blank=True, null=True, verbose_name="Изображение баннера")
    
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        blank=True,
        null=True,
        verbose_name="Родительская категория"
    )
    is_active = models.BooleanField(default=True, db_index=True, verbose_name="Активна")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["order", "name"]
        indexes = [
            models.Index(fields=["slug", "is_active"]),
        ]

    def __str__(self) -> str:
        if self.parent:
            return f"{self.parent.name} -> {self.name}"
        return self.name
