from collections.abc import Iterable
from typing import Any

from playwright.sync_api import APIResponse


def assert_status(response: APIResponse, expected: int | Iterable[int]) -> None:
    expected_set = {expected} if isinstance(expected, int) else set(expected)
    assert response.status in expected_set, (
        f"Expected status {expected_set}, got {response.status}. "
        f"Body: {response.text()[:500]}"
    )


def assert_json_keys(payload: dict[str, Any], required_keys: Iterable[str]) -> None:
    missing = [key for key in required_keys if key not in payload]
    assert not missing, f"Missing keys {missing} in payload: {payload}"


def assert_non_empty_list(payload: Any) -> list[Any]:
    assert isinstance(payload, list), f"Expected list, got {type(payload).__name__}"
    assert len(payload) > 0, "Expected non-empty list"
    return payload
