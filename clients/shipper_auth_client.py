from typing import Any

from playwright.sync_api import APIResponse

from clients.base_client import BaseAPIClient


class ShipperAuthClient(BaseAPIClient):
    """Fetches the country-specific shipper bearer token via client_credentials grant."""

    def login(self) -> APIResponse:
        client_id = self._settings.shipper_client_id.strip()
        client_secret = self._settings.shipper_client_secret.strip()
        if not client_id or not client_secret:
            raise ValueError(
                "SHIPPER_CLIENT_ID and SHIPPER_CLIENT_SECRET must be set via "
                f"config/countries/{self._settings.country}.local.env (local) "
                f"or GitHub secrets SHIPPER_CLIENT_ID_{self._settings.country.upper()} "
                f"/ SHIPPER_CLIENT_SECRET_{self._settings.country.upper()} (CI)"
            )
        return self.post(
            self._settings.shipper_login_path,
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "client_credentials",
            },
        )

    def get_bearer_token(self) -> str:
        client_id = self._settings.shipper_client_id.strip()
        response = self.login()
        if not response.ok:
            raise RuntimeError(
                f"Shipper login failed ({response.status}) for country="
                f"{self._settings.country!r} path={self._settings.shipper_login_path} "
                f"client_id_len={len(client_id)} client_id_suffix=...{client_id[-4:] if len(client_id) >= 4 else '????'}. "
                f"Body: {response.text()}. "
                "Check GitHub Actions secrets match config/countries/<country>.local.env "
                "(no quotes/spaces), or rotate credentials if they were leaked."
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
