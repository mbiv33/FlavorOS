# FlavorOS
## "Keeping it Professional. Keeping it Flavor."

FlavorOS is a multi-agent executive operating system built around human-facing Hermes agents, specialist OpenClaw agents, and a repo-owned support layer.

Khadijah remains the primary conductor, and the owner can now work through Khadijah directly, Sinclair directly, or a shared group bot that includes both Hermes agents.

## Staff

| Agent | Title | Core Role |
|-------|-------|-----------|
| **Khadijah James** | Chief of Staff (COS) | Orchestration, briefs, approvals, synthesis, voice |
| **Maxine Shaw** | Chief Operating Officer (COO) | Projects, finance ops, business operations, renewals |
| **Sinclair James** | Executive Assistant (EA) | Inbox, calendar, meetings, wellness, voice |
| **Scooter** | Chief Logistics Officer (CLO) | Travel, logistics, IT readiness, prep packets, web research |
| **Kyle Barker** | Chief Relationship Officer (CRO) | CRM, follow-ups, networking, brand-social |

Retired as standalone agents, preserved as skillsets:

- **Watson** → wellness inside Sinclair
- **Regine** → social and brand persona inside Kyle
- **Overton** → finance/ops inside Maxine and tech/IT inside Scooter

## Repo Shape

Each active agent now owns its own prompt surface:

- `agents/<name>/SOUL.md`
- `agents/<name>/agent.yaml`
- `agents/<name>/skills/*/SKILL.md`

That keeps persona, role prompts, voice behavior, and Obsidian behavior colocated instead of split across a global `skills/` tree.

## Obsidian

Obsidian is the shared operating memory for CRM, PM, reports, travel notes, wellness notes, and archived decisions.

Every active agent has:

- an Obsidian-aware skill in its local `skills/` folder
- Obsidian plugin metadata in `agent.yaml`
- scoped write access in `infra/obsidian.yaml`

## Deployment Shape

Operational staff target:

- `khadijah`, `sinclair` = Hermes
- `maxine`, `scooter`, `kyle` = OpenClaw

Current VPS reality:

- Khadijah runs in the Hostinger Hermes container `hermes-agent-kxed-hermes-agent-1`.
- Sinclair runs in the Hostinger Hermes container `hermes-agent-isuk-hermes-agent-1`.
- Maxine runs in the Hostinger OpenClaw container `openclaw-pn8l-openclaw-1`.
- Scooter and Kyle are product agents with repo-owned prompt/skill bundles, but they are not deployed as real Hostinger runtimes yet.
- `docker-compose.yml` owns shared infrastructure and app services only. It must not deploy fake Python agent containers.

Human-facing surfaces:

- Khadijah direct
- Sinclair direct
- shared Hermes group chat

## Core Principle

The system handles identify, research, and draft. The owner handles approve, modify, or reject.

## Syncing Real Agent Runtimes

The repo owns prompts, skills, protocols, and shared context. The Hostinger containers are the current real runtimes.

Run this on the VPS to sync repo bundles into the active Hostinger data roots:

```bash
bash deploy/hostinger-agents/sync-agent-bundles.sh
```
