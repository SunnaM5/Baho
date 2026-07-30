from __future__ import annotations

from rest_framework import viewsets, permissions, mixins
from apps.tradein.models import TradeInRequest, InstallmentPlan
from apps.tradein.serializers import TradeInRequestSerializer, InstallmentPlanSerializer


class TradeInViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = TradeInRequestSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        return TradeInRequest.objects.all()


class InstallmentPlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InstallmentPlan.objects.filter(is_active=True)
    serializer_class = InstallmentPlanSerializer
    permission_classes = [permissions.AllowAny]
