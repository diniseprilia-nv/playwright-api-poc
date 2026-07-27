"""Print the shared operator bearer token for manual checks.

Usage:
    python scripts/get_operator_token.py
"""

from playwright.sync_api import sync_playwright

from clients.operator_auth_client import OperatorAuthClient
from config.settings import settings


def main() -> None:
    with sync_playwright() as playwright:
        context = playwright.request.new_context(
            base_url=settings.base_url,
            extra_http_headers=settings.default_headers,
            timeout=settings.api_timeout_ms,
        )
        try:
            token = OperatorAuthClient(context, settings).get_bearer_token()
        finally:
            context.dispose()

    print(token)


if __name__ == "__main__":
    main()
