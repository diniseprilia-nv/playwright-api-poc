from typing import TypedDict


class Post(TypedDict, total=False):
    userId: int
    id: int
    title: str
    body: str


POST_REQUIRED_FIELDS = ("userId", "id", "title", "body")
