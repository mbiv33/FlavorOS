#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
VAULT_DIR="${REPO_ROOT}/vault"
CANVAS_PATH="${VAULT_DIR}/30-Projects/FlavorOS/FlavorOS MVP Delivery.canvas"
INSTALLER="${REPO_ROOT}/scripts/obsidian/install-flavoros-plugins.py"

if [[ ! -d "${VAULT_DIR}" ]]; then
  echo "FlavorOS vault folder not found: ${VAULT_DIR}" >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required to install plugins and encode the Obsidian URI." >&2
  exit 1
fi

echo "Installing/updating FlavorOS Obsidian plugins for this vault..."
python3 "${INSTALLER}" --vault "${VAULT_DIR}"

ENCODED_PATH="$(python3 - "${CANVAS_PATH}" <<'PY'
import sys
import urllib.parse

print(urllib.parse.quote(sys.argv[1], safe=""))
PY
)"

echo "Opening FlavorOS vault Canvas in Obsidian..."
open -a "Obsidian" >/dev/null 2>&1 || true
open "obsidian://open?path=${ENCODED_PATH}"

echo
echo "If Obsidian opens but plugins are disabled, go to Settings -> Community plugins and enable them."
echo "If the URI does not register the vault, choose 'Open folder as vault' and select:"
echo "${VAULT_DIR}"

