# HOSTINGER VPS Terminal Development & Integration Guide

## Purpose

This guide is a terminal-first development and deployment manual for building FlavorOS / BairyOS on a Hostinger VPS.

It assumes the project will run as a VPS-deployed, Docker-based, multi-agent executive operating system with:

- Two human-facing Hermes agents: Khadijah and Sinclair
- Three OpenClaw specialist agents: Maxine, Scooter, and Kyle
- Shared infrastructure: NATS, Redis, Postgres/pgvector, OpenRouter proxy, scheduler, secrets-loader, vault-sync
- A future phone-call voice layer using Twilio Media Streams, Gemini Live / Gemini Flash, and ElevenLabs

This guide is written so Codex, Claude Code, or a terminal-focused coding assistant can help execute the build step by step.

---

## 0. Intended System Shape

### Core Runtime

```text
Hostinger VPS
  ├── Docker Engine
  ├── Docker Compose
  ├── Nginx or Caddy reverse proxy
  ├── FlavorOS repo
  ├── Docker network: flavor
  ├── Agent containers
  │   ├── khadijah     # Hermes / Chief of Staff
  │   ├── sinclair     # Hermes / Executive Assistant
  │   ├── maxine       # OpenClaw / COO
  │   ├── scooter      # OpenClaw / CLO
  │   └── kyle         # OpenClaw / CRO
  ├── Infra containers
  │   ├── nats
  │   ├── redis
  │   ├── postgres
  │   ├── openrouter-proxy
  │   ├── secrets-loader
  │   ├── scheduler
  │   └── vault-sync
  └── Voice containers
      ├── voice-gateway
      └── optional audio-worker
```

### External Services

```text
Twilio
  └── receives phone calls and streams audio to VPS

Gemini Live / Gemini Flash
  └── handles low-latency conversational reasoning / audio model layer

ElevenLabs
  └── produces Khadijah and Sinclair custom voices

OpenRouter
  └── routes model calls for Hermes / OpenClaw where applicable

Obsidian Git Remote
  └── syncs durable operating memory
```

---

## 1. Recommended Hostinger VPS Specification

### Minimum Development VPS

Use this only for early testing.

```text
2 vCPU
4 GB RAM
80 GB NVMe
Ubuntu 24.04 LTS
```

This may run the core containers but will likely feel tight once voice streaming, Postgres, and five agent containers are active.

### Recommended MVP VPS

```text
4 vCPU
8 GB RAM
160 GB NVMe
Ubuntu 24.04 LTS
```

This is the recommended starting point for a real FlavorOS MVP.

### Preferred Production VPS

```text
8 vCPU
16 GB RAM
250+ GB NVMe
Ubuntu 24.04 LTS
```

Use this if you expect persistent voice calls, several background jobs, active vault sync, browser automation, or heavier OpenClaw tasks.

---

## 2. Hostinger Initial Server Setup

### 2.1 Create the VPS

In Hostinger:

1. Create a VPS.
2. Select Ubuntu 24.04 LTS.
3. Enable SSH access.
4. Add your SSH public key if Hostinger offers that option.
5. Record the VPS public IP address.

### 2.2 SSH into the VPS

From your local machine:

```bash
ssh root@YOUR_SERVER_IP
```

If using a private key:

```bash
ssh -i ~/.ssh/YOUR_KEY root@YOUR_SERVER_IP
```

### 2.3 Update the Server

```bash
apt update && apt upgrade -y
apt install -y git curl wget ufw fail2ban ca-certificates gnupg lsb-release unzip jq nano htop
```

### 2.4 Set the Hostname

```bash
hostnamectl set-hostname flavoros-vps
```

Check:

```bash
hostnamectl
```

### 2.5 Create a Non-Root Deploy User

```bash
adduser deploy
usermod -aG sudo deploy
```

Copy SSH access from root to deploy:

```bash
rsync --archive --chown=deploy:deploy ~/.ssh /home/deploy
```

Test login:

```bash
ssh deploy@YOUR_SERVER_IP
```

---

## 3. SSH Hardening

Log in as root first.

