# VPS Inventory Runbook

## Purpose

Create a safe snapshot of the current VPS environment after reinstall and one-click service setup. This is used to decide what the repo should own and what is currently managed by Hostinger one-click deployments.

## Source From Current Notes

Private AppDev notes may list a candidate/current VPS address. Do not commit raw IPs or host-specific identifiers in this runbook.

```text
ssh root@YOUR_SERVER_IP
```

Treat this as a candidate until inventory confirms it.

## Run

On the VPS:

```bash
cd /path/to/FlavorOS
bash scripts/vps-inventory.sh > docs/dev/VPS_INVENTORY.md
```

If the repo is not on the VPS yet:

```bash
bash /tmp/vps-inventory.sh > /tmp/VPS_INVENTORY.md
```

## Safety Rules

- Do not print secret values.
- Do not print full `.env`.
- Do not print Docker inspect environment values.
- Print env variable names only where needed.
- Do not mutate the VPS.
