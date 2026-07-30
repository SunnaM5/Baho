from django.contrib import admin
from apps.tradein.models import TradeInRequest, InstallmentPlan


@admin.register(TradeInRequest)
class TradeInRequestAdmin(admin.ModelAdmin):
    list_display = ("device_name", "customer_name", "phone_number", "condition", "is_processed", "created_at")
    list_filter = ("condition", "is_processed", "created_at")
    search_fields = ("device_name", "customer_name", "phone_number", "imei")
    actions = ["mark_processed"]

    def mark_processed(self, request, queryset):
        queryset.update(is_processed=True)
    mark_processed.short_description = "Отметить как обработанные"


@admin.register(InstallmentPlan)
class InstallmentPlanAdmin(admin.ModelAdmin):
    list_display = ("months", "markup_percent", "is_active")
    list_filter = ("is_active",)
