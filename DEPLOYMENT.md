# FlavorOS Deployment Protocol

Zero-generation deployment. Nothing to fill in at deploy time except the `.env` values and your encrypted secrets blob.

---

## Prerequisites

| Requirement | Minimum |
|---|---|
| VPS | 4 vCPU, 8 GB RAM, 80 GB SSD (Hostinger KVM VPS or equivalent with full root + Docker access) |
| Docker Engine | 24.0+ |
| Docker Compose | v2.20+ (plugin, not standalone) |
| Git | 2.x |
| SOPS | 3.8+ |
| age | 1.1+ |

> **Hostinger note**: The "Container" hosting tier only supports a single container. You need a **KVM VPS** plan (VPS 2 or higher) to get full root access and install Docker yourself.

---

## Directory Shipped in Git

```
FlavorOS/
├── docker-compose.yml          # full stack definition
├── .env.example                # copy to .env, fill in 3 values
├── FLAVOROS_CONTEXT.md   # shared context for all agents
├── agents/
│   ├── khadijah/   (SOUL.md, agent.yaml, skills/)
│   ├── sinclair/   (SOUL.md, agent.yaml, skills/)
│   ├── maxine/     (SOUL.md, agent.yaml, skills/)
│   ├── kyle/       (SOUL.md, agent.yaml, skills/)
│   └── scooter/    (SOUL.md, agent.yaml, skills/)
├── infra/
│   ├── agent-base/        (Dockerfile, agent.py — shared image)
│   ├── secrets-loader/    (Dockerfile, entrypoint.sh)
│   ├── openrouter-proxy/  (Dockerfile, proxy logic)
│   ├── composio-init/     (Dockerfile, init.py — run once)
│   ├── scheduler/         (Dockerfile, cron runner)
│   ├── secrets/           (.sops.yaml, secrets.enc.yaml)
│   ├── openrouter.yaml    (model routing config)
│   ├── composio.yaml      (account grants)
│   ├── obsidian.yaml      (vault permissions)
│   └── voice.yaml         (ElevenLabs config)
├── cron/schedules.yaml
├── vault/                  (Obsidian vault — git-synced)
└── workspace/              (active task files)
```

---

## Step-by-Step Deploy

### 1. Provision VPS

```bash
# SSH into your Hostinger KVM VPS
ssh root@your-vps-ip

# Install Docker
curl -fsSL https://get.docker.com | sh
systemctl enable --now docker

# Install Docker Compose plugin (included in modern Docker, verify)
docker compose version
```

### 2. Clone Repo

```bash
git clone git@github.com:your-org/FlavorOS.git /opt/flavoros
cd /opt/flavoros
```

### 3. Generate Age Key (One-Time Only)

```bash
mkdir -p /etc/flavoros
age-keygen -o /etc/flavoros/age.key
chmod 600 /etc/flavoros/age.key

# Note the PUBLIC key — you'll need it for encrypting secrets locally
cat /etc/flavoros/age.key | grep "public key"
```

### 4. Configure Environment

```bash
cp .env.example .env
nano .env
```

Fill in:
- `KHADIJAH_DOMAIN` — your domain for the Telegram webhook (e.g., `flavor.yourdomain.com`)
- `POSTGRES_PASSWORD` — strong random string
- `OBSIDIAN_GIT_REMOTE` — your vault repo SSH URL

### 5. Encrypt Secrets (On Your Local Machine)

```bash
# Copy the secrets template
cp infra/secrets/secrets.example.yaml infra/secrets/secrets.yaml

# Fill in your actual API keys
nano infra/secrets/secrets.yaml

# Encrypt with SOPS (uses .sops.yaml creation rules)
sops --encrypt --in-place infra/secrets/secrets.yaml
mv infra/secrets/secrets.yaml infra/secrets/secrets.enc.yaml

# Verify: should show encrypted blob, not plaintext
head infra/secrets/secrets.enc.yaml
```

### 6. Deploy Infrastructure

```bash
docker compose up -d nats redis postgres openrouter-proxy secrets-loader vault-sync scheduler
```

Wait for secrets-loader health:
```bash
docker compose logs -f secrets-loader
# Look for per-agent secret output for khadijah, sinclair, maxine, scooter, and kyle
```

### 7. Bootstrap OAuth (One-Time Only)

```bash
docker compose run --rm composio-init
# Follow the interactive prompts — scan QR codes for each OAuth account
# Connection IDs are written back to the encrypted secrets file
```

### 8. Deploy All Agents

```bash
docker compose up -d khadijah sinclair maxine kyle scooter
```