```bash
nano /etc/ssh/sshd_config
```

Set or confirm:

```text
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
```

Restart SSH:

```bash
systemctl restart ssh
```

Keep your current terminal open until you confirm the deploy user can log in.

---

## 4. Firewall Setup

Allow SSH, HTTP, and HTTPS.

```bash
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
ufw status verbose
```

Do not expose Postgres, Redis, NATS, or internal agent ports publicly.

Only expose:

```text
22    SSH
80    HTTP / cert challenge
443   HTTPS / WSS
```

---

## 5. Add Swap Memory

For 4 GB or 8 GB VPS, add swap.

```bash
fallocate -l 4G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
```

Persist swap:

```bash
echo '/swapfile none swap sw 0 0' | tee -a /etc/fstab
```

Tune swappiness:

```bash
echo 'vm.swappiness=20' | tee -a /etc/sysctl.conf
sysctl -p
```

Check:

```bash
free -h
```

---

## 6. Install Docker and Docker Compose

### 6.1 Install Docker

```bash
apt install -y ca-certificates curl gnupg
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg
```

Add Docker repo:

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Install:

```bash
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### 6.2 Add Deploy User to Docker Group

```bash
usermod -aG docker deploy
```

Log out and log back in as `deploy`.

Test:

```bash
docker --version
docker compose version
docker run hello-world
```

---

## 7. Install Reverse Proxy

You may use either **Nginx** or **Caddy**.

For this project, Caddy is simpler because it automatically handles SSL.

### Option A — Install Caddy

```bash
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https curl
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install -y caddy
```

### Option B — Install Nginx

```bash
sudo apt install -y nginx certbot python3-certbot-nginx
```

Caddy is preferred for MVP unless you already have an Nginx pattern.

---

## 8. DNS Configuration

Point your domain or subdomain to the Hostinger VPS IP.

Recommended records:

```text
A     voice.yourdomain.com       YOUR_SERVER_IP
A     api.yourdomain.com         YOUR_SERVER_IP
A     app.yourdomain.com         YOUR_SERVER_IP
```

Suggested usage:

```text
voice.yourdomain.com  → Twilio voice webhook and WebSocket stream
api.yourdomain.com    → internal API / health endpoints
app.yourdomain.com    → optional web dashboard later
```

Wait for DNS to propagate:

```bash
dig voice.yourdomain.com
```

---

## 9. Repo Deployment Layout

Log in as deploy:

```bash
ssh deploy@YOUR_SERVER_IP
```

Create app directory:

```bash
mkdir -p ~/apps
cd ~/apps
```

Clone your repo:

```bash
git clone YOUR_REPO_URL flavoros
cd flavoros
```

Recommended server structure:

```text
/home/deploy/apps/flavoros
  ├── docker-compose.yml
  ├── .env
  ├── CHIEF_OF_STAFF_CONTEXT.md
  ├── agents/
  ├── infra/
  ├── vault/
  ├── workspace/
  ├── cron/
  └── docs/
```

Create required local folders:

```bash
mkdir -p vault workspace cron infra/secrets logs backups
```

---

## 10. Environment Variables

Create `.env`:

```bash
nano .env
```

Recommended starting template:

```env
# Core
POSTGRES_PASSWORD=replace_with_strong_password
OBSIDIAN_GIT_REMOTE=git@github.com:YOUR_ORG/YOUR_OBSIDIAN_VAULT.git
KHADIJAH_DOMAIN=voice.yourdomain.com

# Model routing
OPENROUTER_API_KEY=replace_me
GEMINI_API_KEY=replace_me

# Voice
ELEVENLABS_API_KEY=replace_me
KHADIJAH_ELEVENLABS_VOICE_ID=replace_me
SINCLAIR_ELEVENLABS_VOICE_ID=replace_me

# Twilio
TWILIO_ACCOUNT_SID=replace_me
TWILIO_AUTH_TOKEN=replace_me
TWILIO_PHONE_NUMBER=+15555555555
TWILIO_VOICE_WEBHOOK_URL=https://voice.yourdomain.com/voice
TWILIO_STREAM_URL=wss://voice.yourdomain.com/twilio-stream

