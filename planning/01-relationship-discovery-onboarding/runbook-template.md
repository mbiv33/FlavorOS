# Relationship Discovery Onboarding Runbook Template

## Purpose

Describe how to execute relationship discovery onboarding in FlavorOS.

## Trigger

- New user onboarding
- First relationship discovery session
- Manual start via agent command

## Steps

1. Authorize email/calendar accounts
2. Extract recent contacts and event participants
3. Validate extracted contacts through conversational input
4. Generate or update `current.md`
5. Review onboarding outputs and confirm readiness

## Artifacts

- `current.md`
- `relationship-file-format.md`
- onboarding session notes

## Quality Checks

- Contact data matches canonical relationship format
- `current.md` contains at least one validated relationship summary
- Calendar and email authorization succeeded

## Handoff Notes

- Update the runbook after the first implementation iteration
- Keep integration stubs in `planning/01-relationship-discovery-onboarding/integration/`
