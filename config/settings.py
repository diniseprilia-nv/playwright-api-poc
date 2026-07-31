import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_COUNTRIES_DIR = Path(__file__).resolve().parent / "countries"
_SUPPORTED_COUNTRIES = ("sg", "my", "id")

# Resolve country from process env / root .env first (do not override existing env)
load_dotenv(_PROJECT_ROOT / ".env")

_country = os.getenv("COUNTRY", "sg").strip().lower()
if _country not in _SUPPORTED_COUNTRIES:
    raise ValueError(
        f"Unsupported COUNTRY={_country!r}. Expected one of: {', '.join(_SUPPORTED_COUNTRIES)}"
    )

_country_env = _COUNTRIES_DIR / f"{_country}.env"
if not _country_env.exists():
    raise FileNotFoundError(f"Country config not found: {_country_env}")

_country_local_env = _COUNTRIES_DIR / f"{_country}.local.env"

# Preserve CI/process env secrets: only fill missing keys from files when override=False.
# Order: country defaults → country local secrets → root shared secrets.
load_dotenv(_country_env, override=False)
load_dotenv(_country_local_env, override=False)
load_dotenv(_PROJECT_ROOT / ".env", override=False)

# Keep the selected country authoritative (CLI / COUNTRY env wins)
os.environ["COUNTRY"] = _country


@dataclass(frozen=True)
class Settings:
    country: str
    country_name: str
    timezone: str
    language: str
    locale: str
    currency: str
    base_url: str
    api_timeout_ms: int
    operator_client_id: str
    operator_client_secret: str
    operator_login_country: str
    shipper_client_id: str
    shipper_client_secret: str
    driver_id: int
    hub_id: int
    zone_id: int

    @property
    def operator_login_path(self) -> str:
        return f"/{self.operator_login_country}/aaa/login"

    @property
    def shipper_login_path(self) -> str:
        return f"/{self.country}/aaa/2.0/oauth/access_token"

    @property
    def default_headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "cache-control": "no-cache",
        }

    def auth_headers(self, bearer_token: str) -> dict[str, str]:
        return {
            **self.default_headers,
            "Authorization": f"Bearer {bearer_token}",
        }


def _load_settings() -> Settings:
    client_id = os.getenv("OPERATOR_CLIENT_ID", "").strip()
    client_secret = os.getenv("OPERATOR_CLIENT_SECRET", "").strip()
    if not client_id or not client_secret:
        raise ValueError(
            "OPERATOR_CLIENT_ID and OPERATOR_CLIENT_SECRET must be set in .env"
        )

    country = os.getenv("COUNTRY", "sg").strip().lower()
    country_upper = country.upper()
    # Accept both SHIPPER_CLIENT_ID and SHIPPER_CLIENT_ID_SG (country-suffixed)
    shipper_client_id = (
        os.getenv("SHIPPER_CLIENT_ID", "").strip()
        or os.getenv(f"SHIPPER_CLIENT_ID_{country_upper}", "").strip()
    )
    shipper_client_secret = (
        os.getenv("SHIPPER_CLIENT_SECRET", "").strip()
        or os.getenv(f"SHIPPER_CLIENT_SECRET_{country_upper}", "").strip()
    )

    return Settings(
        country=country,
        country_name=os.getenv("COUNTRY_NAME", "").strip(),
        timezone=os.getenv("TIMEZONE", "Asia/Singapore").strip(),
        language=os.getenv("LANGUAGE", "en").strip(),
        locale=os.getenv("LOCALE", "en-SG").strip(),
        currency=os.getenv("CURRENCY", "SGD").strip(),
        base_url=os.getenv("BASE_URL", "https://api-qa.ninjavan.co").rstrip("/"),
        api_timeout_ms=int(os.getenv("API_TIMEOUT_MS", "30000")),
        operator_client_id=client_id,
        operator_client_secret=client_secret,
        operator_login_country=os.getenv("OPERATOR_LOGIN_COUNTRY", "sg").strip().lower(),
        shipper_client_id=shipper_client_id,
        shipper_client_secret=shipper_client_secret,
        driver_id=int(os.getenv("DRIVER_ID", "0")),
        hub_id=int(os.getenv("HUB_ID", "0")),
        zone_id=int(os.getenv("ZONE_ID", "0")),
    )


settings = _load_settings()
