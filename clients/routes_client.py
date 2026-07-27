from typing import Any

from playwright.sync_api import APIResponse

from clients.base_client import BaseAPIClient


class RoutesClient(BaseAPIClient):
    """Client for /{country}/route-v2/routes endpoints."""

    @property
    def _routes_path(self) -> str:
        return f"/{self._settings.country}/route-v2/routes"

    def create_route(self, payload: dict[str, Any]) -> APIResponse:
        return self.post(self._routes_path, data=payload)

    def archive_route(self, route_id: int | str) -> APIResponse:
        return self.put(f"{self._routes_path}/{route_id}/archive")
