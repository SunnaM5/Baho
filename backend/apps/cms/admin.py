from __future__ import annotations

from django.contrib import admin
from apps.cms.models import (
    SiteSettings,
    HeroSlide,
    HomeSectionLayout,
    ProductCollection,
    FAQItem,
    NewsArticle,
    AdvantageItem
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "phone_primary", "email", "working_hours")
    fieldsets = (
        ("Контакты и Общие настройки", {
            "fields": ("site_name", "logo", "favicon", "phone_primary", "phone_secondary", "email", "address", "google_maps_url", "working_hours")
        }),
        ("Социальные сети", {
            "fields": ("telegram_url", "instagram_url", "facebook_url", "youtube_url", "tiktok_url")
        }),
        ("SEO Настройки", {
            "fields": ("meta_title_ru", "meta_title_uz", "meta_title_en", "meta_description_ru", "meta_description_uz", "meta_description_en")
        }),
    )


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("title_ru", "priority", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title_ru", "title_uz", "title_en", "subtitle_ru")
    fieldsets = (
        ("Основные настройки слайда", {
            "fields": ("priority", "is_active", "desktop_image", "mobile_image", "button_url", "bg_color")
        }),
        ("🇷🇺 Русский", {
            "fields": ("title_ru", "subtitle_ru", "button_text_ru")
        }),
        ("🇺🇿 Узбекский", {
            "fields": ("title_uz", "subtitle_uz", "button_text_uz")
        }),
        ("🇺🇸 English", {
            "fields": ("title_en", "subtitle_en", "button_text_en")
        }),
    )


@admin.register(HomeSectionLayout)
class HomeSectionLayoutAdmin(admin.ModelAdmin):
    list_display = ("section_key", "title_ru", "order", "is_visible")
    list_editable = ("order", "is_visible")
    ordering = ("order",)


@admin.register(ProductCollection)
class ProductCollectionAdmin(admin.ModelAdmin):
    list_display = ("title_ru", "slug", "is_featured_on_home", "order", "is_active")
    list_filter = ("is_active", "is_featured_on_home")
    search_fields = ("title_ru", "slug")
    filter_horizontal = ("products",)
    prepopulated_fields = {"slug": ("title_ru",)}


@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ("question_ru", "category_name", "order", "is_active")
    list_filter = ("category_name", "is_active")
    search_fields = ("question_ru", "question_uz", "answer_ru")


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ("title_ru", "slug", "published_at", "is_published")
    list_filter = ("is_published", "published_at")
    search_fields = ("title_ru", "title_uz", "summary_ru")
    prepopulated_fields = {"slug": ("title_ru",)}


@admin.register(AdvantageItem)
class AdvantageItemAdmin(admin.ModelAdmin):
    list_display = ("title_ru", "icon_name", "order", "is_active")
    list_editable = ("order", "is_active")
