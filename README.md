# Playwright API POC

API automation framework for Ninja Van QA using **Playwright** (`APIRequestContext`), **pytest**, and **pytest-bdd** (Gherkin).

## Layout

```
config/
  countries/           # Per-country env (sg, my, id)
  settings.py          # Loads shared .env + selected country config
clients/               # API clients (operator auth, routes, …)
models/                # Payload builders / response helpers
tests/
  route/
    features/          # Gherkin .feature files
    steps/             # Python step definitions
  conftest.py          # Fixtures, --country / --scenario flags
scripts/               # Helpers (e.g. print operator token)
run                    # Simple CLI: ./run <scenario> --sg
utils/                 # Assertions + console logging
```

## Setup

```bash
git clone git@github.com-work:diniseprilia-nv/playwright-api-poc.git
cd playwright-api-poc
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install
cp .env.example .env
```

Fill `.env` with shared secrets (not country-specific):

```env
COUNTRY=sg
BASE_URL=https://api-qa.ninjavan.co
API_TIMEOUT_MS=30000

OPERATOR_CLIENT_ID=...
OPERATOR_CLIENT_SECRET=...
OPERATOR_LOGIN_COUNTRY=sg
```

Country-specific values live in `config/countries/{sg,my,id}.env` (e.g. `DRIVER_ID`, `HUB_ID`, `ZONE_ID`).

## Operator auth

Bearer token is fetched once per session via:

`POST /{login_country}/aaa/login?grant_type=client_credentials`

Credentials stay in root `.env` (shared across countries). To print a token manually:

```bash
python scripts/get_operator_token.py
```

## Run scenarios

Preferred CLI:

```bash
./run create_route_today --sg
./run archive_route --my
./run --id                    # all route scenarios for ID
```

Equivalent pytest flags:

```bash
pytest tests/route/steps/routing.py --country sg --scenario create_route_today
```

### Route scenario tags

| Tag | Description |
|---|---|
| `create_route_today` | Create route for today using country config |
| `create_route_country_ids` | Assert payload uses country driver/hub/zone |
| `create_route_identity` | Response includes route id (`data.id`) |
| `create_route_missing_driver` | Reject missing `driver_id` |
| `create_route_invalid_driver` | Reject invalid `driver_id` |
| `archive_route` | Create route, then archive it |
| `archive_route_invalid_id` | Archive with invalid route id |

## Logging

Each scenario run prints:

- **Scenario** and **Country** (bold)
- Operator **Bearer** token
- **Request** method/URL/body
- **Response** status (bold) and body
- **Error** message when status is not 2xx

## Notes

- `.env` is gitignored — keep secrets local; commit only `.env.example`
- Default country is `sg` if no `--sg` / `--my` / `--id` flag is given
- Features stay under `tests/route/features/`; Python steps under `tests/route/steps/`
