from __future__ import annotations

import logging
from django.db import connection
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

logger = logging.getLogger(__name__)


class HealthCheckView(APIView):
    """
    GET /health/
    Full system health status check including Database, Cache, and Redis.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        health_status = {
            "status": "healthy",
            "database": "unknown",
            "cache": "unknown",
        }

        # Check Database
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                row = cursor.fetchone()
                if row and row[0] == 1:
                    health_status["database"] = "ok"
        except Exception as e:
            logger.error(f"Health check DB failure: {e}")
            health_status["database"] = "error"
            health_status["status"] = "unhealthy"

        # Check Cache / Redis
        try:
            cache.set("health_test_key", "ok", 10)
            val = cache.get("health_test_key")
            if val == "ok":
                health_status["cache"] = "ok"
            else:
                health_status["cache"] = "error"
                health_status["status"] = "unhealthy"
        except Exception as e:
            logger.error(f"Health check Cache failure: {e}")
            health_status["cache"] = "error"
            health_status["status"] = "unhealthy"

        http_status = status.HTTP_200_OK if health_status["status"] == "healthy" else status.HTTP_533_SERVICE_UNAVAILABLE if hasattr(status, 'HTTP_533_SERVICE_UNAVAILABLE') else status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response(health_status, status=http_status)


class LivenessCheckView(APIView):
    """
    GET /health/live/
    Lightweight Kubernetes/Docker liveness probe.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return Response({"status": "alive"}, status=status.HTTP_200_OK)


class ReadinessCheckView(APIView):
    """
    GET /health/ready/
    Kubernetes/Docker readiness probe verifying database connectivity.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return Response({"status": "ready"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Readiness check failed: {e}")
            return Response({"status": "not_ready", "error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
