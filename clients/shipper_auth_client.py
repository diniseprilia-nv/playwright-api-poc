from typing import Any

from playwright.sync_api import APIResponse

from clients.base_client import BaseAPIClient


class ShipperAuthClient(BaseAPIClient):
    """Fetches the country-specific shipper bearer token via client_credentials grant."""

    def login(self) -> APIResponse:
        if not self._settings.shipper_client_id or not self._settings.shipper_client_secret:
            raise ValueError(
                "SHIPPER_CLIENT_ID and SHIPPER_CLIENT_SECRET must be set in "
                f"config/countries/{self._settings.country}.env"
            )
        return self.post(
            self._settings.shipper_login_path,
            data={
                "client_id": self._settings.shipper_client_id,
                "client_secret": self._settings.shipper_client_secret,
                "grant_type": "client_credentials",
            },
        )

    def get_bearer_token(self) -> str:
        response = self.login()
        if not response.ok:
            raise RuntimeError(
                f"Shipper login failed ({response.status}): {response.text()}"
            )

        body: dict[str, Any] = response.json()
        token = (
            body.get("access_token")
            or body.get("accessToken")
            or body.get("token")
        )
        if not token:
            raise RuntimeError(
                f"Shipper login response missing access token: {body}"
            )
        return str(token)
