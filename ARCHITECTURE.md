# FlavorOS Architecture

FlavorOS is a VPS-deployed, containerized, hub-and-spoke executive OS.

Khadijah and Sinclair are the two human-facing Hermes agents. They coordinate with the three OpenClaw specialists over the internal bus.

## Active Org Chart

| Agent | Title | Runtime | Domain |
|------|------|---------|--------|
| `khadijah` | COS | hermes-agent | orchestration, briefs, approvals, voice |
| `sinclair` | EA | hermes-agent | inbox, calendar, meetings, wellness, voice |
| `maxine` | COO | openclaw | projects, finance ops, business operations |
| `scooter` | CLO | openclaw | travel, logistics, IT readiness, prep, research |
| `kyle` | CRO | openclaw | CRM, follow-ups, networking, brand-social |

Retired as standalone agents:

- `watson` absorbed into `sinclair`
- `regine` preserved as Kyle's internal social persona layer
- `overton` split across `maxine` and `scooter`

## Folder Architecture

```text
agents/
├── khadijah/
│   ├── SOUL.md
│   ├── agent.yaml
│   └── skills/
│       ├── chief-of-staff/
│       ├── khadijah-voice/
│       └── obsidian-chief-of-staff/
├── maxine/
│   ├── SOUL.md
│   ├── agent.yaml
│   └── skills/
│       ├── daily-task-manager/
│       ├── daily-task-prep/
│       ├── financial-management/
│       ├── infrastructure-ops/
│       └── obsidian-operations/
├── sinclair/
│   ├── SOUL.md
│   ├── agent.yaml
│   └── skills/
│       ├── executive-assistant/
│       ├── wellness/
│       ├── sinclair-voice/
│       └── obsidian-executive-assistant/
├── scooter/
│   ├── SOUL.md
│   ├── agent.yaml
│   └── skills/
│       ├── travel-logistics/
│       ├── tech-ops/
│       ├── briefing-coordination/
│       ├── web-research/
│       ├── logistics-research/
│       └── obsidian-logistics/
├── kyle/
│   ├── SOUL.md
│   ├── agent.yaml
│   └── skills/
│       ├── relationship-manager/
│       ├── brand-social/
│       └── obsidian-relationships/
├── CHIEF_OF_STAFF_CONTEXT.md
└── global_project.yaml
```

## Container Topology

Five agent containers plus shared infra:

- `khadijah`
- `maxine`
- `sinclair`
- `scooter`
- `kyle`
- `nats`
- `redis`
- `postgres`
- `openrouter-proxy`
- `secrets-loader`
- `scheduler`
- `vault-sync`

## Bus Model

- `work_order.<agent>` — Khadijah dispatches specialist work
- `report.<agent>` — specialists report back to Khadijah
- `flag.<severity>` — urgent escalation
- `audit.*` — audit fanout

## Obsidian

The Obsidian vault is shared institutional memory.

Primary active folders:

- `10-Briefs` — Khadijah
- `20-Meetings` — Sinclair, Maxine, Scooter
- `30-Projects` — Maxine
- `35-Reports` — Maxine, Sinclair, Scooter, Kyle
- `40-People` — Kyle
- `50-Travel` — Scooter
- `60-Wellness` — Sinclair
- `70-Ops` — Maxine, Scooter
- `80-Journal` — read-only for Sinclair
- `90-Archive` — all active agents

Each active agent has both:

- a role-specific Obsidian skill in `agents/<name>/skills/`
- Obsidian plugin metadata in `agents/<name>/agent.yaml`

Sinclair and Khadijah also have direct voice surfaces.

## Prompt Assembly

Each agent runtime loads:

1. `SOUL.md`
2. `CHIEF_OF_STAFF_CONTEXT.md` when configured
3. all mounted local skills under `/skills/*/SKILL.md`
4. vault and HITL constraints from `agent.yaml`

This keeps persona and role behavior local to each active agent.
