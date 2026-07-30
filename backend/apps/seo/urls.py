from __future__ import annotations

from django.urls import path
from apps.seo.views import SeoMetaView

urlpatterns = [
    path("meta/", SeoMetaView.as_view(), name="seo-meta"),
]
