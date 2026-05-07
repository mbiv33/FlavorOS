# FlavorOS MVP and Beyond Project Plan

Date: 2026-05-07
Owner: Khadijah for product orchestration, Maxine for delivery management
Canonical companion: `task_map.yaml`

## Prime Directive

Ship FlavorOS as a voice-first, multi-agent executive operating system. The MVP must prove a real operating loop:

1. Marcus enters a live voice or text surface.
2. Sinclair or Khadijah responds naturally and knows when to defer.
3. Work-heavy requests become structured work orders.
4. Dark specialists produce durable reports and artifacts.
5. At least one email/calendar flow creates a SIGMA, draft reply, calendar artifact, PM/task artifact, and visible follow-up update.
6. The system is observable through repo docs, Obsidian, and optionally ClickUp.

## Current Reality

What exists:

- Five-agent canon is established.
- VPS deployment shape exists.
- Twilio voice gateway skeleton is live and has confirmed media-stream connectivity.
- ElevenLabs and OpenAI STT have been tested in the phone loop.
- NATS, Redis, Postgres, OpenRouter proxy, secrets-loader, scheduler, and vault sync are represented in compose.
- Planning docs, provider docs, and session protocols exist.
- Temporary VPS dev-agent retasking has already been defined.

Missing or under-modeled:

- UI/UX is not represented as a first-class product surface.
- Agent work orders and reports are not normalized end to end.
- The live voice path still uses a simple policy response instead of full context-aware routing.
- Email/calendar demo flow is not connected.
- The operator dashboard/approval surface is not designed.
- ClickUp and Obsidian visibility are not wired to the project plan.
- Agents are not yet running as an autonomous development crew.

## Delivery Strategy

Prioritize getting agents useful first, because they can create leverage while the broader system is refined.

### Phase 0: Delivery Control Plane

Target: 2026-05-07 to 2026-05-08

Outcomes:

- Canonical project plan and YAML task map exist.
- ClickUp import CSV exists.
- Obsidian dashboard and Kanban board exist.
- `/qq` audit log exists.
- Khadijah and Maxine have delivery-control skills.
- Every new session checks the project map before diving into isolated implementation.

### Phase 1: Agent Runtime and Dev-Agent Leverage

Target: 2026-05-08 to 2026-05-09

Outcomes:

- Product agents can receive normalized work orders and return normalized reports.
- Temporary VPS dev agents are assigned bounded missions:
  - Agent 1: logwatch and syntax checks.
  - Agent 2: provider/API research.
  - Agent 3: endpoint testing client.
- Dev-agent reports land in `docs/dev_context/runtime/`.
- Khadijah or Maxine can turn reports into next actions.

### Phase 2: Voice Demo Completion

Target: 2026-05-08 to 2026-05-10

Outcomes:

- Voice gateway calls a Hermes-aware reasoning path instead of only static policy.
- Context-aware response policy can answer from prepared context, ask one clarifying question, or defer into a work order.
- Readiness artifact creation works from live calls.
- Interruption/barge-in behavior is tested beyond the current DTMF clear hook.
- Khadijah briefing mode and Sinclair impromptu mode are both demonstrable.

### Phase 3: Email/Calendar Operating Loop

Target: 2026-05-09 to 2026-05-11

Outcomes:

- Marcus test email/calendar account path is connected safely.
- One inbound email can be processed into:
  - SIGMA
  - draft reply
  - calendar handling artifact
  - PM/task artifact
  - visible follow-up update
- External sends and calendar commitments remain approval-gated.

### Phase 4: UI/UX and Operator Visibility

Target: 2026-05-09 to 2026-05-13

Outcomes:

- UI/UX is modeled as a system layer.
- MVP operator console design exists.
- Cloudflare free Workers/Pages path is chosen for a lightweight read-only or approval-first dashboard.
- The first UI surface shows:
  - agent status
  - active work orders
  - recent reports
  - pending approvals
  - demo script/briefing state
- Obsidian and ClickUp views match the same task map.

### Phase 5: Deployable Beta

Target: 2026-05-12 to 2026-05-17

Outcomes:

- VPS deploy process is repeatable.
- Secrets are validated without printing values.
- Minimal monitoring and rollback steps exist.
- Christy onboarding is prepared as a consented beta path.
- Client-specific preferences stay out of shared runtime canon.

### Phase 6: Beyond MVP

Target: after 2026-05-17

Outcomes:

