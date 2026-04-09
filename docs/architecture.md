# Inbox Triage MVP Architecture

## Principles

- Keep the first milestone mock-only.
- Separate UI, API, and shared contracts.
- Leave clear seams for future Outlook and model integrations.

## Components

### `apps/outlook-addin`

- React + TypeScript task pane shell
- Displays mock triage artifacts in a right-side panel layout
- Reads from local fixtures for the first milestone

### `services/api`

- FastAPI backend scaffold
- Exposes health and placeholder task endpoints
- Returns deterministic mock payloads for development

### `packages/shared-types`

- Shared TypeScript schemas for frontend contract consistency
- Useful later for API client and test fixtures

## Future Extensions

- Outlook add-in host wiring
- Microsoft Graph mailbox sync
- Model orchestration and prompt layer
- Authentication and user settings
