from __future__ import annotations

from django.contrib import admin
from apps.categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "slug", "is_active", "order", "created_at")
    list_filter = ("is_active", "parent")
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("order", "name")
    fieldsets = (
        ("Основная информация", {
            "fields": ("name", "slug", "parent", "icon", "image", "is_active", "order")
        }),
        ("🇷🇺 Русский перевод", {
            "fields": ("name_ru", "description_ru")
        }),
        ("🇺🇿 Узбекский перевод", {
            "fields": ("name_uz", "description_uz")
        }),
        ("🇺🇸 Английский перевод", {
            "fields": ("name_en", "description_en")
        }),
        ("🔍 Настройки поисковой оптимизации (SEO)", {
            "fields": (
                "meta_title_ru", "meta_title_uz", "meta_title_en", "meta_title",
                "meta_description_ru", "meta_description_uz", "meta_description_en", "meta_description",
                "og_title", "og_description", "canonical_url", "robots_noindex", "robots_nofollow"
            )
        }),
    )
