# FlavorOS Deployment

VPS install + operate runbook.

---

## VPS Requirements

- 4+ vCPU, 8 GB RAM minimum (16 GB recommended for full staff active)
- 80 GB SSD
- Ubuntu 22.04 or Debian 12
- Public IPv4 + a domain pointed at it (for Khadijah's webhook)

## Bootstrap

```bash
# 1. Install Docker + Compose
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# 2. Clone
git clone <your-fork> /opt/flavoros
cd /opt/flavoros

# 3. Secrets
cp .env.example .env
# Fill in: OPENROUTER_API_KEY, COMPOSIO_API_KEY, TELEGRAM_BOT_TOKEN,
#          OBSIDIAN_GIT_REMOTE, POSTGRES_PASSWORD, KHADIJAH_DOMAIN

# 4. Owner config
cp templates/CHIEF_OF_STAFF_CONTEXT.example.md CHIEF_OF_STAFF_CONTEXT.md
# Fill it out

# 5. Bring up infra first
docker compose up -d nats redis postgres caddy

# 6. Initialize Composio accounts (interactive — handles OAuth)
docker compose run --rm composio-init

# 7. Initialize Obsidian vault
docker compose run --rm obsidian-init

# 8. Bring up agents
docker compose up -d khadijah sinclair maxine kyle regine scooter watson overton

# 9. Verify
docker compose ps
docker compose logs -f khadijah
```

## OpenRouter

Single API key in `.env`. Per-agent model routing in `infra/openrouter.yaml`. Cost caps enforced by the openrouter-proxy sidecar — every agent's HTTP client targets `http://openrouter-proxy:8080` instead of `openrouter.ai` directly. This gives us spend metering and circuit breakers without modifying agent code.

## Composio

One Composio workspace. Each owner account (Business A email, Business B email, etc.) is connected once interactively, then referenced by alias in `infra/composio.yaml`. Agents request toolkits + alias; Composio resolves to the right account.

## Obsidian Vault

Mounted at `/vault` in every container. Sync strategy:

- **Option A (recommended)**: A `vault-sync` sidecar runs `git pull/push` every 60s. Vault repo lives on GitHub or a private Gitea. The user's local Obsidian + plugin pulls from the same repo.
- **Option B**: Self-host `obsidian-livesync` on the VPS (CouchDB-based real-time sync).

## Cron / Scheduling

Cron is centralized in `cron/schedules.yaml`. The `scheduler` container reads this file and publishes `work_order.*` messages to NATS at the configured times. No host crontab needed. See [cron/schedules.yaml](cron/schedules.yaml).

## Backups

- Postgres: nightly `pg_dump` to S3-compatible storage (`infra/backup.yaml`)
- Vault: continuous via git remote
- Composio tokens: held in Composio's vault, not on the VPS

## Operations

| Task | Command |
|------|---------|
| Tail an agent's logs | `docker compose logs -f <agent>` |
| Restart one agent | `docker compose restart <agent>` |
| Update all agents | `git pull && docker compose pull && docker compose up -d` |
| Force a Flavor Brief now | `docker compose exec khadijah flavor brief --now` |
| Toggle Operational Mode | `docker compose exec khadijah flavor mode <deep-work\|social\|recovery\|standard>` |
| Pause an agent | `docker compose stop <agent>` |
| Inspect Editorial Memory | `docker compose exec postgres psql -U flavor` |

## Health & Alerts

- Each agent reports a heartbeat every 60s to NATS `health.<agent>`.
- Khadijah escalates to the user via Telegram if any agent misses 3 heartbeats.
- OpenRouter spend cap breach → Khadijah pauses the offending agent and pages user.
