from __future__ import annotations

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q, F

from apps.interactions.models import ProductComparison, RecentlyViewedProduct, StockNotificationRequest
from apps.interactions.serializers import (
    ProductComparisonSerializer,
    RecentlyViewedProductSerializer,
    StockNotificationRequestSerializer
)
from apps.products.models import Product
from apps.products.serializers import ProductListSerializer
from apps.orders.models import OrderItem


class ProductComparisonView(APIView):
    """
    GET /api/v1/interactions/comparison/
    POST /api/v1/interactions/comparison/  (product_id)
    DELETE /api/v1/interactions/comparison/ (product_id)
    Strict enforcement:
      - Max 4 products
      - Same root/category enforcement across all comparison items
    """
    permission_classes = [permissions.AllowAny]

    def _get_or_create_comparison(self, request):
        if request.user.is_authenticated:
            comparison, _ = ProductComparison.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key or request.session.create() or request.session.session_key
            comparison, _ = ProductComparison.objects.get_or_create(session_key=session_key)
        return comparison

    def get(self, request, *args, **kwargs):
        comparison = self._get_or_create_comparison(request)
        serializer = ProductComparisonSerializer(comparison, context={"request": request})
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        product_id = request.data.get("product_id")
        product = get_object_or_404(Product, id=product_id, is_active=True)
        comparison = self._get_or_create_comparison(request)

        current_products = list(comparison.products.all())

        if len(current_products) >= 4:
            return Response(
                {"error": "Максимальное количество товаров для сравнения — 4."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if current_products and any(p.category_id != product.category_id for p in current_products):
            return Response(
                {"error": "Сравнивать можно только товары из одной категории."},
                status=status.HTTP_400_BAD_REQUEST
            )

        comparison.products.add(product)
        serializer = ProductComparisonSerializer(comparison, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get("product_id")
        comparison = self._get_or_create_comparison(request)
        if product_id:
            product = get_object_or_404(Product, id=product_id)
            comparison.products.remove(product)
        else:
            comparison.products.clear()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecentlyViewedView(APIView):
    """
    GET /api/v1/interactions/recently-viewed/
    POST /api/v1/interactions/recently-viewed/ (product_id)
    Strict enforcement: capped at max 30 items per user/session with automatic pruning.
    """
    permission_classes = [permissions.AllowAny]
    MAX_ITEMS = 30

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            items = RecentlyViewedProduct.objects.filter(user=request.user).select_related("product", "product__category", "product__brand").prefetch_related("product__images")[:15]
        else:
            session_key = request.session.session_key or "guest"
            items = RecentlyViewedProduct.objects.filter(session_key=session_key).select_related("product", "product__category", "product__brand").prefetch_related("product__images")[:15]

        serializer = RecentlyViewedProductSerializer(items, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        product_id = request.data.get("product_id")
        product = get_object_or_404(Product, id=product_id, is_active=True)

        if request.user.is_authenticated:
            item, created = RecentlyViewedProduct.objects.get_or_create(user=request.user, product=product)
            qs = RecentlyViewedProduct.objects.filter(user=request.user)
        else:
            session_key = request.session.session_key or request.session.create() or request.session.session_key
            item, created = RecentlyViewedProduct.objects.get_or_create(session_key=session_key, product=product)
            qs = RecentlyViewedProduct.objects.filter(session_key=session_key)

        if not created:
            item.save()

        # Automatic pruning if history exceeds MAX_ITEMS
        excess_ids = list(qs.order_by("-created_at").values_list("id", flat=True)[self.MAX_ITEMS:])
        if excess_ids:
            qs.filter(id__in=excess_ids).delete()

        return Response({"status": "added"}, status=status.HTTP_201_CREATED)


class ProductRecommendationsView(APIView):
    """
    GET /api/v1/interactions/recommendations/?product_id=1
    Multi-faceted recommendations engine considering:
      1. Category & Brand match
      2. Price range (±30% of target product)
      3. Stock availability & rating
      4. True "Customers Also Bought" based on OrderItem co-occurrence
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        product_id = request.query_params.get("product_id") or kwargs.get("product_id")
        product = get_object_or_404(Product, pk=product_id)

        # 1. Multi-factor Similar Products (Category + Brand + Price range ±30% + Stock > 0)
        min_price = product.base_price * Decimal("0.70")
        max_price = product.base_price * Decimal("1.30")

        similar_products = Product.objects.filter(
            is_active=True,
            stock__gt=0,
            category=product.category,
            base_price__gte=min_price,
            base_price__lte=max_price
        ).exclude(id=product.id).select_related("category", "brand").prefetch_related("images").order_by("-rating", "-reviews_count")[:6]

        # Fallback if strict price range returns fewer than 3 products
        if similar_products.count() < 3:
            similar_products = Product.objects.filter(
                is_active=True,
                category=product.category
            ).exclude(id=product.id).select_related("category", "brand").prefetch_related("images").order_by("-rating")[:6]

        # 2. Real Order Co-occurrence ("Customers Also Bought")
        related_order_ids = OrderItem.objects.filter(product=product).values_list("order_id", flat=True)[:100]
        co_bought_ids = list(
            OrderItem.objects.filter(order_id__in=related_order_ids)
            .exclude(product=product)
            .values("product_id")
            .annotate(freq=Count("product_id"))
            .order_by("-freq")
            .values_list("product_id", flat=True)[:4]
        )

        frequently_bought = Product.objects.filter(
            id__in=co_bought_ids,
            is_active=True
        ).select_related("category", "brand").prefetch_related("images")

        # Fallback for frequently bought if no historical order co-occurrences exist yet
        if frequently_bought.count() == 0:
            frequently_bought = Product.objects.filter(
                is_active=True,
                category=product.category
            ).exclude(id=product.id).order_by("-rating", "-reviews_count")[:4]

        return Response({
            "similar_products": ProductListSerializer(similar_products, many=True, context={"request": request}).data,
            "frequently_bought_together": ProductListSerializer(frequently_bought, many=True, context={"request": request}).data
        })


class StockNotificationRequestView(APIView):
    """
    POST /api/v1/interactions/stock-notification/
    Subscribe to back-in-stock notifications.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = StockNotificationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user if request.user.is_authenticated else None
        serializer.save(user=user)
        return Response({"status": "subscribed"}, status=status.HTTP_201_CREATED)
