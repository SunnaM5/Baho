from __future__ import annotations

from rest_framework import serializers
from apps.orders.models import Order, OrderItem
from apps.orders.services import OrderService


class OrderItemInputSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)
    color_name = serializers.CharField(required=False, allow_blank=True, default="")
    memory_capacity = serializers.CharField(required=False, allow_blank=True, default="")
    expected_price = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("id", "product", "product_name", "color_name", "memory_capacity", "price", "quantity", "total_price")


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemInputSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = (
            "id", "order_number", "full_name", "phone_number", "email",
            "delivery_method", "delivery_address", "payment_method",
            "comment", "items", "total_amount", "status", "created_at"
        )
        read_only_fields = ("id", "order_number", "total_amount", "status", "created_at")

    def create(self, validated_data: dict) -> Order:
        items_data = validated_data.pop("items")
        request = self.context.get("request")
        user = request.user if request and request.user.is_authenticated else None

        idempotency_key = None
        if request:
            idempotency_key = request.headers.get("X-Idempotency-Key") or request.headers.get("Idempotency-Key")

        return OrderService.create_order(
            user=user,
            items_data=items_data,
            idempotency_key=idempotency_key,
            **validated_data
        )


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id", "order_number", "full_name", "phone_number", "email",
            "delivery_method", "delivery_address", "payment_method",
            "is_paid", "total_amount", "status", "comment", "items", "created_at"
        )
