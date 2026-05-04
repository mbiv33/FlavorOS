# Skills Inventory

Existing v1 skills cover the basics. The list below shows what each agent **needs** to actually do its job for a 2-business + heavy-travel owner. Items marked **[exists]** are already in `skills/`. Items marked **[stub]** need to be authored.

---

## Khadijah (chief-of-staff)
- **[exists]** chief-of-staff (orchestrator)
- **[stub]** morning-brief — assemble Flavor Brief from all reports
- **[stub]** midday-pulse — light midday check, brief only if changed
- **[stub]** eod-review
- **[stub]** weekly-review — Friday roll-up of wins/misses/next week
- **[stub]** flavor-brief-template — canonical brief format
- **[stub]** mode-switcher — Deep Work / Social / Recovery / Standard transitions
- **[stub]** approval-handler — verify HITL signature before unblocking actions
- **[stub]** escalation-router — Tier 3 → Telegram, with throttling

## Sinclair (executive-assistant)
- **[exists]** executive-assistant
- **[stub]** inbox-sweep (haiku)
- **[stub]** draft-email (sonnet)
- **[stub]** schedule-meeting (sonnet) — multi-account aware
- **[stub]** calendar-lookahead (haiku)
- **[stub]** meeting-prep (sonnet) — pulls into vault/20-Meetings
- **[stub]** reschedule (sonnet)
- **[stub]** decline-politely (haiku)
- **[stub]** holding-reply (haiku)
- **[stub]** vip-flag-routing (haiku)
- **[stub]** out-of-office-handler

## Maxine (daily-task-manager + project layer)
- **[exists]** daily-task-manager
- **[exists]** daily-task-prep
- **[stub]** milestone-risk-scan (sonnet) — flags slipping deadlines
- **[stub]** project-status-roundup (sonnet) — Mon roll-up per business
- **[stub]** prioritization (sonnet) — re-rank when load spikes
- **[stub]** goal-alignment (sonnet) — challenges low-leverage tasks
- **[stub]** kpi-rollup (haiku)
- **[stub]** contract-deadline-watch (haiku)
- **[stub]** task-from-email (haiku) — converts a Sinclair flag into a task

## Kyle (relationship-manager + finance layer)
- **[exists]** relationship-manager
- **[stub]** followup-cadence — drafts day-2/5/7 follow-ups; Sinclair sends
- **[stub]** vip-health-check
- **[stub]** finance-pulse — weekly cash + AR + AP across both businesses
- **[stub]** overhead-audit — monthly anomaly scan
- **[stub]** invoice-tracker
- **[stub]** expense-anomaly-scan
- **[stub]** pipeline-rollup
- **[stub]** win-logger
- **[stub]** client-sentiment-scan — flag at-risk client signals

## Regine (brand-social) — all stub
- **[exists]** brand-social
- **[stub]** vet-contact
- **[stub]** network-pulse
- **[stub]** event-lookahead
- **[stub]** event-prep
- **[stub]** event-debrief
- **[stub]** brand-voice-check
- **[stub]** warm-intro-finder
- **[stub]** going-cold-scan

## Scooter (travel-logistics) — all stub
- **[exists]** travel-logistics
- **[stub]** travel-horizon-scan — 14-day forward
- **[stub]** flight-research
- **[stub]** hotel-research
- **[stub]** ground-transport
- **[stub]** itinerary-builder — writes vault/50-Travel/<trip>
- **[stub]** pre-trip-check — fires <72h
- **[stub]** timezone-impact — coordinates with Watson
- **[stub]** per-diem-tracker

## Watson (wellness) — all stub
- **[exists]** wellness
- **[stub]** morning-vitals
- **[stub]** calendar-load-check — flags tomorrow overload
- **[stub]** perma-v-checkin — weekly
- **[stub]** journal-sentiment-scan — read-only on vault/80-Journal
- **[stub]** sleep-trend
- **[stub]** stress-trend
- **[stub]** deep-work-block-audit
- **[stub]** recovery-mode-recommender

## Overton (infrastructure-ops) — all stub
- **[exists]** infrastructure-ops
- **[stub]** bill-radar — daily 7-day forward
- **[stub]** subscription-audit — monthly
- **[stub]** tech-health-check — weekly
- **[stub]** domain-renewal-scan
- **[stub]** security-advisory-scan
- **[stub]** vendor-contact-log
- **[stub]** utility-spend-trend
- **[stub]** recovery-mode-handler — clears bills queue when owner unplugs

---

## Cross-cutting skills (live in `skills/_shared/`)
- **[stub]** vault-write-arbiter — Khadijah-arbitrated writes to prevent vault conflicts
- **[stub]** composio-account-resolver — maps "Business A email" → connected Composio account
- **[stub]** hitl-gate — universal pause-and-await-approval primitive
- **[stub]** audit-emit — append every external action to postgres audit log
- **[stub]** trace-context — propagates trace_id across NATS messages

## Build order (recommended)
1. Cross-cutting (`vault-write-arbiter`, `hitl-gate`, `audit-emit`)
2. Khadijah's `morning-brief` + `flavor-brief-template`
3. Sinclair's `inbox-sweep` + `draft-email` (proves OpenRouter dual-profile)
4. Maxine's `daily-task-prep` upgrade to read Kyle's follow-up file
5. Kyle's `followup-cadence` + `finance-pulse`
6. Watson's `morning-vitals` + `calendar-load-check`
7. Scooter's `travel-horizon-scan` + `itinerary-builder`
8. Overton's `bill-radar`
9. Regine's `vet-contact` + `network-pulse`
10. Backfill remaining stubs as patterns emerge.