# Optional
APP_ENV=production
LOG_LEVEL=info
TIMEZONE=America/New_York
```

Lock permissions:

```bash
chmod 600 .env
```

---

## 11. Secrets Strategy

Your compose file already expects a `secrets-loader` and a tmpfs secrets directory.

For MVP, use `.env` during development.

For production, migrate secrets into:

```text
infra/secrets/
```

Suggested files:

```text
infra/secrets/_shared/openrouter.key
infra/secrets/_shared/gemini.key
infra/secrets/_shared/elevenlabs.key
infra/secrets/_shared/twilio.key
infra/secrets/khadijah/composio.key
infra/secrets/sinclair/composio.key
```

Create folders:

```bash
mkdir -p infra/secrets/_shared infra/secrets/khadijah infra/secrets/sinclair
```

Write secret files:

```bash
printf '%s' "$OPENROUTER_API_KEY" > infra/secrets/_shared/openrouter.key
printf '%s' "$GEMINI_API_KEY" > infra/secrets/_shared/gemini.key
printf '%s' "$ELEVENLABS_API_KEY" > infra/secrets/_shared/elevenlabs.key
printf '%s' "$TWILIO_AUTH_TOKEN" > infra/secrets/_shared/twilio.key
```

Lock permissions:

```bash
chmod -R 600 infra/secrets
find infra/secrets -type d -exec chmod 700 {} \;
```

If your secrets-loader expects encrypted age files, keep `.env` for the first MVP and later formalize age encryption.

---

## 12. Docker Compose Baseline Bring-Up

From repo root:

```bash
docker compose config
```

Build:

```bash
docker compose build
```

Start infrastructure first:

```bash
docker compose up -d nats redis postgres openrouter-proxy secrets-loader scheduler vault-sync
```

Check:

```bash
docker compose ps
docker compose logs -f secrets-loader
```

Then start agents:

```bash
docker compose up -d khadijah sinclair maxine scooter kyle
```

Check:

```bash
docker compose ps
docker compose logs -f khadijah
```

---

## 13. Add Voice Gateway Container

Your current compose file needs an additional service for Twilio / Gemini / ElevenLabs call handling.

Recommended location:

```text
infra/voice-gateway/
  ├── Dockerfile
  ├── requirements.txt
  └── app/
      ├── main.py
      ├── twilio_routes.py
      ├── twilio_stream.py
      ├── gemini_live.py
      ├── elevenlabs_tts.py
      ├── audio_codec.py
      ├── hermes_router.py
      └── state.py
```

### 13.1 Add to docker-compose.yml

Add this service:

```yaml
  voice-gateway:
    build: ./infra/voice-gateway
    container_name: voice-gateway
    restart: unless-stopped
    environment:
      APP_ENV: ${APP_ENV:-production}
      LOG_LEVEL: ${LOG_LEVEL:-info}
      TIMEZONE: ${TIMEZONE:-America/New_York}
      NATS_URL: nats://nats:4222
      REDIS_URL: redis://redis:6379
      POSTGRES_URL: postgres://flavor:${POSTGRES_PASSWORD}@postgres:5432/flavor
      GEMINI_API_KEY: ${GEMINI_API_KEY}
      ELEVENLABS_API_KEY: ${ELEVENLABS_API_KEY}
      KHADIJAH_ELEVENLABS_VOICE_ID: ${KHADIJAH_ELEVENLABS_VOICE_ID}
      SINCLAIR_ELEVENLABS_VOICE_ID: ${SINCLAIR_ELEVENLABS_VOICE_ID}
      TWILIO_ACCOUNT_SID: ${TWILIO_ACCOUNT_SID}
      TWILIO_AUTH_TOKEN: ${TWILIO_AUTH_TOKEN}
      TWILIO_STREAM_URL: ${TWILIO_STREAM_URL}
      VAULT_PATH: /vault
    volumes:
      - ./vault:/vault
      - ./workspace:/workspace
      - ./CHIEF_OF_STAFF_CONTEXT.md:/etc/flavoros/CHIEF_OF_STAFF_CONTEXT.md:ro
    depends_on:
      - nats
      - redis
      - postgres
      - khadijah
      - sinclair
    expose:
      - "8088"
    networks:
      - flavor
