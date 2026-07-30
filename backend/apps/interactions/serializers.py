from __future__ import annotations

from rest_framework import serializers
from apps.interactions.models import ProductComparison, RecentlyViewedProduct, StockNotificationRequest
from apps.products.serializers import ProductListSerializer, ProductDetailSerializer
from apps.products.models import Product


class ProductComparisonSerializer(serializers.ModelSerializer):
    products = ProductDetailSerializer(many=True, read_only=True)

    class Meta:
        model = ProductComparison
        fields = ("id", "products", "updated_at")


class RecentlyViewedProductSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = RecentlyViewedProduct
        fields = ("id", "product", "created_at")


class StockNotificationRequestSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source="product")

    class Meta:
        model = StockNotificationRequest
        fields = ("id", "product_id", "email", "phone", "is_notified", "created_at")
