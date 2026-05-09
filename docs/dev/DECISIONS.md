# FlavorOS Development Decisions

## Accepted Decisions

### Five-Agent Canon

FlavorOS has five active agents:

| Agent | Runtime | Interface | Domain |
|---|---|---|---|
| Khadijah | Hermes | human-facing | briefings, orchestration, approvals, synthesis |
| Sinclair | Hermes | human-facing | impromptu requests, calendar/email, wellness, notes |
| Maxine | OpenClaw | dark specialist | operations, PM, finance coordination, execution state |
| Scooter | OpenClaw | dark specialist | travel, logistics, prep, research, readiness |
| Kyle | OpenClaw | dark specialist | CRM, relationships, follow-up, brand-social |

Retired standalone agents:

- Watson becomes wellness capability inside Sinclair.
- Regine becomes social/persona capability inside Kyle.
- Overton splits into operations/infrastructure capability inside Maxine and tech/logistics capability inside Scooter.

### Persona Packs

Regine and Overton should be preserved as persona packs. Persona packs can provide brief anecdotes, presence, framing, and latency cover during briefings. They do not own secrets, receive work orders, act externally, or appear as independent agents.

### SIGMA and Readiness Outputs

SIGMAs are created intelligence artifacts, not triggers. System events, data points, logs, and protocol results can cause agents to create SIGMAs. SIGMAs are used later by agents to improve decisions and artifact generation.

Readiness artifacts are user-facing or action-facing prepared outputs: draft messages, calendar proposals, conflict flags, receipt packets, research packets, task plans, reports, and suggested next moves.

### Client Model

Marcus is the test client. Christy is the target first client. The product must not hardcode Marcus-only assumptions. OAuth and personal preferences for Christy are pending explicit onboarding after the demo.

### Secrets

No partial key rotation. Use a full stack API protocol to collect required variables, validate templates, encrypt once, deploy once, and verify service access.

### Close-Loop Trigger

Manual close-loop trigger is `/ctl`. It means update handoff docs, regenerate the latest context snapshot, and report next actions.

If an active LLM/user development session passes 2.5 hours without a close-loop, run the close-loop protocol before starting another module or risky work.

### Context Spin-Up Trigger

Manual context spin-up trigger is `/ctx`. It means read the latest context snapshot, next actions, decisions, session log, and module backlog, then report active canon, current module, blockers, next actions, and do-not-touch notes.

`/ctx` does not regenerate the snapshot unless requested or obviously stale.

### Product IT Director Trigger

Manual Product IT Director trigger is `/itc`. It means read the latest context snapshot, project control docs, MVP docs, and dev-context docs, then report where the last session ended along with the current completed task list, next todos, blockers, and any directive drift.

`/itc` is the execution-focused startup command when the session needs immediate product and delivery control, not just a lightweight context load.

### Shared Context File

`FLAVOROS_CONTEXT.md` is the shared operating context file for agents and runtime services.

It is not a user profile. Personal preferences, private contact details, account mappings, and client-specific context should live in client envelopes, workspace files, or vault artifacts instead.

### Canonical Delivery Source

FlavorOS delivery state is canonical in git, not in a SaaS tool.

Primary control artifacts are:

- `planning/00-flavoros-mvp-delivery-system/FLAVOROS_MVP_PROJECT_PLAN.md`
- `planning/00-flavoros-mvp-delivery-system/task_map.yaml`

ClickUp and Obsidian are projections of that source for visibility and execution support. They must not become competing task authorities during MVP.

### UI UX As First-Class Scope

UI/UX is a system area, not a cleanup phase after runtime work.

Operator visibility, pending approvals, task state legibility, and demo comprehension should be planned alongside agent runtime and voice work, even if the first shipped surface is read-only.

### Ripple Architecture: Observation + Synthesis

Specialist agents (Scooter, Sinclair, Maxine, Kyle) do not mint ripple SIGMAs directly. They emit lightweight observation files into `vault/00-Inbox/ripple-observations/` whenever their work touches another person/place/project/obligation. Khadijah's `ripple-synthesis` skill aggregates those observations on a 6-hour pulse and a nightly deep pass, folds corroborating ones, scores `rank: 1-5` and `proximity: immediate|near|mid|far`, mints the formal ripple SIGMAs, and prioritizes findings for the morning brief.

Rationale: no specialist holds the cross-domain view needed to score ripples honestly. Khadijah's role as COS is the natural place for synthesis. Multiple specialists noticing the same intersection corroborates it; synthesis tracks all contributors.

### Empirical Weighting (Deferred By Design)

SIGMAs that drive option-curation workflows (planning, scheduling, vendor selection) do **not** carry numeric weights for scoring options. Instead, every option-presentation step records a `decision_log` entry: options presented, recommended, chosen, override flag, override reason, and the active `constraint_priority` at decision time.

