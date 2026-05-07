# Codex / Claude Code Build Instructions

## Role

You are helping build BairyOS / FlavorOS on a Hostinger VPS.

Follow these instructions exactly.

## Primary Objective

Build a VPS-hosted, phone-call-accessible, multi-agent executive operating system.

The live experience:

```text
User calls Twilio number
Khadijah or Sinclair answers
The agent checks current state
If ready, it answers
If not ready, it delegates internally
Specialist agents work in background
A file is created in the vault
User gets follow-up by Telegram/SMS
```

## Non-Negotiable Architecture Rules

```text
Khadijah and Sinclair are the only human-facing agents.
Maxine, Scooter, and Kyle are dark specialists.
Specialists never speak directly to the user.
All specialist work routes through NATS work_order.<agent> and report.<agent>.
Money, legal, contracts, bookings, external sends, and sensitive relationship actions require user approval.
Voice calls are for presence, triage, and brief delivery.
Telegram/SMS are for follow-up and approvals.
The vault is durable memory and work product.
```

## Build Order

### Phase 1 — Server Foundation

```text
1. Harden Hostinger VPS.
2. Install Docker and Compose.
3. Configure DNS.
4. Install Caddy or Nginx.
5. Clone repo.
6. Create .env from .env.example.
7. Bring up base Docker services.
```

### Phase 2 — Existing FlavorOS Runtime

```text
1. Build agent containers.
2. Start NATS, Redis, Postgres, OpenRouter proxy, scheduler, vault-sync.
3. Start Khadijah, Sinclair, Maxine, Scooter, Kyle.
4. Verify logs.
5. Verify vault mounts.
6. Verify agent skill mounts.
```

### Phase 3 — Twilio Skeleton

```text
1. Add voice-gateway service.
2. Add /health.
3. Add /voice returning TwiML.
4. Add /twilio-stream WebSocket.
5. Confirm Twilio call reaches server.
```

Do not implement Gemini or ElevenLabs until Twilio successfully connects to `/twilio-stream`.

### Phase 4 — Audio Round Trip

```text
1. Parse Twilio connected/start/media/stop/mark events.
2. Decode Twilio audio.
3. Send test audio back to Twilio.
4. Confirm caller hears generated audio.
```

### Phase 5 — Gemini Live

```text
1. Open Gemini Live WebSocket.
2. Send setup config.
3. Forward user audio to Gemini.
4. Receive Gemini text/audio.
5. Send response audio back to Twilio.
```

### Phase 6 — ElevenLabs Voices

```text
1. Receive transcript from Gemini or STT.
2. Generate response text through Hermes.
3. Send response text to ElevenLabs.
4. Convert ElevenLabs audio to mu-law 8k.
5. Play response through Twilio.
```

### Phase 7 — Agent Routing

```text
1. Build hermes_router.py.
2. Route Khadijah/Sinclair requests.
3. Publish specialist work orders to NATS.
4. Receive specialist reports.
5. Create deferral/follow-up responses.
```

## Required Files

```text
.env.example
.gitignore
docker-compose.yml
infra/voice-gateway/Dockerfile
infra/voice-gateway/requirements.txt
infra/voice-gateway/app/main.py
infra/voice-gateway/app/twilio_stream.py
infra/voice-gateway/app/gemini_live.py
infra/voice-gateway/app/elevenlabs_tts.py
infra/voice-gateway/app/audio_codec.py
infra/voice-gateway/app/hermes_router.py
infra/voice-gateway/app/state.py
scripts/deploy.sh
scripts/status.sh
scripts/backup-postgres.sh
```

## Definition of Done

```text
[ ] Hostinger VPS is secured and running Docker
[ ] FlavorOS base services are live
[ ] Five agent containers are live
[ ] Voice-gateway is live behind HTTPS/WSS
[ ] Twilio calls reach /voice
[ ] Twilio Media Stream connects to /twilio-stream
[ ] Caller audio is received and logged
[ ] System can speak test audio back to caller
[ ] Gemini Live session can receive user audio
[ ] Khadijah or Sinclair can respond through the call
[ ] A new task can be deferred into work_order.scooter or work_order.maxine
[ ] A report can return to Khadijah/Sinclair
[ ] User receives a follow-up through Telegram or SMS
[ ] Vault file is created for deferred work
```
