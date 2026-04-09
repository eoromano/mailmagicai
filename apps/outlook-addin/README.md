# ThreadSense Outlook Add-in

This app is the right-side task pane shell for ThreadSense. It is a local React + TypeScript app with a small adapter boundary between the UI and Outlook-specific message access.

## Purpose

- Provide the initial UI shape for the ThreadSense copilot
- Keep message access isolated so the app can swap between mock data and a real Outlook source later
- Stay safe by using local fixtures and a minimal Outlook stub

## Key Files

- `src/App.tsx` for the panel shell
- `src/components/` for small presentational UI pieces
- `src/adapters/` for the message access boundary and normalization helpers
- `src/lib/` for API and frontend data orchestration
- `src/styles.css` for the current panel styling

## Run

```bash
cd apps/outlook-addin
cp .env.example .env.local
npm install
npm run dev
```

For the most reliable milestone demo, use:

```bash
VITE_APP_MODE=mock
VITE_MESSAGE_SOURCE=mock
```

## Outlook On The Web Test Path

Outlook on the web expects an XML manifest file and an HTTPS-hosted add-in URL.

1. Start the add-in locally:

```bash
npm run dev:addin
```

2. Expose it over HTTPS with a tunnel such as:

```bash
cloudflared tunnel --url http://localhost:3000
```

or

```bash
ngrok http 3000
```

3. Generate the uploadable manifest:

```bash
./scripts/generate-outlook-manifest.sh https://your-https-url
```

4. Upload the generated file:

`apps/outlook-addin/manifest/dist/threadsense-manifest.xml`

In Outlook on the web:

- `Get Add-ins`
- `My add-ins`
- `Add a custom add-in`
- `Add from file`

5. Open a message in read mode and use the `Open ThreadSense` command.

## GitHub Pages Option

If you want a fast public HTTPS host without running a tunnel, the repo now includes a GitHub Pages workflow for the add-in frontend.

Expected Pages URL for this repository:

`https://eoromano.github.io/mailmagicai/`

Once Pages is live, you can generate the Outlook manifest with:

```bash
./scripts/generate-outlook-manifest.sh https://eoromano.github.io/mailmagicai
```

That gives you a stable public manifest target for Outlook on the web testing.

## Adapter Modes

- `VITE_MESSAGE_SOURCE=mock` uses the mock adapter and returns normalized threads built from local fixtures.
- `VITE_MESSAGE_SOURCE=outlook` uses Office.js to read the currently open Outlook message in read mode.

## Local Settings

- Task-pane settings are stored in browser `localStorage` through a small storage abstraction in `src/lib/settingsStorage.ts`.
- The settings card currently supports VIP senders, priority domains, urgency keywords, copied-only keywords, draft voice preferences, a save-history toggle, and a mock-mode toggle.
- Future persistence can move behind the same interface, for example by syncing preferences to the FastAPI service or a user profile store once auth exists.

## Outlook Stub Notes

- The Outlook adapter reads the current message only. It does not fetch mailbox lists or full thread history yet.
- `getUnreadThreads()` returns an empty list in Outlook mode until a real mailbox integration exists.
- The adapter uses supported Office.js message APIs only: current item metadata, recipients, attachments, body reads, and internet headers.
- Sent time is derived from the message `Date` internet header when available, with `dateTimeCreated` as the fallback because Office.js does not expose a richer dedicated sent-time field for the current item.
- Missing Outlook fields fall back to empty strings or empty arrays instead of guessed values.
- The add-in converts the normalized adapter model into the shared `EmailThread` API contract before calling the backend.

## Outlook Setup Notes

- The app now references Office.js from the Microsoft CDN in `index.html`, which is the supported loading pattern for Office Add-ins.
- To test current-message reading, run the app inside Outlook with a message open in reading mode.
- If Outlook isn't available, or the current context is unsupported, the adapter returns no thread and the task pane can still fall back to mock mode.
- The generated manifest uses a `MessageReadCommandSurface` button with `ShowTaskpane`, which is the standard sideload path for testing a read-mode Outlook add-in.

## Current Scope

- Mock and local API analysis modes
- Mock adapter plus Outlook message-source stub
- No Microsoft Graph or mailbox listing integration yet

## Milestone Notes

- Mock mode is the default happy path and renders the full task pane experience end to end.
- Local API mode is available for deterministic backend testing without changing the UI contract.
- Outlook mode is intentionally minimal and should be treated as a future integration seam, not a production data source yet.
