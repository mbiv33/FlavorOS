# FlavorOS 12-Hour MVP PRD

## Objective

Deliver a voice-forward FlavorOS demo that shows a real executive operating system, not a chatbot. The demo should prove that Khadijah and Sinclair can hold a natural live conversation, coordinate around email/calendar/workflow context, and create durable internal intelligence plus prepared work products.

## Primary User

Marcus is the test client. Christy is the intended first real client after demo and consented onboarding.

## Target Demo

1. User enters a live conversation with Khadijah and/or Sinclair.
2. The conversation feels natural and can tolerate interruptions.
3. Khadijah leads a briefing or presentation moment.
4. Sinclair answers impromptu questions and takes notes.
5. A sample inbound email is processed.
6. The system creates:
   - a SIGMA,
   - a draft email response,
   - a calendar handling artifact,
   - a PM/task artifact,
   - and a visible follow-up update within minutes.

## Non-Goals for 12 Hours

- Full production-hardening of every agent.
- Complete Christy onboarding.
- Autonomous external sends or bookings.
- Full travel agent automation.
- Perfect long-term web UI.

## Must-Haves

- Five-agent architecture is the only active architecture.
- Secrets are handled by protocol, not pasted into chat or docs.
- VPS inventory is captured without secret values.
- Voice demo uses African American voice/style choices where available.
- OAuth/connectors support multiple calendars and multiple email accounts by design.
- Every meaningful workflow creates a SIGMA and readiness artifacts.

## Preferred Workflow Ranking

1. Calendar/email unification and triage.
2. Logistics/travel/receipts.
3. Briefings and project management.

## Acceptance Criteria

- A user can speak with the demo voice surface.
- The voice surface can respond naturally and handle interruptions.
- Khadijah/Sinclair can present a briefing-style exchange.
- The repo contains current project control docs.
- The VPS has been inventoried without leaking secrets.
- At least one email/calendar demo flow produces durable artifacts.
- Agent updates are visible after processing, even if delayed by several minutes.

