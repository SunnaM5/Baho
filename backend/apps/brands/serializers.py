from __future__ import annotations

from rest_framework import serializers
from apps.brands.models import Brand


from apps.common.serializers import TranslatableModelSerializer


class BrandSerializer(TranslatableModelSerializer):
    translatable_fields = ("description", "meta_title", "meta_description")

    class Meta:
        model = Brand
        fields = (
            "id", "name", "slug", "logo", "description", "country", "is_active",
            "meta_title", "meta_description", "og_title", "og_description"
        )
