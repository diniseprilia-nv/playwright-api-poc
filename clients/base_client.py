from typing import Any

from playwright.sync_api import APIRequestContext, APIResponse

from config.settings import Settings


class BaseAPIClient:
    """Thin wrapper around Playwright APIRequestContext."""

    def __init__(self, request_context: APIRequestContext, settings: Settings) -> None:
        self._request = request_context
        self._settings = settings

    def _merge_headers(self, headers: dict[str, str] | None) -> dict[str, str]:
        merged = dict(self._settings.default_headers)
        if headers:
            merged.update(headers)
        return merged

    def get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> APIResponse:
        return self._request.get(
            path,
            params=params,
            headers=self._merge_headers(headers),
            timeout=self._settings.api_timeout_ms,
        )

    def post(
        self,
        path: str,
        *,
        data: Any = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> APIResponse:
        return self._request.post(
            path,
            data=data,
            params=params,
            headers=self._merge_headers(headers),
            timeout=self._settings.api_timeout_ms,
        )

    def put(
        self,
        path: str,
        *,
        data: Any = None,
        headers: dict[str, str] | None = None,
    ) -> APIResponse:
        return self._request.put(
            path,
            data=data,
            headers=self._merge_headers(headers),
            timeout=self._settings.api_timeout_ms,
        )

    def patch(
        self,
        path: str,
        *,
        data: Any = None,
        headers: dict[str, str] | None = None,
    ) -> APIResponse:
        return self._request.patch(
            path,
            data=data,
            headers=self._merge_headers(headers),
            timeout=self._settings.api_timeout_ms,
        )

    def delete(
        self,
        path: str,
        *,
        headers: dict[str, str] | None = None,
    ) -> APIResponse:
        return self._request.delete(
            path,
            headers=self._merge_headers(headers),
            timeout=self._settings.api_timeout_ms,
        )