```

Do not publish `8088` directly to the internet unless needed for debugging. Use Caddy/Nginx as reverse proxy.

---

## 14. Voice Gateway Dockerfile

Create:

```bash
mkdir -p infra/voice-gateway/app
nano infra/voice-gateway/Dockerfile
```

Content:

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    sox \
    libsox-fmt-all \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app /app/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8088", "--proxy-headers"]
```

---

## 15. Voice Gateway Requirements

Create:

```bash
nano infra/voice-gateway/requirements.txt
```

Content:

```txt
fastapi==0.115.6
uvicorn[standard]==0.34.0
websockets==14.1
python-dotenv==1.0.1
pydantic==2.10.4
httpx==0.28.1
numpy==2.2.1
nats-py==2.9.0
redis==5.2.1
asyncpg==0.30.0
```

Optional later:

```txt
twilio==9.4.1
```

The MVP can return TwiML manually without the Twilio SDK.

---

## 16. Voice Gateway App Skeleton

Create:

```bash
nano infra/voice-gateway/app/main.py
```

Content:

```python
import os
from fastapi import FastAPI, WebSocket, Request, Response

app = FastAPI(title="FlavorOS Voice Gateway")

TWILIO_STREAM_URL = os.getenv("TWILIO_STREAM_URL", "wss://voice.example.com/twilio-stream")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "voice-gateway"}

@app.post("/voice")
async def voice_webhook(request: Request):
    # Twilio calls this endpoint when a phone call arrives.
    # It returns TwiML that connects the call to the WebSocket stream.
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Connect>
    <Stream url="{TWILIO_STREAM_URL}" />
  </Connect>
</Response>"""
    return Response(content=twiml, media_type="application/xml")

@app.websocket("/twilio-stream")
async def twilio_stream(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"event": "server_ready"})

    try:
        while True:
            message = await websocket.receive_text()
            # TODO:
            # 1. Parse Twilio JSON message.
            # 2. On start: store streamSid/callSid.
            # 3. On media: decode base64 mu-law audio.
            # 4. Resample to PCM 16k.
            # 5. Send to Gemini Live session.
            # 6. Receive Gemini/ElevenLabs audio.
            # 7. Encode to mu-law 8k and send media back to Twilio.
            print(message[:500])
    except Exception as exc:
        print(f"WebSocket closed/error: {exc}")
```

This gets Twilio connected first. Do not try to solve Gemini and ElevenLabs before confirming Twilio can connect to `/twilio-stream`.

---

## 17. Caddy Reverse Proxy

Create Caddyfile:

```bash
sudo nano /etc/caddy/Caddyfile
```

Content:

```caddy
voice.yourdomain.com {
    encode gzip

    reverse_proxy /voice voice-gateway:8088
    reverse_proxy /twilio-stream voice-gateway:8088
    reverse_proxy /health voice-gateway:8088
}
```

If Caddy runs on the host and `voice-gateway` is inside Docker, Caddy cannot resolve `voice-gateway` unless Caddy is also inside Docker or the container port is published.

For host-level Caddy, publish the voice gateway port only on localhost:

```yaml
    ports:
      - "127.0.0.1:8088:8088"
```

Then use:

```caddy
voice.yourdomain.com {
    encode gzip
    reverse_proxy 127.0.0.1:8088
}
```

Reload:

```bash
sudo systemctl reload caddy
```

Check:

```bash
curl https://voice.yourdomain.com/health
```

---

## 18. Nginx Reverse Proxy Alternative

Create:

```bash
sudo nano /etc/nginx/sites-available/flavoros-voice
```

Content:

```nginx
server {
    listen 80;
    server_name voice.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8088;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 3600;
        proxy_send_timeout 3600;
    }
}
```

Enable:

