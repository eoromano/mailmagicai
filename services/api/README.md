# ThreadSense API

This service is the backend foundation for ThreadSense. It uses FastAPI, pydantic, environment-based configuration, deterministic intelligence services, and model-ready orchestration so the app can run end to end before Outlook or model integrations exist.

## Endpoints

- `GET /health`
- `POST /triage/thread`
- `POST /summarize/thread`
- `POST /extract/asks`
- `POST /draft/reply`
- `POST /catchup`
- `POST /thoughtpartner`

## Run

```bash
cd services/api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

You can also use the repo root helpers:

```bash
npm run setup:api
npm run dev:api
```

For the first milestone, this API is optional for the default mock demo but ready for deterministic end-to-end testing with the add-in.

## Structure

- `app/config/` contains settings and logging setup
- `app/routes/` contains the HTTP endpoints
- `app/schemas/` contains request and response models
- `app/services/` contains deterministic logic, model boundaries, and orchestration
- `app/prompts/` contains markdown prompt files for each major intelligence feature
- `app/main.py` creates the app and middleware

## Current Scope

- Deterministic responses only
- No auth
- No Graph access
- No real model client yet, but each feature now has a model-ready boundary

## Rules To Model Evolution

Each intelligence area now follows the same shape:

- deterministic logic stays in focused modules such as `triage_scoring.py`, `summarization.py`, `ask_extraction.py`, `draft_generation.py`, `catchup_briefing.py`, and `thought_partner.py`
- feature orchestration lives in `app/services/intelligence/features.py`
- structured feature input and output contracts live in `app/services/intelligence/contracts.py`
- markdown prompt assets live in `app/prompts/*.md`
- the model boundary lives in `app/services/modeling/client.py`
- JSON parsing guardrails live in `app/services/modeling/json_guardrails.py`

Today the `NullModelClient` always returns `None`, so every feature keeps using deterministic fallback behavior. A future LLM integration should:

- implement `ModelClient.generate_structured(...)`
- send the markdown prompt plus the structured feature input
- parse the raw model response through the JSON guardrails
- return a validated schema object or fall back to rules on any parse or validation error

Feature-by-feature evolution guidance:

- `triage`: use the model for better tradeoff handling between urgency, risk, and context, while preserving deterministic fallback scoring for safety
- `summarize`: use the model for stronger long-thread compression and entity resolution, while keeping rules for quote stripping and deadline extraction
- `extract asks`: use the model for better implicit ask detection and owner inference, while keeping deterministic precision filters
- `draft reply`: use the model for tone quality and sentence flow, while keeping template fallback to avoid fabrication
- `catch up`: use the model for richer themes and ranking explanations, while keeping deterministic bucket ranking
- `thought partner`: use the model for sharper evidence-to-inference synthesis, while keeping deterministic grounded structure

## V1 Triage Logic

The triage endpoint now uses deterministic, explainable heuristics rather than fixed placeholder responses. The scoring model considers:

- whether the user is in `To` or only in `Cc`
- direct questions and request language
- deadline phrases like `today`, `EOD`, or weekday names
- broad recipient patterns
- automated sender patterns
- status-update and FYI language
- explicit user mentions
- old unread threads that may be getting buried

The scoring implementation lives in `app/services/triage_scoring.py`.

## V1 Summarization Logic

Thread summarization is currently rule-based and lives in `app/services/summarization.py`. It:

- weights the latest message more heavily than earlier ones
- strips obvious quoted reply text and noisy forwarded markers
- extracts unresolved items, deadlines, and waiting relationships
- keeps earlier context only when it changes the decision context

An LLM could later improve tone smoothing, better entity resolution, and more precise deduplication across long threads without changing the response schema.

## V1 Reply Drafting Logic

Reply drafting is template-driven and lives in `app/services/draft_generation.py`. It combines:

- the structured thread summary
- extracted asks
- triage bucket and suggested next move
- user signature and tone settings

The current templates generate three intentionally different options: `shortReply`, `strategicReply`, and `clarifyingReply`. An LLM can later replace or refine those templates without changing the route contract.

## Environment Variables

- `APP_NAME` sets the FastAPI application name
- `APP_ENV` sets the runtime environment label
- `API_PORT` documents the local port to use
- `LOG_LEVEL` controls structured log verbosity
- `MOCK_MODE` keeps the service in deterministic mock mode

## Request Shape

All POST endpoints accept:

```json
{
  "thread": { "...": "EmailThread" },
  "userSettings": { "...": "optional UserSettings" }
}
```

`userSettings` is optional and can influence deterministic ranking, summarization, drafting, and local preference-aware behavior.