After enough decisions accumulate (~10–20 trips), the universe-update protocol can derive observed weights and write them into the relevant long-term knowledge layer. Until then, the agent presents 2–3 ranked options and the user chooses; the recommendation is editorial, not authoritative.

`constraint_priority` is per-instance, not global: dates can outrank budget when context demands.

### Skill Triggers: Use-If Pattern

Skills must produce useful behavior at the **cron + calendar + email** baseline. Geofence, SMS, third-party APIs, and device connections are *enrichment tiers* — they refine timing and reduce prompts when present, but their absence must never block a skill from running.

Every SKILL.md should declare its trigger tiers explicitly with the fallback for each absent tier.

### SIGMAs Are Runtime-Only (Acknowledged, Deferred)

SIGMAs are produced and consumed during workflow execution. Persistent knowledge (preferences, destination intelligence, vendor intelligence, relationship tier, project state, wellness baseline) belongs in DB tables, codified preference docs, or readiness artifacts — **not** as long-term SIGMAs.

The current SIGMA type catalog includes "long-term" types (`travel-preferences`, `destination-intelligence`, `vendor-intelligence`, `relationship`, `project-state`, `wellness-baseline`) that are misnamed and will be migrated. Migration deferred to its own work block.

### Voice Brain Path

For the current MVP, use Twilio for phone transport, OpenAI STT for caller transcription, ElevenLabs for Sinclair/Khadijah spoken voices, and OpenRouter for agent text reasoning where needed.

Gemini/Gemini Live may remain in the secret schema, but it is not the active live-call path yet. Do not wire Gemini Live until the SIGMA/context policy and deferred-work path are stable, to avoid double-billing and complexity.

Sinclair is the primary live conversational lane. Khadijah is the briefing/executive synthesis lane and should not handle every improvised live response unless explicitly selected.

### Functional Workflows Become Skills Plus Protocols

The functional model should not stop at planning PRDs. Planning packages are the design source, while agent-level `SKILL.md` files and `protocols/*.protocol.md` files are the runtime operating layer.

Each baseline workflow needs:

- an owner agent,
- a mounted skill or subskill,
- a protocol with trigger, inputs, phase contract, SIGMA/readiness contract, approval gates, handoffs, failure modes, and completion signal,
- a Khadijah approval path when it can create an external commitment or sensitive action.

### Communications Unification Split

Universal communication handling is split across Sinclair, Kyle, and Khadijah.

Sinclair owns ingestion, normalization, triage, and scheduling staging. Kyle owns CRM/relationship extraction from triaged communications. Khadijah owns the HITL decision brief and routes approved execution back to Sinclair.

Canonical bus events for this layer:

- `event.inbox.triaged`
- `request.approval.khadijah`
- `execute.sinclair.calendar`
- `execute.sinclair.comms`
- `audit.approval.comms`

No external send, calendar accept/decline, counter-proposal, or external hold should execute from ingestion alone.

### User Interface Boundary

The real user-facing FlavorOS interface should not expose internal `work_orders`, queue state, or orchestration mechanics by default. Those objects are runtime/operator concerns.

The user surface should emphasize:

- what needs attention,
- what FlavorOS has prepared,
- what needs approval,
- what changed or was handled.

Work-order visibility can exist in an internal operator/admin surface later if needed, but that is not the primary user experience target.

### Current Build Focus: VPS And Agent Runtime

UI implementation is proceeding in a separate environment. Inside this repo, the near-term build focus is:

- VPS service readiness,
- agent startup reliability,
- NATS work-order/report movement,
- Postgres persistence,
- provider ingestion,
- durable artifacts and approvals.

### Hostinger Runtimes Are The Near-Term Agent Runtime

The repo-owned Python agent containers were scaffolding and should not be treated as the real FlavorOS agent architecture.

Current VPS agent runtime mapping:

- Khadijah: Hostinger Hermes `hermes-agent-kxed-hermes-agent-1`
- Sinclair: Hostinger Hermes `hermes-agent-isuk-hermes-agent-1`
- Maxine: Hostinger OpenClaw `openclaw-pn8l-openclaw-1`

The repo owns prompts, skills, protocols, shared context, support services, app/API code, and sync scripts. `docker-compose.yml` owns shared support services only and must not deploy fake Python agent containers.

Scooter and Kyle remain product agents in the canon, but they are not deployed as real Hostinger runtimes yet.

### Dee Pre-Change Guard

Before implementation, deployment, or architecture edits, Dee must run `/itc`, name directive drift, and pass `scripts/dee-prechange-check.sh`.

This guard exists because startup commands were previously treated as conversational hints instead of executable repo protocols.
