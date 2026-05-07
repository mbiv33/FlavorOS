#!/usr/bin/env bash
set -euo pipefail

section() {
  printf '\n## %s\n\n' "$1"
}

run() {
  local label="$1"
  shift
  printf '### %s\n\n' "$label"
  printf '```text\n'
  "$@" 2>&1 || true
  printf '```\n\n'
}

section "VPS Inventory"
printf -- "- Generated at: %s\n" "$(date -u +%FT%TZ)"
printf -- "- Hostname: %s\n" "$(hostname 2>/dev/null || true)"
printf -- "- User: %s\n" "$(id -un 2>/dev/null || true)"

section "OS"
run "uname" uname -a
if [ -r /etc/os-release ]; then
  run "os-release" sh -c "grep -E '^(PRETTY_NAME|VERSION|ID|VERSION_ID)=' /etc/os-release"
fi

section "Network"
run "listening ports" sh -c "command -v ss >/dev/null && ss -tulpn || netstat -tulpn"
run "public ip probe" sh -c "command -v curl >/dev/null && curl -fsS https://ifconfig.me || true"

section "Git"
run "git version" git --version
if git rev-parse --show-toplevel >/dev/null 2>&1; then
  run "git root" git rev-parse --show-toplevel
  run "git branch" git branch --show-current
  run "git status short" git status --short
  run "git remote names" git remote -v
else
  printf "No git repo detected in current directory.\n\n"
fi

section "Docker"
run "docker version" docker --version
run "docker compose version" docker compose version
run "docker ps" docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
run "docker images" docker images --format 'table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.CreatedSince}}\t{{.Size}}'
run "docker networks" docker network ls
run "docker volumes" docker volume ls

section "Compose"
if [ -f docker-compose.yml ] || [ -f compose.yml ] || [ -f compose.yaml ]; then
  run "compose config services" docker compose config --services
  run "compose ps" docker compose ps
else
  printf "No compose file detected in current directory.\n\n"
fi

section "Reverse Proxy"
run "caddy status" sh -c "command -v caddy >/dev/null && caddy version && systemctl is-active caddy || true"
run "nginx status" sh -c "command -v nginx >/dev/null && nginx -v && systemctl is-active nginx || true"
run "traefik containers" sh -c "docker ps --format '{{.Names}} {{.Image}}' | grep -i traefik || true"

section "FlavorOS Paths"
run "candidate app dirs" sh -c "find /home /opt /srv /var/www -maxdepth 4 -type d \\( -iname '*flavor*' -o -iname '*hermes*' -o -iname '*openclaw*' \\) 2>/dev/null | sort"
run "repo top files" sh -c "pwd; find . -maxdepth 2 -type f \\( -name 'README.md' -o -name 'docker-compose.yml' -o -name 'agent.yaml' -o -name 'SOUL.md' \\) -print 2>/dev/null | sort"

section "Environment Names Only"
run "process env names" sh -c "env | cut -d= -f1 | sort"

section "Recent Logs"
if [ "${INCLUDE_LOGS:-0}" = "1" ]; then
  run "recent docker logs redacted" sh -c "docker ps --format '{{.Names}}' | while read -r name; do echo \"--- $name\"; docker logs --tail=20 \"$name\" 2>&1 | sed -E 's/(api[_-]?key|token|password|secret|authorization)[^[:space:]]*/REDACTED/Ig'; done"
else
  printf "Skipped by default. Re-run with INCLUDE_LOGS=1 only after confirming logs do not contain raw secrets.\n\n"
fi

section "Inventory Complete"
printf "Review this file before running deploy or secrets commands.\n"
