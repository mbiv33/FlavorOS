# Heartbeat

**What this file is**: Instructions for Sinclair's recurring sweep (runs every 15 minutes during business hours). The cron job invokes the executive-assistant skill with these standing orders.

## What the Heartbeat Does and Does Not Do

**Does**:
- Triages inbox messages per the authority framework (Act / Draft / Escalate)
- Acts on Tier 1 items (archive, acknowledge, confirm meetings)
- Drafts Tier 2 items for owner review — Khadijah packages these into the next Flavor Brief
- Escalates Tier 3 items immediately to Khadijah
- Notes any wellness signals for Sinclair's wellness layer
- Summarizes actions taken at the end of each sweep

**Does not**:
- Send follow-up emails during sweeps — follow-up drafting happens in Kyle's dedicated cron run
- Message the owner when nothing is actionable — silence means everything is handled
- Override the current Operational Mode (Deep Work, Social, Recovery, Standard)

## Sweep Procedure

1. Check current Operational Mode in `CHIEF_OF_STAFF_CONTEXT.md`.
   - **Deep Work**: Only process Tier 3 escalations and wellness flags. All else waits.
   - **Recovery**: Only process Tier 3 escalations. Maxine handles business admin exposure.
   - **Social / Standard**: Full sweep.
2. Check `workspace/tasks/current.md` for tasks due now or overdue.
3. Check inbox for new messages (use message-level search, not thread-only).
4. For each new message: classify per authority framework.
   - **Tier 1 (Act)**: Handle it. Archive, acknowledge, confirm, etc.
   - **Tier 2 (Draft)**: Prepare a draft and flag for Khadijah's next Flavor Brief.
   - **Tier 3 (Escalate)**: Summarize and send to Khadijah immediately via escalation channel.
5. Check calendar for events in the next 2 hours — flag conflicts or prep needs.
6. Check `workspace/relationships/current.md` for follow-ups due today. Note them in the sweep summary — do not draft or send. Kyle handles this in the dedicated follow-up rhythm.

## Escalation

Urgent items go to Khadijah via the configured escalation channel (`CHIEF_OF_STAFF_CONTEXT.md`). Khadijah decides whether to assemble a Flavor Brief immediately or queue for the next scheduled briefing.

Urgent = time-sensitive within 2 hours, or flagged by the owner as high priority.

## Quiet Hours

During configured quiet hours, only escalate genuinely urgent Tier 3 items. Everything else waits for the morning Flavor Brief.

## When Nothing Is Actionable

Return `HEARTBEAT_OK` — no message to the owner, no noise.

## Operating Principles

- Be proactive but don't create noise.
- Handle what you can, escalate what you should, ignore what doesn't matter.
- Respect the current Operational Mode.
- Prioritize: urgent tasks > new high-value emails > calendar prep > follow-ups > routine inbox.
