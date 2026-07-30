from __future__ import annotations

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cms.models import (
    SiteSettings,
    HeroSlide,
    HomeSectionLayout,
    ProductCollection,
    FAQItem,
    NewsArticle,
    AdvantageItem
)
from apps.cms.serializers import (
    SiteSettingsSerializer,
    HeroSlideSerializer,
    HomeSectionLayoutSerializer,
    ProductCollectionSerializer,
    FAQItemSerializer,
    NewsArticleSerializer,
    AdvantageItemSerializer
)


from django.core.cache import cache

CACHE_KEY_HOMEPAGE = "cms_homepage_data_{lang}"


class HomePageDataView(APIView):
    """
    Unified Endpoint for Homepage rendering (Zero roundtrips) with Redis caching.
    Returns hero slides, ordered layout sections, featured collections, advantages, news, and site settings.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        lang = request.query_params.get("lang") or request.headers.get("Accept-Language", "ru")[:2]
        if lang not in ["ru", "uz", "en"]:
            lang = "ru"

        cache_key = CACHE_KEY_HOMEPAGE.format(lang=lang)
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        settings = SiteSettings.objects.first()
        sections = HomeSectionLayout.objects.filter(is_visible=True).order_by("order")
        slides = HeroSlide.objects.filter(is_active=True).order_by("priority")
        collections = ProductCollection.objects.filter(is_active=True, is_featured_on_home=True).prefetch_related(
            "products__images", "products__category", "products__brand"
        )
        advantages = AdvantageItem.objects.filter(is_active=True).order_by("order")
        news = NewsArticle.objects.filter(is_published=True).order_by("-published_at")[:4]

        data = {
            "settings": SiteSettingsSerializer(settings, context={"request": request}).data if settings else None,
            "layout_sections": HomeSectionLayoutSerializer(sections, many=True, context={"request": request}).data,
            "hero_slides": HeroSlideSerializer(slides, many=True, context={"request": request}).data,
            "featured_collections": ProductCollectionSerializer(collections, many=True, context={"request": request}).data,
            "advantages": AdvantageItemSerializer(advantages, many=True, context={"request": request}).data,
            "latest_news": NewsArticleSerializer(news, many=True, context={"request": request}).data,
        }

        cache.set(cache_key, data, timeout=3600)  # 1 hour cache with auto-invalidation on model save
        return Response(data)


class ProductCollectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductCollection.objects.filter(is_active=True).prefetch_related("products__images")
    serializer_class = ProductCollectionSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"


class FAQItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FAQItem.objects.filter(is_active=True).order_by("order")
    serializer_class = FAQItemSerializer
    permission_classes = [permissions.AllowAny]


class NewsArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NewsArticle.objects.filter(is_published=True).order_by("-published_at")
    serializer_class = NewsArticleSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"
