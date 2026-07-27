"""Python step definitions for create/archive route Gherkin scenarios."""

from datetime import date
from pathlib import Path
from typing import Any

import pytest
from playwright.sync_api import APIResponse
from pytest_bdd import given, parsers, scenarios, then, when

from clients.routes_client import RoutesClient
from config.settings import settings
from models.route import (
    build_create_route_payload,
    extract_route_id,
    has_route_identity,
)
from utils.assertions import assert_status
from utils.console_log import (
    log_bearer_token,
    log_error,
    log_request,
    log_response,
    log_scenario_header,
)

_FEATURES_DIR = Path(__file__).resolve().parent.parent / "features"
scenarios(_FEATURES_DIR / "create_route.feature")
scenarios(_FEATURES_DIR / "archive_route.feature")


@pytest.fixture
def route_ctx() -> dict[str, Any]:
    return {}


@pytest.fixture(autouse=True)
def _log_scenario_run(
    request: pytest.FixtureRequest,
    operator_bearer_token: str,
    route_ctx: dict[str, Any],
) -> None:
    tags = [
        mark.name
        for mark in request.node.iter_markers()
        if mark.name.startswith(("create_route_", "archive_route"))
    ]
    scenario_name = tags[0] if tags else request.node.name
    log_scenario_header(scenario_name, settings.country)
    log_bearer_token(operator_bearer_token)
    route_ctx["bearer_token"] = operator_bearer_token


@given("I am authenticated as an operator")
def authenticated_as_operator(routes_client: RoutesClient) -> RoutesClient:
    """Operator bearer token is applied via the api_request_context fixture."""
    return routes_client


@given("a create route payload for today using country config")
def create_route_payload(route_ctx: dict[str, Any]) -> None:
    route_ctx["payload"] = build_create_route_payload(settings)


@given("country config has valid driver hub and zone ids")
def country_config_has_valid_ids() -> None:
    assert settings.driver_id > 0
    assert settings.hub_id > 0
    assert settings.zone_id > 0


@given(parsers.parse('the payload is missing "{field}"'))
def payload_missing_field(route_ctx: dict[str, Any], field: str) -> None:
    payload = route_ctx["payload"]
    assert field in payload, f"Field {field!r} not in payload: {payload}"
    del payload[field]


@given(parsers.parse("the payload driver_id is set to {driver_id:d}"))
def payload_driver_id_set(route_ctx: dict[str, Any], driver_id: int) -> None:
    route_ctx["payload"]["driver_id"] = driver_id


@given(parsers.parse("the route id is set to {route_id:d}"))
def route_id_is_set(route_ctx: dict[str, Any], route_id: int) -> None:
    route_ctx["route_id"] = route_id


@when("I create a route")
def create_route(routes_client: RoutesClient, route_ctx: dict[str, Any]) -> None:
    path = f"/{settings.country}/route-v2/routes"
    url = f"{settings.base_url}{path}"
    payload = route_ctx["payload"]

    log_request("POST", url, payload)
    response = routes_client.create_route(payload)
    route_ctx["response"] = response
    log_response(response)


@when("I archive the stored route")
def archive_stored_route(routes_client: RoutesClient, route_ctx: dict[str, Any]) -> None:
    route_id = route_ctx.get("route_id")
    assert route_id is not None, "route_id is required before archive"
    path = f"/{settings.country}/route-v2/routes/{route_id}/archive"
    url = f"{settings.base_url}{path}"

    log_request("PUT", url)
    response = routes_client.archive_route(route_id)
    route_ctx["response"] = response
    log_response(response)


@then(parsers.parse("the response status should be {statuses}"))
def response_status_should_be(route_ctx: dict[str, Any], statuses: str) -> None:
    expected = tuple(int(part.strip()) for part in statuses.replace(" or ", ",").split(","))
    response: APIResponse = route_ctx["response"]
    try:
        assert_status(response, expected)
    except AssertionError as exc:
        log_error(str(exc))
        raise


@then("the payload date should be today")
def payload_date_should_be_today(route_ctx: dict[str, Any]) -> None:
    today = date.today().isoformat()
    payload = route_ctx["payload"]
    assert payload["date"] == today
    assert payload["datetime"] == f"{today}T00:00:00Z"


@then("the payload should use country driver hub and zone ids")
def payload_uses_country_ids(route_ctx: dict[str, Any]) -> None:
    payload = route_ctx["payload"]
    assert payload["driver_id"] == settings.driver_id
    assert payload["hub_id"] == settings.hub_id
    assert payload["zone_id"] == settings.zone_id


@then("the response body should not be empty")
def response_body_not_empty(route_ctx: dict[str, Any]) -> None:
    body = route_ctx["response"].json()
    assert body, f"Expected non-empty create route response, got: {body}"


@then("the response should include a route identity")
def response_includes_route_identity(route_ctx: dict[str, Any]) -> None:
    body = route_ctx["response"].json()
    assert has_route_identity(body), (
        f"Expected route id in response (or response.data): {body}"
    )


@then("I store the created route id")
def store_created_route_id(route_ctx: dict[str, Any]) -> None:
    body = route_ctx["response"].json()
    route_ctx["route_id"] = extract_route_id(body)
