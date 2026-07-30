from __future__ import annotations

from rest_framework import serializers
from apps.cart.models import Cart, CartItem
from apps.products.serializers import ProductListSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.UUIDField(write_only=True)
    variant_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    color_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    memory_variant_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    
    variant_sku = serializers.CharField(source="variant.sku", read_only=True)
    color_name = serializers.CharField(source="color.name", read_only=True)
    memory_capacity = serializers.CharField(source="memory_variant.capacity", read_only=True)
    unit_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = (
            "id", "product", "product_id", "variant_id", "color_id", "memory_variant_id",
            "variant_sku", "color_name", "memory_capacity", "quantity", "unit_price", "subtotal"
        )
        read_only_fields = ("id", "unit_price", "subtotal")


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    items_count = serializers.IntegerField(read_only=True)
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ("id", "items", "items_count", "subtotal", "total")
