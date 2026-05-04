---
id: PROJ-{{date:YYYY}}-{{project_number}}
title: "{{title}}"
status: 🟢 Active        # 🟢 Active | 🟡 On Hold | 🔴 Blocked | ✅ Completed
priority: P2              # P1 High | P2 Medium | P3 Low
type: Structured          # Structured | Organic | Instant
business: Biz A           # Biz A | Biz B | Personal
architect: Maxine
conductor: Khadijah
created: {{date:YYYY-MM-DD}}
updated: {{date:YYYY-MM-DD}}

team:
  - Sinclair (EA)

start_date: {{date:YYYY-MM-DD}}
due_date: 
target_revenue:           # optional
budget:                   # optional

dependencies: []
blockers: []

energy_required: Medium   # High | Medium | Low
perma_v_impact:           # Achievement | Engagement | Relationships | Meaning | Vitality
mood_check:
---

# {{title}}

## Why This Matters
<!-- 1–2 sentences: what's the purpose and the win condition -->

## Milestones

```mermaid
gantt
    title {{title}}
    dateFormat YYYY-MM-DD
    section Phase 1
    Research           :a1, {{date:YYYY-MM-DD}}, 7d
    section Phase 2
    Execution          :a2, after a1, 7d
    section Phase 3
    Review & Close     :a3, after a2, 3d
```

| # | Milestone | Owner | Due | Status |
|---|-----------|-------|-----|--------|
| 1 | | | | ⬜ |
| 2 | | | | ⬜ |
| 3 | | | | ⬜ |

## Key Decisions

| Date | Decision | Made by | Notes |
|------|----------|---------|-------|
| | | | |

## Resources & Links

- **PM board:** 
- **Brief:** 
- **Budget doc:** 
- **Contacts:** 

## Constraint Brief
<!-- Filled by Maxine when resource polling returns a blocker -->

- **Calendar (Sinclair):** ✅ Clear
- **Budget (Kyle):** ✅ Clear
- **Infrastructure (Overton):** ✅ Clear

## Status Log

| Date | Update | By |
|------|--------|----|
| {{date:YYYY-MM-DD}} | Project created | Maxine |

## Related Reports
<!-- Links to 35-Reports/ entries for this project -->

-
