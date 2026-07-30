from __future__ import annotations

import uuid
from django.db import models
from django.core.exceptions import ValidationError


class TimeStampedModel(models.Model):
    """
    Abstract base model providing created_at and updated_at timestamps.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SEOFields(models.Model):
    """
    SEO-ready fields that can be embedded into domain entities with i18n support.
    """
    meta_title = models.CharField(max_length=70, blank=True, default="", verbose_name="Meta Title (Основной)")
    meta_title_ru = models.CharField(max_length=70, blank=True, default="", verbose_name="Meta Title (RU)")
    meta_title_uz = models.CharField(max_length=70, blank=True, default="", verbose_name="Meta Title (UZ)")
    meta_title_en = models.CharField(max_length=70, blank=True, default="", verbose_name="Meta Title (EN)")

    meta_description = models.CharField(max_length=160, blank=True, default="", verbose_name="Meta Description (Основной)")
    meta_description_ru = models.CharField(max_length=160, blank=True, default="", verbose_name="Meta Description (RU)")
    meta_description_uz = models.CharField(max_length=160, blank=True, default="", verbose_name="Meta Description (UZ)")
    meta_description_en = models.CharField(max_length=160, blank=True, default="", verbose_name="Meta Description (EN)")

    og_title = models.CharField(max_length=70, blank=True, default="", verbose_name="OpenGraph Заголовок (og:title)")
    og_description = models.CharField(max_length=160, blank=True, default="", verbose_name="OpenGraph Описание (og:description)")

    canonical_url = models.URLField(max_length=500, blank=True, default="", verbose_name="Канонический URL (Canonical URL)")
    schema_org = models.JSONField(blank=True, null=True, verbose_name="Данные Schema.org (JSON)")

    robots_noindex = models.BooleanField(default=False, verbose_name="Запретить индексацию (noindex)")
    robots_nofollow = models.BooleanField(default=False, verbose_name="Запретить переход по ссылкам (nofollow)")

    class Meta:
        abstract = True

    def clean(self) -> None:
        super().clean()
        if self.robots_noindex and self.canonical_url:
            raise ValidationError({"canonical_url": "canonical_url is not recommended when robots_noindex is enabled."})
