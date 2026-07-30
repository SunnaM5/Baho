from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class HealthCheckAPIViewTests(APITestCase):
    def test_healthcheck_returns_ok(self):
        response = self.client.get(reverse("health-check"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "healthy")

    def test_liveness_and_readiness(self):
        live_res = self.client.get(reverse("health-live"))
        self.assertEqual(live_res.status_code, status.HTTP_200_OK)
        self.assertEqual(live_res.data["status"], "alive")

        ready_res = self.client.get(reverse("health-ready"))
        self.assertEqual(ready_res.status_code, status.HTTP_200_OK)
        self.assertEqual(ready_res.data["status"], "ready")
