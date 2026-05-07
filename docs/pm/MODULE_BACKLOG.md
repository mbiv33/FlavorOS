# FlavorOS Module Backlog

## Module 0: Development Control Plane

Status: complete enough for active development.

Goal: make the work followable by humans, Codex, Claude Code, and future agents.

Artifacts:

- `docs/dev/SESSION_LOG.md`
- `docs/dev/DECISIONS.md`
- `docs/dev/NEXT_ACTIONS.md`
- `docs/prd/FLAVOROS_12_HOUR_MVP.md`
- `docs/pm/MODULE_BACKLOG.md`

Exit criteria:

- Any new session can read the latest state in under five minutes.

## Module 0.5: MVP Delivery Control Plane

Status: complete enough for active development.

Goal: make FlavorOS delivery state visible and assignable instead of prompt-local.

Artifacts:

- `planning/00-flavoros-mvp-delivery-system/FLAVOROS_MVP_PROJECT_PLAN.md`
- `planning/00-flavoros-mvp-delivery-system/task_map.yaml`
- `planning/00-flavoros-mvp-delivery-system/clickup_import.csv`
- `planning/00-flavoros-mvp-delivery-system/AGENT_WORKSTREAMS.md`
- `vault/30-Projects/FlavorOS/FlavorOS MVP Dashboard.md`
- `vault/30-Projects/FlavorOS/FlavorOS MVP Kanban.md`
- `vault/30-Projects/FlavorOS/FlavorOS MVP Tasks.md`

Exit criteria:

- Plan, task map, and vault projections reflect the same active MVP work.
- A new worker can identify the current focus tasks, owner, and blockers in under five minutes.

## Module 1: VPS Truth and Deploy Surface

Goal: know what is actually running.

Artifacts:

- `scripts/vps-inventory.sh`
- `docs/dev/VPS_INVENTORY.md`

Exit criteria:

- Current OS, Docker, containers, ports, repos, domains, reverse proxy, and service health are known.
- No secret values are printed.

## Module 2: Canonical Five-Agent Architecture

Status: complete enough for active development.

Goal: remove old deployable agent shape and preserve personality where useful.

Artifacts:

- Updated `docker-compose.yml`.
- Updated deployment docs.
- Persona packs for Regine and Overton.

Exit criteria:

- Only five active agent services remain.
- Retired personas are available as pack files, not services.

## Module 3: Stack API Protocol

Goal: load current and new provider credentials in one controlled pass.

Artifacts:

- Provider inventory.
- Secret schema.
- Validation checklist.
- Encrypted SOPS blob.
- Secrets-loader verification.

Exit criteria:

- Services can read required secret files.
- Logs show presence/health only, never values.

## Module 4: Live Voice Demo

Goal: prove live conversation, interruption handling, and voice identity.

Artifacts:

- Voice provider configuration.
- Khadijah/Sinclair briefing prompt.
- Voice endpoint or provider integration.

Exit criteria:

- User can have a natural voice conversation.
- Khadijah leads scheduled/briefing moments.
- Sinclair handles impromptu questions and notes.

Current focus:

- Replace the static policy lane with Hermes-aware routing.
- Add deferred work artifact creation.
- Verify interruption handling beyond the current DTMF clear hook.

## Module 5: Email/Calendar Workflow

Goal: prove FlavorOS is an operating system.

Artifacts:

- Email intake protocol.
- Calendar invite protocol.
- PM task protocol.
- SIGMA and readiness artifact samples.

Exit criteria:

- One inbound email generates durable intelligence and prepared work.

## Module 6: Agent Runtime And Operator Console

Goal: make delegation, specialist reports, and approval visibility real.

Artifacts:

- Normalized work-order contract
- Normalized specialist-report contract
- Durable artifact writer
- `docs/dev_context/runtime/` report set
- Operator console IA and first read-only surface

Exit criteria:

- Human-facing agents can delegate work in a stable shape and get a stable report back.
- The operator can see agent activity, pending approvals, and recent artifacts without reading raw logs.
