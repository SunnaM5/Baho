from __future__ import annotations

from rest_framework import serializers
from apps.favorites.models import Favorite
from apps.products.serializers import ProductListSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Favorite
        fields = ("id", "product", "product_id", "created_at")
        read_only_fields = ("id", "created_at")

    def create(self, validated_data: dict) -> Favorite:
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
