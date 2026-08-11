#!/usr/bin/env python3
"""Generic Runtime Manifest validator (Manifest Contract V0).

Validates INV-01/02/03/04/07/08/09 against a Manifest Contract V0 document.
It knows nothing about what a specific Runtime Release contains (no field
names, no version strings, no required templates) — only that the
Manifest's own declarations are internally consistent with disk and git
state.

Usage:
  python3 scripts/validate_runtime_consistency.py [manifest_path]

Defaults to runtime/ACTIVE_MANIFEST.md.
"""

from __future__ import annotations

import hashlib
import csv
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "runtime" / "ACTIVE_MANIFEST.md"
VALID_STATUS = {"DRAFT", "TRIAL", "ACTIVE", "DEPRECATED"}
USER_GATE_START = "ZH-20260801-011"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_manifest(text: str) -> dict:
    def field(name: str):
        m = re.search(rf"^{name}:[ \t]*(.*)$", text, re.MULTILINE)
        value = m.group(1).strip() if m else None
        return value or None

    manifest = {
        "runtime_version": field("Runtime Version"),
        "status": field("Status"),
        "published_at": field("Published At"),
        "based_on_commit": field("Based On Commit"),
        "partitions": [],
        "regression_tests": [],
    }

    part_section = re.search(r"^## Partitions\s*\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    if part_section:
        chunks = re.split(r"(?m)^### ", part_section.group(1))
        for chunk in chunks[1:]:
            name_line, _, body = chunk.partition("\n")
            files = []
            for row in re.finditer(r"^\|\s*([^|\n]+?)\s*\|\s*([^|\n]*?)\s*\|\s*$", body, re.MULTILINE):
                path_cell, sha_cell = row.group(1).strip(), row.group(2).strip()
                if path_cell.lower() == "path" or set(path_cell) <= {"-"}:
                    continue
                files.append({"path": path_cell, "sha256": sha_cell})
            manifest["partitions"].append({"name": name_line.strip(), "files": files})

    test_section = re.search(r"^## Regression Tests\s*\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    if test_section:
        for item in re.finditer(r"^-\s+(\S.*)$", test_section.group(1), re.MULTILINE):
            val = item.group(1).strip()
            if val.startswith("（") or val.startswith("("):
                continue
            manifest["regression_tests"].append(val)

    return manifest


def commit_exists(commit: str) -> bool:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "cat-file", "-e", commit],
        capture_output=True,
    )
    return result.returncode == 0


def git_blob(commit: str, path: str) -> bytes | None:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "cat-file", "-p", f"{commit}:{path}"],
        capture_output=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout


def find_active_manifests(manifest_path: Path) -> list[Path]:
    runtime_dir = manifest_path.parent
    found = []
    if not runtime_dir.exists():
        return found
    for p in sorted(runtime_dir.glob("*.md")):
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if re.search(r"^Runtime Version:", text, re.MULTILINE) and re.search(
            r"^Status:\s*ACTIVE\s*$", text, re.MULTILINE
        ):
            found.append(p)
    return found


def production_sort_key(production_id: str) -> str:
    m = re.match(r"^(ZH-\d{8}-\d{3})$", production_id)
    return m.group(1) if m else production_id


def user_gate_applies(production_id: str) -> bool:
    return production_sort_key(production_id) >= USER_GATE_START


