# Agent 3 Endpoint Tests

Status: not started
Last updated: 2026-05-07

## Mission

Act as a synthetic test client for local/internal Hermes, voice, and text endpoints using fake data only.

## Latest Test

- Endpoint or subject:
- Fake input:
- Expected result:
- Actual result:
- Pass/fail:
- Next fix:

## Safe Checks

```text
GET /health
POST /voice
synthetic work_order.<agent>
synthetic report.<agent>
```

## Boundaries

- Never use real phone numbers.
- Never use real emails.
- Never use real calendar data.
- Never use real client data.
- Never print or read raw secrets.

