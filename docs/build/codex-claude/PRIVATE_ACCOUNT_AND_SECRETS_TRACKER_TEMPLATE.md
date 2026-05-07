# Private Account and Secrets Tracker Template

## Purpose

Use this template only in a gitignored local file such as:

```text
.ops-private/account-secrets-tracker.md
```

Do not commit the filled version.
Do not paste live secrets into chat.

This tracker is for readiness status, custodianship, storage location, and last-check timestamps.
If you need to store actual secret values before encryption, use only local gitignored files such as:

```text
.env
infra/secrets/secrets.yaml
infra/secrets/secrets.local.yaml
```

## Readiness Summary

```text
Accounts ready: no
Secrets ready: no
Last reviewed:
Primary operator:
Password manager:
Age private key backup location:
```

## Provider Access

```text
- Hostinger
  status:
  owner:
  login path:
  required feature confirmed:
  credential storage plan:

- GitHub
  status:
  owner:
  login path:
  required feature confirmed:
  credential storage plan:

- Twilio
  status:
  owner:
  login path:
  required feature confirmed:
  credential storage plan:

- Gemini / Google AI Studio
  status:
  owner:
  login path:
  required feature confirmed:
  credential storage plan:

- ElevenLabs
  status:
  owner:
  login path:
  required feature confirmed:
  credential storage plan:

- OpenRouter
  status:
  owner:
  login path:
  required feature confirmed:
  credential storage plan:

- Domain / DNS provider
  status:
  owner:
  login path:
  required feature confirmed:
  credential storage plan:

- Obsidian Git remote
  status:
  owner:
  login path:
  required feature confirmed:
  credential storage plan:

- Telegram
  status:
  owner:
  login path:
  required feature confirmed:
  credential storage plan:

- Composio
  status:
  owner:
  login path:
  required feature confirmed:
  credential storage plan:

- Email provider
  status:
  owner:
  login path:
  required feature confirmed:
  credential storage plan:
```

## Required Runtime Values

Mark each as `present`, `missing`, `not in scope`, or `stored in password manager only`.

```text
- POSTGRES_PASSWORD:
- APP_ENV:
- LOG_LEVEL:
- TIMEZONE:
- KHADIJAH_DOMAIN:
- PUBLIC_BASE_URL:
- VOICE_BASE_URL:
- TWILIO_ACCOUNT_SID:
- TWILIO_AUTH_TOKEN:
- TWILIO_PHONE_NUMBER:
- TWILIO_VOICE_WEBHOOK_URL:
- TWILIO_STREAM_URL:
- GEMINI_API_KEY:
- GEMINI_MODEL:
- GEMINI_LIVE_MODEL:
- ELEVENLABS_API_KEY:
- ELEVENLABS_MODEL_ID:
- KHADIJAH_ELEVENLABS_VOICE_ID:
- SINCLAIR_ELEVENLABS_VOICE_ID:
- OPENROUTER_API_KEY:
- OPENROUTER_BASE_URL:
- OBSIDIAN_GIT_REMOTE:
```

## Storage Map

```text
.env
- APP_ENV
- LOG_LEVEL
- TIMEZONE
- PUBLIC_BASE_URL
- VOICE_BASE_URL
- KHADIJAH_DOMAIN
- TWILIO_VOICE_WEBHOOK_URL
- TWILIO_STREAM_URL
- GEMINI_MODEL
- GEMINI_LIVE_MODEL
- ELEVENLABS_MODEL_ID
- OPENROUTER_BASE_URL
- OBSIDIAN_GIT_REMOTE

infra/secrets/secrets.yaml or secrets.local.yaml
- POSTGRES_PASSWORD
- OPENROUTER_API_KEY
- GEMINI_API_KEY
- ELEVENLABS_API_KEY
- TWILIO_ACCOUNT_SID
- TWILIO_AUTH_TOKEN
- KHADIJAH_ELEVENLABS_VOICE_ID
- SINCLAIR_ELEVENLABS_VOICE_ID

Password manager only
- age private key backup
- recovery codes
- provider owner passwords
```

## Blockers

```text
- 
```

## Next Action

```text
- 
```