def validate_publish_gate() -> list[str]:
    """Check published article map rows against the current release gate.

    Historical bypasses are allowed only when they are explicitly recorded in
    Publish_Queue.md. Future COMPLETE rows need visible USER_APPROVED evidence
    in the queue or production ledger before they can pass this validator.
    """
    failures: list[str] = []
    article_map = ROOT / "data" / "production_article_map.csv"
    publish_queue = ROOT / "data" / "Publish_Queue.md"
    ledger = ROOT / "data" / "production_ledger.md"

    if not article_map.exists():
        return failures

    queue_text = publish_queue.read_text(encoding="utf-8") if publish_queue.exists() else ""
    ledger_text = ledger.read_text(encoding="utf-8") if ledger.exists() else ""
    bypass_section_match = re.search(
        r"^## Gate Bypass Log\s*\n(.*?)(?=^## |\Z)",
        queue_text,
        re.MULTILINE | re.DOTALL,
    )
    bypass_text = bypass_section_match.group(1) if bypass_section_match else ""

    with article_map.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            production_id = (row.get("production_id") or "").strip()
            trace_status = (row.get("trace_status") or "").strip()
            if not production_id or trace_status != "COMPLETE":
                continue
            if not production_id.startswith("ZH-") or not user_gate_applies(production_id):
                continue

            in_queue = re.search(rf"\|\s*{re.escape(production_id)}\s*\|.*\bUSER_APPROVED\b", queue_text)
            in_bypass_log = re.search(rf"\|\s*{re.escape(production_id)}\s*\|", bypass_text)
            in_ledger = re.search(rf"\|\s*{re.escape(production_id)}\s*\|.*\bUSER_APPROVED\b", ledger_text)

            if not (in_queue or in_bypass_log or in_ledger):
                failures.append(
                    "PUBLISH-GATE COMPLETE article lacks USER_APPROVED evidence or Gate Bypass Log entry: "
                    f"{production_id}"
                )

    return failures


def main(argv: list[str]) -> int:
    manifest_path = Path(argv[1]).resolve() if len(argv) > 1 else DEFAULT_MANIFEST
    failures: list[str] = []

    if not manifest_path.exists():
        print("Fail")
        print(f"- missing manifest: {manifest_path}")
        return 1

    text = manifest_path.read_text(encoding="utf-8")
    manifest = parse_manifest(text)

    # INV-01
    if manifest["status"] not in VALID_STATUS:
        failures.append(f"INV-01 invalid or missing Status: {manifest['status']!r}")
    if not manifest["runtime_version"]:
        failures.append("INV-01 missing Runtime Version")

    # INV-07
    if not manifest["partitions"]:
        failures.append("INV-07 no Partitions declared")
    for part in manifest["partitions"]:
        if not part["files"]:
            failures.append(f"INV-07 empty partition: {part['name']}")

    # INV-02 / INV-03
    for part in manifest["partitions"]:
        for f in part["files"]:
            fpath = ROOT / f["path"]
            if not fpath.exists():
                failures.append(f"INV-02 missing file: {f['path']} (partition {part['name']})")
                continue
            actual = sha256(fpath)
            if not f["sha256"]:
                failures.append(f"INV-03 missing sha256 declaration: {f['path']}")
            elif actual != f["sha256"]:
                failures.append(f"INV-03 sha256 mismatch: {f['path']}")

    # INV-04
    commit = manifest["based_on_commit"]
    if not commit:
        failures.append("INV-04 missing Based On Commit")
    elif not commit_exists(commit):
        failures.append(f"INV-04 commit not found in git history: {commit}")
    else:
        for part in manifest["partitions"]:
            for f in part["files"]:
                fpath = ROOT / f["path"]
                if not fpath.exists():
                    continue
                blob = git_blob(commit, f["path"])
                if blob is None:
                    failures.append(f"INV-04 file not present in commit tree: {f['path']} @ {commit}")
                elif hashlib.sha256(blob).hexdigest() != sha256(fpath):
                    failures.append(f"INV-04 disk content diverges from Based On Commit: {f['path']}")

    # INV-08
    for test_path in manifest["regression_tests"]:
        tpath = ROOT / test_path
        if not tpath.exists():
            failures.append(f"INV-08 missing regression test: {test_path}")
            continue
        result = subprocess.run([sys.executable, str(tpath)], cwd=ROOT, capture_output=True)
        if result.returncode != 0:
            failures.append(f"INV-08 regression test failed (exit {result.returncode}): {test_path}")

    # INV-09
    if manifest["status"] == "ACTIVE":
        actives = find_active_manifests(manifest_path)
        if len(actives) > 1:
            failures.append(f"INV-09 more than one ACTIVE manifest found: {[str(p) for p in actives]}")

    failures.extend(validate_publish_gate())

    if failures:
        print("Fail")
        for item in failures:
            print(f"- {item}")
        return 1

    print("Pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
