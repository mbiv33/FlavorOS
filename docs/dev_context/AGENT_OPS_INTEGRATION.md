# Agent Ops Integration

Generated for the FlavorOS 12-hour MVP on 2026-05-07.

This file is the operational map for the five-agent system. It defines ownership, required skills, NATS message contracts, vault routing, and the MVP path from live voice to durable artifacts.

## Prime Directive

FlavorOS must demo as an executive operating system, not a chatbot.

The minimum proof:

1. Marcus speaks to the live voice surface.
2. Sinclair or Khadijah responds naturally.
3. Unknown or work-heavy requests become durable readiness artifacts.
4. A specialist receives a work order over NATS.
5. A specialist report returns to the human-facing lane.
6. One email/calendar flow creates a SIGMA, draft reply, calendar artifact, PM/task artifact, and visible follow-up.

## Active Canon

Only these five agents are active:

| Agent | Role | Runtime | Interface | Primary domain |
| --- | --- | --- | --- | --- |
| `khadijah` | Chief of Staff | `hermes-agent` | Human-facing | briefings, orchestration, approvals, synthesis |
| `sinclair` | Executive Assistant | `hermes-agent` | Human-facing | inbox, calendar, meetings, wellness, notes, live impromptu voice |
| `maxine` | Chief Operating Officer | `openclaw` | Dark specialist | projects, finance ops, business operations, PM artifacts |
| `scooter` | Chief Logistics Officer | `openclaw` | Dark specialist | travel, logistics, technical readiness, prep, research |
| `kyle` | Chief Relationship Officer | `openclaw` | Dark specialist | CRM, relationships, follow-up, brand-social |

Retired identities:

- Watson is a Sinclair wellness capability, not a service.
- Regine is a Kyle persona/capability pack, not a service.
- Overton is split into Maxine operations and Scooter technical/logistics capability, not a service.

## Communication Rules

Human-facing:

- Khadijah and Sinclair can speak directly to the user.
- Khadijah owns decisions, approvals, synthesis, and briefing framing.
- Sinclair owns live impromptu support, inbox/calendar, meeting prep, notes, and wellness.

Dark specialists:

- Maxine, Scooter, and Kyle never speak directly to the user.
- They receive structured work orders.
- They return structured reports.
- Khadijah or Sinclair translates specialist output into user-facing language.

Approval-gated actions:

- Money movement
- Invoice disputes
- Contract/legal terms
- Travel bookings
- External email send
- External text send
- Calendar commitments that block external time
- Sensitive relationship moves
- Public statements or posts

## NATS Bus Contract

Current subjects:

```text
work_order.<agent>
report.<agent>
flag.<severity>
audit.*
health.*
```

Current expected agent subscriptions:

| Agent | Subscribes | Publishes |
| --- | --- | --- |
| `khadijah` | `report.*`, `health.*`, `flag.*` | `work_order.*`, `flag.*`, `audit.*` |
| `sinclair` | `work_order.sinclair` | `report.sinclair`, `flag.*` |
| `maxine` | `work_order.maxine` | `report.maxine`, `flag.*` |
| `scooter` | `work_order.scooter` | `report.scooter`, `flag.*` |
| `kyle` | `work_order.kyle` | `report.kyle`, `flag.*` |

MVP standard work order:

```json
{
  "work_order_id": "wo_2026_05_07_001",
  "source": "voice-gateway",
  "requested_by": "Marcus",
  "front_agent": "sinclair",
  "target_agent": "scooter",
  "skill": "web-research",
  "task_type": "research_brief",
  "user_request": "Find the missing API docs for Twilio interruption handling.",
  "context_summary": "User is in a live MVP build session. Need implementation-ready notes, not broad research.",
  "deliverable": "Short implementation brief with source links and code-impact notes.",
  "vault_path": "15-Readiness/",
  "priority": "normal",
  "requires_approval": false,
  "call_sid": "CA...",
  "created_at": "2026-05-07T12:00:00-04:00"
}
```

Compatibility payload for current `infra/agent-base/agent.py`:

```json
{
  "id": "wo_2026_05_07_001",
  "agent": "scooter",
  "skill": "web-research",
  "args": {
    "task_type": "research_brief",
    "user_request": "Find the missing API docs for Twilio interruption handling.",
    "context_summary": "Need implementation-ready notes with source links.",
    "deliverable": "Short implementation brief.",
    "vault_path": "15-Readiness/",
    "requires_approval": false
  },
  "fired_at": "2026-05-07T16:00:00Z"
}
```

MVP standard report:

```json
{
  "work_order_id": "wo_2026_05_07_001",
  "agent": "scooter",
  "skill": "web-research",
  "status": "complete",
  "summary": "Twilio interruption is handled by sending clear messages and tracking returned mark events.",
  "vault_file": "15-Readiness/twilio-interruption-wo_2026_05_07_001.md",
  "user_facing_response": "I found the interruption pattern and put the implementation notes in the readiness folder.",
  "requires_approval": false,
  "completed_at": "2026-05-07T12:20:00-04:00"
}
```

Current runtime report shape:

