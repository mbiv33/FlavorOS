# PTQ Resolution Engine Protocol

## Header

- Owner agent: Maxine
- Supporting agents: Khadijah, Sinclair, Kyle
- Related skill: `ptq-resolution-engine`
- Planning source: `planning/14-pac-ptq-evaluation-engine/`

## Purpose

Resolve Project / Task Qualifications so PACs become a real task, a real project, or a cleanly closed non-work item.

## Trigger

- `event.pac.logged`
- `event.ptq.condition_met`
- time-based PTQ review
- manual review request from Khadijah or the owner

## Inputs

- PAC record
- PTQ record
- source artifacts
- service templates
- current task and project state

## Phase Contract

1. PTQ Dispatch: route the qualification gate to the correct resolver.
2. Condition Monitoring: wait for response, time passage, dependency completion, or owner decision.
3. Resolution Assessment: classify result as yes, no, or redirect.
4. Conversion Or Closure: create the execution object or close the PAC.
5. Audit Update: clear or update the PAC master list and write final state.

## Artifacts

- PAC master list state update
- PTQ status note when the qualification is non-trivial
- task packet or project-initiation handoff when qualified
- closure note when rejected or expired

## SIGMA and Readiness Contract

- PTQ state lives durably in runtime storage and is rendered into vault artifacts for operator visibility.
- Create or update a project-state SIGMA only when a PAC becomes active work or materially changes an existing project.
- Task packets, project-initiation handoffs, and closure notes are readiness artifacts.

## Approval Gates

- Route owner-facing decisions through Khadijah.
- Do not create new scope, budget exposure, or external obligations without the required approval path.

## Handoffs

- Qualified bounded work goes to Maxine's task-management layer as a task packet.
- Qualified structured work goes to `project-initiation-milestone-mapping`.
- User-confirmation PTQs flow through `workflow-approval-control` or Khadijah briefing patterns as appropriate.

## Failure Modes

- PTQ stalls: mark waiting state and surface the blocker.
- PTQ resolves to an existing project: attach context and close the PAC as redirected.
- PTQ reveals no work: archive context if useful and close the PAC.

## Completion Signal

- Publish `report.maxine.ptq-resolved`.
