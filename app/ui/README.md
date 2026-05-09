# FlavorOS App UI

This is the first visible MVP app surface for FlavorOS.

## Purpose

- Show provider health
- Show normalized inbox state
- Show agent work, approvals, and outbound actions
- Give the repo a real app shell while backend ingestion and runtime paths are being wired

## Current state

- Static HTML, CSS, and JavaScript
- Reads live dashboard state from `app-api` at `http://127.0.0.1:8091/api/dashboard-state`
- Includes a sample Gmail ingest action that writes to Postgres and emits a Sinclair work order over NATS

## Next steps

1. Replace mock ingest with real Gmail provider reads.
2. Read agent reports back into the dashboard once Sinclair processes live work orders.
3. Add item detail pages and approval actions.
