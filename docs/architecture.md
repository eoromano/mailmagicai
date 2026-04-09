# ThreadSense MVP Architecture

## Principles

- Keep the first milestone mock-first and safe by default.
- Separate UI, API, and shared contracts.
- Leave clear seams for future Outlook and model integrations.

## Components

### `apps/outlook-addin`

- React + TypeScript task pane shell
- Right-side panel layout for Outlook reading mode
- Supports frontend mock mode and local API mode
- Uses an adapter boundary for message access and a storage boundary for local settings

### `services/api`

- FastAPI backend with deterministic intelligence features
- Exposes health plus feature endpoints for triage, summarize, extract asks, draft reply, catch-up, and thought partner
- Separates deterministic logic from model-ready orchestration and prompt assets

### `packages/shared-types`

- Shared TypeScript schemas for frontend contract consistency
- Shared example mocks and settings defaults

## Future Extensions

- Outlook add-in host wiring
- Microsoft Graph mailbox sync
- Real model client implementation behind the structured feature layer
- Authentication and backend settings persistence
