from __future__ import annotations

from rest_framework import serializers
from apps.search.models import SearchSynonym, PopularSearchQuery, SearchHistory, SearchAnalytics
from apps.products.serializers import ProductListSerializer


class SearchSynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchSynonym
        fields = ("id", "source_term", "target_terms", "is_active")


class PopularSearchQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = PopularSearchQuery
        fields = ("id", "query", "search_count", "results_count", "is_pinned")


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ("id", "query", "results_count", "created_at")


class SearchSuggestionsSerializer(serializers.Serializer):
    products = ProductListSerializer(many=True)
    categories = serializers.ListField(child=serializers.DictField())
    brands = serializers.ListField(child=serializers.DictField())
    popular_queries = serializers.ListField(child=serializers.CharField())
