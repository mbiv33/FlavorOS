# Account Access and Secrets Readiness Protocol

## Purpose

Use this protocol before VPS deployment, before agent bring-up, and any time a new provider is added to the stack.

The goal is to answer two questions clearly:

1. Do we have every required account and access path for the active stack?
2. Do we have every required secret and config value needed for agent operation?

This protocol is safe to commit because it contains process only. Do not place live secret values in this file.

## Inputs

Read these first:

- `docs/build/codex-claude/TECH_STACK.md`
- `docs/build/codex-claude/ACCOUNT_CHECKLIST.md`
- `docs/build/codex-claude/SECRETS_MANIFEST.md`
- `docs/build/codex-claude/ENV_EXAMPLE.md`
- `docker-compose.yml`

Initialize the local private workspace before collecting anything sensitive:

```bash
bash scripts/init-private-secrets-workspace.sh
```

## Output

At the end of this protocol, produce one readiness report with:

- `Accounts ready`: yes/no
- `Secrets ready`: yes/no
- `Blocked providers`: list
- `Missing variables`: list
- `Storage plan`: where each secret will live
- `Next action`: one concrete next step

## Rules

- Do not paste real passwords, tokens, API keys, or private keys into repo docs.
- Do not paste real passwords, tokens, API keys, or private keys into LLM chat.
- Do not commit `.env`, `infra/secrets/*`, or private key material.
- Record status and ownership, not secret values.
- Treat the repo as the source of truth for what the runtime expects today.

## Phase 1: Confirm Active Stack

Build the active provider list from `TECH_STACK.md` and `docker-compose.yml`.

Current required stack for MVP:

- Hostinger VPS
- Ubuntu 24.04 LTS
- Docker Engine
- Docker Compose
- Domain/DNS provider
- GitHub
- Twilio
- Google AI Studio / Gemini API
- ElevenLabs
- OpenRouter
- NATS
- Redis
- Postgres / pgvector
- Obsidian Git remote

Current optional or later-stage stack:

- Telegram
- Composio
- Email provider
- Uptime Kuma
- Sentry
- Vertex AI service account flow

If a provider is not being used in the active build, mark it `not in scope` instead of `missing`.

## Phase 2: Account Access Audit

For each in-scope provider, verify:

- account exists
- billing is enabled if required
- the owner can log in now
- the correct dashboard or console is reachable
- the needed feature is enabled
- the credential issuance path is known

Use these statuses only:

- `ready`
- `blocked`
- `not in scope`

Minimum evidence to capture for each provider:

- owner or credential custodian
- login path or dashboard URL
- required feature confirmed
- note about where the credential will be stored

Provider-specific checks:

- `Hostinger`: VPS exists, SSH access works, DNS target is known
- `GitHub`: repo access works, vault remote exists or will exist, deploy key path is known
- `Twilio`: account active, billing on, phone number acquired, programmable voice enabled
- `Gemini`: AI Studio access works, API key can be issued, target models are available
- `ElevenLabs`: API access works, Khadijah and Sinclair voice IDs exist or creation is assigned
- `OpenRouter`: account active, API key can be issued, model routing plan is chosen
- `Domain/DNS`: DNS zone editable, target hostnames chosen
- `Obsidian Git remote`: remote repo exists, branch known, SSH auth plan known
- `Telegram`: BotFather access works if async follow-up is in scope
- `Composio`: workspace exists if integrations are in scope
- `Email provider`: SMTP/API access exists if email actions are in scope

## Phase 3: Secret Inventory Audit

Start from `SECRETS_MANIFEST.md`, then confirm each variable is either:

- `present`
- `missing`
- `optional`
- `not in scope`

Required now for MVP runtime:

