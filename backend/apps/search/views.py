from __future__ import annotations

from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

from apps.search.models import PopularSearchQuery, SearchHistory, SearchAnalytics
from apps.search.services import EnterpriseSearchEngine
from apps.search.serializers import (
    PopularSearchQuerySerializer,
    SearchHistorySerializer,
    SearchSuggestionsSerializer
)
from apps.products.serializers import ProductListSerializer
from apps.categories.models import Category
from apps.brands.models import Brand


class EnterpriseSearchView(APIView):
    """
    GET /api/v1/search/
    Full-text & multi-language search with dynamic synonym expansion, filters, and analytics logging.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        query = request.query_params.get("q", "").strip()

        filters = {
            "category_id": request.query_params.get("category"),
            "brand_id": request.query_params.get("brand"),
            "min_price": request.query_params.get("min_price"),
            "max_price": request.query_params.get("max_price"),
            "is_on_sale": request.query_params.get("is_on_sale") == "true",
        }

        queryset, results_count = EnterpriseSearchEngine.search_products(query, filters)

        # Log analytics and search history
        if query:
            # Update or create PopularSearchQuery stats
            pop_q, created = PopularSearchQuery.objects.get_or_create(query=query)
            if not created:
                pop_q.search_count += 1
            pop_q.results_count = results_count
            pop_q.save()

            # Record Search History
            user = request.user if request.user.is_authenticated else None
            session_key = request.session.session_key or "guest"
            SearchHistory.objects.create(user=user, session_key=session_key, query=query, results_count=results_count)

            # Record Search Analytics
            SearchAnalytics.objects.create(
                query=query,
                results_count=results_count,
                user_agent=request.META.get("HTTP_USER_AGENT", "")[:250]
            )

        # Paginate results
        page = self.paginate_queryset(queryset, request)
        if page is not None:
            serializer = ProductListSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)

        serializer = ProductListSerializer(queryset, many=True, context={"request": request})
        return Response({"count": results_count, "results": serializer.data})

    def paginate_queryset(self, queryset, request):
        from rest_framework.pagination import PageNumberPagination
        self.paginator = PageNumberPagination()
        self.paginator.page_size = 20
        return self.paginator.paginate_queryset(queryset, request, view=self)

    def get_paginated_response(self, data):
        return self.paginator.get_paginated_response(data)


class SearchSuggestionsView(APIView):
    """
    GET /api/v1/search/suggestions/?q=iph
    Autocomplete endpoint returning matching products, categories, brands, and popular search queries.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        query = request.query_params.get("q", "").strip()
        if not query or len(query) < 2:
            return Response({"products": [], "categories": [], "brands": [], "popular_queries": []})

        # Match products
        products_qs, _ = EnterpriseSearchEngine.search_products(query)
        products = ProductListSerializer(products_qs[:5], many=True, context={"request": request}).data

        # Match categories
        categories = list(
            Category.objects.filter(
                Q(name__icontains=query) | Q(name_ru__icontains=query) | Q(name_uz__icontains=query) | Q(name_en__icontains=query)
            ).values("id", "name", "slug")[:3]
        )

        # Match brands
        brands = list(
            Brand.objects.filter(name__icontains=query).values("id", "name", "slug")[:3]
        )

        # Popular queries
        popular = list(
            PopularSearchQuery.objects.filter(query__icontains=query).values_list("query", flat=True)[:5]
        )

        return Response({
            "products": products,
            "categories": categories,
            "brands": brands,
            "popular_queries": popular
        })


class PopularSearchQueryView(APIView):
    """
    GET /api/v1/search/popular/
    Returns top popular search terms.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        queries = PopularSearchQuery.objects.order_by("-is_pinned", "-search_count")[:10]
        serializer = PopularSearchQuerySerializer(queries, many=True)
        return Response(serializer.data)


class SearchHistoryView(APIView):
    """
    GET /api/v1/search/history/
    DELETE /api/v1/search/history/
    User / Guest search history management.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            history = SearchHistory.objects.filter(user=request.user)[:10]
        else:
            session_key = request.session.session_key or "guest"
            history = SearchHistory.objects.filter(session_key=session_key)[:10]

        serializer = SearchHistorySerializer(history, many=True)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            SearchHistory.objects.filter(user=request.user).delete()
        else:
            session_key = request.session.session_key or "guest"
            SearchHistory.objects.filter(session_key=session_key).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
