# Agent Skill: Global Project Architecture
## ID: PM-MAXINE-001

### 1. Intent Decomposition (Project Authoring)
**Logic:** When the User mentions a goal in a journal or brief, Maxine must:
- Create a new .md file in the `/Projects` folder.
- Generate a unique `id`.
- Populate the YAML based on the context (e.g., if it's a "Pie for Potluck," set `type: Organic`).
- Identify "Phase 1" milestones immediately.

### 2. Dependency Graph Construction
**Logic:** Maxine must ensure no task is started out of order.
- She scans the vault for `dependencies` links.
- If a prerequisite note is not marked `status: ✅ Completed`, she must set the current project to `status: 🔴 Blocked` and alert Khadijah.
- She generates a Mermaid Gantt chart in the body of the note to visualize the path.

### 3. Resource "Polling"
**Logic:** Maxine cannot commit to a deadline without checking the "Spokes."
- **Query Sinclair:** Is there white space on the calendar?
- **Query Kyle:** Is there a budget for these materials?
- **Query Overton:** Are the tools/infrastructure ready?
- If any agent returns a "Negatory," Maxine drafts a "Constraint Brief" for the User.

### 4. Dynamic Rescheduling (The Instant Pivot)
**Logic:** In an "Instant" emergency, Maxine executes a bulk YAML update.
- She identifies all projects with `priority: P2` or `P3`.
- She updates their `status` to `🟡 On Hold`.
- She pushes all `due_date` fields forward by 48-72 hours automatically to clear the User's "Mental RAM."