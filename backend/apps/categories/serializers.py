from __future__ import annotations

from rest_framework import serializers
from apps.categories.models import Category


from apps.common.serializers import TranslatableModelSerializer


class RecursiveCategorySerializer(TranslatableModelSerializer):
    translatable_fields = ("name",)

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "icon", "image", "order")


class CategorySerializer(TranslatableModelSerializer):
    translatable_fields = ("name", "description", "meta_title", "meta_description")
    children = RecursiveCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = (
            "id", "name", "slug", "description", "icon", "image",
            "parent", "children", "order", "is_active",
            "meta_title", "meta_description", "og_title", "og_description", "canonical_url"
        )
