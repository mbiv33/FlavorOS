# BairyOS / FlavorOS Build Docs for Codex and Claude Code

## Purpose

This folder contains the working technical stack, account checklist, secrets template, deployment assumptions, and coding-agent instructions for building the BairyOS / FlavorOS VPS-hosted voice-agent system.

These files are intended to be copied into the project repo, preferably under:

```text
docs/build/
```

## Critical Warning About Secrets

Do **not** commit real secrets, API keys, auth tokens, private keys, database passwords, Twilio tokens, ElevenLabs keys, Gemini keys, OpenRouter keys, or OAuth credentials to GitHub.

Commit only templates and instructions:

```text
.env.example
SECRETS_MANIFEST.md
ACCOUNT_CHECKLIST.md
ACCOUNT_ACCESS_AND_SECRETS_PROTOCOL.md
PRIVATE_ACCOUNT_AND_SECRETS_TRACKER_TEMPLATE.md
TECH_STACK.md
CODEX_CLAUDE_BUILD_INSTRUCTIONS.md
```

Keep real secrets in:

```text
.env
infra/secrets/
.ops-private/
Hostinger environment variables
GitHub Actions secrets
1Password / Bitwarden / Doppler / Infisical
```

## Safe Intake Workflow

For account setup and secret collection without exposing values in chat:

```bash
bash scripts/init-private-secrets-workspace.sh
bash scripts/validate-secrets-readiness.sh
bash scripts/encrypt-secrets.sh
```

This creates local gitignored working files for provider readiness and secret entry, validates only presence and shape, then encrypts the secrets file into a repo-safe artifact.

## System Summary

BairyOS / FlavorOS is a VPS-hosted, phone-call-accessible, multi-agent executive operating system.

The user calls a Twilio number. Twilio streams live audio to the VPS. A FastAPI voice gateway connects the audio stream to Gemini Live / Gemini Flash, routes agent actions through Hermes and OpenClaw, speaks back through ElevenLabs voices, and stores state in Redis, Postgres, and the Obsidian vault.

## Non-Negotiable Architecture Rules

```text
Khadijah and Sinclair are the only human-facing agents.
Maxine, Scooter, and Kyle are dark specialists.
Specialist work routes through NATS work_order.<agent> and report.<agent>.
Money, legal, contracts, bookings, external sends, and sensitive relationship actions require approval.
Voice calls are for presence, triage, and brief delivery.
Telegram/SMS are for follow-up and approvals.
The vault is durable memory and work product.
```
