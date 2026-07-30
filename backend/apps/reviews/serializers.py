from __future__ import annotations

from rest_framework import serializers
from apps.reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ("id", "product", "user", "user_name", "rating", "title", "comment", "pros", "cons", "created_at")
        read_only_fields = ("id", "user", "user_name", "created_at")

    def get_user_name(self, obj: Review) -> str:
        name = f"{obj.user.first_name} {obj.user.last_name}".strip()
        return name if name else "Покупатель"

    def create(self, validated_data: dict) -> Review:
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
