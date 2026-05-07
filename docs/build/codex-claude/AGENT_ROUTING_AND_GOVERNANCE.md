# Agent Routing and Governance

## Staff

```text
Khadijah — Chief of Staff — Hermes — human-facing
Sinclair — Executive Assistant — Hermes — human-facing
Maxine — COO — OpenClaw — dark specialist
Scooter — CLO — OpenClaw — dark specialist
Kyle — CRO — OpenClaw — dark specialist
```

## Hard Rule

```text
Khadijah and Sinclair are the only agents that speak directly to the user.
Maxine, Scooter, and Kyle never speak directly to the user.
```

## Default Routing Logic

```text
if executive / approval / decision / unclear:
    Khadijah owns first response
elif schedule / inbox / meeting / wellness:
    Sinclair owns response
elif operations / finance / execution:
    Khadijah delegates to Maxine
elif travel / logistics / research / tech prep:
    Khadijah or Sinclair delegates to Scooter
elif relationships / CRM / brand-social:
    Khadijah delegates to Kyle
else:
    Khadijah owns first response
```

## Answer / Clarify / Defer

```text
ANSWER   → “I have that. The short version is...”
CLARIFY  → “I can do that. Are we solving for fastest, cheapest, or easiest?”
DEFER    → “I don’t have that ready yet. I’ll have Scooter pull the options, add the file to the vault, and text you when it’s ready.”
```

## Human-in-the-Loop Rules

Require approval before:

```text
money movement
contract action
legal advice/action
booking travel
external email send
external text send
sensitive relationship move
public post
calendar commitment that blocks time
```

## Work Order Contract

Subject:

```text
work_order.<agent>
```

Payload:

```json
{
  "work_order_id": "wo_2026_05_05_001",
  "source": "voice-gateway",
  "caller": "+15555555555",
  "call_sid": "CAxxxx",
  "requested_by": "Marcus",
  "front_agent": "khadijah",
  "target_agent": "scooter",
  "task_type": "travel_options",
  "user_request": "Find me options for Dallas next Thursday.",
  "context_summary": "User is on a live call. He wants options, not booking.",
  "deliverable": "3-option travel brief",
  "vault_path": "50-Travel/",
  "priority": "normal",
  "requires_approval": true,
  "created_at": "2026-05-05T12:00:00-04:00"
}
```

## Report Contract

Subject:

```text
report.<agent>
```

Payload:

```json
{
  "work_order_id": "wo_2026_05_05_001",
  "agent": "scooter",
  "status": "complete",
  "summary": "Found three Dallas travel options.",
  "vault_file": "50-Travel/dallas-options-2026-05-05.md",
  "user_facing_response": "I found three good options and put them in the travel folder.",
  "requires_approval": true,
  "completed_at": "2026-05-05T12:20:00-04:00"
}
```

## Vault Routing

```text
Khadijah → 10-Briefs, 35-Reports
Sinclair → 20-Meetings, 60-Wellness
Maxine → 30-Projects, 70-Ops
Scooter → 50-Travel, 70-Ops, 20-Meetings
Kyle → 40-People, 35-Reports
```