```bash
sudo ln -s /etc/nginx/sites-available/flavoros-voice /etc/nginx/sites-enabled/flavoros-voice
sudo nginx -t
sudo systemctl reload nginx
```

Issue SSL:

```bash
sudo certbot --nginx -d voice.yourdomain.com
```

---

## 19. Twilio Console Configuration

In Twilio Console:

1. Go to Phone Numbers.
2. Select your number.
3. Under Voice Configuration, set incoming call webhook:

```text
https://voice.yourdomain.com/voice
```

4. Method: `POST`.
5. Save.

Test call:

```bash
docker compose logs -f voice-gateway
```

Call the Twilio number and confirm logs show messages.

---

## 20. Audio Bridge Development Tasks

After Twilio connects, build these modules in order.

### 20.1 `audio_codec.py`

Responsibilities:

```text
mulaw 8k base64 → PCM 16k bytes
PCM 24k bytes → mulaw 8k base64
optional: PCM 16k bytes → mulaw 8k base64
```

Implementation options:

- Use Python `audioop` for mu-law conversions where available.
- Use `ffmpeg` subprocess for reliable production conversion.
- Use `sox` for streaming conversion if lower latency is needed.

Target functions:

```python
def twilio_payload_to_pcm16k(payload_b64: str) -> bytes:
    ...

def pcm24k_to_twilio_payload(pcm_bytes: bytes) -> str:
    ...
```

### 20.2 `gemini_live.py`

Responsibilities:

```text
open Gemini Live websocket
send setup config
send audio chunks
receive audio/text deltas
handle session close
```

Target class:

```python
class GeminiLiveSession:
    async def connect(self, system_prompt: str): ...
    async def send_audio(self, pcm16k: bytes): ...
    async def receive_loop(self): ...
    async def close(self): ...
```

### 20.3 `elevenlabs_tts.py`

Responsibilities:

```text
send text to ElevenLabs
stream audio response
convert audio to Twilio-compatible mu-law 8k
```

Target class:

```python
class ElevenLabsTTS:
    async def synthesize(self, text: str, voice_id: str) -> bytes:
        ...
```

### 20.4 `hermes_router.py`

Responsibilities:

```text
route transcript to Khadijah or Sinclair
create work orders for Maxine, Scooter, Kyle
publish to NATS
listen for reports
return speakable response to voice-gateway
```

Target routing logic:

```text
if request is executive synthesis / approval / priorities:
    route to khadijah
elif request is inbox / calendar / meetings / wellness:
    route to sinclair
elif request is operations / finance / project execution:
    create work_order.maxine
elif request is travel / logistics / research / technical prep:
    create work_order.scooter
elif request is CRM / relationships / brand-social:
    create work_order.kyle
else:
    Khadijah owns first response
```

---

## 21. NATS Message Contracts

Use clear JSON contracts.

### 21.1 Work Order

Subject:

```text
work_order.<agent>
```

Payload:

```json
{
  "work_order_id": "wo_2026_05_05_001",
  "source": "voice-gateway",
  "caller": "+15555555555",
  "call_sid": "CAxxxx",
  "requested_by": "Marcus",
  "front_agent": "khadijah",
  "target_agent": "scooter",
  "task_type": "travel_options",
  "user_request": "Find me options for Dallas next Thursday.",
  "context_summary": "User is on a live call. He wants options, not booking.",
  "deliverable": "3-option travel brief",
  "vault_path": "50-Travel/",
  "priority": "normal",
  "requires_approval": true,
  "created_at": "2026-05-05T12:00:00-04:00"
}
```

### 21.2 Report

Subject:

```text
report.<agent>
```

Payload:

```json
{
  "work_order_id": "wo_2026_05_05_001",
  "agent": "scooter",
  "status": "complete",
  "summary": "Found three Dallas travel options.",
  "vault_file": "50-Travel/dallas-options-2026-05-05.md",
  "user_facing_response": "I found three good options and put them in the travel folder.",
  "requires_approval": true,
  "completed_at": "2026-05-05T12:20:00-04:00"
}
```

### 21.3 Urgent Flag

Subject:

```text
flag.<severity>
```

Payload:

