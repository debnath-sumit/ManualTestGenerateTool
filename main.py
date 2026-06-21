"""Manual Test Case Generator.

A small FastAPI app that turns a Short Description, Description and
Acceptance Criteria into structured manual test cases using Claude.

Run locally:
    uvicorn main:app --reload
Then open http://localhost:8000
"""

import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import anthropic

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

MODEL = "claude-sonnet-4-6"

app = FastAPI(title="Manual Test Case Generator")


class GenerateRequest(BaseModel):
    short_description: str
    description: str = ""
    acceptance_criteria: str = ""


SYSTEM_PROMPT = """\
You are a senior QA engineer who writes clear, thorough manual test cases.

Given a feature's short description, description and acceptance criteria, \
produce a set of manual test cases that gives good coverage: positive paths, \
negative paths, and edge/boundary conditions. Derive cases from the \
acceptance criteria where possible, and add sensible additional cases a \
skilled tester would think of.

Return ONLY a JSON array (no prose, no markdown fences). Each element must be \
an object with exactly these keys:
  - "id": string, like "TC-01"
  - "title": short descriptive title
  - "preconditions": string (use "None" if not applicable)
  - "steps": array of strings, each a single numbered-free action
  - "expectedResult": string describing the expected outcome
  - "priority": one of "High", "Medium", "Low"
  - "type": one of "Positive", "Negative", "Edge"

Aim for 5-12 well-chosen test cases. Keep steps concrete and actionable.
"""


def build_user_prompt(req: GenerateRequest) -> str:
    return (
        f"Short Description:\n{req.short_description.strip()}\n\n"
        f"Description:\n{req.description.strip() or '(none provided)'}\n\n"
        f"Acceptance Criteria:\n{req.acceptance_criteria.strip() or '(none provided)'}\n"
    )


def extract_json_array(text: str):
    """Parse a JSON array from the model output, tolerating code fences."""
    text = text.strip()
    # Strip ```json ... ``` or ``` ... ``` fences if present.
    fence = re.match(r"^```(?:json)?\s*(.*?)\s*```$", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Last resort: grab the outermost [ ... ].
        start, end = text.find("["), text.rfind("]")
        if start != -1 and end != -1 and end > start:
            return json.loads(text[start : end + 1])
        raise


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/generate")
async def generate(req: GenerateRequest):
    if not req.short_description.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Short Description is required."},
        )

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return JSONResponse(
            status_code=500,
            content={
                "error": "ANTHROPIC_API_KEY is not set. Add it to .env "
                "locally or to your Vercel environment variables."
            },
        )

    client = anthropic.Anthropic(api_key=api_key)
    try:
        message = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": build_user_prompt(req)}],
        )
        raw = "".join(
            block.text for block in message.content if block.type == "text"
        )
        test_cases = extract_json_array(raw)
    except anthropic.APIError as exc:
        return JSONResponse(
            status_code=502,
            content={"error": f"Claude API error: {exc}"},
        )
    except (json.JSONDecodeError, ValueError):
        return JSONResponse(
            status_code=502,
            content={"error": "Could not parse test cases from the model response."},
        )

    if not isinstance(test_cases, list):
        return JSONResponse(
            status_code=502,
            content={"error": "Model did not return a list of test cases."},
        )

    return {"testCases": test_cases}
