# Shared Types

The `shared-types` package contains the contract vocabulary for ThreadSense.

## Exports

- `contracts.ts` defines the production-facing TypeScript schemas
- `mocks.ts` provides example objects for the major schemas
- `index.ts` re-exports both files for a simple package entry point

## What It Covers

- email thread and message shapes
- triage, summary, ask extraction, draft reply, catch-up, and thought-partner contracts
- user settings defaults for the current local-first milestone

## Evolution Notes

- Keep the top-level names stable so the UI and API can evolve without churn.
- Add optional fields before introducing breaking renames.
- Split display-only UI state from backend response contracts.
- Introduce narrower enums only when the product flow truly needs them.
