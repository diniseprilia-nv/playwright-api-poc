from playwright.sync_api import APIResponse

from clients.base_client import BaseAPIClient


class UsersClient(BaseAPIClient):
    """Client for /users endpoints."""

    def list_users(self) -> APIResponse:
        return self.get("/users")

    def get_user(self, user_id: int) -> APIResponse:
        return self.get(f"/users/{user_id}")
