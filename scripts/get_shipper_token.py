"""Print the country-specific shipper bearer token for manual checks.

Usage:
    COUNTRY=sg python scripts/get_shipper_token.py
    python scripts/get_shipper_token.py   # uses COUNTRY from .env
"""

from playwright.sync_api import sync_playwright

from clients.shipper_auth_client import ShipperAuthClient
from config.settings import settings


def main() -> None:
    with sync_playwright() as playwright:
        context = playwright.request.new_context(
            base_url=settings.base_url,
            extra_http_headers=settings.default_headers,
            timeout=settings.api_timeout_ms,
        )
        try:
            token = ShipperAuthClient(context, settings).get_bearer_token()
        finally:
            context.dispose()

    print(token)


if __name__ == "__main__":
    main()
