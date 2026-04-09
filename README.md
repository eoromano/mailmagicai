# ThreadSense

ThreadSense is an AI email triage copilot. It helps a user catch up on unread mail, summarize threads, extract direct asks, draft replies, and think through what is really happening in a thread.

## Milestone Status

This first milestone is coherent and runnable today:

- Outlook-style task pane in React + TypeScript
- local mock adapter plus a minimal Outlook adapter stub
- FastAPI backend with deterministic triage, summarization, ask extraction, draft reply, catch-up, and thought-partner flows
- shared contracts across the add-in and API
- local settings, history, and mock-mode controls
- model-ready backend service boundaries with deterministic fallback behavior

Default development is safe and local-first. No real mailbox access, auth, Graph integration, or live LLM calls are enabled.

## Demo

Mock mode task pane:

![ThreadSense mock mode](/Users/roman/Documents/mailmagic/docs/images/mock-mode-task-pane.svg)

## Repo Shape

```text
apps/
  outlook-addin/     Outlook-style task pane built with React + TypeScript
services/
  api/               FastAPI service with deterministic intelligence features
packages/
  shared-types/      Shared TypeScript schemas and example mocks
docs/                Product, setup, and milestone notes
scripts/             Thin local development helpers
```

## Quick Start

```bash
npm install
npm run setup:api
npm run dev:addin
npm run dev:api
```

The add-in runs on `http://127.0.0.1:3000` and the API runs on `http://127.0.0.1:8000`.

For the simplest demo:

- keep `apps/outlook-addin/.env.local` aligned with `VITE_APP_MODE=mock`
- keep `VITE_MESSAGE_SOURCE=mock`
- open the add-in and click `Scan this thread`

For deterministic backend mode:

- set `VITE_APP_MODE=api`
- keep `VITE_MESSAGE_SOURCE=mock`
- run the local FastAPI service

## GitHub Pages

The repo is now prepared to publish the ThreadSense frontend to GitHub Pages through GitHub Actions.

What it deploys:

- the Outlook add-in frontend only
- default Pages build mode is `mock`
- the deployed site is suitable for demoing the task pane UI and for generating an Outlook manifest that points at a public HTTPS URL

What it does not deploy:

- the FastAPI backend

After pushing to `main`:

1. In GitHub, open repository `Settings` -> `Pages`
2. Under `Source`, choose `GitHub Actions`
3. Wait for the `Deploy ThreadSense Frontend` workflow to finish
4. Your site should publish at:

`https://eoromano.github.io/mailmagicai/`

Once that URL is live, generate the Outlook manifest with:

```bash
./scripts/generate-outlook-manifest.sh https://eoromano.github.io/mailmagicai
```

## Local Validation

```bash
npm run check
cd services/api && .venv/bin/pytest -q
```

## What Is Complete

- Mock task pane experience with loading, empty, error, catch-up, thought-partner, and settings flows
- End-to-end local API path with typed client wiring
- Deterministic intelligence features for triage, summarize, ask extraction, draft reply, catch-up, and thought partner
- Adapter boundary for future Outlook message access
- Storage boundary for future settings persistence
- Model boundary for future LLM-assisted features

## What Comes Next

- Real Outlook reading-mode integration
- Better mailbox-sourced fixtures and thread ingestion
- Backend persistence for settings and history
- Real model client implementation behind the structured feature layer
- Authentication and account-aware behavior

## Where To Start

- Read [apps/outlook-addin/README.md](/Users/roman/Documents/mailmagic/apps/outlook-addin/README.md) for the task pane app
- Read [services/api/README.md](/Users/roman/Documents/mailmagic/services/api/README.md) for the backend
- Read [packages/shared-types/README.md](/Users/roman/Documents/mailmagic/packages/shared-types/README.md) for shared contract notes
- Read [docs/setup.md](/Users/roman/Documents/mailmagic/docs/setup.md) for the local run path
- Read [docs/architecture.md](/Users/roman/Documents/mailmagic/docs/architecture.md) for the current MVP structure
