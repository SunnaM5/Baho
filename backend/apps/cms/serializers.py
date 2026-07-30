from __future__ import annotations

from rest_framework import serializers
from apps.common.serializers import TranslatableModelSerializer
from apps.cms.models import (
    SiteSettings,
    HeroSlide,
    HomeSectionLayout,
    ProductCollection,
    FAQItem,
    NewsArticle,
    AdvantageItem
)
from apps.products.serializers import ProductListSerializer


class SiteSettingsSerializer(TranslatableModelSerializer):
    translatable_fields = ("meta_title", "meta_description")

    class Meta:
        model = SiteSettings
        fields = (
            "site_name", "logo", "favicon", "phone_primary", "phone_secondary",
            "email", "address", "google_maps_url", "working_hours",
            "telegram_url", "instagram_url", "facebook_url", "youtube_url", "tiktok_url",
            "meta_title", "meta_description", "og_title", "og_description", "canonical_url"
        )


class HeroSlideSerializer(TranslatableModelSerializer):
    translatable_fields = ("title", "subtitle", "button_text")
    title = serializers.CharField(read_only=True, required=False)
    subtitle = serializers.CharField(read_only=True, required=False)
    button_text = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = HeroSlide
        fields = (
            "id", "title", "subtitle", "desktop_image", "mobile_image",
            "button_text", "button_url", "bg_color", "priority"
        )


class HomeSectionLayoutSerializer(TranslatableModelSerializer):
    translatable_fields = ("title",)
    title = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = HomeSectionLayout
        fields = ("id", "section_key", "title", "order", "is_visible")


class ProductCollectionSerializer(TranslatableModelSerializer):
    translatable_fields = ("title", "meta_title", "meta_description")
    title = serializers.CharField(read_only=True, required=False)
    meta_title = serializers.CharField(read_only=True, required=False)
    meta_description = serializers.CharField(read_only=True, required=False)
    products = ProductListSerializer(many=True, read_only=True)

    class Meta:
        model = ProductCollection
        fields = (
            "id", "title", "slug", "banner_image", "products",
            "is_featured_on_home", "order",
            "meta_title", "meta_description", "og_title", "og_description"
        )


class FAQItemSerializer(TranslatableModelSerializer):
    translatable_fields = ("question", "answer")
    question = serializers.CharField(read_only=True, required=False)
    answer = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = FAQItem
        fields = ("id", "question", "answer", "category_name", "order")


class NewsArticleSerializer(TranslatableModelSerializer):
    translatable_fields = ("title", "summary", "content", "meta_title", "meta_description")
    title = serializers.CharField(read_only=True, required=False)
    summary = serializers.CharField(read_only=True, required=False)
    content = serializers.CharField(read_only=True, required=False)
    meta_title = serializers.CharField(read_only=True, required=False)
    meta_description = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = NewsArticle
        fields = (
            "id", "title", "slug", "summary", "content", "cover_image",
            "published_at", "meta_title", "meta_description", "og_title", "og_description"
        )


class AdvantageItemSerializer(TranslatableModelSerializer):
    translatable_fields = ("title", "subtitle")
    title = serializers.CharField(read_only=True, required=False)
    subtitle = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = AdvantageItem
        fields = ("id", "title", "subtitle", "icon_name", "order")
