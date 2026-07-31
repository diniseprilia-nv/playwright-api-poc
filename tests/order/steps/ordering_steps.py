"""Python step definitions for create order Gherkin scenarios (shipper auth)."""

import os
from typing import Any
from uuid import uuid4

import pytest
from playwright.sync_api import APIResponse
from pytest_bdd import given, parsers, then, when

from clients.orders_client import OrdersClient
from config.settings import settings
from models.order import build_create_order_payload, extract_tracking_number
from utils.assertions import assert_status
from utils.console_log import (
    log_bearer_token,
    log_error,
    log_request,
    log_response,
    log_scenario_header,
)

_DYNAMIC_FIELDS = {"service_type", "service_level", "from_data", "to_data", "number_of_order"}


def _resolve_number_of_order(options: dict[str, str], pytestconfig: pytest.Config) -> int:
    """Feature table value, overridden by --number-of-order or NUMBER_OF_ORDER env."""
    number_of_order = int(options.get("number_of_order", "1"))
    cli_value = pytestconfig.getoption("number_of_order")
    env_value = os.getenv("NUMBER_OF_ORDER", "").strip()

    if cli_value is not None:
        number_of_order = int(cli_value)
    elif env_value:
        number_of_order = int(env_value)

    if number_of_order < 1:
        raise ValueError("number_of_order must be >= 1")
    return number_of_order


@pytest.fixture
def order_ctx() -> dict[str, Any]:
    return {
        "options": {},
        "payloads": [],
        "responses": [],
        "tracking_numbers": [],
    }


@pytest.fixture(autouse=True)
def _log_scenario_run(
    request: pytest.FixtureRequest,
    shipper_bearer_token: str,
    order_ctx: dict[str, Any],
) -> None:
    tags = [
        mark.name
        for mark in request.node.iter_markers()
        if mark.name.startswith("create_order")
    ]
    scenario_name = tags[0] if tags else request.node.name
    log_scenario_header(scenario_name, settings.country)
    log_bearer_token(shipper_bearer_token)
    order_ctx["bearer_token"] = shipper_bearer_token


@given("I am authenticated as a shipper")
def authenticated_as_shipper(orders_client: OrdersClient) -> OrdersClient:
    return orders_client


@given("a create order payload with:")
def create_order_payload_with_table(
    order_ctx: dict[str, Any],
    datatable: list[list[object]],
    pytestconfig: pytest.Config,
) -> None:
    data_rows = datatable
    if data_rows and str(data_rows[0][0]).strip().lower() in {"field", "key"}:
        data_rows = data_rows[1:]

    options: dict[str, str] = {}
    for row in data_rows:
        if len(row) < 2:
            continue
        options[str(row[0]).strip()] = str(row[1]).strip()

    unknown = set(options) - _DYNAMIC_FIELDS
    if unknown:
        raise ValueError(
            f"Unsupported payload fields {sorted(unknown)}. "
            f"Allowed: {sorted(_DYNAMIC_FIELDS)}"
        )

    number_of_order = _resolve_number_of_order(options, pytestconfig)
    print(f"number_of_order: {number_of_order}")

    order_ctx["options"] = options
    order_ctx["number_of_order"] = number_of_order
    order_ctx["payloads"] = [
        build_create_order_payload(
            settings,
            service_type=options.get("service_type", "Parcel"),
            service_level=options.get("service_level", "Standard"),
            from_data=options.get("from_data", "Random"),
            to_data=options.get("to_data", "Random"),
            merchant_order_number=f"ship-{uuid4().hex[:10]}-{index + 1}",
        )
        for index in range(number_of_order)
    ]


@when("I create the order(s)")
def create_the_orders(orders_client: OrdersClient, order_ctx: dict[str, Any]) -> None:
    payloads: list[dict[str, Any]] = order_ctx["payloads"]
    assert payloads, "No order payloads prepared"
    path = f"/{settings.country}/order-create/4.1/orders"
    url = f"{settings.base_url}{path}"

    responses: list[APIResponse] = []
    for index, payload in enumerate(payloads, start=1):
        print(f"\nOrder {index}/{len(payloads)}")
        log_request("POST", url, payload)
        response = orders_client.create_order(payload)
        log_response(response)
        responses.append(response)

    order_ctx["responses"] = responses
    order_ctx["response"] = responses[-1]


@then(parsers.parse("each order response status should be {statuses}"))
def each_order_response_status(order_ctx: dict[str, Any], statuses: str) -> None:
    expected = tuple(int(part.strip()) for part in statuses.replace(" or ", ",").split(","))
    responses: list[APIResponse] = order_ctx["responses"]
    assert responses, "No order responses captured"
    for index, response in enumerate(responses, start=1):
        try:
            assert_status(response, expected)
        except AssertionError as exc:
            log_error(f"Order {index}: {exc}")
            raise


@then("I store the tracking number(s)")
def store_tracking_numbers(order_ctx: dict[str, Any]) -> None:
    tracking_numbers: list[str] = []
    for index, response in enumerate(order_ctx["responses"], start=1):
        body = response.json()
        tracking = extract_tracking_number(body)
        tracking_numbers.append(tracking)
        print(f"Stored tracking_number[{index}]: {tracking}")

    order_ctx["tracking_numbers"] = tracking_numbers
    order_ctx["tracking_number"] = tracking_numbers[0]
