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
- [x] Preserve Hostinger one-click Hermes/OpenClaw containers as references while deploying repo-owned FlavorOS alongside them.
- [x] Clone/deploy FlavorOS repo onto VPS under `/home/deploy/apps/flavoros`.

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

## Next 3 Actions

- [ ] Finish FOS-MVP-005 so temporary VPS dev agents have stable report paths and handoff shape.
- [ ] Start FOS-MVP-006/FOS-MVP-007 to normalize work orders and specialist reports before deeper demo wiring.
- [ ] Define FOS-MVP-016 so UI/UX and approval visibility stay aligned with runtime work.
