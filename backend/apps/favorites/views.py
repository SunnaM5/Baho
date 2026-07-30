from __future__ import annotations

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.favorites.models import Favorite
from apps.favorites.serializers import FavoriteSerializer
from apps.products.models import Product


class FavoriteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Favorite.objects.filter(user=self.request.user).select_related("product")
        return Favorite.objects.none()

    @action(detail=False, methods=["post"], url_path="toggle")
    def toggle(self, request):
        product_id = request.data.get("product_id")
        if not product_id:
            return Response({"detail": "Поле product_id обязательно."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response({"detail": "Товар не найден."}, status=status.HTTP_404_NOT_FOUND)

        if request.user.is_authenticated:
            favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
            if not created:
                favorite.delete()
                return Response({"is_favorite": False, "detail": "Товар удален из избранного."})
            return Response({"is_favorite": True, "detail": "Товар добавлен в избранное."}, status=status.HTTP_201_CREATED)

        return Response({"is_favorite": True, "detail": "Гостевое избранное обновлено локально."}, status=status.HTTP_200_OK)
