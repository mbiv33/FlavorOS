#!/usr/bin/env python3
"""
composio-init — interactive OAuth bootstrap.

Walks every alias in infra/composio.yaml, prints an OAuth URL the user opens
on a phone/laptop, polls Composio until the connection is authorized, and
writes connection_ids back to infra/secrets/secrets.yaml (plaintext, ready
for the operator to re-encrypt with SOPS).

Connection_ids themselves are opaque references — Composio holds the actual
OAuth tokens. We never see refresh tokens, access tokens, or passwords.
"""

import os, sys, time, argparse, yaml, qrcode
from pathlib import Path
from composio import Composio, App

CONFIG = Path("/etc/flavoros/composio.yaml")
SECRETS = Path("/secrets/secrets.yaml")  # plaintext; operator re-encrypts after

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reauth", help="Re-authorize a single alias")
    ap.add_argument("--list",   action="store_true", help="List current connections")
    args = ap.parse_args()

    api_key = os.environ.get("COMPOSIO_API_KEY") or sys.exit("COMPOSIO_API_KEY required")
    client = Composio(api_key=api_key)

    cfg = yaml.safe_load(CONFIG.read_text())
    accounts = cfg["accounts"]
    secrets = yaml.safe_load(SECRETS.read_text()) if SECRETS.exists() else {}
    secrets.setdefault("composio_connections", {})

    targets = [args.reauth] if args.reauth else list(accounts.keys())

    for alias in targets:
        spec = accounts[alias]
        toolkit = spec["toolkit"]
        label   = spec.get("label", alias)
        existing = secrets["composio_connections"].get(alias)

        if existing and not args.reauth:
            print(f"[skip] {alias} already connected ({existing[:8]}…)")
            continue

        print(f"\n── Connecting {alias} ({toolkit}) — {label} ─────────────")
        req = client.connected_accounts.initiate(app=App[toolkit.upper()])
        url = req.redirect_url

        # Print URL + QR so user can hop to a phone if needed.
        print(f"\n  Open in browser:\n    {url}\n")
        qr = qrcode.QRCode()
        qr.add_data(url); qr.make(fit=True); qr.print_ascii(invert=True)

        print("  Waiting for OAuth completion…")
        conn = req.wait_until_active(timeout=600)
        print(f"  ✓ connected: {conn.id}")
        secrets["composio_connections"][alias] = conn.id

    SECRETS.write_text(yaml.safe_dump(secrets, sort_keys=False))
    print(f"\nWrote {len(targets)} connection(s) to {SECRETS}")
    print("Now re-encrypt with SOPS:")
    print(f"  sops --encrypt --in-place {SECRETS}")
    print(f"  mv {SECRETS} {SECRETS.with_suffix('.enc.yaml')}")

if __name__ == "__main__":
    main()
