# FlavorOS Context

This file is the shared operating context for the FlavorOS runtime.

It is not a user profile and it must not become a dumping ground for personal preferences, private account details, or client-specific state. Client context belongs in `clients/`, `workspace/`, and vault artifacts such as `05-SIGMA`, `15-Readiness`, `20-Meetings`, `35-Reports`, and `40-People`.

## System Identity

- Product: FlavorOS
- Category: voice-first, multi-agent executive operating system
- Deployment model: VPS-hosted support services plus Hostinger-managed Hermes/OpenClaw agent runtimes
- Current mission: ship the 12-hour MVP as fast as possible without breaking secrets or architecture canon

## Active Canon

- Five product agents only: `khadijah`, `sinclair`, `maxine`, `scooter`, `kyle`
- Khadijah and Sinclair are the only human-facing agents
- Maxine, Scooter, and Kyle are dark specialists
- Current deployed real runtimes are Khadijah, Sinclair, and Maxine only
- Regine, Watson, and Overton are persona/capability packs, not deployable agents
- Every meaningful workflow should produce durable intelligence and prepared work product

## Runtime Topology

- Human-facing runtime class: Hostinger Hermes
- Specialist runtime class: Hostinger OpenClaw
- Bus: NATS
- Hot state: Redis
- Durable state and audit: Postgres
- Durable artifacts: Obsidian-style vault markdown under `vault/`
- Secret distribution: `secrets-loader` to `/run/flavor/secrets`
- Model routing: `openrouter-proxy`
- Live voice edge: `voice-gateway`
- Repo-owned Python agent containers are stale scaffolding and must not be redeployed as the real agents

## Command Protocol

- `/ctx`: load current session context from handoff docs and workspace state
- `/itc`: activate Product IT Director mode, resume from the last stopping point, and generate the current completed/next todo list
- `/ctl`: close the loop, update handoff docs, verify directive consistency, and regenerate the latest snapshot
- before changes: run `/itc`, then `bash scripts/dee-prechange-check.sh --ack`, then `bash scripts/dee-prechange-check.sh`

## Routing Model

- Khadijah owns decisions, executive framing, approvals, and synthesis
- Sinclair owns inbox, calendar, meetings, notes, wellness, and default live voice
- Maxine owns PM, ops, finance coordination, and execution state
- Scooter owns travel, logistics, readiness, technical research, and prep
- Kyle owns CRM, relationships, follow-up, and brand-social context

If a request is unclear, high-stakes, cross-functional, or approval-heavy, route through Khadijah first.

## MVP Operating Rules

- Build only what moves the 12-hour MVP forward
- Use the current live path: Twilio transport, OpenAI STT, ElevenLabs voice, OpenRouter reasoning
- Keep live voice responses short
- If the answer is not ready in prepared context, defer cleanly
- Unknowns should become readiness artifacts and, when useful, specialist work orders
- At least one email/calendar flow must create a SIGMA, draft reply, calendar artifact, PM/task artifact, and a visible follow-up update

## Artifact Contract

Primary durable outputs:

- `vault/05-SIGMA/`: durable intelligence artifacts
- `vault/10-Briefs/`: executive briefings and synthesis
- `vault/15-Readiness/`: prepared actions, proposals, and deferred work
- `vault/20-Meetings/`: prep, notes, and calendar handling
- `vault/30-Projects/`: execution plans and project state
- `vault/35-Reports/`: specialist reports and updates
- `vault/40-People/`: CRM and relationship memory
- `vault/50-Travel/`: logistics and trip options
- `vault/60-Wellness/`: wellness tracking
- `vault/70-Ops/`: ops audits and infrastructure readiness

## Approval Boundaries

Always require human approval for:

- money movement
- contract or legal action
- external sends
- travel bookings
- calendar commitments that create external obligations
- public statements
- sensitive relationship moves

## Configuration Boundaries

- Do not put raw secrets in this file
- Do not put personal contact details, OAuth tokens, phone numbers, or private account mappings in this file
- Do not store temporary session notes here
- Client-specific preferences should be stored in client envelopes, workspace files, or agent-owned vault files

## Current Focus

- Keep the repo-native MVP plan and `task_map.yaml` canonical
- Normalize work orders and specialist reports before deeper multi-agent demo wiring
- Make the live voice path context-aware
- Turn unknown live requests into durable readiness artifacts
- Design operator visibility alongside runtime work, not after it
- Keep session-control docs, planning docs, and dev-context docs aligned as the protocols evolve