```json
{
  "agent": "scooter",
  "skill": "web-research",
  "order_id": "wo_2026_05_07_001",
  "content": "..."
}
```

Launch note:

- Keep compatibility with the current shape until application code is updated.
- The next code pass should normalize report payloads to include `work_order_id`, `status`, `summary`, `vault_file`, and `user_facing_response`.

## Routing Logic

Default routing:

```text
executive / approval / decision / unclear -> khadijah
inbox / calendar / meeting / wellness / live note -> sinclair
operations / finance / PM / execution state -> maxine
travel / logistics / research / technical readiness -> scooter
relationships / CRM / brand-social / follow-up -> kyle
```

Voice handling:

```text
live phone call
  -> Sinclair by default
  -> Khadijah when briefing mode, approval, or executive synthesis is requested
  -> if answer is in context, answer briefly
  -> if not, create readiness artifact
  -> publish specialist work order when useful
  -> speak deferral plus next step
```

Email/calendar demo handling:

```text
sample inbound email
  -> Sinclair extracts request and urgency
  -> create SIGMA for durable intelligence
  -> create draft reply artifact
  -> create calendar handling artifact
  -> delegate PM/task artifact to Maxine when execution is required
  -> delegate relationship context to Kyle when people/follow-up matter
  -> Khadijah summarizes final update
```

## Khadijah

Role:

- Chief of Staff.
- Primary executive orchestrator.
- Owns approvals, high-level synthesis, briefings, and final user-facing framing.

Runtime:

- `hermes-agent`

Mounted skills:

- `chief-of-staff`
- `khadijah-voice`
- `obsidian-chief-of-staff`

Model config:

- Primary: `anthropic/claude-sonnet-4.6`
- Endpoint: `${OPENROUTER_BASE_URL}`

Vault read/write:

- Reads all vault content.
- Writes:
  - `00-Inbox/**`
  - `05-SIGMA/**`
  - `10-Briefs/**`
  - `15-Readiness/**`
  - `35-Reports/**`
  - `90-Archive/**`

Bus:

- Publishes:
  - `work_order.*`
  - `flag.*`
  - `audit.*`
- Subscribes:
  - `report.*`
  - `health.*`
  - `flag.*`

Required behavior:

- Convert ambiguous user requests into clear owner/work-order decisions.
- Require approval for all sensitive external actions.
- Synthesize specialist reports into brief, executive-quality updates.
- Create or finalize SIGMAs when new intelligence is learned.
- Create readiness artifacts when follow-up work is promised.

MVP tasks:

- Present one briefing-style exchange.
- Summarize the state of the voice demo and email/calendar flow.
- Receive at least one specialist report and turn it into a user-facing follow-up.

## Sinclair

Role:

- Executive Assistant.
- Primary live impromptu lane.
- Owns inbox, calendar, meeting prep, notes, and wellness context.

Runtime:

- `hermes-agent`

Mounted skills:

- `executive-assistant`
- `wellness`
- `sinclair-voice`
- `obsidian-executive-assistant`

Model profiles:

- `thinking`: `anthropic/claude-sonnet-4.6`
- `fast`: `openai/gpt-5.4-mini`

Key routing rules:

- Inbox sweep, label, archive, vitals, and calendar load checks use `fast`.
- High-stakes email drafts, schedule decisions, and meeting prep use `thinking`.

Vault read/write:

- Reads all vault content.
- Writes:
  - `05-SIGMA/**`
  - `15-Readiness/**`
  - `20-Meetings/**`
  - `35-Reports/**`
  - `60-Wellness/**`

Bus:

- Subscribes:
  - `work_order.sinclair`
- Publishes:
  - `report.sinclair`
  - `flag.*`

HITL:

- Always drafts for approval:
  - `send_email`
  - `accept_meeting_external`
  - `reschedule_external`
- Can act autonomously on low-risk mailbox hygiene:
  - archive
  - label
  - mark read
  - accept recurring
  - decline obvious spam

Required behavior:

- Keep live voice answers short and useful.
- Take notes into durable artifacts.
- For unknowns, defer cleanly and publish work orders.
- For email/calendar flow, create draft artifacts and never send externally without approval.

MVP tasks:

- Default voice lane.
- Process one sample inbound email.
- Create SIGMA, draft reply, and calendar handling artifact.
- Route PM/task follow-up to Maxine when needed.

## Maxine

Role:

- Chief Operating Officer.
- Dark specialist for operations, finance ops, PM, execution state, and business coordination.

Runtime:

- `openclaw`

Mounted skills:

- `daily-task-manager`
- `daily-task-prep`
- `financial-management`
- `infrastructure-ops`
- `obsidian-operations`

Model profiles:

- `thinking`: `anthropic/claude-sonnet-4.6`
- `report`: `openai/gpt-5.4-mini`

Key routing:

- Reports and task prep use `report`.
- Risk, prioritization, finance, subscriptions, and project status use `thinking`.

Vault read/write:

- Reads all vault content.
- Writes:
  - `05-SIGMA/**`
  - `15-Readiness/**`
  - `20-Meetings/**`
  - `30-Projects/**`
  - `35-Reports/**`
  - `70-Ops/**`

