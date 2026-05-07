# Tech Account Checklist

## Purpose

Use this checklist to make sure every required vendor account, dashboard, token, and credential source exists before building the VPS deployment.

Do not store actual secrets in this file.

## Account Checklist

| Account | Needed For | Status |
|---|---|---|
| Hostinger | VPS hosting | TODO |
| GitHub | repo, deployment source, vault sync | TODO |
| Twilio | phone number, calls, SMS, Media Streams | TODO |
| Google AI Studio / Gemini API | Gemini Live / Flash | TODO |
| ElevenLabs | Khadijah and Sinclair voices | TODO |
| OpenRouter | model routing for agents | TODO |
| Telegram BotFather | Khadijah/Sinclair Telegram bots | TODO |
| Obsidian Git remote | durable vault sync | TODO |
| Composio | app/service integrations, if used | TODO |
| Domain/DNS provider | voice.yourdomain.com and related DNS | TODO |
| Email provider | notifications / future email actions | TODO |
| Optional: Uptime Kuma | uptime monitoring | TODO |
| Optional: Sentry | app error tracking | TODO |
| Optional: 1Password / Bitwarden | secrets management | TODO |

## Twilio

Required:

```text
Twilio account
billing enabled
Programmable Voice enabled
phone number purchased
Voice webhook configured
optional SMS enabled
```

Needed values:

```text
TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN
TWILIO_PHONE_NUMBER
TWILIO_VOICE_WEBHOOK_URL
TWILIO_STREAM_URL
```

Webhook:

```text
https://voice.yourdomain.com/voice
```

Stream URL:

```text
wss://voice.yourdomain.com/twilio-stream
```

## Gemini / Google AI Studio

Required:

```text
Google account
Google AI Studio access
Gemini API key
Gemini Live API access
```

Needed values:

```text
GEMINI_API_KEY
GEMINI_MODEL
GEMINI_LIVE_MODEL
```

Suggested defaults:

```text
GEMINI_MODEL=gemini-3.1-flash
GEMINI_LIVE_MODEL=gemini-3.1-flash-live
```

If the exact model name differs in the API, update the `.env` and voice-gateway config.

## ElevenLabs

Required:

```text
ElevenLabs account
API key
Khadijah voice created
Sinclair voice created
```

Needed values:

```text
ELEVENLABS_API_KEY
KHADIJAH_ELEVENLABS_VOICE_ID
SINCLAIR_ELEVENLABS_VOICE_ID
ELEVENLABS_MODEL_ID
```

## GitHub

Commit:

```text
.env.example
docs/build/*.md
docker-compose.yml
infra/voice-gateway/*
scripts/deploy.sh
scripts/status.sh
scripts/backup-postgres.sh
```

Never commit:

```text
.env
infra/secrets/*
private keys
API keys
database passwords
OAuth tokens
Twilio auth token
ElevenLabs API key
Gemini API key
```
