from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.tradein.views import TradeInViewSet, InstallmentPlanViewSet

router = DefaultRouter()
router.register(r"tradein", TradeInViewSet, basename="tradein")
router.register(r"installments", InstallmentPlanViewSet, basename="installment")

urlpatterns = [
    path("", include(router.urls)),
]
