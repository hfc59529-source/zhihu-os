#!/usr/bin/env python3
"""Match one ACTIVE structure for a Zhihu run.

The output keeps Chinese fields for human audit and English aliases for script
compatibility.

Usage:
  python3 scripts/match_structure.py \
    --run-id RUN-20260731-002 \
    --analyzer reports/analyzer_20260731_task_taken_returned.json \
    --out reports/structure_match_RUN-20260731-002_task_taken_returned.json
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "runtime" / "知乎结构库快照.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def line_value(text: str, label: str) -> str:
    match = re.search(rf"(?m)^{re.escape(label)}：\s*(.*)$", text)
    return match.group(1).strip() if match else ""


def numbered_items(text: str) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(r"(?m)^\s*\d+\.\s*(.+)$", text)]


def parse_structures() -> list[dict[str, object]]:
    raw = read(STRUCTURE)
    version = line_value(raw, "版本")
    items: list[dict[str, object]] = []
    for match in re.finditer(r"(?ms)^## (ACTIVE-\d+)｜([^\n]+)\n(.*?)(?=^## ACTIVE-|\Z)", raw):
        body = match.group(3).strip()
        items.append({
            "id": match.group(1),
            "name": match.group(2).strip(),
            "version": version,
            "applicable": line_value(body, "适用"),
            "trigger": line_value(body, "触发条件"),
            "forbidden": line_value(body, "禁用条件"),
            "steps": numbered_items(body),
        })
    return items


def score_structure(structure: dict[str, object], analyzer: dict[str, object]) -> tuple[int, list[str]]:
    text = " ".join([
        analyzer.get("question", ""),
        analyzer.get("problem_type", ""),
        analyzer.get("user_intent", ""),
        analyzer.get("core_mechanism", ""),
        " ".join(analyzer.get("hidden_constraints", [])),
    ])
    applicable = str(structure["applicable"])
    trigger = str(structure["trigger"])
    score = 0
    evidence: list[str] = []

    if "职场" in text and any(token in applicable for token in ["领导", "管理", "组织", "责任"]):
        score += 4
        evidence.append("题目属于职场场景，且涉及领导、任务、责任或组织运行。")
    if any(token in text for token in ["领导", "任务", "责任", "资源", "权限", "验收"]):
        score += 3
        evidence.append("问题核心不是单纯方法步骤，而是权责、资源、评价和风险重新分配。")
    if "建议型" in text and "方法论" in str(structure["name"]):
        score += 1
        evidence.append("题目包含行动建议需求。")
    if "人为什么" in trigger and any(token in text for token in ["为什么", "动机", "选择"]):
        score += 1
        evidence.append("题目含行为动机解释。")
    if str(structure["id"]) == "ACTIVE-01" and (
        "职场组织" in analyzer.get("problem_type", "")
        or "组织" in analyzer.get("core_mechanism", "")
        or "组织" in analyzer.get("selection_reason", "")
    ):
        score += 2
        evidence.append("Analyzer 核心机制已指向组织内过程信息、资源调配和结果控制。")

    return score, evidence


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--analyzer", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    analyzer = json.loads(read(ROOT / args.analyzer))
    structures = parse_structures()
    scored = []
    for structure in structures:
        score, evidence = score_structure(structure, analyzer)
        scored.append((score, structure, evidence))
    scored.sort(key=lambda item: item[0], reverse=True)
    selected_score, selected, selected_evidence = scored[0]

    rejected = []
    for score, structure, evidence in scored[1:]:
        rejected.append({
            "结构编号": structure["id"],
            "结构名称": structure["name"],
            "未选原因": "本题主冲突更偏组织权责和风险分配，优先使用职场组织型结构。",
            "匹配分": score,
            "匹配证据": evidence,
        })

    result = {
        "运行编号": args.run_id,
        "结构匹配": {
            "选中结构": selected["id"],
            "结构名称": selected["name"],
            "结构版本": selected["version"],
            "选择理由": selected_evidence,
            "匹配证据": selected_evidence,
            "未选结构": rejected,
            "置信度": "high" if selected_score >= 7 else "medium",
            "匹配分": selected_score,
            "来源": str(STRUCTURE.relative_to(ROOT)),
        },
        "structure_match": {
            "selected_structure_id": selected["id"],
            "selected_structure_name": selected["name"],
            "structure_version": selected["version"],
            "confidence": "high" if selected_score >= 7 else "medium",
            "score": selected_score,
            "evidence": selected_evidence,
        },
    }
    out = ROOT / args.out
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(out.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
