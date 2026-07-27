"""Shared pytest fixtures and CLI flags.

Flags:
  --country / --env   Country environment: sg | my | id
  --scenario          Run a single scenario by its Gherkin tag
"""

from __future__ import annotations

import os
import sys

import pytest

_SUPPORTED_COUNTRIES = ("sg", "my", "id")


def _apply_country_from_argv() -> None:
    """Set COUNTRY before config.settings is imported."""
    argv = sys.argv
    for i, arg in enumerate(argv):
        if arg in ("--sg", "--my", "--id"):
            os.environ["COUNTRY"] = arg.lstrip("-")
            return
        if arg in ("--country", "--env") and i + 1 < len(argv):
            os.environ["COUNTRY"] = argv[i + 1].strip().lower()
            return
        if arg.startswith("--country="):
            os.environ["COUNTRY"] = arg.split("=", 1)[1].strip().lower()
            return
        if arg.startswith("--env="):
            os.environ["COUNTRY"] = arg.split("=", 1)[1].strip().lower()
            return


_apply_country_from_argv()

from playwright.sync_api import APIRequestContext, Playwright  # noqa: E402

from clients.operator_auth_client import OperatorAuthClient  # noqa: E402
from clients.posts_client import PostsClient  # noqa: E402
from clients.routes_client import RoutesClient  # noqa: E402
from clients.users_client import UsersClient  # noqa: E402
from config.settings import settings  # noqa: E402


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("env")
    group.addoption(
        "--country",
        "--env",
        action="store",
        dest="country",
        default=os.getenv("COUNTRY", "sg"),
        choices=_SUPPORTED_COUNTRIES,
        help="Country environment to use: sg, my, id (default: sg or COUNTRY from .env)",
    )
    group.addoption(
        "--scenario",
        action="store",
        default=None,
        help=(
            "Run one scenario by Gherkin tag, e.g. "
            "--scenario create_route_today"
        ),
    )


def pytest_configure(config: pytest.Config) -> None:
    country = config.getoption("country")
    if country:
        os.environ["COUNTRY"] = str(country).strip().lower()

    config.addinivalue_line("markers", "create_route_today: create route happy path")
    config.addinivalue_line(
        "markers", "create_route_country_ids: payload uses country config ids"
    )
    config.addinivalue_line(
        "markers", "create_route_identity: response includes route identity"
    )
    config.addinivalue_line(
        "markers", "create_route_missing_driver: reject missing driver_id"
    )
    config.addinivalue_line(
        "markers", "create_route_invalid_driver: reject invalid driver_id"
    )
    config.addinivalue_line(
        "markers", "archive_route: create then archive a route"
    )
    config.addinivalue_line(
        "markers", "archive_route_invalid_id: archive with invalid route id"
    )


def pytest_collection_modifyitems(
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    scenario = config.getoption("scenario")
    if not scenario:
        return

    tag = scenario.lstrip("@").strip()
    selected: list[pytest.Item] = []
    deselected: list[pytest.Item] = []
    for item in items:
        marker_names = {mark.name for mark in item.iter_markers()}
        if tag in marker_names or item.name == f"test_{tag}" or item.name == tag:
            selected.append(item)
        else:
            deselected.append(item)

    if not selected:
        available = sorted(
            {
                mark.name
                for item in items
                for mark in item.iter_markers()
                if mark.name.startswith(("create_route_", "archive_route"))
            }
        )
        raise pytest.UsageError(
            f"No tests matched --scenario={scenario!r}. "
            f"Available tags: {', '.join(available) or '(none)'}"
        )

    if deselected:
        config.hook.pytest_deselected(items=deselected)
    items[:] = selected


def pytest_report_header(config: pytest.Config) -> str:
    scenario = config.getoption("scenario")
    parts = [f"country: {settings.country}", f"base_url: {settings.base_url}"]
    if scenario:
        parts.append(f"scenario: {scenario}")
    return " | ".join(parts)


@pytest.fixture(scope="session")
def operator_bearer_token(playwright: Playwright) -> str:
    """Fetch once per session; token is shared across all countries."""
    context = playwright.request.new_context(
        base_url=settings.base_url,
        extra_http_headers=settings.default_headers,
        timeout=settings.api_timeout_ms,
    )
    try:
        return OperatorAuthClient(context, settings).get_bearer_token()
    finally:
        context.dispose()


@pytest.fixture(scope="function")
def api_request_context(
    playwright: Playwright,
    operator_bearer_token: str,
) -> APIRequestContext:
    context = playwright.request.new_context(
        base_url=settings.base_url,
        extra_http_headers=settings.auth_headers(operator_bearer_token),
        timeout=settings.api_timeout_ms,
    )
    yield context
    context.dispose()


@pytest.fixture(scope="function")
def operator_auth_client(api_request_context: APIRequestContext) -> OperatorAuthClient:
    return OperatorAuthClient(api_request_context, settings)


@pytest.fixture(scope="function")
def routes_client(api_request_context: APIRequestContext) -> RoutesClient:
    return RoutesClient(api_request_context, settings)


@pytest.fixture(scope="function")
def posts_client(api_request_context: APIRequestContext) -> PostsClient:
    return PostsClient(api_request_context, settings)


@pytest.fixture(scope="function")
def users_client(api_request_context: APIRequestContext) -> UsersClient:
    return UsersClient(api_request_context, settings)
