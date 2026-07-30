from __future__ import annotations

from typing import Any

from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import exception_handler


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination class for API endpoints.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data: Any) -> Response:
        return Response({
            "status": "success",
            "code": status.HTTP_200_OK,
            "data": {
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            },
            "errors": None
        })


def custom_exception_handler(exc: Exception, context: dict[str, Any]) -> Response | None:
    """
    Custom exception handler for REST Framework that standardizes error responses.
    """
    response = exception_handler(exc, context)

    if response is not None:
        custom_data = {
            "status": "error",
            "code": response.status_code,
            "data": None,
            "errors": response.data if isinstance(response.data, (dict, list)) else {"detail": str(response.data)}
        }
        response.data = custom_data

    return response
