"""Pretty console logging for API scenario runs."""

from __future__ import annotations

import json
from typing import Any

from playwright.sync_api import APIResponse

BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
RESET = "\033[0m"


def bold(text: str) -> str:
    return f"{BOLD}{text}{RESET}"


def _pretty(data: Any) -> str:
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            return data
    try:
        return json.dumps(data, indent=2, ensure_ascii=False)
    except (TypeError, ValueError):
        return str(data)


def _extract_error_message(body: Any) -> str | None:
    if body is None:
        return None
    if isinstance(body, str):
        text = body.strip()
        return text or None
    if not isinstance(body, dict):
        return str(body)

    for key in ("message", "error", "error_message", "errorMessage", "detail", "title"):
        value = body.get(key)
        if value:
            return str(value)

    errors = body.get("errors")
    if isinstance(errors, list) and errors:
        return "; ".join(str(item) for item in errors)
    if isinstance(errors, dict) and errors:
        return _pretty(errors)
    return None


def log_scenario_header(scenario: str, country: str) -> None:
    print()
    print(f"{CYAN}{'─' * 60}{RESET}")
    print(f"Scenario : {bold(scenario)}")
    print(f"Country  : {bold(country.upper())}")
    print(f"{CYAN}{'─' * 60}{RESET}")


def log_bearer_token(token: str) -> None:
    print(f"Bearer   : {token}")


def log_request(method: str, url: str, body: Any = None) -> None:
    print(f"\n{DIM}Request{RESET}")
    print(f"  {method.upper()} {url}")
    if body is not None:
        print("  Body:")
        for line in _pretty(body).splitlines():
            print(f"    {line}")


def log_response(response: APIResponse) -> None:
    status = response.status
    ok = 200 <= status < 300
    color = GREEN if ok else RED
    print(f"\n{DIM}Response{RESET}")
    print(f"  Status : {color}{bold(str(status))}{RESET}")

    text = response.text()
    body: Any
    try:
        body = response.json()
    except Exception:
        body = text

    print("  Body:")
    for line in _pretty(body).splitlines():
        print(f"    {line}")

    if not ok:
        error_message = _extract_error_message(body) or text.strip() or "(no error message)"
        print(f"  {RED}{bold('Error')}{RESET}  : {error_message}")


def log_error(message: str) -> None:
    print(f"{RED}{bold('Error')}{RESET}  : {message}")
