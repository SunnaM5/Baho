from __future__ import annotations

from rest_framework import serializers
from apps.accounts.models import User, UserAddress


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "phone_number", "first_name", "last_name", "email", "role", "created_at")
        read_only_fields = ("id", "role", "created_at")


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ("phone_number", "first_name", "last_name", "email", "password")

    def create(self, validated_data: dict) -> User:
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = (
            "id", "user", "title", "city", "district", "street",
            "building", "apartment", "floor", "comment", "is_default", "created_at"
        )
        read_only_fields = ("id", "user", "created_at")

    def create(self, validated_data: dict) -> UserAddress:
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
