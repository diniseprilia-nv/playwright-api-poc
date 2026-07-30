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

# with uv (recommended)
uv sync
source .venv/bin/activate
uv run playwright install

# or with pip
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
./run create_order_success --sg
./run create_order_success --sg --number-of-order 3
./run --id                    # all scenarios for ID
```

Equivalent pytest flags:

```bash
pytest tests/route/steps/routing.py --country sg --scenario create_route_today
pytest tests/order/steps/ordering.py --country sg --scenario create_order_success --number-of-order 3
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

### Order scenario tags

| Tag | Description |
|---|---|
| `create_order_success` | Create order(s) with shipper bearer token |

Dynamic order fields in the feature table: `service_type`, `service_level`, `from_data` (`Random` / `index-0..9`), `to_data`, `number_of_order`.  
CLI/env override: `--number-of-order N` or `NUMBER_OF_ORDER=N`.

## Logging

Each scenario run prints:

- **Scenario** and **Country** (bold)
- Operator **Bearer** token
- **Request** method/URL/body
- **Response** status (bold) and body
- **Error** message when status is not 2xx

## Run on GitHub Actions

### 1. Add secrets in GitHub

1. Open the repo: https://github.com/diniseprilia-nv/playwright-api-poc
2. Go to **Settings** → **Secrets and variables** → **Actions**
3. Under **Repository secrets**, click **New repository secret** and add:

| Name | Value |
|---|---|
| `OPERATOR_CLIENT_ID` | your operator client id |
| `OPERATOR_CLIENT_SECRET` | your operator client secret |
| `SHIPPER_CLIENT_ID_SG` | SG shipper client id |
| `SHIPPER_CLIENT_SECRET_SG` | SG shipper client secret |
| `SHIPPER_CLIENT_ID_MY` | MY shipper client id (when needed) |
| `SHIPPER_CLIENT_SECRET_MY` | MY shipper client secret (when needed) |
| `SHIPPER_CLIENT_ID_ID` | ID shipper client id (when needed) |
| `SHIPPER_CLIENT_SECRET_ID` | ID shipper client secret (when needed) |

Optional (as **Variables**, not secrets):

| Name | Example |
|---|---|
| `BASE_URL` | `https://api-qa.ninjavan.co` |
| `API_TIMEOUT_MS` | `30000` |
| `OPERATOR_LOGIN_COUNTRY` | `sg` |

### Local shipper secrets

Do **not** put shipper credentials in committed `config/countries/*.env` files.

```bash
cp config/countries/sg.local.env.example config/countries/sg.local.env
# edit sg.local.env with SHIPPER_CLIENT_ID / SHIPPER_CLIENT_SECRET
```

`*.local.env` is gitignored.

### 2. Run the workflow

- **Automatic:** every push / PR to `main`
- **Manual:**
  1. Go to **Actions** → **API Tests**
  2. Click **Run workflow**
  3. Pick country (`sg` / `my` / `id`)
  4. Set scenario tag (e.g. `create_order_success` or `create_route_today`)
  5. Set **number_of_order** (e.g. `3`) for order scenarios
  6. Click **Run workflow**

## Notes

- `.env` is gitignored — keep secrets local; commit only `.env.example`
- On GitHub, secrets come from Actions secrets (do not commit `.env`)
- Default country is `sg` if no `--sg` / `--my` / `--id` flag is given
- Features stay under `tests/route/features/`; Python steps under `tests/route/steps/`
