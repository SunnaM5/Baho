from __future__ import annotations

from django.urls import path
from apps.search.views import (
    EnterpriseSearchView,
    SearchSuggestionsView,
    PopularSearchQueryView,
    SearchHistoryView
)

urlpatterns = [
    path("", EnterpriseSearchView.as_view(), name="search-main"),
    path("suggestions/", SearchSuggestionsView.as_view(), name="search-suggestions"),
    path("popular/", PopularSearchQueryView.as_view(), name="search-popular"),
    path("history/", SearchHistoryView.as_view(), name="search-history"),
]
