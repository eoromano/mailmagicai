# Local Setup

Use the repo root whenever possible so local development stays predictable.

## Recommended First Run

```bash
npm install
npm run setup:api
npm run dev:addin
npm run dev:api
```

Open [http://127.0.0.1:3000](http://127.0.0.1:3000).

## Add-In Modes

For the safest milestone demo, keep:

- `VITE_APP_MODE=mock`
- `VITE_MESSAGE_SOURCE=mock`

Mode meanings:

- `VITE_APP_MODE=mock`: the add-in uses in-memory mock responses
- `VITE_APP_MODE=api`: the add-in calls the local FastAPI backend
- `VITE_MESSAGE_SOURCE=mock`: thread data comes from local fixtures
- `VITE_MESSAGE_SOURCE=outlook`: thread data comes from the minimal Outlook adapter stub

## Milestone Demo Path

1. Start the add-in with `npm run dev:addin`.
2. Leave the add-in in mock mode with mock message source.
3. Open the task pane and click `Scan this thread`.
4. Confirm the verdict, summary, direct asks, draft reply, catch-up list, thought partner, and settings sections render.

## Validation

```bash
npm run check
cd services/api && .venv/bin/pytest -q
```

## Environment Templates

- `apps/outlook-addin/.env.example`
- `services/api/.env.example`

The repo is still local-first and safe by default. No real mailbox or LLM access is required for this milestone.
