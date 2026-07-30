from typing import Any
from uuid import uuid4

from playwright.sync_api import APIResponse

from clients.base_client import BaseAPIClient


class OrdersClient(BaseAPIClient):
    """Client for /{country}/order-create/4.1/orders endpoints."""

    @property
    def _orders_path(self) -> str:
        return f"/{self._settings.country}/order-create/4.1/orders"

    def create_order(self, payload: dict[str, Any]) -> APIResponse:
        headers = {
            "x-nv-request-id": str(uuid4()),
        }
        return self.post(self._orders_path, data=payload, headers=headers)
