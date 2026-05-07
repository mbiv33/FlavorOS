# Secrets Manifest

## Purpose

This manifest lists every secret or sensitive config value required by the project.

This file is safe to commit because it contains names and descriptions only. Do not add real secret values to this file.

## Secret Handling Rules

Do not commit:

```text
.env
infra/secrets/*
private SSH keys
OAuth refresh tokens
Twilio auth token
API keys
database passwords
```

Commit:

```text
.env.example
SECRETS_MANIFEST.md
ACCOUNT_CHECKLIST.md
```

## Core Secrets

| Variable | Required | Used By |
|---|---:|---|
| POSTGRES_PASSWORD | Yes | Postgres, Docker Compose |
| APP_ENV | Yes | all app services |
| LOG_LEVEL | Yes | all app services |
| TIMEZONE | Yes | scheduler, agents, voice gateway |

## Public Config

| Variable | Required | Used By |
|---|---:|---|
| KHADIJAH_DOMAIN | Yes | Khadijah, webhook config |
| PUBLIC_BASE_URL | Yes | app links |
| VOICE_BASE_URL | Yes | app links |
| TWILIO_VOICE_WEBHOOK_URL | Yes | Twilio |
| TWILIO_STREAM_URL | Yes | Twilio Media Streams |

## Twilio

| Variable | Required | Used By |
|---|---:|---|
| TWILIO_ACCOUNT_SID | Yes | voice-gateway |
| TWILIO_AUTH_TOKEN | Yes | voice-gateway |
| TWILIO_PHONE_NUMBER | Yes | voice-gateway |
| TWILIO_MESSAGING_SERVICE_SID | Optional | SMS follow-up |
| TWILIO_STATUS_CALLBACK_URL | Optional | call lifecycle tracking |

## Gemini / Google AI

| Variable | Required | Used By |
|---|---:|---|
| GEMINI_API_KEY | Yes | voice-gateway |
| GEMINI_MODEL | Yes | voice-gateway |
| GEMINI_LIVE_MODEL | Yes | voice-gateway |
| GEMINI_PROJECT_ID | Optional | Vertex AI |
| GOOGLE_APPLICATION_CREDENTIALS | Optional | Vertex AI service account |

## ElevenLabs

| Variable | Required | Used By |
|---|---:|---|
| ELEVENLABS_API_KEY | Yes | voice-gateway, Hermes TTS |
| KHADIJAH_ELEVENLABS_VOICE_ID | Yes | Khadijah voice |
| SINCLAIR_ELEVENLABS_VOICE_ID | Yes | Sinclair voice |
| ELEVENLABS_MODEL_ID | Yes | TTS model |

## OpenRouter

| Variable | Required | Used By |
|---|---:|---|
| OPENROUTER_API_KEY | Yes | openrouter-proxy |
| OPENROUTER_BASE_URL | Yes | Hermes/OpenClaw model calls |
| OPENROUTER_DEFAULT_MODEL | Optional | model routing |
| OPENROUTER_FAST_MODEL | Optional | fast routing |
| OPENROUTER_DEEP_MODEL | Optional | deep routing |

## Telegram

| Variable | Required | Used By |
|---|---:|---|
| TELEGRAM_KHADIJAH_BOT_TOKEN | Optional | Khadijah Telegram |
| TELEGRAM_SINCLAIR_BOT_TOKEN | Optional | Sinclair Telegram |
| TELEGRAM_SHARED_GROUP_BOT_TOKEN | Optional | shared group bot |
| TELEGRAM_SHARED_GROUP_CHAT_ID | Optional | async follow-up |
| TELEGRAM_OWNER_USER_ID | Optional | owner verification |

## Obsidian / Vault

| Variable | Required | Used By |
|---|---:|---|
| OBSIDIAN_GIT_REMOTE | Yes | vault-sync |
| OBSIDIAN_VAULT_BRANCH | Optional | vault-sync |
| GIT_SSH_COMMAND | Optional | vault-sync |
| DEPLOY_KEY_PATH | Optional | Git SSH access |

## Suggested Secret File Layout

```text
infra/secrets/
  _shared/
    openrouter.key
    gemini.key
    elevenlabs.key
    twilio.key
    postgres_password
  khadijah/
    composio.key
    telegram.token
  sinclair/
    composio.key
    telegram.token
```

## Git Ignore Requirements

```gitignore
.env
.env.*
!.env.example
infra/secrets/*
!infra/secrets/.gitkeep
*.pem
*.key
*.p12
*.pfx
id_rsa
id_ed25519
backups/
logs/
```
