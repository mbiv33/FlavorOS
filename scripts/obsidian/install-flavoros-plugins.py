#!/usr/bin/env python3
"""Install FlavorOS Obsidian community plugins into the repo vault.

The installer downloads official GitHub release assets into:
  vault/.obsidian/plugins/<plugin-id>/

It also writes:
  vault/.obsidian/community-plugins.json
  vault/.obsidian/flavoros-plugin-install-report.md
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_VAULT = ROOT / "vault"
REGISTRY = DEFAULT_VAULT / ".obsidian" / "flavoros-plugin-registry.json"
ASSET_NAMES = {"manifest.json", "main.js", "styles.css"}


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "FlavorOS-Obsidian-Plugin-Installer",
        },
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        return json.loads(resp.read().decode("utf-8"))


def download(url: str, target: Path) -> None:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "FlavorOS-Obsidian-Plugin-Installer"},
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        target.write_bytes(resp.read())


def copy_from_zip(zip_path: Path, dest: Path) -> set[str]:
    copied: set[str] = set()
    with zipfile.ZipFile(zip_path) as zf:
        for name in zf.namelist():
            asset_name = Path(name).name
            if asset_name in ASSET_NAMES:
                dest.joinpath(asset_name).write_bytes(zf.read(name))
                copied.add(asset_name)
    return copied


def latest_release(repo: str) -> dict:
    return fetch_json(f"https://api.github.com/repos/{repo}/releases/latest")


def install_plugin(plugin: dict, plugins_dir: Path) -> dict:
    expected_id = plugin["id"]
    repo = plugin["repo"]
    dest = plugins_dir / expected_id
    temp_dest = plugins_dir / f".{expected_id}.tmp"
    if temp_dest.exists():
        shutil.rmtree(temp_dest)
    temp_dest.mkdir(parents=True)

    result = {
        "name": plugin["name"],
        "expected_id": expected_id,
        "repo": repo,
        "status": "pending",
        "installed_id": expected_id,
        "version": None,
        "files": [],
        "error": None,
    }

    try:
        release = latest_release(repo)
        assets = release.get("assets", [])
        found: set[str] = set()

        for asset in assets:
            asset_name = asset.get("name", "")
            if asset_name in ASSET_NAMES:
                download(asset["browser_download_url"], temp_dest / asset_name)
                found.add(asset_name)

        if not {"manifest.json", "main.js"}.issubset(found):
            zip_assets = [a for a in assets if a.get("name", "").lower().endswith(".zip")]
            for asset in zip_assets:
                zip_path = temp_dest / asset["name"]
                download(asset["browser_download_url"], zip_path)
                found.update(copy_from_zip(zip_path, temp_dest))
                zip_path.unlink(missing_ok=True)
                if {"manifest.json", "main.js"}.issubset(found):
                    break

        if not {"manifest.json", "main.js"}.issubset(found):
            missing = sorted({"manifest.json", "main.js"} - found)
            raise RuntimeError(f"missing required release assets: {', '.join(missing)}")

        manifest = json.loads((temp_dest / "manifest.json").read_text())
        installed_id = manifest.get("id", expected_id)
        result["installed_id"] = installed_id
        result["version"] = manifest.get("version")
        final_dest = plugins_dir / installed_id

        if final_dest.exists():
            shutil.rmtree(final_dest)
        temp_dest.rename(final_dest)

        if installed_id != expected_id and dest.exists() and dest != final_dest:
            shutil.rmtree(dest)

        result["files"] = sorted(p.name for p in final_dest.iterdir() if p.is_file())
        result["status"] = "installed"
        return result
    except Exception as exc:  # noqa: BLE001 - installer should keep going.
        result["status"] = "failed"
        result["error"] = str(exc)
        shutil.rmtree(temp_dest, ignore_errors=True)
        return result


def write_report(vault: Path, results: list[dict], enabled: list[str]) -> None:
    report = vault / ".obsidian" / "flavoros-plugin-install-report.md"
    lines = [
        "# FlavorOS Obsidian Plugin Install Report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Enabled Plugins",
        "",
    ]
    if enabled:
        lines.extend(f"- `{plugin_id}`" for plugin_id in enabled)
    else:
        lines.append("- none")

    lines.extend(["", "## Results", ""])
    for result in results:
        lines.append(f"### {result['name']}")
        lines.append("")
        lines.append(f"- Repo: `{result['repo']}`")
        lines.append(f"- Expected ID: `{result['expected_id']}`")
        lines.append(f"- Installed ID: `{result['installed_id']}`")
        lines.append(f"- Status: `{result['status']}`")
        if result["version"]:
            lines.append(f"- Version: `{result['version']}`")
        if result["files"]:
            lines.append(f"- Files: {', '.join(f'`{name}`' for name in result['files'])}")
        if result["error"]:
            lines.append(f"- Error: {result['error']}")
        lines.append("")

    report.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", default=str(DEFAULT_VAULT), help="Path to Obsidian vault folder")
    parser.add_argument("--registry", default=str(REGISTRY), help="Plugin registry JSON")
    parser.add_argument("--required-only", action="store_true", help="Install only Dataview and Kanban")
    args = parser.parse_args()

    vault = Path(args.vault).expanduser().resolve()
    registry_path = Path(args.registry).expanduser().resolve()
    obsidian_dir = vault / ".obsidian"
    plugins_dir = obsidian_dir / "plugins"

    obsidian_dir.mkdir(parents=True, exist_ok=True)
    plugins_dir.mkdir(parents=True, exist_ok=True)

    registry = json.loads(registry_path.read_text())
    plugins = registry["plugins"]
    if args.required_only:
        plugins = [p for p in plugins if p["id"] in {"dataview", "obsidian-kanban"}]

    results = [install_plugin(plugin, plugins_dir) for plugin in plugins]
    enabled = [
        result["installed_id"]
        for plugin, result in zip(plugins, results)
        if result["status"] == "installed" and plugin.get("enable_by_default", True)
    ]

    (obsidian_dir / "community-plugins.json").write_text(
        json.dumps(enabled, indent=2) + "\n",
        encoding="utf-8",
    )
    write_report(vault, results, enabled)

    installed = sum(1 for result in results if result["status"] == "installed")
    failed = len(results) - installed
    print(f"Installed {installed}/{len(results)} plugins into {plugins_dir}")
    if failed:
        print(f"{failed} plugin(s) failed. See vault/.obsidian/flavoros-plugin-install-report.md")
    return 0 if installed else 1


if __name__ == "__main__":
    sys.exit(main())