### 9. Verify

```bash
# All containers running
docker compose ps

# Check agent logs
docker compose logs khadijah --tail 20
docker compose logs sinclair --tail 20

# Test NATS connectivity
docker compose exec nats nats-server --signal ldm

# Verify Khadijah responds on Telegram
# Send a test message to your bot
```

---

## Per-Agent Deployment Anatomy

Every agent deploys identically. Zero per-agent generation is required because:

| Layer | Source | Mounted As |
|---|---|---|
| Runtime code | `infra/agent-base/` (shared image) | Built once, used by all |
| Personality | `agents/<name>/SOUL.md` | `/etc/flavoros/SOUL.md` |
| Config | `agents/<name>/agent.yaml` | `/etc/flavoros/agent.yaml` |
| Skills | `agents/<name>/skills/` | `/skills` |
| Secrets | `secrets-tmpfs` (decrypted at boot) | `/run/flavor/secrets` |
| Vault | `./vault` | `/vault` |
| Context | `FLAVOROS_CONTEXT.md` | `/etc/flavoros/FLAVOROS_CONTEXT.md` |

To add a new agent:
1. Create `agents/<name>/SOUL.md`
2. Create `agents/<name>/agent.yaml`
3. Create `agents/<name>/skills/` directory with skill bundles
4. Add service block to `docker-compose.yml` (copy any existing agent block, change name)
5. Add NATS subscription in agent.yaml
6. `docker compose up -d <name>`

---

## Agent Roster (All 5)

| Agent | Role | Runtime | Primary Model | Bus Topic |
|---|---|---|---|---|
| khadijah | Chief of Staff | hermes | claude-sonnet-4.6 | `work_order.khadijah` |
| sinclair | Executive Assistant | hermes | claude-sonnet-4.6 / gpt-5.4-mini | `work_order.sinclair` |
| maxine | COO | openclaw | claude-sonnet-4.6 / gpt-5.4-mini | `work_order.maxine` |
| kyle | CRO | openclaw | claude-sonnet-4.6 / gpt-5.4-mini | `work_order.kyle` |
| scooter | CLO | openclaw | claude-sonnet-4.6 / gpt-5.4-mini | `work_order.scooter` |

Retired standalone agents are preserved as skills/persona packs inside active agents:

- Watson is inside Sinclair.
- Regine is inside Kyle.
- Overton is split across Maxine and Scooter.

---

## Operations

### Update an Agent's Personality or Skills

```bash
# Edit the soul or skills locally, push to git, then on VPS:
git pull
docker compose restart <agent-name>
```

### Rotate Secrets

```bash
# On local machine:
sops infra/secrets/secrets.enc.yaml   # edit encrypted file in-place
git add infra/secrets/secrets.enc.yaml && git commit -m "rotate keys"
git push

# On VPS:
git pull
docker compose restart secrets-loader
# All agents pick up new secrets on their next request (read from tmpfs)
```

### Scale Down (Disable an Agent)

```bash
docker compose stop <agent-name>
# Agent is offline but config remains; `docker compose up -d <name>` brings it back
```

### Full Stack Restart

```bash
docker compose down
docker compose up -d
```

### View Logs

```bash
docker compose logs -f                    # all containers
docker compose logs -f khadijah sinclair  # specific agents
```

---

## Health Checks

| Check | Command | Healthy Signal |
|---|---|---|
| All running | `docker compose ps` | All services "Up" |
| Secrets loaded | `docker compose exec secrets-loader ls /run/flavor/secrets/` | Per-agent dirs present |
| NATS connected | `docker compose logs nats \| tail -5` | "Listening for client connections" |
| Khadijah alive | Send Telegram message | Response within 30s |
| Vault synced | `docker compose logs vault-sync \| tail -5` | "sync complete" |

---

## Hostinger-Specific Notes

1. **Plan**: You need **KVM VPS 2** or higher (4 vCPU / 8 GB). The "Container" or "Web Hosting" tiers do not support running your own Docker daemon.
2. **Firewall**: Open ports 443 (Khadijah webhook via Caddy) and 22 (SSH). All inter-container traffic stays on the Docker bridge network.
3. **Storage**: 80 GB SSD is comfortable for 13 containers + Obsidian vault + Postgres. Monitor with `df -h`.
4. **Backups**: Enable Hostinger's weekly VPS snapshots. Additionally, the vault is git-synced and Postgres can be backed up with `pg_dump` via cron.
5. **Domain**: Point your domain's A record to the VPS IP. Caddy (if added) handles TLS automatically via Let's Encrypt.
