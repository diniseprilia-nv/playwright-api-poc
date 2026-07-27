from typing import Any

from playwright.sync_api import APIResponse

from clients.base_client import BaseAPIClient


class OperatorAuthClient(BaseAPIClient):
    """Fetches the shared operator bearer token via client_credentials grant."""

    def login(self) -> APIResponse:
        return self.post(
            self._settings.operator_login_path,
            params={"grant_type": "client_credentials"},
            data={
                "clientId": self._settings.operator_client_id,
                "clientSecret": self._settings.operator_client_secret,
            },
        )

    def get_bearer_token(self) -> str:
        response = self.login()
        if not response.ok:
            raise RuntimeError(
                f"Operator login failed ({response.status}): {response.text()}"
            )

        body: dict[str, Any] = response.json()
        token = (
            body.get("access_token")
            or body.get("accessToken")
            or body.get("token")
        )
        if not token:
            raise RuntimeError(
                f"Operator login response missing access token: {body}"
            )
        return str(token)
