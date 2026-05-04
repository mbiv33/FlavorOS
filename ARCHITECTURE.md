# FlavorOS Architecture

VPS-deployed, containerized, multi-agent system. Each agent runs in its own container. Khadijah (the hub) is the only agent the user talks to directly. All inter-agent traffic flows through her via a message bus.

---

## Topology

```
                                      ┌──────────────┐
                              ┌──────▶│  USER (you)  │◀──────┐
                              │       └──────────────┘       │
                              │   Telegram (text + voice)     │
                              │                               │
                       ┌──────▼──────┐    Flavor Brief        │
                       │  KHADIJAH   │ ◀─── synthesis ────────┘
                       │  (hermes)   │ ── ElevenLabs TTS ──▶ voice notes
                       │  sonnet-4.6 │ ◀─ Whisper STT ────── inbound voice
                       └──┬────────┬─┘
                          │ NATS / Redis Streams (message bus)
        ┌─────────┬───────┼────────┼───────┬─────────┬─────────┬─────────┐
        ▼         ▼       ▼        ▼       ▼         ▼         ▼         ▼
   ┌────────┐┌────────┐┌──────┐┌──────┐┌──────┐┌────────┐┌────────┐┌────────┐
   │SINCLAIR││ MAXINE ││ KYLE ││REGINE││SCOOTER││ WATSON ││OVERTON ││  ...   │
   │openclaw││openclaw││ ocl  ││ ocl  ││ ocl   ││  ocl   ││  ocl   ││        │
   └───┬────┘└───┬────┘└──┬───┘└──┬───┘└──┬────┘└───┬────┘└───┬────┘
       │         │        │       │       │         │         │
       └─────────┴────────┴───────┴───────┴─────────┴─────────┘
                              │
                  ┌───────────┼────────────┬──────────────┐
                  ▼           ▼            ▼              ▼
            ┌─────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
            │OpenRouter│ │ Composio │ │ Obsidian │ │ Postgres+pgvector│
            │ (models) │ │  (accts) │ │  (vault) │ │  (memory/state)  │
            └─────────┘ └──────────┘ └──────────┘ └──────────────┘
```

## Containers

Eight long-running services + four infra services. All on a private Docker network; only Khadijah's UI is exposed.

| Container | Runtime | Models (via OpenRouter) | Purpose |
|-----------|---------|--------------------------|---------|
| `khadijah` | hermes-agent | `anthropic/claude-sonnet-4.6` | Hub. Orchestration, Flavor Briefs, user interface |
| `sinclair` | openclaw | thinking: `claude-sonnet-4.6` / sweep: `claude-haiku-4.5` | Inbox + calendar |
| `maxine` | openclaw | thinking: `claude-sonnet-4.6` / report: `claude-haiku-4.5` | Tasks + project tracking |
| `kyle` | openclaw | `openai/gpt-5-mini` | CRM + finance |
| `regine` | openclaw | `openai/gpt-5-mini` | Brand + social |
| `scooter` | openclaw | `openai/gpt-5-mini` | Travel + logistics |
| `watson` | openclaw | `openai/gpt-5-mini` *(confirm "5.4")* | Wellness + PERMA-V |
| `overton` | openclaw | `claude-haiku-4.5` *(filling gap)* | Bills + tech ops |
| `nats` | nats:latest | — | Message bus (Work Orders + replies) |
| `redis` | redis:7 | — | Cache + scheduled-task queue |
| `postgres` | pgvector/pgvector:pg16 | — | Editorial Memory, embeddings, audit log |
| `caddy` | caddy:2 | — | TLS + reverse proxy for Khadijah's webhook |

## Model Routing (OpenRouter)

All model calls route through OpenRouter. Each agent reads its model assignment from `agents/<name>/agent.yaml`. Two-tier setup for Sinclair and Maxine: a "thinking" model for synthesis/decisions and a "crawl" model for high-volume sweeps.

Cost guardrails per agent in `infra/openrouter.yaml` — daily token cap, fallback model, and a hard stop that pages Khadijah if exceeded.

## Multi-Account Integration (Composio)

User has **2 businesses + heavy travel**, so most domains have multiple accounts.

| Domain | Accounts | Composio Toolkit |
|--------|----------|------------------|
| Email | Business A, Business B, Personal | `gmail` (×3) or `outlook` |
| Calendar | Same 3 accounts | `googlecalendar` (×3) |
| Finance | Business A bank, Business B bank, Personal cards | `plaid` or `mercury`, `ramp`, `quickbooks` |
| CRM | Per-business CRM | `hubspot`, `attio`, or `pipedrive` |
| PM | Per-business PM | `linear`, `asana`, or `notion` |
| Travel | Personal | `googleflights`, `hotels`, `tripit` |

