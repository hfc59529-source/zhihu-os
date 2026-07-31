#!/usr/bin/env python3
"""Assemble a Writer Input Package from Slim IR and ACTIVE runtime assets.

Usage:
  python3 scripts/assemble_writer_input_package.py \
    --run-id RUN-20260731-002 \
    --ir reports/ir_20260731_task_taken_returned.json \
    --card reports/production_20260731_task_taken_returned_card.txt \
    --out reports/writer_input_package_RUN-20260731-002_task_taken_returned.json
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "runtime" / "知乎结构库快照.md"
ACTIVE_RULES = ROOT / "runtime" / "知乎ACTIVE规律快照.md"
REASONING = ROOT / "docs" / "知乎正文推理协议 V1.0.md"
EXPRESSION = ROOT / "docs" / "知乎正文表达协议 V3.md"
PARAMS = ROOT / "runtime" / "知乎内容质量参数快照.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def section(text: str, field: str) -> str:
    if field == "变量证据":
        match = re.search(r"(?ms)^变量证据：\s*(.*?)(?=^问题理解调用：|\Z)", text)
        return match.group(1).strip() if match else ""

    fields = [
        "问题", "问题链接", "平台", "题型", "唯一主变量", "辅助变量", "变量证据",
        "问题理解调用", "认知奖励目标", "质量参数调用", "行为目标", "本篇重点执行",
        "核心机制", "正文结构", "禁止推导", "结尾任务", "写作约束",
    ]
    joined = "|".join(re.escape(item) for item in fields)
    match = re.search(rf"(?ms)^{re.escape(field)}：\s*(.*?)(?=^(?:{joined})：|\Z)", text)
    return match.group(1).strip() if match else ""


def line_value(text: str, label: str) -> str:
    match = re.search(rf"(?m)^{re.escape(label)}：\s*(.*)$", text)
    return match.group(1).strip() if match else ""


def numbered_items(text: str) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(r"(?m)^\s*\d+\.\s*(.+)$", text)]


def bullet_items(text: str) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(r"(?m)^\s*[-*]\s*(.+)$", text)]


def extract_structure(question_type: str) -> dict[str, object]:
    raw = read(STRUCTURE)
    version = line_value(raw, "版本")
    if "职场组织" in question_type or "领导" in question_type:
        structure_id = "ACTIVE-01"
    elif "人性" in question_type:
        structure_id = "ACTIVE-02"
    else:
        structure_id = "ACTIVE-03"
    pattern = rf"(?ms)^## {re.escape(structure_id)}[^\n]*\n(.*?)(?=^## ACTIVE-|\Z)"
    match = re.search(pattern, raw)
    body = match.group(1).strip() if match else ""
    required_steps = numbered_items(body)
    return {
        "structure_id": structure_id,
        "structure_version": version,
        "source": str(STRUCTURE.relative_to(ROOT)),
        "required_steps": required_steps,
        "step_obligations": [
            f"必须兑现结构步骤：{item}" for item in required_steps
        ],
        "forbidden_reordering": True,
    }


def extract_structure_by_id(structure_id: str) -> dict[str, object]:
    raw = read(STRUCTURE)
    version = line_value(raw, "版本")
    pattern = rf"(?ms)^## {re.escape(structure_id)}[^\n]*\n(.*?)(?=^## ACTIVE-|\Z)"
    title = re.search(rf"(?m)^## {re.escape(structure_id)}｜(.+)$", raw)
    match = re.search(pattern, raw)
    body = match.group(1).strip() if match else ""
    required_steps = numbered_items(body)
    return {
        "structure_id": structure_id,
        "structure_version": version,
        "source": str(STRUCTURE.relative_to(ROOT)),
        "required_steps": required_steps,
        "step_obligations": [
            f"必须兑现结构步骤：{item}" for item in required_steps
        ],
        "forbidden_reordering": True,
        "结构编号": structure_id,
        "结构名称": title.group(1).strip() if title else "",
        "结构版本": version,
        "结构步骤": required_steps,
    }


def protocol_status(raw: str) -> str:
    return line_value(raw, "Status") or "ACTIVE"


def make_package(
    run_id: str,
    ir_path: Path,
    card_path: Path,
    writer_model: str,
    structure_match_path: Path | None = None,
) -> dict[str, object]:
    ir = json.loads(read(ir_path))
    card = read(card_path)
    question_type = section(card, "题型") or ir.get("problem_type", "")
    quality = section(card, "质量参数调用")
    behavior = section(card, "行为目标")
    cr = section(card, "认知奖励目标")
    focus = section(card, "本篇重点执行")
    structure = section(card, "正文结构")
    forbidden = ir.get("forbidden") or numbered_items(section(card, "禁止推导"))

    primary_behavior = line_value(behavior, "主要目标")
    secondary_behavior = line_value(behavior, "次要目标")

    if structure_match_path and structure_match_path.exists():
        structure_match = json.loads(read(structure_match_path))
        selected_id = structure_match.get("结构匹配", {}).get("选中结构") or structure_match.get("structure_match", {}).get("selected_structure_id")
        structure_contract = extract_structure_by_id(selected_id)
        structure_contract["匹配证据"] = structure_match.get("结构匹配", {}).get("匹配证据", [])
        structure_contract["选择理由"] = structure_match.get("结构匹配", {}).get("选择理由", [])
        structure_contract["未选结构"] = structure_match.get("结构匹配", {}).get("未选结构", [])
        structure_contract["置信度"] = structure_match.get("结构匹配", {}).get("置信度", "")
    else:
        structure_contract = extract_structure(question_type)

    return {
        "schema_version": "writer_input_package_v1",
        "run_meta": {
            "run_id": run_id,
            "question": ir.get("question", ""),
            "question_url": ir.get("question_url", ""),
            "platform": ir.get("platform", "知乎"),
            "writer_model": writer_model,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        },
        "decision_ir": {
            "core_judgment": ir.get("core_judgment", ""),
            "core_mechanism": ir.get("core_mechanism", ""),
            "route": ir.get("route", ""),
            "ending": ir.get("ending_judgment", ""),
            "forbidden": forbidden,
        },
        "structure_contract": structure_contract,
        "behavior_contract": {
            "primary_behavior": primary_behavior,
            "secondary_behavior": secondary_behavior,
            "cr_target": {
                "primary": line_value(cr, "主CR"),
                "primary_goal": line_value(cr, "目标"),
                "secondary": line_value(cr, "辅助CR"),
                "secondary_goal": "",
            },
            "reading_progression": [
                "首屏必须给继续阅读理由",
                "每完成一次解释，下一段必须推进问题或落到场景",
                "连续两个新判断后插入现实观察、动作、对话或停顿",
            ],
        },
        "expression_contract": {
            "reasoning_protocol": {
                "id": "知乎正文推理协议 V1.0",
                "source": str(REASONING.relative_to(ROOT)),
                "status": protocol_status(read(REASONING)),
                "obligations": [
                    "禁止伪反常识和绝对化推理",
                    "只保留一条主推导链",
                    "现象 -> 机制 -> 利益关系 -> 行为结果 -> 结论",
                    "不得新增 Production Card 外变量、事实或一级机制",
                ],
            },
            "expression_protocol": {
                "id": "知乎正文表达协议 V3",
                "source": str(EXPRESSION.relative_to(ROOT)),
                "status": protocol_status(read(EXPRESSION)),
                "obligations": [
                    "先讲现象，不先讲概念",
                    "每个机制必须落到具体动作",
                    "每段回答一个隐含问题",
                    "结尾必须给判断工具、观察信号或决策标准",
                ],
            },
            "rr_obligations": [
                item for item in [
                    "RR-01 唯一主判断",
                    "RR-04 阅读节奏",
                    "RR-05 现实承接",
                    "RR-06 阅读奖励",
                ] if item in quality
            ],
            "re_obligations": [
                item for item in [
                    "RE-08 AI痕迹控制",
                    "RE-09 机械结构检测",
                    "RE-10 真人观察感",
                ] if item in quality
            ],
        },
        "material_package": {
            "evidence": bullet_items(section(card, "变量证据")) + [line for line in section(card, "变量证据").splitlines() if "：" in line],
            "reality_anchors": [
                item for item in numbered_items(focus) + numbered_items(structure)
                if any(token in item for token in ["领导", "任务", "现状", "权限", "资源", "验收", "汇报", "群"])
            ],
            "author_observation": [
                "用泛化职场观察承接，不编造具体公司、人物和无来源数字"
            ],
            "available_examples": [
                "当前进度同步",
                "接手清单",
                "领导确认权限、资源和验收标准",
            ],
        },
        "acceptance_contract": {
            "qa_a_requirements": [
                "遵守 Slim IR 核心判断",
                "不新增主变量或一级机制",
                "完成结尾任务",
                "不违反 forbidden",
            ],
            "qa_b_requirements": [
                "逐项检查 structure_contract obligation",
                "逐项检查 CR / 行为目标 / 阅读推进",
                "逐项检查 RR / RE obligation",
                "输出 evidence，不只给总分",
            ],
            "publish_gate": [
                "QA-A PASS",
                "QA-B 无 FAIL",
                "obligation_coverage 无 FAIL，WARNING 必须给修正指令",
            ],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--ir", required=True)
    parser.add_argument("--card", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--writer-model", default="Claude")
    parser.add_argument("--structure-match")
    args = parser.parse_args()

    package = make_package(
        args.run_id,
        ROOT / args.ir,
        ROOT / args.card,
        args.writer_model,
        ROOT / args.structure_match if args.structure_match else None,
    )
    out = ROOT / args.out
    out.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(out.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
