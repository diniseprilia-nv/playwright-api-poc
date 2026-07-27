# Playwright Python API Automation Framework

Structured API test framework using **Playwright** (`APIRequestContext`) + **pytest**.

Demo target: [JSONPlaceholder](https://jsonplaceholder.typicode.com). Point at your own API by changing `.env`.

## Layout

```
config/          # BASE_URL, timeout, auth from env
clients/         # BaseAPIClient + resource clients
models/          # TypedDict response shapes
tests/           # fixtures + test cases
utils/           # assertion helpers
```

## Setup

```bash
cd /Users/diniseprilia/my-project/playwright-api-framework
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install
cp .env.example .env
```

## Run tests

```bash
source .venv/bin/activate
pytest -v
```

## Switch to your API

Edit `.env`:

```
BASE_URL=https://your-api.example.com
API_TIMEOUT_MS=30000
AUTH_TOKEN=your-token-here
```
