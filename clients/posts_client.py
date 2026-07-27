from typing import Any

from playwright.sync_api import APIResponse

from clients.base_client import BaseAPIClient


class PostsClient(BaseAPIClient):
    """Client for /posts endpoints."""

    def list_posts(self) -> APIResponse:
        return self.get("/posts")

    def get_post(self, post_id: int) -> APIResponse:
        return self.get(f"/posts/{post_id}")

    def create_post(self, payload: dict[str, Any]) -> APIResponse:
        return self.post("/posts", data=payload)
