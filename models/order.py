from __future__ import annotations

from datetime import date
from typing import Any
from uuid import uuid4

from config.settings import Settings
from data.contacts import contact_to_party, resolve_contact

_TRACKING_KEYS = ("tracking_number", "trackingNumber", "requested_tracking_number")


def build_create_order_payload(
    settings: Settings,
    *,
    service_type: str = "Parcel",
    service_level: str = "Standard",
    from_data: str = "Random",
    to_data: str = "Random",
    order_date: date | None = None,
    merchant_order_number: str | None = None,
) -> dict[str, Any]:
    """Build order-create body with dynamic contacts and today's dates."""
    target_date = (order_date or date.today()).isoformat()
    country_code = settings.country.upper()
    from_contact = resolve_contact(settings.country, from_data)
    to_contact = resolve_contact(settings.country, to_data)
    from_party = contact_to_party(from_contact, country_code)
    to_party = contact_to_party(to_contact, country_code)
    order_ref = merchant_order_number or f"ship-{uuid4().hex[:10]}"

    return {
        "is_staged": False,
        "service_type": service_type,
        "service_level": service_level,
        "requested_tracking_number": None,
        "reference": {
            "merchant_order_number": order_ref,
            "merchant_order_metadata": {
                "delivery_verification_identity": None,
            },
        },
        "from": from_party,
        "to": to_party,
        "parcel_job": {
            "cash_on_delivery": None,
            "is_pickup_required": True,
            "pickup_date": target_date,
            "pickup_service_type": "Scheduled",
            "pickup_service_level": "Standard",
            "pickup_timeslot": {
                "start_time": "09:00",
                "end_time": "22:00",
                "timezone": settings.timezone,
            },
            "pickup_address": from_party,
            "pickup_address_id": f"paid-{settings.country}-{uuid4().hex[:6]}",
            "pickup_instruction": "Please be careful on pickup",
            "delivery_start_date": target_date,
            "delivery_timeslot": {
                "start_time": "09:00",
                "end_time": "18:00",
                "timezone": settings.timezone,
            },
            "delivery_instruction": "Please be careful with the parcel.",
            "dimensions": {
                "weight": 7,
                "height": 2.7,
                "length": 2.8,
                "width": 1,
            },
        },
        "internal_ref": {
            "stamp_id": None,
        },
    }


def extract_tracking_number(body: dict[str, Any]) -> str:
    """Read tracking_number from top-level or nested data envelope."""
    candidates: list[dict[str, Any]] = [body]
    data = body.get("data")
    if isinstance(data, dict):
        candidates.append(data)
    elif isinstance(data, list) and data and isinstance(data[0], dict):
        candidates.append(data[0])

    for candidate in candidates:
        for key in _TRACKING_KEYS:
            value = candidate.get(key)
            if value:
                return str(value)

    raise AssertionError(
        f"Expected one of {_TRACKING_KEYS} in response (or response.data): {body}"
    )
