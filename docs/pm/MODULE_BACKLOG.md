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

Status: architecture defined; runtime wiring pending.

Goal: prove FlavorOS is an operating system.

Artifacts:

- Communications Unification Protocol.
- Universal inbox ingestion skill.
- Universal calendar sync skill.
- Comms CRM extraction skill.
- Comms approval orchestration skill.
- Readiness templates for inbox triage, pending scheduling, deferred follow-ups, and decision brief.
- SIGMA and readiness artifact samples.

Exit criteria:

- One inbound email generates durable intelligence and prepared work.

Current focus:

- Connect test email read path.
- Connect test calendar read/proposal path.
- Use `vault/15-Readiness/universal-inbox-triage.md` and `vault/20-Meetings/pending-scheduling.md` as the first artifact targets.

## Module 7: SIGMA Tooling and Travel Skill Family

Status: in-progress.

Goal: codify SIGMA lifecycle as runnable tooling, then build Scooter's complete travel workflow as defined in `planning/FLAVOR WORKFLOW.pdf`.

Artifacts:

- `docs/architecture/SIGMA_SPEC.md`
- `scripts/sigma/` (full toolchain)
- `vault/05-SIGMA/_templates/` (5 new SIGMA templates)
- `vault/15-Readiness/_templates/` (8 new readiness templates)
- `vault/00-Inbox/ripple-observations/` (observation queue)
- `agents/scooter/skills/` (8 new skills)
- `agents/khadijah/skills/ripple-synthesis/`
- `cron/schedules.yaml` (9 new entries)

Exit criteria:

- All 11 protocols from the FLAVOR Travel Workflow PDF exist as runnable skills.
- A trip can be scaffolded, planned, booked, prepped, lived, returned, debriefed, and closed end-to-end (any phase failure is auditable).
- Ripple observation/synthesis loop produces ranked, prioritized findings consumable by the morning brief.

Architectural debt to clear in a follow-up:

- Migrate "long-term" SIGMA types to DB/codified-doc form (SIGMAs are runtime-only).
- Decide cross-agent shared-skill strategy and propagate `ripple-observation` to Sinclair, Maxine, Kyle.

## Module 6: Agent Runtime And Operator Console

Status: active, corrected around Hostinger-managed runtimes.

Goal: make delegation, specialist reports, and approval visibility real.

Artifacts:

- Hostinger agent bundle sync path for Khadijah, Sinclair, and Maxine
- Normalized work-order contract
- Normalized specialist-report contract
- Durable artifact writer
- `docs/dev_context/runtime/` report set
- Operator console IA and first read-only surface

Exit criteria:

- Repo-owned compose runs shared infrastructure and app/API services only, not fake Python agent containers.
- Khadijah, Sinclair, and Maxine Hostinger runtimes receive current repo prompts, skills, protocols, and context bundles.
- Human-facing agents can delegate work in a stable shape and get a stable report back.
- The operator can see agent activity, pending approvals, and recent artifacts without reading raw logs.

Current focus:

- Sync Khadijah to `hermes-agent-kxed`, Sinclair to `hermes-agent-isuk`, and Maxine to `openclaw-pn8l`.
- Bring up only repo-owned support services on the VPS.
- Align new UI/PRD behavior with agent skills before adding more runtimes.

## Module 8: Functional Model Skills And Protocols

Status: documentation and agent architecture layer complete; runtime implementation pending.

Goal: turn the FlavorOS functional model into agent-operable skills and protocols.

Artifacts:

- `planning/FUNCTIONAL_WORKFLOW_BASELINE.md`
- `planning/04-*` through `planning/13-*`
- `agents/FUNCTIONAL_MODEL_SKILL_PROTOCOL_MAP.md`
- `agents/PROTOCOL_DRAFTING_STANDARD.md`
- `agents/*/protocols/`
- agent-level skills for Sinclair, Kyle, Maxine, and Khadijah

Exit criteria:

- Every baseline workflow has an owning agent, skill, protocol, approval rule, and durable artifact contract.
- Runtime work orders can invoke these skills and produce the expected readiness artifacts.

Current focus:

- Implement normalized work order/report contracts.
- Implement durable artifact writer.
- Wire communications unification to real email/calendar connectors.
