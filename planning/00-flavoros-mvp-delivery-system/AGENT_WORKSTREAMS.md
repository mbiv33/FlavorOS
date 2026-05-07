# FlavorOS Agent Workstreams

Date: 2026-05-07

## Principle

Agents should be assigned concrete work with an output path. Do not start an agent because it is available. Start it because it has a task, a context packet, an owner, and a report destination.

## Product Agents

### Khadijah

Role: product orchestrator and decision gate.

Immediate responsibilities:

- Keep the MVP prime directive visible.
- Decide whether a request needs Sinclair, Maxine, Scooter, Kyle, or local Codex.
- Preserve UI/UX as a first-class product surface.
- Convert specialist reports into user-facing updates.
- Halt work that risks secrets, external sends, bookings, money movement, or client commitments.

### Sinclair

Role: live voice and email/calendar experience owner.

Immediate responsibilities:

- Own the impromptu voice lane.
- Drive the email/calendar demo flow.
- Create draft artifacts, not external sends.
- Maintain meeting and calendar artifact quality.

### Maxine

Role: delivery manager and PM artifact owner.

Immediate responsibilities:

- Maintain `task_map.yaml`.
- Keep ClickUp and Obsidian projections aligned.
- Create PM/task artifacts for demo flows.
- Track blockers, dependencies, and release readiness.

### Scooter

Role: technical readiness, provider research, endpoint testing, and deployment support.

Immediate responsibilities:

- Stand up dev-agent report paths.
- Own provider/API research queue.
- Coordinate endpoint tests with fake data.
- Own VPS and Cloudflare deployment readiness.

### Kyle

Role: CRM and relationship intelligence.

Immediate responsibilities:

- Join email/calendar demo work when people, follow-up, or relationship context matters.
- Produce relationship-aware follow-up artifacts.
- Keep public or sensitive relationship moves approval-gated.

## Temporary VPS Dev Agents

These are not product agents and must not contaminate the five-agent canon.

### Dev Agent 1: Logwatch and Syntax

Output:

- `docs/dev_context/runtime/agent1-logwatch.md`

Allowed:

- Docker compose service status.
- Safe logs.
- Syntax checks.
- Secrets readiness by presence only.

Blocked:

- Secret values.
- External actions.
- Production data modification.

### Dev Agent 2: Provider Research

Output:

- `docs/dev_context/runtime/agent2-provider-research.md`

Allowed:

- Official docs research.
- API shape summaries.
- Rate-limit and retry notes.
- Code-impact recommendations.

Priority queue:

1. Twilio interruption clear/mark handling.
2. ElevenLabs lowest-latency Twilio output path.
3. OpenRouter metadata, retries, and fallback.
4. Gmail minimal scopes for read, draft, and label without send.
5. Calendar proposal/hold strategy without notifications.
6. Obsidian Git conflict strategy.

### Dev Agent 3: Endpoint Test Client

Output:

- `docs/dev_context/runtime/agent3-endpoint-tests.md`

Allowed:

- Health endpoint checks.
- TwiML shape checks.
- Synthetic NATS work orders with fake data.
- Report loop tests.

Blocked:

- Real phone numbers.
- Real emails.
- Real calendar data.
- Raw secrets.

## Agent Work Order Definition of Ready

A work order is ready when it has:

- `work_order_id`
- target agent
- task type
- context summary
- deliverable
- artifact path
- priority
- approval risk
- verification request

## Agent Report Definition of Done

A report is done when it includes:

- status
- summary
- actions taken
- artifact path
- blockers
- recommended next action
- user-facing response
- approval requirement

