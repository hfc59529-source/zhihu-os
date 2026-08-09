#!/usr/bin/env python3
"""Release Builder (Manifest Contract V0).

Reads a draft Runtime Manifest that declares Partitions (which files belong
to this release) and Regression Tests. Ignores whatever the draft says for
sha256 / Based On Commit / Published At / Status — those are computed fresh
from disk and git, never trusted from the draft. Runs the generic validator
against the computed candidate; only writes the target manifest if the
candidate passes. Never mutates the target on failure.

Release Builder is the only entry point allowed to write a published Runtime
status (TRIAL / ACTIVE). Every call must explicitly declare its target status
via --status; there is no default. Running it is the deliberate human act
that constitutes Approval of that specific status — nothing here approves
content on your behalf, and TRIAL is not a lesser form of ACTIVE, it is a
distinct declared target with its own execution authority (see Compiler V1
§14 and the Runtime Lifecycle note in §15).

Usage:
  python3 scripts/release_runtime.py --draft runtime/ACTIVE_MANIFEST.md \
      --status TRIAL|ACTIVE [--out runtime/ACTIVE_MANIFEST.md] [--commit <sha>]

If --out is omitted it defaults to --draft (in-place promotion).
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_runtime_consistency as validator  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def current_commit() -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def render_manifest(manifest: dict) -> str:
    lines = [
        "# Runtime Manifest",
        "",
        f"Runtime Version: {manifest['runtime_version']}",
        f"Status: {manifest['status']}",
        f"Published At: {manifest['published_at']}",
        f"Based On Commit: {manifest['based_on_commit']}",
        "",
        "## Partitions",
        "",
    ]
    for part in manifest["partitions"]:
        lines.append(f"### {part['name']}")
        lines.append("")
        lines.append("| path | sha256 |")
        lines.append("|---|---|")
        for f in part["files"]:
            lines.append(f"| {f['path']} | {f['sha256']} |")
        lines.append("")
    lines.append("## Regression Tests")
    lines.append("")
    if manifest["regression_tests"]:
        for t in manifest["regression_tests"]:
            lines.append(f"- {t}")
    else:
        lines.append("- （无；本次发布未声明可独立执行的回归测试脚本）")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft", required=True)
    parser.add_argument("--status", required=True, choices=["TRIAL", "ACTIVE"])
    parser.add_argument("--out", default=None)
    parser.add_argument("--commit", default=None)
    args = parser.parse_args(argv[1:])

    draft_path = Path(args.draft).resolve()
    out_path = Path(args.out).resolve() if args.out else draft_path

    if not draft_path.exists():
        print("Fail")
        print(f"- draft not found: {draft_path}")
        return 1

    manifest = validator.parse_manifest(draft_path.read_text(encoding="utf-8"))

    if not manifest["runtime_version"]:
        print("Fail")
        print("- draft missing Runtime Version")
        return 1
    if not manifest["partitions"]:
        print("Fail")
        print("- draft declares no Partitions")
        return 1

    commit = args.commit or current_commit()

    for part in manifest["partitions"]:
        for f in part["files"]:
            fpath = ROOT / f["path"]
            if not fpath.exists():
                print("Fail")
                print(f"- declared file missing on disk: {f['path']}")
                return 1
            f["sha256"] = sha256(fpath)

    manifest["based_on_commit"] = commit
    manifest["published_at"] = datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )
    manifest["status"] = args.status

    rendered = render_manifest(manifest)

    candidate_path = out_path.with_name(out_path.name + ".release-candidate")
    candidate_path.write_text(rendered, encoding="utf-8")

    rc = validator.main(["validate_runtime_consistency.py", str(candidate_path)])
    if rc != 0:
        print("")
        print(f"Fail")
        print(f"- release candidate did not pass validate_runtime_consistency.py; not writing {out_path}")
        candidate_path.unlink(missing_ok=True)
        return 1

    candidate_path.replace(out_path)
    print("")
    print(f"Released: {out_path}")
    print(f"Runtime Version: {manifest['runtime_version']}")
    print(f"Based On Commit: {commit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
