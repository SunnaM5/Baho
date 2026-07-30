from __future__ import annotations

from django.urls import path
from apps.interactions.views import (
    ProductComparisonView,
    RecentlyViewedView,
    ProductRecommendationsView,
    StockNotificationRequestView
)

urlpatterns = [
    path("comparison/", ProductComparisonView.as_view(), name="interactions-comparison"),
    path("recently-viewed/", RecentlyViewedView.as_view(), name="interactions-recently-viewed"),
    path("recommendations/", ProductRecommendationsView.as_view(), name="interactions-recommendations"),
    path("stock-notification/", StockNotificationRequestView.as_view(), name="interactions-stock-notification"),
]
