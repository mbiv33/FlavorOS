# ENV Example

Copy the content below into a root-level `.env.example`.

```env
# -------------------------------------------------------------------
# BairyOS / FlavorOS Environment Template
# -------------------------------------------------------------------

APP_ENV=production
LOG_LEVEL=info
TIMEZONE=America/New_York

PUBLIC_BASE_URL=https://voice.yourdomain.com
VOICE_BASE_URL=https://voice.yourdomain.com
KHADIJAH_DOMAIN=voice.yourdomain.com

POSTGRES_PASSWORD=replace_with_strong_password
POSTGRES_USER=flavor
POSTGRES_DB=flavor
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_URL=postgres://flavor:replace_with_strong_password@postgres:5432/flavor

REDIS_URL=redis://redis:6379
NATS_URL=nats://nats:4222

OPENROUTER_API_KEY=replace_me
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_DEFAULT_MODEL=replace_me
OPENROUTER_FAST_MODEL=replace_me
OPENROUTER_DEEP_MODEL=replace_me

GEMINI_API_KEY=replace_me
GEMINI_MODEL=gemini-3.1-flash
GEMINI_LIVE_MODEL=gemini-3.1-flash-live

ELEVENLABS_API_KEY=replace_me
ELEVENLABS_MODEL_ID=eleven_multilingual_v2
KHADIJAH_ELEVENLABS_VOICE_ID=replace_me
SINCLAIR_ELEVENLABS_VOICE_ID=replace_me

TWILIO_ACCOUNT_SID=replace_me
TWILIO_AUTH_TOKEN=replace_me
TWILIO_PHONE_NUMBER=+15555555555
TWILIO_VOICE_WEBHOOK_URL=https://voice.yourdomain.com/voice
TWILIO_STREAM_URL=wss://voice.yourdomain.com/twilio-stream
TWILIO_STATUS_CALLBACK_URL=https://voice.yourdomain.com/twilio-status
TWILIO_MESSAGING_SERVICE_SID=replace_me_optional

TELEGRAM_KHADIJAH_BOT_TOKEN=replace_me_optional
TELEGRAM_SINCLAIR_BOT_TOKEN=replace_me_optional
TELEGRAM_SHARED_GROUP_BOT_TOKEN=replace_me_optional
TELEGRAM_SHARED_GROUP_CHAT_ID=replace_me_optional
TELEGRAM_OWNER_USER_ID=replace_me_optional

OBSIDIAN_GIT_REMOTE=git@github.com:YOUR_ORG/YOUR_OBSIDIAN_VAULT.git
OBSIDIAN_VAULT_BRANCH=main
VAULT_PATH=/vault

COMPOSIO_API_KEY=replace_me_optional
COMPOSIO_KHADIJAH_API_KEY=replace_me_optional
COMPOSIO_SINCLAIR_API_KEY=replace_me_optional

GOOGLE_CLIENT_ID=replace_me_optional
GOOGLE_CLIENT_SECRET=replace_me_optional
GOOGLE_REFRESH_TOKEN=replace_me_optional

EMAIL_FROM=replace_me_optional
SMTP_HOST=replace_me_optional
SMTP_PORT=587
SMTP_USER=replace_me_optional
SMTP_PASSWORD=replace_me_optional

SECRETS_DIR=/run/flavor/secrets

```
