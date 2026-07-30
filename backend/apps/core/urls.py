from __future__ import annotations

from django.urls import path
from apps.core.views import HealthCheckView, LivenessCheckView, ReadinessCheckView

urlpatterns = [
    path("", HealthCheckView.as_view(), name="health-check"),
    path("live/", LivenessCheckView.as_view(), name="health-live"),
    path("ready/", ReadinessCheckView.as_view(), name="health-ready"),
]
