from __future__ import annotations

from django.contrib import admin
from apps.brands.models import Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "country", "is_active", "created_at")
    list_filter = ("is_active", "country")
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        ("Основная информация", {
            "fields": ("name", "slug", "logo", "country", "is_active", "description")
        }),
        ("🇷🇺 Русский перевод", {
            "fields": ("description_ru",)
        }),
        ("🇺🇿 Узбекский перевод", {
            "fields": ("description_uz",)
        }),
        ("🇺🇸 Английский перевод", {
            "fields": ("description_en",)
        }),
        ("🔍 Настройки поисковой оптимизации (SEO)", {
            "fields": (
                "meta_title_ru", "meta_title_uz", "meta_title_en", "meta_title",
                "meta_description_ru", "meta_description_uz", "meta_description_en", "meta_description",
                "og_title", "og_description", "canonical_url", "robots_noindex", "robots_nofollow"
            )
        }),
    )
