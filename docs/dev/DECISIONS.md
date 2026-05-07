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

### Voice Brain Path

For the current MVP, use Twilio for phone transport, OpenAI STT for caller transcription, ElevenLabs for Sinclair/Khadijah spoken voices, and OpenRouter for agent text reasoning where needed.

Gemini/Gemini Live may remain in the secret schema, but it is not the active live-call path yet. Do not wire Gemini Live until the SIGMA/context policy and deferred-work path are stable, to avoid double-billing and complexity.

Sinclair is the primary live conversational lane. Khadijah is the briefing/executive synthesis lane and should not handle every improvised live response unless explicitly selected.
