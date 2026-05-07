# Full Tech Stack — BairyOS / FlavorOS Voice-Agent Build

## 1. Hosting / Infrastructure

```text
Hostinger VPS
Ubuntu 24.04 LTS
Docker Engine
Docker Compose
UFW firewall
fail2ban
SSH key authentication
swap memory
cron
```

Recommended MVP VPS:

```text
4 vCPU
8 GB RAM
160 GB NVMe
```

Preferred production VPS:

```text
8 vCPU
16 GB RAM
250+ GB NVMe
```

## 2. Reverse Proxy / Public Access

Recommended:

```text
Caddy
```

Alternative:

```text
Nginx
Certbot
Let's Encrypt
```

Public endpoints:

```text
https://voice.yourdomain.com/voice
wss://voice.yourdomain.com/twilio-stream
https://voice.yourdomain.com/health
```

## 3. Telephony

```text
Twilio Programmable Voice
Twilio phone number
Twilio Voice webhook
Twilio Media Streams
```

Call flow:

```text
User calls Twilio number
Twilio hits /voice webhook
App returns TwiML
Twilio opens WebSocket to /twilio-stream
Voice-gateway handles live audio
```

Protocols:

```text
TwiML
<Connect><Stream>
WebSocket / WSS
audio/x-mulaw
8 kHz audio
base64 media payloads
```

## 4. Voice Gateway

```text
Python 3.12
FastAPI
Uvicorn
WebSockets
asyncio
httpx
pydantic
ffmpeg
sox
```

Core files:

```text
infra/voice-gateway/
  Dockerfile
  requirements.txt
  app/main.py
  app/twilio_stream.py
  app/gemini_live.py
  app/elevenlabs_tts.py
  app/audio_codec.py
  app/hermes_router.py
  app/state.py
```

Responsibilities:

```text
Receive Twilio webhook
Return TwiML
Accept Twilio WebSocket stream
Parse Twilio media events
Decode caller audio
Connect to Gemini Live
Route transcripts to Hermes
Call ElevenLabs for voice output
Encode audio back to Twilio format
Publish work orders to NATS
Maintain call state in Redis/Postgres
```

## 5. Conversational Layer

```text
Gemini 3.1 Flash / Gemini Live API
```

Role:

```text
Low-latency conversation
Speech understanding
Turn-taking
Real-time response rhythm
```

Important distinction:

```text
Gemini is not the operating system.
Gemini is the interactive voice / conversation layer.
Hermes + OpenClaw + state drive remain the operating intelligence.
```

## 6. Voice Identity

```text
ElevenLabs
Khadijah custom voice
Sinclair custom voice
```

Audio conversion:

```text
ElevenLabs output
↓
PCM / MP3 / streaming audio
↓
convert to audio/x-mulaw 8k
↓
send back to Twilio
```

## 7. Human-Facing Agents

Runtime:

```text
Hermes Agent
```

Agents:

```text
Khadijah — Chief of Staff
Sinclair — Executive Assistant
```

Khadijah owns:

```text
briefs
approvals
synthesis
priorities
decisions
routing
project triage
money/legal/contract escalation
```

Sinclair owns:

```text
calendar
inbox
meetings
meeting prep
reminders
wellness
schedule pressure
```

## 8. Specialist Agents

Runtime:

```text
OpenClaw
```

Specialists:

```text
Maxine — COO
Scooter — CLO
Kyle — CRO
```

Rule:

```text
Specialists stay dark.
They do not speak directly to the user.
They report back through Khadijah or Sinclair.
```

## 9. Internal Message Bus

```text
NATS
```

Subjects:

```text
work_order.khadijah
work_order.sinclair
work_order.maxine
work_order.scooter
work_order.kyle

report.khadijah
report.sinclair
report.maxine
report.scooter
report.kyle

flag.low
flag.medium
flag.high
flag.critical

audit.*
```

## 10. State and Database

Live state:

```text
Redis
```

Durable data:

```text
Postgres
pgvector
```

Core tables:

```text
voice_calls
voice_turns
work_orders
agent_reports
audit_events
```

## 11. Vault

```text
Obsidian vault
Git remote sync
vault-sync container
```

Folders:

```text
10-Briefs
20-Meetings
30-Projects
35-Reports
40-People
50-Travel
60-Wellness
70-Ops
80-Journal
90-Archive
```

## 12. Model Routing

```text
OpenRouter
openrouter-proxy container
```

## 13. Async Follow-Up

MVP:

```text
Telegram bot
shared Hermes group thread
Khadijah direct Telegram
Sinclair direct Telegram
```

Later:

```text
Twilio SMS
Email
Push notification
Web dashboard notification
```

## 14. Development Tools

```text
Codex
Claude Code
SSH
Git
Docker Compose
GitHub
.env.example
deployment scripts
status scripts
backup scripts
```

## Simple Full Stack Summary

```text
Hostinger VPS
Ubuntu
Docker Compose
Caddy/Nginx
Twilio Programmable Voice
Twilio Media Streams
FastAPI voice-gateway
Gemini Live / Gemini Flash
ElevenLabs
Hermes Agent
OpenClaw
NATS
Redis
Postgres + pgvector
Obsidian vault + Git sync
OpenRouter proxy
Scheduler
Telegram bot
GitHub
Codex / Claude Code
ffmpeg / sox
```