Bus:

- Subscribes:
  - `work_order.maxine`
- Publishes:
  - `report.maxine`
  - `flag.*`

Escalates:

- Any payment
- Invoice disputes
- Contract terms
- New subscription commitments

Required behavior:

- Turn vague execution needs into PM/task artifacts.
- Track risk, owner, deadline, next action, and dependency.
- Produce reports with vault file paths and approval requirements.

MVP tasks:

- Create PM/task artifact for the sample email/calendar flow.
- Optionally monitor CI/CD and syntax checks during development if temporarily retasked.

## Scooter

Role:

- Chief Logistics Officer.
- Dark specialist for travel, logistics, technical readiness, prep, research, and web research.

Runtime:

- `openclaw`

Mounted skills:

- `travel-logistics`
- `tech-ops`
- `briefing-coordination`
- `web-research`
- `logistics-research`
- `obsidian-logistics`

Model profiles:

- `thinking`: `anthropic/claude-sonnet-4.6`
- `fast`: `openai/gpt-5.4-mini`

Key routing:

- High-stakes or multi-constraint travel, tech, briefing, research, and logistics use `thinking`.
- Simpler research or prep uses `fast`.

Vault read/write:

- Reads all vault content.
- Writes:
  - `05-SIGMA/**`
  - `15-Readiness/**`
  - `20-Meetings/**`
  - `35-Reports/**`
  - `50-Travel/**`
  - `70-Ops/**`

Bus:

- Subscribes:
  - `work_order.scooter`
- Publishes:
  - `report.scooter`
  - `flag.*`

Required behavior:

- Produce options, readiness checks, implementation notes, and prep briefs.
- Never book travel without approval.
- Return concise options and clear recommendation logic.

MVP tasks:

- Support missing API research or Twilio/voice readiness.
- Create readiness artifacts when live voice defers a technical/logistics question.

## Kyle

Role:

- Chief Relationship Officer.
- Dark specialist for CRM, relationship maintenance, follow-ups, and brand-social context.

Runtime:

- `openclaw`

Mounted skills:

- `relationship-manager`
- `brand-social`
- `obsidian-relationships`

Model profiles:

- `thinking`: `anthropic/claude-sonnet-4.6`
- `fast`: `openai/gpt-5.4-mini`

Vault read/write:

- Reads all vault content.
- Writes:
  - `05-SIGMA/**`
  - `15-Readiness/**`
  - `35-Reports/**`
  - `40-People/**`

Bus:

- Subscribes:
  - `work_order.kyle`
- Publishes:
  - `report.kyle`
  - `flag.*`

Escalates:

- Public statements
- Partnership terms
- Contract terms
- Sensitive relationship moves

Required behavior:

- Maintain people context and follow-up state.
- Draft relationship-sensitive language, never send it directly.
- Use Regine persona pack only as internal flavor/presence, not as a standalone agent.

MVP tasks:

- If the sample email involves relationship context, produce a contact/follow-up readiness artifact.
- Otherwise stay dark until needed.

## Vault Artifact Contract

Every work-producing flow should create one or more of:

- SIGMA: durable intelligence
- Readiness artifact: prepared action/output
- Agent report: specialist result
- Brief: executive summary
- PM/task artifact: execution plan

Minimum front matter:

```yaml
---
id: sigma_or_artifact_id
created_at: 2026-05-07T12:00:00-04:00
source: voice-gateway
requested_by: Marcus
front_agent: sinclair
owner_agent: maxine
work_order_id: wo_2026_05_07_001
status: draft
requires_approval: true
---
```

Readiness artifact body:

```markdown
# Title

## User Request

## Context Used

## Prepared Output

## Risks And Approval Gates

## Next Action

## Links
```

## MVP Launch Flow

Phase 1: voice context path

- Replace canned policy with a context loader.
- Check prepared context in `vault/05-SIGMA`, `vault/10-Briefs`, and `vault/15-Readiness`.
- Answer if confidence is high.
- Otherwise create readiness artifact and publish work order.

Phase 2: deferred work path

- Work order goes to Maxine, Scooter, or Kyle.
- Specialist creates or updates vault artifact.
- Specialist publishes report.
- Khadijah or Sinclair sends visible follow-up.

Phase 3: email/calendar proof

- Sinclair reads one sample inbound email.
- Sinclair creates SIGMA and draft reply.
- Sinclair creates calendar handling artifact.
- Maxine creates PM/task artifact.
- Khadijah summarizes final state.

## Implementation Notes For Next Code Pass

Make these changes before broadening provider scope:

- Add `infra/voice-gateway/app/context_policy.py`.
- Add `infra/voice-gateway/app/artifacts.py`.
- Add `infra/voice-gateway/app/bus.py`.
- Normalize work order payloads while preserving compatibility with `infra/agent-base/agent.py`.
- Add a small artifact index in Postgres or JSON fallback.
- Add no-secret audit logs for provider calls and NATS publications.

Do not start:

- Full web UI.
- Full Christy onboarding.
- Autonomous external sends.
- Full travel booking automation.
- Gemini Live unless current STT/TTS path fails demo needs.
