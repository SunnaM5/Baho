from __future__ import annotations

from rest_framework import viewsets, permissions, mixins
from apps.orders.models import Order
from apps.orders.serializers import OrderCreateSerializer, OrderDetailSerializer


class OrderViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    lookup_field = "order_number"

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all().prefetch_related("items")
        return Order.objects.filter(user=user).prefetch_related("items")

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderDetailSerializer
