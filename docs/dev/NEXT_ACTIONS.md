# Next Actions

## Module 0: Control Plane

Status: complete enough for active development.

- [x] Create development session log.
- [x] Create decisions log.
- [x] Create next-actions tracker.
- [x] Add no-secrets VPS inventory script.
- [x] Attempt VPS inventory from local Codex environment.
- [x] Add session summarization protocol.
- [x] Add local context snapshot script.
- [x] Register `/ctl` close-loop trigger.
- [x] Register `/ctx` session spin-up trigger.
- [x] Register `/itc` Product IT Director trigger.
- [x] Generate latest context snapshot.
- [x] Curate raw AppDev import into safe docs/archive locations.
- [x] Run `/ctl` before restart on 2026-05-05.
- [x] Replace `CHIEF_OF_STAFF_CONTEXT.md` with `FLAVOROS_CONTEXT.md` for active runtime docs.
- [x] Re-run VPS inventory from an SSH-authenticated terminal and save sanitized output to `docs/dev/VPS_INVENTORY.md`.
- [x] Confirm current VPS services from inventory.
- [x] Preserve Hostinger one-click Hermes/OpenClaw containers as the real near-term agent runtimes.
- [x] Clone/deploy FlavorOS repo onto VPS under `/home/deploy/apps/flavoros`.
- [x] Remove stale repo-owned Python FlavorOS agent containers from the VPS.
- [x] Add Hostinger agent sync path for Khadijah, Sinclair, and Maxine.

## Module 0.5: MVP Delivery Control Plane

Status: complete enough for active development.

- [x] Create canonical MVP delivery plan.
- [x] Create canonical YAML task map.
- [x] Create ClickUp import projection.
- [x] Create Obsidian dashboard, Kanban, and task index projections.
- [x] Add project-management control skill for Khadijah.
- [x] Add ClickUp/Obsidian PM skill for Maxine.
- [x] Define agent workstreams and temporary VPS dev-agent report paths.
- [x] Expand `/ctx` startup reads for planning, Obsidian, and task-map work.
- [ ] Keep the dashboard, task index, and YAML task map aligned as tasks move.
- [ ] Convert active work into normalized work orders and reports instead of planning-only artifacts.

## Module 1: Canonical Architecture Cleanup

- [x] Remove Regine, Watson, and Overton as deployable services.
- [x] Preserve Regine and Overton as persona packs.
- [x] Preserve Watson as a Sinclair wellness persona/capability pack.
- [x] Align `docker-compose.yml`, `DEPLOYMENT.md`, `README.md`, and `ARCHITECTURE.md`.
- [x] Fix vault write drift for Khadijah and Maxine.

## Module 2: Stack API Protocol

- [ ] Run this before rotating or adding keys.
- [x] Build provider inventory for the live voice demo path.
- [x] Update `.env.example` names only.
- [x] Update `infra/secrets/secrets.example.yaml` names only.
- [x] Replace placeholder age recipient with local public age recipient.
- [x] Validate secret shape without values.
- [x] Encrypt in one SOPS pass.
- [x] Deploy and run no-value health checks.
- [ ] Rotate provider keys that appeared in local diagnostic output before any public/shareable handoff.

## Module 3: Voice-Forward Demo

- [x] Decide fastest live voice surface from current accounts.
- [x] Configure `flavoros.bairyos.com` and `voice.flavoros.bairyos.com` DNS plan.
- [x] Stand up Twilio voice endpoint and media stream skeleton.
- [x] Confirm Twilio call reaches `/voice`.
- [x] Confirm Twilio Media Stream connects to `/twilio-stream`.
- [x] Add audio round-trip test response.
- [x] Confirm Sinclair ElevenLabs voice can speak over the phone.
- [x] Confirm OpenAI STT can transcribe caller audio.
- [x] Confirm basic live policy response over the phone.
- [ ] FOS-MVP-009: connect voice gateway to a Hermes-aware response path.
- [ ] FOS-MVP-010: add deferred work artifact creation from live voice requests.
- [ ] FOS-MVP-011: test interruption and barge-in beyond the current DTMF clear hook.
- [ ] FOS-MVP-012: create the Khadijah and Sinclair demo briefing script.

## Module 4: Email/Calendar Demo Flow

- [x] Define agent-level Communications Unification Protocol.
- [x] Define normalized universal inbox item shape.
- [x] Add readiness templates for universal inbox triage, pending scheduling, Kyle deferred follow-ups, and communications decision brief.
- [ ] FOS-MVP-013: connect Marcus test email read path.
- [ ] FOS-MVP-014: connect Marcus test calendar read/proposal path.
- [ ] FOS-MVP-015: build the email-to-artifacts demo flow.

## Module 5: Agent Runtime And Operator Visibility

- [ ] FOS-MVP-005: stand up temporary VPS dev-agent report paths end to end.
- [ ] FOS-MVP-006: normalize work-order payload shape in runtime docs and code.
- [ ] FOS-MVP-007: normalize specialist report shape.
- [ ] FOS-MVP-008: create durable artifact writer for readiness outputs.
- [ ] FOS-MVP-016: define MVP operator console information architecture.
- [ ] FOS-MVP-017: choose Cloudflare free-tier dashboard deployment path.
- [ ] FOS-MVP-018: build the first read-only operator console.

## Module 6: VPS Runtime And Agent Movement

Status: active priority.

- [ ] Add `app-api` to the VPS deployment path as a first-class support service.
- [ ] Verify repo-owned support service startup order for `postgres`, `nats`, `openrouter-proxy`, `secrets-loader`, and `app-api`.
- [ ] Point Hostinger Khadijah, Sinclair, and Maxine runtimes at synced repo bundles.
- [ ] Apply the MVP schema on the VPS Postgres instance and verify seed records.
- [ ] Confirm the support bus can move handoffs between `app-api` and Hostinger-backed agent workflows.
- [ ] Persist specialist reports into Postgres and durable artifacts on VPS.
- [ ] Replace mock Gmail ingest with real Gmail read path against safe test credentials.
- [ ] Verify Hostinger Sinclair can receive real inbound Gmail-derived context and return a persisted artifact/report.

## Module 7: SIGMA Tooling and Travel Skill Family

Status: in-progress. 9 of 11 PDF protocols built; toolchain hardened with init/validate/render/supersede/merge/--check-links.

- [x] Author `docs/architecture/SIGMA_SPEC.md` (operational spec extending the existing readiness contract).
- [x] Build `scripts/sigma/` toolchain (init, validate, render, supersede, merge, trip_init).
- [x] Add `--check-links` cross-reference resolution to validate.
- [x] Author SIGMA templates: trip-instance, ripple, travel-preferences, destination-intelligence, vendor-intelligence.
- [x] Author readiness templates: plan-trip, booking-execution, trip-brief, receipt-prompt, itinerary-live, return-checklist, debrief-survey, trip-debrief, plus observation template.
- [x] Build Scooter skills: travel-planning, travel-booking, travel-prep, travel-receipts, travel-itinerary, travel-return, travel-debrief, travel-universe-update.
- [x] Build Khadijah skill: ripple-synthesis.
- [x] Refactor ripple system to observation + synthesis (rank 1-5 + proximity).
- [x] Wire all new skills + cron schedules.
- [ ] Build `travel-logistics-active` — handles modifications/rebookings during active phase.
- [ ] Build `travel-agenda-prep` — T-2h voice prep per agenda item.
- [ ] Decide cross-agent shared-skill strategy (per-agent duplicate vs `skills/_shared/` mount).
- [ ] Add `ripple-observation` skills for Sinclair, Maxine, Kyle.
- [ ] Build `sigma_promote.py` (draft→active gate) and `sigma_query.py`.
- [ ] **Architectural debt:** migrate "long-term" SIGMA types (travel-preferences, destination-intelligence, vendor-intelligence) to DB/codified-doc form per the runtime-only-SIGMA correction.

## Module 8: Functional Model Skills And Protocols

Status: documentation and agent architecture layer complete; runtime implementation pending.

- [x] Create functional workflow baseline for Communication, Preparation, Finance, and Work Product.
- [x] Scaffold planning packages for workflows 04 through 13.
- [x] Create agent-level skill/protocol map.
- [x] Create protocol drafting standard.
- [x] Add Sinclair skills/protocols for inbound communications, meeting lifecycle, boundary defense, universal inbox ingestion, and calendar staging.
- [x] Add Kyle skills/protocols for executive prep, post-event synthesis, and comms CRM extraction.
- [x] Add Maxine skills/protocols for AR, AP, monthly reporting, project initiation, and daily status.
- [x] Add Khadijah workflow approval and communications approval orchestration.
- [x] Track `FOS-MVP-021` through `FOS-MVP-024` in the canonical task map.
- [ ] Implement runtime artifact writer that can create these readiness files from work orders/events.
- [ ] Add connector-backed ingestion adapters for email/calendar first.
- [ ] Decide whether communication-specific SIGMA type is needed or whether supported meeting/relationship/project/wellness SIGMAs are enough for MVP.

## Next 3 Actions

- [ ] Sync Khadijah, Sinclair, and Maxine repo bundles into Hostinger agent data roots and restart those real runtimes.
- [ ] Bring up repo-owned support services: `postgres`, `nats`, `secrets-loader`, `openrouter-proxy`, and `app-api`.
- [ ] Run a UI/PRD-to-agent skill mapping pass from `docs/mockups/`, `docs/prd/ui/`, and `docs/dev/UI_PLAN.md`, then update Khadijah, Sinclair, and Maxine skills before testing work orders.
