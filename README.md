# 🧪 Manual Test Case Generator

A small web app that turns a **Short Description**, **Description** and
**Acceptance Criteria** into structured manual test cases using Claude.

Each test case includes: ID, Title, Preconditions, Steps, Expected Result,
Priority and Type (Positive / Negative / Edge). Results show in a table and
can be **copied to clipboard** or **downloaded as CSV** (Excel / TestRail /
Zephyr / Xray friendly).

Built with **FastAPI** + the official **Anthropic Python SDK**. Runs locally
and deploys to **Vercel**.

## Run locally

```bash
# 1. Install dependencies (use a virtualenv if you like)
pip install -r requirements.txt

# 2. Add your Anthropic API key
cp .env.example .env
#   then edit .env and paste your key

# 3. Start the app
uvicorn main:app --reload
```

Open http://localhost:8000

## Deploy to Vercel

1. Push this repo to GitHub.
2. In Vercel, **Add New → Project** and import the repo.
3. Under **Settings → Environment Variables**, add:
   - `ANTHROPIC_API_KEY` = your key
4. Deploy. Vercel uses `vercel.json` to run `main.py` as a Python
   serverless function.

> The API key lives only on the server (env var) — it is never sent to the
> browser.

## Project structure

```
main.py              FastAPI app: serves the page + /api/generate endpoint
templates/index.html The single-page UI (form, table, copy, CSV)
requirements.txt     Python dependencies
vercel.json          Vercel Python build + routing config
.env.example         Template for your local .env
```

## Configuration

- Model is set in `main.py` via `MODEL = "claude-sonnet-4-6"`. Change it
  there if you want a different Claude model.