```json
{
  "severity": "high",
  "source": "voice-gateway",
  "issue": "Gemini Live session failed during active call.",
  "call_sid": "CAxxxx",
  "recommended_action": "Switch to fallback scripted response and text user."
}
```

---

## 22. State Drive Design

Use Redis for live state and Postgres for durable state.

### 22.1 Redis Keys

```text
call:{call_sid}:state
call:{call_sid}:transcript
call:{call_sid}:active_agent
call:{call_sid}:stream_sid
call:{call_sid}:pending_audio
call:{call_sid}:last_user_intent
```

### 22.2 Call State Object

```json
{
  "call_sid": "CAxxxx",
  "stream_sid": "MZxxxx",
  "caller": "+15555555555",
  "active_agent": "khadijah",
  "mode": "standard",
  "started_at": "2026-05-05T12:00:00-04:00",
  "last_user_utterance": "What do I need to know today?",
  "last_agent_response": "The most important item is...",
  "open_work_orders": [],
  "handoff_status": null
}
```

### 22.3 Postgres Tables

Suggested migrations:

```sql
CREATE TABLE IF NOT EXISTS voice_calls (
  id SERIAL PRIMARY KEY,
  call_sid TEXT UNIQUE NOT NULL,
  stream_sid TEXT,
  caller TEXT,
  active_agent TEXT,
  started_at TIMESTAMPTZ DEFAULT now(),
  ended_at TIMESTAMPTZ,
  status TEXT DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS voice_turns (
  id SERIAL PRIMARY KEY,
  call_sid TEXT NOT NULL,
  turn_index INTEGER NOT NULL,
  speaker TEXT NOT NULL,
  text TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS work_orders (
  id TEXT PRIMARY KEY,
  call_sid TEXT,
  source TEXT,
  target_agent TEXT,
  task_type TEXT,
  user_request TEXT,
  status TEXT DEFAULT 'pending',
  vault_file TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  completed_at TIMESTAMPTZ
);
```

---

## 23. Agent Voice Rules

### 23.1 Khadijah

Khadijah should speak when:

```text
briefing
approval
decision
priorities
project triage
money/legal/contract escalation
unclear ownership
```

Khadijah voice behavior:

```text
Direct
Warm
Firm
Maternal
Lead with the most important item
End with Decision Needed when applicable
```

### 23.2 Sinclair

Sinclair should speak when:

```text
calendar
inbox
meeting prep
wellness
reminders
next action
schedule pressure
```

Sinclair voice behavior:

```text
Organized
Supportive
Precise
Practical
Focused on time and readiness
```

### 23.3 Specialists

Specialists do not speak directly to the user.

```text
Maxine → reports through Khadijah
Scooter → reports through Khadijah or Sinclair
Kyle → reports through Khadijah
```

---

## 24. Deferral and Remote Worker Simulation

The call should feel like talking to two remote workers, not a chatbot.

Every request should resolve into one of three states.

### 24.1 Answer Now

Use when the state drive already has enough information.

```text
“I have that. The short version is...”
```

### 24.2 Clarify

Use when the request is ambiguous.

```text
“I can do that. Are we solving for fastest, cheapest, or easiest?”
```

### 24.3 Defer and Delegate

Use when the system lacks the information.

```text
“I don’t have that ready yet. I’ll have Scooter pull the options, add the file to the vault, and text you when it’s ready.”
```

A deferral must create:

```text
work order
owner
specialist
expected follow-up
vault destination
user notification channel
approval flag
```

---

## 25. Twilio SMS / Telegram Follow-Up

After a work order is complete, notify the user.

Possible channels:

```text
Telegram group bot
Khadijah direct Telegram
SMS via Twilio
Email summary
```

MVP recommendation:

```text
Voice call = live conversation
Telegram = async status and approvals
Vault = durable file
```

Later:

```text
SMS = “Your brief is ready.”
```

---

## 26. Health Checks

Add endpoints to voice-gateway:

```text
GET /health
GET /health/twilio
GET /health/gemini
GET /health/elevenlabs
GET /health/nats
GET /health/redis
```