- `POSTGRES_PASSWORD`
- `APP_ENV`
- `LOG_LEVEL`
- `TIMEZONE`
- `KHADIJAH_DOMAIN`
- `PUBLIC_BASE_URL`
- `VOICE_BASE_URL`
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER`
- `TWILIO_VOICE_WEBHOOK_URL`
- `TWILIO_STREAM_URL`
- `GEMINI_API_KEY`
- `GEMINI_MODEL`
- `GEMINI_LIVE_MODEL`
- `ELEVENLABS_API_KEY`
- `ELEVENLABS_MODEL_ID`
- `KHADIJAH_ELEVENLABS_VOICE_ID`
- `SINCLAIR_ELEVENLABS_VOICE_ID`
- `OPENROUTER_API_KEY`
- `OPENROUTER_BASE_URL`
- `OBSIDIAN_GIT_REMOTE`

Optional or conditional:

- `TWILIO_MESSAGING_SERVICE_SID`
- `TWILIO_STATUS_CALLBACK_URL`
- `OPENROUTER_DEFAULT_MODEL`
- `OPENROUTER_FAST_MODEL`
- `OPENROUTER_DEEP_MODEL`
- `TELEGRAM_KHADIJAH_BOT_TOKEN`
- `TELEGRAM_SINCLAIR_BOT_TOKEN`
- `TELEGRAM_SHARED_GROUP_BOT_TOKEN`
- `TELEGRAM_SHARED_GROUP_CHAT_ID`
- `TELEGRAM_OWNER_USER_ID`
- `COMPOSIO_API_KEY`
- `COMPOSIO_KHADIJAH_API_KEY`
- `COMPOSIO_SINCLAIR_API_KEY`
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_REFRESH_TOKEN`
- `GEMINI_PROJECT_ID`
- `GOOGLE_APPLICATION_CREDENTIALS`
- `EMAIL_FROM`
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASSWORD`
- `OBSIDIAN_VAULT_BRANCH`
- `GIT_SSH_COMMAND`
- `DEPLOY_KEY_PATH`

## Phase 4: Storage Plan

Decide where each value will live before deployment.

Use this split unless the runtime changes:

- `.env`: non-secret config and values Docker Compose interpolates directly
- `infra/secrets/` or host-managed secret files: API keys, tokens, passwords, private key material
- password manager: source of truth for operators

Recommended `.env` values:

- `APP_ENV`
- `LOG_LEVEL`
- `TIMEZONE`
- `PUBLIC_BASE_URL`
- `VOICE_BASE_URL`
- `KHADIJAH_DOMAIN`
- `TWILIO_VOICE_WEBHOOK_URL`
- `TWILIO_STREAM_URL`
- `TWILIO_STATUS_CALLBACK_URL`
- `TWILIO_PHONE_NUMBER`
- `GEMINI_MODEL`
- `GEMINI_LIVE_MODEL`
- `ELEVENLABS_MODEL_ID`
- `OPENROUTER_BASE_URL`
- `OPENROUTER_DEFAULT_MODEL`
- `OPENROUTER_FAST_MODEL`
- `OPENROUTER_DEEP_MODEL`
- `OBSIDIAN_GIT_REMOTE`
- `OBSIDIAN_VAULT_BRANCH`
- `VAULT_PATH`
- `SECRETS_DIR`

Recommended file-based secrets:

- `POSTGRES_PASSWORD`
- `OPENROUTER_API_KEY`
- `GEMINI_API_KEY`
- `ELEVENLABS_API_KEY`
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `KHADIJAH_ELEVENLABS_VOICE_ID`
- `SINCLAIR_ELEVENLABS_VOICE_ID`
- `TELEGRAM_*`
- `COMPOSIO_*`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_REFRESH_TOKEN`
- `SMTP_PASSWORD`
- deploy SSH keys

Current repo note:

- `docker-compose.yml` already expects some secrets to be mounted under `/run/flavor/secrets`.
- Do not assume putting every value into `.env` makes it available to every agent.
- If a service expects a `*_FILE` path or mounted secret file, satisfy that contract directly.

Local operator files:

- `.ops-private/account-secrets-tracker.md`: readiness tracker, ownership, blockers, no live secrets required
- `.env`: local runtime config, gitignored
- `infra/secrets/secrets.yaml`: local plaintext staging file before encryption, gitignored

Validate without printing values:

```bash
bash scripts/validate-secrets-readiness.sh
```

Encrypt the local plaintext secret file when ready:

```bash
bash scripts/encrypt-secrets.sh
```

## Phase 5: Readiness Gate

The stack is not ready for deployment until all of the following are true:

- every in-scope provider is `ready`
- every required secret is `present`
- every required secret has a storage location
- `.gitignore` protections are in place
- the operator knows how to rotate each critical secret

If any required provider or secret is missing, stop and produce a blocker list instead of starting deployment.

## Operator Checklist Template

Use this exact structure in session notes or a private tracker:

```text
Accounts ready: yes/no
Secrets ready: yes/no

Providers
- Hostinger: ready/blocked/not in scope
- GitHub: ready/blocked/not in scope
- Twilio: ready/blocked/not in scope
- Gemini: ready/blocked/not in scope
- ElevenLabs: ready/blocked/not in scope
- OpenRouter: ready/blocked/not in scope
- Domain/DNS: ready/blocked/not in scope
- Obsidian Git remote: ready/blocked/not in scope
- Telegram: ready/blocked/not in scope
- Composio: ready/blocked/not in scope
- Email provider: ready/blocked/not in scope

Required secrets
- POSTGRES_PASSWORD: present/missing
- TWILIO_ACCOUNT_SID: present/missing
- TWILIO_AUTH_TOKEN: present/missing
- GEMINI_API_KEY: present/missing
- ELEVENLABS_API_KEY: present/missing
- OPENROUTER_API_KEY: present/missing
- KHADIJAH_ELEVENLABS_VOICE_ID: present/missing
- SINCLAIR_ELEVENLABS_VOICE_ID: present/missing
- OBSIDIAN_GIT_REMOTE: present/missing

Storage plan
- .env:
- infra/secrets:
- password manager:

Blocked providers:
- 

Missing variables:
- 

Next action:
- 
```

## Recommended Usage With Codex or Claude Code

When asking an agent to run this protocol, use:

```text
Run the Account Access and Secrets Readiness Protocol for the current FlavorOS stack. Do not print live secret values. Produce a readiness report with blockers, missing variables, and the storage plan.
```
