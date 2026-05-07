---
id: FOS-OBS-TASKS
title: FlavorOS MVP Tasks
type: task_index
status: active
owner_agent: maxine
created: 2026-05-07
updated: 2026-05-07
tags:
  - flavoros
  - tasks
  - mvp
---

# FlavorOS MVP Tasks

These tasks mirror the canonical repo task map:

```text
planning/00-flavoros-mvp-delivery-system/task_map.yaml
```

- [x] Create canonical MVP delivery plan [flavoros_id:: FOS-MVP-001] [task_status:: done] [priority:: P0] [owner_agent:: maxine] [workstream:: Delivery Control Plane] [system_area:: planning] [due:: 2026-05-07] [external_action_risk:: false]
- [x] Create agent-readable YAML task map [flavoros_id:: FOS-MVP-002] [task_status:: done] [priority:: P0] [owner_agent:: maxine] [workstream:: Delivery Control Plane] [system_area:: planning] [due:: 2026-05-07] [external_action_risk:: false]
- [x] Create ClickUp import projection [flavoros_id:: FOS-MVP-003] [task_status:: done] [priority:: P1] [owner_agent:: maxine] [workstream:: Delivery Control Plane] [system_area:: planning] [due:: 2026-05-07] [external_action_risk:: false]
- [x] Create Obsidian dashboard and Kanban views [flavoros_id:: FOS-MVP-004] [task_status:: done] [priority:: P1] [owner_agent:: maxine] [workstream:: Delivery Control Plane] [system_area:: obsidian] [due:: 2026-05-07] [external_action_risk:: false]
- [ ] Stand up temporary VPS dev-agent report paths [flavoros_id:: FOS-MVP-005] [task_status:: in_progress] [priority:: P0] [owner_agent:: scooter] [workstream:: Agent Runtime] [system_area:: vps-agents] [due:: 2026-05-08] [dependency_ids:: FOS-MVP-002] [external_action_risk:: false]
- [ ] Normalize work order payload shape in runtime docs and code [flavoros_id:: FOS-MVP-006] [task_status:: ready] [priority:: P0] [owner_agent:: khadijah] [workstream:: Agent Runtime] [system_area:: agent-runtime] [due:: 2026-05-08] [dependency_ids:: FOS-MVP-005] [external_action_risk:: false]
- [ ] Normalize specialist report shape [flavoros_id:: FOS-MVP-007] [task_status:: ready] [priority:: P0] [owner_agent:: khadijah] [workstream:: Agent Runtime] [system_area:: agent-runtime] [due:: 2026-05-08] [dependency_ids:: FOS-MVP-006] [external_action_risk:: false]
- [ ] Create durable artifact writer for readiness outputs [flavoros_id:: FOS-MVP-008] [task_status:: backlog] [priority:: P0] [owner_agent:: maxine] [workstream:: Agent Runtime] [system_area:: vault] [due:: 2026-05-09] [dependency_ids:: FOS-MVP-007] [external_action_risk:: false]
- [ ] Connect voice gateway to Hermes-aware response path [flavoros_id:: FOS-MVP-009] [task_status:: ready] [priority:: P0] [owner_agent:: sinclair] [workstream:: Voice Demo] [system_area:: voice-gateway] [due:: 2026-05-09] [dependency_ids:: FOS-MVP-006] [external_action_risk:: false]
- [ ] Add live voice deferred work artifact creation [flavoros_id:: FOS-MVP-010] [task_status:: backlog] [priority:: P0] [owner_agent:: sinclair] [workstream:: Voice Demo] [system_area:: voice-gateway] [due:: 2026-05-09] [dependency_ids:: FOS-MVP-008,FOS-MVP-009] [external_action_risk:: false]
- [ ] Test interruption and barge-in behavior [flavoros_id:: FOS-MVP-011] [task_status:: backlog] [priority:: P1] [owner_agent:: scooter] [workstream:: Voice Demo] [system_area:: voice-gateway] [due:: 2026-05-10] [dependency_ids:: FOS-MVP-009] [external_action_risk:: false]
- [ ] Create Khadijah and Sinclair demo briefing script [flavoros_id:: FOS-MVP-012] [task_status:: backlog] [priority:: P1] [owner_agent:: khadijah] [workstream:: Voice Demo] [system_area:: demo] [due:: 2026-05-10] [dependency_ids:: FOS-MVP-009] [external_action_risk:: false]
- [ ] Connect Marcus test email read path [flavoros_id:: FOS-MVP-013] [task_status:: backlog] [priority:: P0] [owner_agent:: sinclair] [workstream:: Email Calendar Loop] [system_area:: gmail] [due:: 2026-05-10] [dependency_ids:: FOS-MVP-006] [external_action_risk:: false]
- [ ] Connect Marcus test calendar read/proposal path [flavoros_id:: FOS-MVP-014] [task_status:: backlog] [priority:: P0] [owner_agent:: sinclair] [workstream:: Email Calendar Loop] [system_area:: calendar] [due:: 2026-05-10] [dependency_ids:: FOS-MVP-006] [external_action_risk:: true]
- [ ] Build email-to-artifacts demo flow [flavoros_id:: FOS-MVP-015] [task_status:: backlog] [priority:: P0] [owner_agent:: sinclair] [workstream:: Email Calendar Loop] [system_area:: email-calendar-demo] [due:: 2026-05-11] [dependency_ids:: FOS-MVP-008,FOS-MVP-013,FOS-MVP-014] [external_action_risk:: true]
- [ ] Define MVP operator console information architecture [flavoros_id:: FOS-MVP-016] [task_status:: ready] [priority:: P0] [owner_agent:: khadijah] [workstream:: UI UX Operator Console] [system_area:: ui-ux] [due:: 2026-05-09] [dependency_ids:: FOS-MVP-001] [external_action_risk:: false]
- [ ] Choose Cloudflare free-tier dashboard deployment path [flavoros_id:: FOS-MVP-017] [task_status:: backlog] [priority:: P1] [owner_agent:: scooter] [workstream:: UI UX Operator Console] [system_area:: cloudflare] [due:: 2026-05-10] [dependency_ids:: FOS-MVP-016] [external_action_risk:: false]
- [ ] Build first read-only operator console [flavoros_id:: FOS-MVP-018] [task_status:: backlog] [priority:: P1] [owner_agent:: maxine] [workstream:: UI UX Operator Console] [system_area:: ui-ux] [due:: 2026-05-13] [dependency_ids:: FOS-MVP-016,FOS-MVP-017] [external_action_risk:: false]
- [ ] Create MVP release checklist [flavoros_id:: FOS-MVP-019] [task_status:: backlog] [priority:: P0] [owner_agent:: scooter] [workstream:: Deployment Operations] [system_area:: deployment] [due:: 2026-05-11] [dependency_ids:: FOS-MVP-009,FOS-MVP-015] [external_action_risk:: false]
- [ ] Prepare Christy beta onboarding plan [flavoros_id:: FOS-MVP-020] [task_status:: backlog] [priority:: P2] [owner_agent:: khadijah] [workstream:: Beta and Beyond] [system_area:: beta] [due:: 2026-05-17] [dependency_ids:: FOS-MVP-015,FOS-MVP-019] [external_action_risk:: true]

