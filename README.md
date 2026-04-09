# Inbox Triage

Inbox Triage is a safe MVP monorepo for an AI email triage copilot. The first version is intentionally mock-only and focuses on helping a user catch up on unread mail, summarize threads, extract direct asks, and draft replies without connecting to a real mailbox.

## Monorepo Layout

```text
apps/
  outlook-addin/     React + TypeScript mock task pane
services/
  api/               FastAPI scaffold with placeholder AI endpoints
packages/
  shared-types/      Shared TypeScript schemas and example types
docs/                Product and local setup notes
```

## What Is Included

- Mock Outlook add-in panel shell with placeholder sections for:
  - verdict
  - summary
  - direct asks
  - draft reply
  - catch up list
- FastAPI service scaffold with:
  - `GET /health`
  - `POST /triage/thread`
  - `POST /summarize/thread`
  - `POST /extract/asks`
  - `POST /draft/reply`
  - `POST /catchup`
- Shared TypeScript schemas for:
  - email thread
  - triage result
  - summary result
- Mock fixtures for a sample thread and triage response
- Environment templates and local run instructions

## Quick Start

### 1. Frontend

```bash
cd apps/outlook-addin
cp .env.example .env.local
npm install
npm run dev
```

The mock task pane will be available through Vite in local development.

### 2. API

```bash
cd services/api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

The API will run at `http://127.0.0.1:8000`.

## Notes

- No Outlook mailbox integration is included yet.
- No Microsoft Graph integration is included yet.
- No authentication is included yet.
- All responses are mocked to keep the MVP safe and easy to iterate on.
