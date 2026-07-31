#!/usr/bin/env python3
"""Validate local Zhihu runtime snapshot consistency for V3 teacher structure.

Usage:
  python3 scripts/validate_runtime_consistency.py
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "runtime" / "ACTIVE_MANIFEST.md"
TEMPLATE = ROOT / "templates" / "Production Card模板.md"
CARD_VALIDATOR = ROOT / "scripts" / "validate_production_card.py"
EXPECTED_VERSION = "ZH-RUNTIME-V3.0-TEACHER"
EXPECTED_STRUCTURE = "STRUCT-V3.0-TEACHER"

REQUIRED_CARD_FIELDS = [
    "问题",
    "问题链接",
    "平台",
    "题型",
    "读者真实困惑",
    "读者原始理解",
    "唯一核心判断",
    "ACTIVE结构名称",
    "ACTIVE结构ID",
    "结构版本",
    "结构实例化",
    "分段施工说明",
    "事实和安全边界",
    "表达约束",
]

REQUIRED_RUNTIME_FILES = [
    "runtime/ACTIVE_MANIFEST.md",
    "runtime/知乎内容质量参数快照.md",
    "runtime/知乎ACTIVE规律快照.md",
    "runtime/知乎结构库快照.md",
    "runtime/logs/production_runs.jsonl",
    "runtime/logs/qa_results.jsonl",
    "runtime/logs/publish_results.csv",
    "docs/08_总AI执行中心.md",
    "docs/知乎OS执行协议.md",
    "templates/知乎OS总控提示词.md",
    "templates/Production Card模板.md",
    "skills/Skill006_知乎生产卡生成器.md",
]

REQUIRED_SCRIPTS = [
    "scripts/validate_production_card.py",
    "scripts/validate_reasoning.py",
    "scripts/validate_reading_experience.py",
    "scripts/validate_runtime_consistency.py",
    "scripts/assemble_writer_input_package.py",
    "scripts/match_structure.py",
    "scripts/validate_obligation_coverage.py",
    "scripts/search_historical_assets.py",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def extract_manifest_table(text: str) -> dict[str, str]:
    paths: dict[str, str] = {}
    for line in text.splitlines():
        if not line.startswith("|") or " --- " in line or "文件路径" in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 4:
            continue
        rel, digest = cells[1], cells[2]
        if re.match(r"^(docs|skills|templates|runtime|scripts|production_variable_library\.md)", rel):
            paths[rel] = digest
    return paths


def main() -> int:
    failures: list[str] = []

    if not MANIFEST.exists():
        print("Fail")
        print(f"- missing manifest: {MANIFEST.relative_to(ROOT)}")
        return 1

    manifest_text = read(MANIFEST)
    if "状态：ACTIVE" not in manifest_text:
        fail("runtime/ACTIVE_MANIFEST.md is not ACTIVE", failures)
    if EXPECTED_VERSION not in manifest_text:
        fail("runtime/ACTIVE_MANIFEST.md missing V3 runtime version", failures)
    if "版本一致性校验结果" not in manifest_text or "结果：PASS" not in manifest_text:
        fail("runtime/ACTIVE_MANIFEST.md missing version consistency PASS", failures)

    for rel in REQUIRED_RUNTIME_FILES + REQUIRED_SCRIPTS:
        path = ROOT / rel
        if not path.exists():
            fail(f"missing required file: {rel}", failures)

    for rel, expected_digest in extract_manifest_table(manifest_text).items():
        path = ROOT / rel
        if not path.exists():
            fail(f"manifest references missing file: {rel}", failures)
            continue
        if sha256(path) != expected_digest:
            fail(f"manifest sha256 mismatch: {rel}", failures)

    version_files = [
        "docs/08_总AI执行中心.md",
        "docs/知乎OS执行协议.md",
        "templates/知乎OS总控提示词.md",
        "templates/Production Card模板.md",
        "skills/Skill006_知乎生产卡生成器.md",
        "runtime/ACTIVE_MANIFEST.md",
        "runtime/知乎内容质量参数快照.md",
        "runtime/知乎ACTIVE规律快照.md",
    ]
    for rel in version_files:
        path = ROOT / rel
        if path.exists() and EXPECTED_VERSION not in read(path):
            fail(f"version marker mismatch: {rel}", failures)

    structure_path = ROOT / "runtime/知乎结构库快照.md"
    if structure_path.exists():
        structure_text = read(structure_path)
        for marker in [
            EXPECTED_STRUCTURE,
            "ACTIVE-TS01",
            "老师爆款推进字段",
            "开头具体抓取的困惑或反差",
            "读者原始理解",
            "核心反转位置",
            "续读动力",
            "必须使用的具体场景",
            "因果追问层数",
            "因果追问终点",
            "核心判断出现位置",
            "结尾回收方式",
            "固定推进顺序",
        ]:
            if marker not in structure_text:
                fail(f"structure snapshot missing teacher marker: {marker}", failures)
    else:
        fail("missing runtime/知乎结构库快照.md", failures)

    if TEMPLATE.exists():
        template_text = read(TEMPLATE)
        for field in REQUIRED_CARD_FIELDS:
            if f"{field}：" not in template_text:
                fail(f"Production Card template missing field: {field}", failures)
        for old_field in ["唯一主变量", "辅助变量", "质量参数调用", "本篇重点执行", "正文结构"]:
            if f"{old_field}：" in template_text:
                fail(f"Production Card template still contains old field: {old_field}", failures)
    else:
        fail("missing Production Card template", failures)

    if CARD_VALIDATOR.exists():
        validator_text = read(CARD_VALIDATOR)
        for field in REQUIRED_CARD_FIELDS:
            if f'"{field}"' not in validator_text:
                fail(f"validate_production_card.py missing field rule: {field}", failures)
        for code in [
            "FAIL-STRUCTURE-NOT-ACTIVE",
            "FAIL-STRUCTURE-INVENTED",
            "FAIL-CARD-ABSTRACT",
            "FAIL-CARD-NO-SCENE",
            "FAIL-CARD-NO-CAUSAL-CHAIN",
            "FAIL-RUNTIME-VERSION-MISMATCH",
        ]:
            if code not in validator_text:
                fail(f"validate_production_card.py missing failure code: {code}", failures)
    else:
        fail("missing validate_production_card.py", failures)

    if failures:
        print("Fail")
        for item in failures:
            print(f"- {item}")
        return 1

    print("Pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
