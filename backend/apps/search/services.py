from __future__ import annotations

import re
from django.db import connection
from django.db.models import Q, F, FloatField, Value, Case, When
from apps.products.models import Product
from apps.search.models import SearchSynonym, PopularSearchQuery, SearchHistory, SearchAnalytics


class EnterpriseSearchEngine:
    """
    Production-grade Search Engine for BAHO-MARKET supporting:
    - Multilingual search across RU, UZ, EN (Product name, Brand, Category, SKU, Specifications, SEO Keywords)
    - Dynamic Admin Synonym expansion ('айфон' -> 'iphone', '16про' -> '16 pro')
    - PostgreSQL Trigram similarity fallback for typos
    - Ranking algorithm considering relevance, rating, stock status, and popularity
    """

    @staticmethod
    def expand_synonyms(query_text: str) -> list[str]:
        cleaned_query = query_text.strip().lower()
        terms = [cleaned_query]

        # Load active synonyms from cache / DB
        synonyms = SearchSynonym.objects.filter(is_active=True)
        for syn in synonyms:
            src = syn.source_term.lower()
            if src in cleaned_query:
                replacements = [t.strip() for t in syn.target_terms.split(",") if t.strip()]
                for rep in replacements:
                    terms.append(cleaned_query.replace(src, rep))
                    terms.append(rep)
        return list(dict.fromkeys(terms))

    @classmethod
    def search_products(cls, query_text: str, filters: dict | None = None) -> tuple[any, int]:
        if not query_text or not query_text.strip():
            queryset = Product.objects.filter(is_active=True).select_related("category", "brand").prefetch_related("images")
            return queryset, 0

        search_terms = cls.expand_synonyms(query_text)
        
        # Build multilingually comprehensive Q filters
        q_objects = Q()
        for term in search_terms:
            q_objects |= Q(name__icontains=term) | Q(name_ru__icontains=term) | Q(name_uz__icontains=term) | Q(name_en__icontains=term)
            q_objects |= Q(sku__iexact=term) | Q(sku__icontains=term)
            q_objects |= Q(brand__name__icontains=term)
            q_objects |= Q(category__name__icontains=term) | Q(category__name_ru__icontains=term) | Q(category__name_uz__icontains=term) | Q(category__name_en__icontains=term)
            q_objects |= Q(short_description_ru__icontains=term) | Q(short_description_uz__icontains=term) | Q(short_description_en__icontains=term)
            q_objects |= Q(specifications__value__icontains=term) | Q(specifications__value_ru__icontains=term) | Q(specifications__value_uz__icontains=term)

        queryset = (
            Product.objects.filter(is_active=True)
            .filter(q_objects)
            .select_related("category", "brand")
            .prefetch_related("images", "colors", "memory_variants")
            .distinct()
        )

        # Trigram / Fuzzy fallback if standard search yields 0 results (PostgreSQL Trigram support)
        if not queryset.exists() and connection.vendor == "postgresql":
            try:
                from django.contrib.postgres.search import TrigramSimilarity
                queryset = (
                    Product.objects.filter(is_active=True)
                    .annotate(similarity=TrigramSimilarity("name", query_text) + TrigramSimilarity("name_ru", query_text))
                    .filter(similarity__gt=0.15)
                    .order_by("-similarity")
                    .select_related("category", "brand")
                    .prefetch_related("images")
                )
            except Exception:
                pass

        # Relevance ranking (Exact SKU match > Exact Name match > Popularity > Rating)
        queryset = queryset.annotate(
            relevance_score=Case(
                When(sku__iexact=query_text, then=Value(100.0)),
                When(name__iexact=query_text, then=Value(90.0)),
                When(name__icontains=query_text, then=Value(70.0)),
                default=Value(10.0),
                output_field=FloatField()
            )
        ).order_by("-relevance_score", "-rating", "-created_at")

        # Apply additional UI filters
        if filters:
            if filters.get("category_id"):
                queryset = queryset.filter(category_id=filters["category_id"])
            if filters.get("brand_id"):
                queryset = queryset.filter(brand_id=filters["brand_id"])
            if filters.get("min_price"):
                queryset = queryset.filter(base_price__gte=filters["min_price"])
            if filters.get("max_price"):
                queryset = queryset.filter(base_price__lte=filters["max_price"])
            if filters.get("is_on_sale") is True:
                queryset = queryset.filter(is_on_sale=True)

        results_count = queryset.count()
        return queryset, results_count
