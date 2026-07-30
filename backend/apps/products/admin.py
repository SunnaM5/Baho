from __future__ import annotations

from django.contrib import admin
from apps.products.models import (
    Product,
    ProductColor,
    ProductMemoryVariant,
    ProductSimVariant,
    ProductVariant,
    ProductImage,
    ProductVideo,
    ProductSpecification
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fields = ("image", "color", "alt_text", "is_main", "order")
    extra = 1


class ProductColorInline(admin.TabularInline):
    model = ProductColor
    fields = ("name", "name_ru", "name_uz", "name_en", "hex_code", "image", "price_override", "stock")
    extra = 1


class ProductMemoryVariantInline(admin.TabularInline):
    model = ProductMemoryVariant
    fields = ("capacity", "capacity_ru", "capacity_uz", "capacity_en", "price_override", "stock")
    extra = 1


class ProductSimVariantInline(admin.TabularInline):
    model = ProductSimVariant
    fields = ("sim_type", "name_override", "price_override", "stock")
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    fields = (
        "memory", "sim", "color", "price", "old_price",
        "installment_3m_price", "installment_6m_price", "installment_12m_price",
        "stock", "sku", "is_active"
    )
    extra = 2
    verbose_name = "Точная комбинация (Матрица цен Terabayt)"
    verbose_name_plural = "⚡ ТОЧНЫЕ КОМБИНАЦИИ ЦЕН, РАССРОЧКИ И ОСТАТКОВ (ПАМЯТЬ + SIM + ЦВЕТ)"


class ProductVideoInline(admin.TabularInline):
    model = ProductVideo
    extra = 0


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 2


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name", "sku", "category", "brand", "base_price",
        "discount_price", "is_on_sale", "stock", "rating", "is_active"
    )
    list_filter = ("is_active", "is_on_sale", "is_featured", "category", "brand")
    search_fields = ("name", "name_ru", "name_uz", "name_en", "sku", "description")
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        ("Основная информация", {
            "fields": ("name", "slug", "sku", "category", "brand", "stock", "guarantee_months", "battery_health", "is_active", "is_featured")
        }),
        ("🇷🇺 Русский перевод", {
            "fields": ("name_ru", "short_description_ru", "description_ru")
        }),
        ("🇺🇿 Узбекский перевод", {
            "fields": ("name_uz", "short_description_uz", "description_uz")
        }),
        ("🇺🇸 Английский перевод", {
            "fields": ("name_en", "short_description_en", "description_en")
        }),
        ("🔍 Настройки поисковой оптимизации (SEO)", {
            "fields": (
                "meta_title_ru", "meta_title_uz", "meta_title_en", "meta_title",
                "meta_description_ru", "meta_description_uz", "meta_description_en", "meta_description",
                "og_title", "og_description", "canonical_url", "robots_noindex", "robots_nofollow"
            )
        }),
    )
    inlines = [
        ProductImageInline,
        ProductColorInline,
        ProductMemoryVariantInline,
        ProductSimVariantInline,
        ProductVariantInline,
        ProductVideoInline,
        ProductSpecificationInline
    ]
