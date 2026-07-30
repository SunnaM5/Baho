from __future__ import annotations

from rest_framework import viewsets, permissions
from apps.brands.models import Brand
from apps.brands.serializers import BrandSerializer


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.filter(is_active=True)
    serializer_class = BrandSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"
