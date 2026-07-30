from __future__ import annotations

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.cms.views import (
    HomePageDataView,
    ProductCollectionViewSet,
    FAQItemViewSet,
    NewsArticleViewSet
)

router = DefaultRouter()
router.register("collections", ProductCollectionViewSet, basename="cms-collections")
router.register("faq", FAQItemViewSet, basename="cms-faq")
router.register("news", NewsArticleViewSet, basename="cms-news")

urlpatterns = [
    path("home/", HomePageDataView.as_view(), name="cms-home-data"),
    path("", include(router.urls)),
]
