#!/usr/bin/env bash
set -euo pipefail

section() {
  printf '\n## %s\n\n' "$1"
}

run_block() {
  local label="$1"
  shift
  printf '### %s\n\n' "$label"
  printf '```text\n'
  "$@" 2>&1 || true
  printf '```\n\n'
}

section "FlavorOS Context Snapshot"
printf -- "- Generated at: %s\n" "$(date -u +%FT%TZ)"
printf -- "- Working directory: %s\n" "$(pwd)"

section "Git"
run_block "status short" git status --short
run_block "branch" git branch --show-current

section "Compose"
if [ -f docker-compose.yml ]; then
  run_block "compose services" docker compose config --services
else
  printf "No docker-compose.yml found.\n\n"
fi

section "Active Agents"
run_block "agent configs" find agents -maxdepth 2 -name agent.yaml -print
run_block "persona packs" find agents -path '*/personas/*/PERSONA.md' -print

section "Project Control Docs"
run_block "dev docs" find docs/dev docs/pm docs/prd docs/runbooks docs/architecture -maxdepth 2 -type f -print

section "Important Reminders"
cat <<'EOF'
- Five active agents only: khadijah, sinclair, maxine, scooter, kyle.
- Retired identities are persona/capability packs, not deployable agents.
- SIGMAs are created intelligence artifacts, not triggers.
- Do not rotate secrets until the full stack API protocol.
- Do not print secret values in summaries, logs, or chat.
EOF