Example response:

```json
{
  "status": "ok",
  "checks": {
    "twilio": "configured",
    "gemini": "configured",
    "elevenlabs": "configured",
    "nats": "ok",
    "redis": "ok"
  }
}
```

---

## 27. Logging

Recommended log files:

```text
logs/voice-gateway.log
logs/twilio-stream.log
logs/gemini-live.log
logs/nats-work-orders.log
logs/errors.log
```

Docker logs:

```bash
docker compose logs -f voice-gateway
docker compose logs -f khadijah
docker compose logs -f sinclair
docker compose logs -f nats
```

Enable Docker log rotation:

```bash
sudo nano /etc/docker/daemon.json
```

Content:

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "5"
  }
}
```

Restart Docker:

```bash
sudo systemctl restart docker
```

---

## 28. Backups

Create backup directory:

```bash
mkdir -p ~/apps/flavoros/backups
```

### 28.1 Postgres Backup Script

Create:

```bash
nano scripts/backup-postgres.sh
```

Content:

```bash
#!/usr/bin/env bash
set -euo pipefail

TS=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/deploy/apps/flavoros/backups"
mkdir -p "$BACKUP_DIR"

docker compose exec -T postgres pg_dump -U flavor flavor > "$BACKUP_DIR/flavor_$TS.sql"
gzip "$BACKUP_DIR/flavor_$TS.sql"

find "$BACKUP_DIR" -name "flavor_*.sql.gz" -mtime +14 -delete
```

Make executable:

```bash
chmod +x scripts/backup-postgres.sh
```

Cron:

```bash
crontab -e
```

Add:

```cron
0 3 * * * cd /home/deploy/apps/flavoros && ./scripts/backup-postgres.sh >> logs/backup.log 2>&1
```

### 28.2 Vault Backup

If vault-sync uses Git, verify:

```bash
cd vault
git status
git remote -v
```

Manual sync:

```bash
git add .
git commit -m "vault backup $(date -Iseconds)"
git push
```

---

## 29. Update and Redeploy Workflow

Pull new code:

```bash
cd ~/apps/flavoros
git pull
```

Validate compose:

```bash
docker compose config
```

Rebuild changed services:

```bash
docker compose build voice-gateway khadijah sinclair maxine scooter kyle
```

Restart:

```bash
docker compose up -d
```

Check:

```bash
docker compose ps
curl https://voice.yourdomain.com/health
```

---

## 30. Debugging Checklist

### 30.1 Twilio Call Does Not Connect

Check:

```bash
curl https://voice.yourdomain.com/health
```

Check Caddy/Nginx logs:

```bash
sudo journalctl -u caddy -f
sudo tail -f /var/log/nginx/error.log
```

Check Twilio Console debugger.

Confirm webhook:

```text
https://voice.yourdomain.com/voice
```

### 30.2 WebSocket Does Not Connect

Confirm endpoint:

```text
wss://voice.yourdomain.com/twilio-stream
```

Check reverse proxy supports Upgrade headers.

Check logs:

```bash
docker compose logs -f voice-gateway
```

### 30.3 No Audio Back to Caller

Check:

```text
Is stream bidirectional?
Are you using <Connect><Stream> and not <Start><Stream>?
Are you sending audio/x-mulaw at 8000 Hz?
Is payload base64 encoded with no file header bytes?
Are you using the correct streamSid?
```

### 30.4 Gemini Not Responding

Check API key:

```bash
docker compose exec voice-gateway env | grep GEMINI
```

Check logs:

```bash
docker compose logs -f voice-gateway | grep -i gemini
```

### 30.5 ElevenLabs Voice Not Working

Check:

```text
ELEVENLABS_API_KEY
KHADIJAH_ELEVENLABS_VOICE_ID
SINCLAIR_ELEVENLABS_VOICE_ID
```

Test from container:

```bash
docker compose exec voice-gateway python -c "import os; print(bool(os.getenv('ELEVENLABS_API_KEY')))"
```

### 30.6 Agents Not Receiving Work Orders

Check NATS:

```bash
docker compose logs -f nats
```

Check agent logs:

```bash
docker compose logs -f khadijah
docker compose logs -f scooter
```

---

## 31. MVP Build Order for Codex / Claude Code

Use this order exactly.

### Phase 1 — Server Foundation

```text
1. Harden Hostinger VPS.
2. Install Docker and Compose.
3. Configure DNS.
4. Install Caddy or Nginx.
5. Clone repo.
6. Create .env.
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

