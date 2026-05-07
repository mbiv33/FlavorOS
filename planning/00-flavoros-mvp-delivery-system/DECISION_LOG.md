# FlavorOS MVP Delivery Decision Log

## 2026-05-07

### D-001: Keep development system inside FlavorOS for MVP

Decision: The delivery system lives in the FlavorOS repo for now.

Reason: The current failure mode is context fragmentation. A separate repo would make it easier for execution to drift away from the product.

Review trigger: Revisit after the MVP is deployed and the development system becomes reusable across more than one product.

### D-002: Repo-native plan is canonical

Decision: Markdown plus YAML in git is canonical. ClickUp and Obsidian are projections.

Reason: Agents, Codex, and future scripts can read git-native artifacts reliably. ClickUp is useful for visibility, but should not become hidden state before sync is automated.

### D-003: Agents first

Decision: Prioritize setting up product-agent and temporary VPS dev-agent loops before polishing the full planning system.

Reason: Useful agents can research, test, and report while the system is still being refined.

### D-004: UI/UX is a system component

Decision: UI/UX is now tracked as a first-class workstream.

Reason: FlavorOS cannot ship as only backend runtime, tests, and docs. Human-facing and operator-facing surfaces are part of the product.

### D-005: Cloudflare is edge support, not core runtime

Decision: Use Cloudflare free Workers/Pages for lightweight dashboard or edge helpers only during MVP.

Reason: The core runtime already belongs on the VPS. Moving the core agent runtime before MVP would create unnecessary architecture churn.