Each agent declares the toolkits it can call in `agents/<name>/agent.yaml`. Composio handles OAuth, rate limits, and account scoping. The same toolkit can be bound to multiple authenticated accounts via `account_aliases`.

## Obsidian Vault

A single git-synced Obsidian vault is mounted into every container as `/vault` (read-only) and `/vault-rw` for the few agents that write. Khadijah arbitrates writes to avoid conflicts.

| Folder | Purpose | Writers |
|--------|---------|---------|
| `vault/00-Inbox/` | Captures, raw notes | Khadijah, user |
| `vault/10-Briefs/` | Flavor Briefs (one per day) | Khadijah |
| `vault/20-Meetings/` | Pre-meeting prep + post-meeting notes | Sinclair, Maxine |
| `vault/30-Projects/` | Active project pages | Maxine |
| `vault/35-Reports/` | Agent-generated reports: project status, pipeline, weekly summaries, KPI rollups | Maxine, Kyle, Sinclair, Watson, Overton, Regine, Scooter |
| `vault/40-People/` | Per-contact CRM pages | Kyle, Regine |
| `vault/50-Travel/` | Per-trip pages | Scooter |
| `vault/60-Wellness/` | PERMA-V journal, biometrics summaries | Watson |
| `vault/70-Ops/` | Bill audits, tech inventory | Overton |
| `vault/80-Journal/` | User's own journal (read-only for agents) | User only |
| `vault/90-Archive/` | Closed items | All |

Sync via `obsidian-livesync` or git-cron. The user's `80-Journal/` is read-only to agents — Watson can analyze sentiment, never edit.

## Memory Layers

1. **Hot state** — Redis. Active Work Orders, in-flight conversations.
2. **Canonical files** — `workspace/tasks/current.md`, `workspace/relationships/current.md`, `CHIEF_OF_STAFF_CONTEXT.md`. Source of truth for the things they cover.
3. **Editorial Memory** — Postgres + pgvector. Owner preferences, prior decisions, vetting outcomes, sentiment baselines. Embedded for retrieval.
4. **Vault** — Obsidian. Long-form context, briefs, journals.
5. **Audit log** — Postgres append-only. Every Work Order, every approval/rejection, every external action.

## The Flavor Bus (Inter-Agent Protocol)

NATS subjects:

- `work_order.<agent>` — Khadijah → specialist
- `report.<agent>` — specialist → Khadijah
- `flag.<severity>` — any agent → Khadijah (urgent escalation)
- `audit.*` — fanout to audit log

Message envelope (JSON):
```json
{
  "id": "wo_01J...",
  "from": "khadijah",
  "to": "sinclair",
  "type": "work_order",
  "task": "Triage VIP inbox",
  "context": {...},
  "due_by": "2026-05-03T14:00:00Z",
  "expects": "summary",
  "trace_id": "..."
}
```

## Human Interface (Khadijah-Exclusive)

The user only ever talks to Khadijah. Specialists are dark from the user's perspective — they never publish to Telegram, never send email on the user's behalf without going through Sinclair, and never appear by name in the chat unless Khadijah cites them.

- **Inbound text**: Telegram → Khadijah (normal message handling)
- **Inbound voice**: Telegram voice note → OpenAI Whisper STT → transcript becomes a normal Khadijah message. Original audio is discarded after transcription.
- **Outbound text**: Khadijah → Telegram `sendMessage`
- **Outbound voice**: Khadijah → ElevenLabs TTS → OGG/Opus → Telegram `sendVoice`. Voice ID and delivery rules in `infra/voice.yaml`.

Voice is a Khadijah-only capability. The bus enforces this — `human_interface` permissions are granted to exactly one agent.

## Security

- Khadijah is the only container exposed to the internet (via Caddy, behind auth).
- All other agents are on the private Docker network.
- Composio holds OAuth tokens — agents never see raw credentials.
- Secrets at rest are SOPS-encrypted with age (see [SECRETS.md](SECRETS.md)).
- Postgres encrypted at rest. Vault snapshotted hourly to off-VPS storage.
- HITL is enforced at the bus level: any message of `type: action_pending_approval` cannot be executed until Khadijah receives a signed `approval` from the user.

See [DEPLOYMENT.md](DEPLOYMENT.md) for the install and operate runbook, and [SECRETS.md](SECRETS.md) for the encrypted-secrets protocol.