- Multi-client OAuth and account grants mature.
- Durable Postgres schema is formalized for work orders, reports, artifacts, provider events, and approvals.
- Agent dashboard moves from read-only to interactive approval workflow.
- Cloudflare Workers handles edge UI, webhook helpers, or lightweight routing where free tier is sufficient.
- ClickUp sync becomes automated only after the repo-native task map is stable.

## Workstreams

### A. Delivery Control Plane

Purpose: prevent prompt-isolated execution.

Owner: Maxine

Key outputs:

- Project plan
- Task map
- ClickUp import
- Obsidian dashboard
- Session guardrails

Definition of done:

- A new agent or Codex session can identify the current goal, next work, blockers, and owner in under five minutes.

### B. Agent Runtime

Purpose: make the five-agent system real and useful.

Owner: Khadijah

Key outputs:

- Normalized work-order schema
- Normalized report schema
- Runtime adapter changes
- Dev-agent reports
- Agent status visibility

Definition of done:

- A human-facing agent can delegate to a dark specialist, receive a report, write a vault artifact, and summarize the result.

### C. Voice Experience

Purpose: make the demo feel like an executive OS, not a phone bot.

Owner: Sinclair for impromptu voice, Khadijah for briefing voice

Key outputs:

- Live response policy
- Context lookup
- Deferred work path
- Barge-in handling
- Briefing script

Definition of done:

- Marcus can call, ask a real request, receive a concise response, and see a follow-up artifact after the call.

### D. Email and Calendar Loop

Purpose: prove operating-system behavior.

Owner: Sinclair, with Maxine and Kyle support

Key outputs:

- Gmail/Calendar account path
- Inbound email parser
- Draft reply artifact
- Calendar proposal artifact
- PM task artifact
- Follow-up update

Definition of done:

- One controlled email/calendar demo flow produces all five MVP artifacts without external sends.

### E. UI/UX and Operator Console

Purpose: make FlavorOS legible to humans.

Owner: Product direction through Khadijah, implementation through a future frontend task owner

Key outputs:

- UX map
- Operator console IA
- Pending approvals view
- Agent activity view
- Cloudflare free-tier deployment path

Definition of done:

- A non-technical user can understand what the agents are doing, what needs approval, and what has been prepared.

### F. Deployment and Operations

Purpose: keep the product shippable.

Owner: Scooter for tech readiness, Maxine for release coordination

Key outputs:

- VPS health checklist
- Docker compose verification
- Secrets health without values
- Release checklist
- Rollback plan

Definition of done:

- The MVP can be restarted, verified, and demonstrated from documented steps.

## Agent-First Priority

The next highest leverage move is to make agents useful while planning continues.

Immediate assignments:

- Khadijah: own the product plan and delegation gate.
- Maxine: own task map, ClickUp/Obsidian projections, and PM artifact generation.
- Scooter: own provider research, endpoint testing coordination, and VPS readiness.
- Sinclair: own voice and email/calendar demo experience.
- Kyle: join when demo email or calendar context includes relationship follow-up.
- VPS Dev Agent 1: watch logs and run safe syntax/config checks.
- VPS Dev Agent 2: research official provider docs and implementation details.
- VPS Dev Agent 3: run synthetic endpoint tests with fake data.

## UI/UX Product Surfaces

FlavorOS has these user-facing or operator-facing surfaces:

- Live phone call: Sinclair/Khadijah voice.
- Text bot or group channel: fast command and follow-up surface.
- Obsidian vault: durable intelligence and project memory.
- Operator console: agent status, work orders, reports, approvals, and demo state.
- ClickUp: optional execution view for task management.
- Email/calendar artifacts: draft replies, calendar proposals, and meeting prep.
- Client onboarding view: later beta path for Christy.

The MVP does not need a full marketing site. It does need a coherent operator experience.

## Cloudflare Free-Tier Role

Use Cloudflare only where it reduces deployment burden:

- Static or Workers-hosted operator console.
- Read-only status dashboard pulling sanitized JSON from VPS or checked-in artifacts.
- Lightweight webhook/proxy helpers if they simplify public ingress.
- DNS and TLS support.

Do not move the core agent runtime to Cloudflare before MVP.

## ClickUp and Obsidian Projection

ClickUp is for execution visibility and assignment.

Obsidian is for durable context, dashboards, and reasoning artifacts.

Repo YAML remains canonical until automated sync exists.

## Quality Gates

Before a task is considered done:

- It advances one named workstream.
- It has a clear acceptance criterion.
- It has no secret leakage.
- It respects approval boundaries.
- It is reflected in the task map if it changes delivery state.
- It has the smallest useful verification for shipping risk.

