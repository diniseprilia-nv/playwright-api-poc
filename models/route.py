from datetime import date
from typing import Any

from config.settings import Settings

_ROUTE_ID_KEYS = ("id", "route_id", "routeId")


def build_create_route_payload(settings: Settings, *, route_date: date | None = None) -> dict[str, Any]:
    """Build create-route body using today's date and country config IDs."""
    target_date = route_date or date.today()
    date_str = target_date.isoformat()
    return {
        "date": date_str,
        "datetime": f"{date_str}T00:00:00Z",
        "driver_id": settings.driver_id,
        "hub_id": settings.hub_id,
        "zone_id": settings.zone_id,
    }


def extract_route_id(body: dict[str, Any]) -> int | str:
    """Read route id from top-level or nested `data` envelope."""
    candidates: list[dict[str, Any]] = [body]
    data = body.get("data")
    if isinstance(data, dict):
        candidates.append(data)

    for candidate in candidates:
        for key in _ROUTE_ID_KEYS:
            value = candidate.get(key)
            if value is not None:
                return value

    raise AssertionError(
        f"Expected one of {_ROUTE_ID_KEYS} in response (or response.data): {body}"
    )


def has_route_identity(body: dict[str, Any]) -> bool:
    try:
        extract_route_id(body)
        return True
    except AssertionError:
        return False
