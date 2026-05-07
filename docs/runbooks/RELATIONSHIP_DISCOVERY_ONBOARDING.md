# Relationship Discovery Onboarding

## Purpose

Build the Relationship Discovery onboarding flow for the MVP prerequisite. This flow prepares FlavorOS to own contact discovery, relationship validation, and relationship tracking through `workspace/relationships/current.md`.

## Scope

- Authorize the owner's email and calendar accounts.
- Extract contacts and relationship signals from email and calendar context.
- Validate relationship candidates through conversational input.
- Initialize `workspace/relationships/current.md` as the canonical relationship tracking file.

## Prerequisites

- `FLAVOROS_CONTEXT.md` exists as the shared system context file.
- Active client/account mappings live in client envelopes, workspace docs, or the authorized connector/tool configuration.
- Email/calendar MCP connectors are configured and available for the owner.
- `workspace/TOOLS.md` is present to document which accounts are in use.
- `relationship-file-format.md` exists as the canonical format reference.

## Onboarding Flow

### 1. Authorize email and calendar accounts

1. Confirm the active client's authorized email and calendar accounts from client envelopes, workspace docs, or the connected tool configuration.
2. Verify the MCP connector or OAuth config for each account.
3. Test access with two checks:
   - "What email accounts are connected?"
   - "What events are on my calendar today?"
4. If access is not available, escalate with an explicit account authorization checklist and skip to manual discovery.

### 2. Extract contacts and relationship signals

1. Pull recent inbound/outbound email threads from connected accounts.
2. Pull upcoming meetings and attendees from the calendar accounts.
3. Identify high-priority relationship candidates:
   - active project contacts
   - VIP stakeholders
   - near-term meeting attendees
   - recent unanswered threads
4. Capture for each candidate:
   - name
   - context
   - last contact date
   - relationship type (e.g. follow-up, nurture, event prep)

### 3. Validate via conversational input

1. Present the first-pass contact list to the owner.
2. Ask the owner to confirm or correct:
   - whether each person should be an active follow-up, nurture contact, or archive.
   - relationship priority and desired outcome.
   - any missing people or accounts that were not captured automatically.
3. Capture explicit validation in conversational form:
   - "Confirm these three contacts as priority follow-ups." 
   - "Add this person to nurture with monthly check-ins."

### 4. Initialize `workspace/relationships/current.md`

1. Create a clean relationship tracking file with sections:
   - Active Follow-ups
   - Nurture
   - Archived
2. Use the format from `relationship-file-format.md`.
3. Add validated contacts with proper fields and next follow-up/check-in dates.
4. Save the file as the canonical source of truth for relationship state.

## Delivery Artifacts

- `relationship-file-format.md`
- `docs/runbooks/RELATIONSHIP_DISCOVERY_ONBOARDING.md`
- `workspace/relationships/current.md` initialized as the canonical relationship file
- Updated `skills/relationship-manager/SKILL.md` to include onboarding guidance

## Notes

- If account access is incomplete, build a manual discovery checklist and validate it with the owner.
- The relationship discovery onboarding flow is the MVP prerequisite for follow-up execution, meeting prep, and relationship momentum tracking.
