from __future__ import annotations

from django.contrib import admin
from apps.search.models import SearchSynonym, PopularSearchQuery, SearchHistory, SearchAnalytics


@admin.register(SearchSynonym)
class SearchSynonymAdmin(admin.ModelAdmin):
    list_display = ("source_term", "target_terms", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("source_term", "target_terms")


@admin.register(PopularSearchQuery)
class PopularSearchQueryAdmin(admin.ModelAdmin):
    list_display = ("query", "search_count", "results_count", "is_pinned", "updated_at")
    list_filter = ("is_pinned",)
    list_editable = ("is_pinned",)
    search_fields = ("query",)


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ("query", "user", "session_key", "results_count", "created_at")
    list_filter = ("created_at",)
    search_fields = ("query", "user__phone", "session_key")


@admin.register(SearchAnalytics)
class SearchAnalyticsAdmin(admin.ModelAdmin):
    list_display = ("query", "results_count", "converted_order", "created_at")
    list_filter = ("converted_order", "created_at")
    search_fields = ("query",)
