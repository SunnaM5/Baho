from __future__ import annotations

from django.contrib import admin
from apps.orders.models import Order, OrderItem, OrderHistory


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "product_name", "color_name", "memory_capacity", "price", "quantity", "total_price")


class OrderHistoryInline(admin.TabularInline):
    model = OrderHistory
    extra = 0
    readonly_fields = ("old_status", "new_status", "comment", "created_at")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number", "full_name", "phone_number", "delivery_method",
        "payment_method", "total_amount", "status", "is_paid", "created_at"
    )
    list_filter = ("status", "delivery_method", "payment_method", "is_paid", "created_at")
    search_fields = ("order_number", "full_name", "phone_number", "delivery_address")
    inlines = [OrderItemInline, OrderHistoryInline]
