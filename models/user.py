from typing import TypedDict


class User(TypedDict, total=False):
    id: int
    name: str
    username: str
    email: str


USER_REQUIRED_FIELDS = ("id", "name", "username", "email")
