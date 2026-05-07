# Client Envelope Architecture

## Purpose

FlavorOS must work for Marcus during development and for Christy after onboarding. Agent behavior should resolve through a `client_id`, not hardcoded assumptions.

## Directory Shape

```text
clients/
  marcus/
    profile.yaml
    preferences.yaml
    account_aliases.yaml
    hitl_policy.yaml
    onboarding_status.yaml
  christy/
    profile.yaml
    preferences.yaml
    account_aliases.yaml
    hitl_policy.yaml
    onboarding_status.yaml
```

## Rules

- Do not store OAuth tokens, API keys, passwords, or refresh tokens in `clients/`.
- Store account aliases and human-readable configuration only.
- Client OAuth is explicit and consent-based.
- Christy's OAuth and personal preferences remain pending until after demo/onboarding.
- Marcus may be used as the test client for OAuth and communication flows.

## Client-Aware Agent Inputs

Every workflow should include:

```yaml
client_id: marcus
request_source: voice | telegram | email | calendar | cron | manual
authority_mode: draft_only
```

## Early Client IDs

- `marcus`: development and test client.
- `christy`: first intended real client, pending onboarding.

