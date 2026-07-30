from __future__ import annotations

from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from apps.products.models import Product
from apps.products.serializers import ProductListSerializer, ProductDetailSerializer
from apps.products.filters import ProductFilter


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Product.objects.filter(is_active=True)
        .select_related("category", "brand")
        .prefetch_related(
            "images", "colors", "memory_variants", "sim_variants", "variants", "videos", "specifications"
        )
    )
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs[lookup_url_kwarg]
        
        # Try fetching by slug first, fallback to PK if UUID is passed
        obj = queryset.filter(slug=lookup_value).first()
        if not obj:
            obj = queryset.filter(pk=lookup_value).first()
        if not obj:
            from rest_framework.exceptions import NotFound
            raise NotFound("Product not found")
        
        self.check_object_permissions(self.request, obj)
        return obj
    search_fields = [
        "name", "name_ru", "name_uz", "name_en",
        "sku", "short_description", "short_description_ru", "short_description_uz", "short_description_en",
        "description", "description_ru", "description_uz", "description_en",
        "brand__name", "category__name", "category__name_ru", "category__name_uz", "category__name_en",
        "specifications__value", "specifications__value_ru", "specifications__value_uz", "specifications__value_en"
    ]
    ordering_fields = ["base_price", "created_at", "rating"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductListSerializer
