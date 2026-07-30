from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.accounts.models import User, UserAddress


class UserAddressInline(admin.TabularInline):
    model = UserAddress
    extra = 0
    fields = ("title", "city", "district", "street", "building", "apartment", "is_default")


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("phone_number", "first_name", "last_name", "role", "is_staff", "is_active", "created_at")
    list_filter = ("role", "is_staff", "is_active", "created_at")
    search_fields = ("phone_number", "first_name", "last_name", "email")
    ordering = ("-created_at",)
    inlines = [UserAddressInline]

    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Личные данные", {"fields": ("first_name", "last_name", "email")}),
        ("Права доступа", {"fields": ("role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Даты", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "first_name", "last_name", "role", "password1", "password2"),
            },
        ),
    )


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "city", "street", "building", "is_default", "created_at")
    list_filter = ("city", "is_default")
    search_fields = ("user__phone_number", "user__first_name", "user__last_name", "street", "title")
