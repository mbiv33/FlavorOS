# Relationship Discovery Onboarding PRD

## Goal

Build an MVP relationship discovery onboarding flow that captures key contacts and initializes current relationship context in FlavorOS.

## Scope

- Authorize email and calendar accounts
- Extract contacts and recent participants from connected accounts
- Validate extracted contacts through conversational input
- Initialize `current.md` with the first relationship summary
- Use existing relationship format artifacts such as `relationship-file-format.md`

## Success Criteria

- A clear onboarding sequence exists in documentation
- Authentication integration points are defined for email/calendar services
- Contact extraction is represented as a FlavorOS integration stub
- A conversational validation step is described and scaffolded
- `current.md` initialization is modeled and output requirements are documented

## Integration Notes

### Existing workspace assets

- `relationship-file-format.md` exists at repository root
- `skills/relationship-manager/references/relationship-file-format.md` contains relationship schema guidance

### Planned integration

- Create a FlavorOS onboarding flow that can be invoked by agent or CLI
- Store extracted contact metadata using the canonical relationship file format
- Generate `current.md` in a relationship workspace location or within `vault/20-Relationships/`

## Required new deliverables

- `docs/runbooks/relationship-discovery-onboarding.md` (new runbook)
- `planning/01-relationship-discovery-onboarding/integration/relationship_discovery_onboarding.py`
- `planning/01-relationship-discovery-onboarding/integration/README.md`
- onboarding flow design notes for conversational validation

## MVP Prerequisite

This feature is the prerequisite for relationship discovery and should be implemented before broader relationship management workflows.