### Phase 4 — Audio Round Trip

```text
1. Parse Twilio start/media/stop events.
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

### Phase 8 — Productionization

```text
1. Add health checks.
2. Add backups.
3. Add log rotation.
4. Add uptime monitoring.
5. Add Twilio failure fallback.
6. Add deployment script.
```

---

## 32. Deployment Scripts

Create:

```bash
mkdir -p scripts
nano scripts/deploy.sh
```

Content:

```bash
#!/usr/bin/env bash
set -euo pipefail

cd /home/deploy/apps/flavoros

echo "Pulling latest code..."
git pull

echo "Validating compose..."
docker compose config > /tmp/flavoros-compose-check.yml

echo "Building services..."
docker compose build

echo "Starting services..."
docker compose up -d

echo "Current service status:"
docker compose ps

echo "Health check:"
curl -fsS https://voice.yourdomain.com/health || true
```

Make executable:

```bash
chmod +x scripts/deploy.sh
```

---

## 33. One-Command Status Script

Create:

```bash
nano scripts/status.sh
```

Content:

```bash
#!/usr/bin/env bash
set -euo pipefail

cd /home/deploy/apps/flavoros

echo "== Docker services =="
docker compose ps

echo ""
echo "== Disk =="
df -h

echo ""
echo "== Memory =="
free -h

echo ""
echo "== Voice health =="
curl -fsS https://voice.yourdomain.com/health || true

echo ""
echo "== Recent voice logs =="
docker compose logs --tail=50 voice-gateway || true
```

Make executable:

```bash
chmod +x scripts/status.sh
```

---

## 34. Production Security Checklist

Before letting real users call the system:

```text
[ ] SSH root login disabled
[ ] Password SSH disabled
[ ] UFW enabled
[ ] Only 22, 80, 443 open
[ ] .env chmod 600
[ ] secrets folder chmod 600 files / 700 dirs
[ ] Docker log rotation enabled
[ ] Postgres not publicly exposed
[ ] Redis not publicly exposed
[ ] NATS not publicly exposed
[ ] Caddy/Nginx SSL working
[ ] Twilio webhook uses HTTPS
[ ] Twilio stream uses WSS
[ ] Webhook validates Twilio signatures
[ ] Backups tested
[ ] Vault sync tested
[ ] Agent escalation rules tested
[ ] Money/legal/external-send actions require approval
```

---

## 35. Final Development Instruction for Coding Agents

When using Codex or Claude Code, give it this instruction:

```text
You are helping build FlavorOS on a Hostinger VPS. Follow HOSTINGER_VPS_TERMINAL_DEVELOPMENT_INTEGRATION.md exactly. Do not skip phases. First verify Docker Compose base services. Then add voice-gateway. Do not implement Gemini or ElevenLabs until Twilio successfully connects to /twilio-stream. Preserve the existing hub-and-spoke architecture: Khadijah and Sinclair are the only human-facing agents. Maxine, Scooter, and Kyle remain dark specialists. All specialist work must route through NATS work_order.<agent> and report.<agent> subjects. Maintain human-in-the-loop controls for money, legal, contracts, bookings, and external sends.
```

---

## 36. First Terminal Session Checklist

Run this when beginning development on the Hostinger VPS:

```bash
ssh deploy@YOUR_SERVER_IP
cd ~/apps/flavoros
git status
docker compose config
docker compose ps
curl https://voice.yourdomain.com/health
./scripts/status.sh
```

If any command fails, fix that layer before moving forward.

---

## 37. Definition of Done for MVP

The MVP is complete when:

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

At that point, the system has become a real VPS-hosted remote staff voice layer rather than a simple voice chatbot.

