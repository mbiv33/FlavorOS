# Quick Question Audit Log

This log records `/qq` questions so quick side questions do not derail the active session direction.

## 2026-05-07

### QQ-2026-05-07-001

- Question: Why does step 1 require rereading the context docs if the files are already open in the IDE?
- Answer summary: Open tabs show file names, not full durable contents. For serious planning and code changes, Dee must read the actual repo files from disk because the source of truth may have changed.
- Follow-up impact: Project planning now treats open IDE context as a navigation hint, not a loaded source.

### QQ-2026-05-07-002

- Question: When spinning up with `/itc`, are the necessary context files and understanding added to the current session?
- Answer summary: `/itc` provides orientation and a required read list. It does not permanently load every file into active working memory. Repo docs remain the durable source of truth.
- Follow-up impact: The new project plan adds a session guardrail so product context is checked before narrow implementation work.

### QQ-2026-05-07-003

- Question: If Obsidian plugins are installed on the desktop directly, will visualizations open regardless of which vault is opened?
- Answer summary: No. Obsidian community plugins are installed and enabled per vault. FlavorOS visualization plugins must be installed in the FlavorOS vault config.
- Follow-up impact: Created vault-level `.obsidian/plugins/` installation and a macOS launcher for the FlavorOS vault.

### QQ-2026-05-07-004

- Question: Why did Dee not act accordingly after being asked to become an Obsidian expert?
- Answer summary: Dee treated Obsidian compatibility as file-format compatibility instead of validating real vault/plugin usability.
- Follow-up impact: Future "become an expert" requests require checking the real workflow, setup, constraints, and failure modes before acting.

### QQ-2026-05-07-005

- Question: What does "become an expert" mean for executing a prompt?
- Answer summary: It means verify the real workflow, constraints, tools, setup, and failure modes before acting, then produce something usable in practice.
- Follow-up impact: Expertise requests should produce practical, runnable outcomes rather than technically plausible artifacts.
