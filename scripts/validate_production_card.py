#!/usr/bin/env python3
"""Validate Claude版 Production Card V3 teacher-structure cards.

Usage:
  python3 scripts/validate_production_card.py card.txt
  cat card.txt | python3 scripts/validate_production_card.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


BEGIN_MARKER = "===Production Card Begin==="
END_MARKER = "===Production Card End==="
EXPECTED_RUNTIME_VERSION = "ZH-RUNTIME-V3.0-TEACHER"
EXPECTED_STRUCTURE_VERSION_PREFIX = "STRUCT-V3.0-TEACHER"
ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FIELDS = [
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

STRUCTURE_INSTANCE_FIELDS = [
    "开头具体困惑或反差",
    "核心反转句",
    "续读动力",
    "因果追问链",
    "因果追问终点",
    "核心判断位置",
    "结尾回收方式",
]

FORBIDDEN_CARD_TOKENS = [
    "26维审计",
    "26 维审计",
    "26维总审计",
    "26 维总审计",
    "认知校正",
    "利益重分配",
    "风险传导",
    "PD｜",
    "RR｜",
    "RE｜",
    "BT｜",
    "CR｜",
]

ABSTRACT_ONLY_TOKENS = [
    "反转",
    "机制",
    "承接",
    "升华",
    "收藏价值",
    "认知升级",
    "现实承接",
]

EXPLANATION_TARGET_REQUIREMENTS = [
    "读者真实困惑",
    "因果追问链",
    "因果追问终点",
    "唯一核心判断",
]

CLAUDE_DIRECT_OUTPUT_REQUIREMENTS = [
    "直接生成一篇可发布的知乎回答",
    "不要反问",
    "不要改卡",
    "不要要求用户确认篇幅或素材",
    "只输出正文",
    "不输出分析",
    "卡片",
    "生成说明",
    "自检结果",
]


def read_input() -> str:
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).read_text(encoding="utf-8")
    return sys.stdin.read()


def extract_card(raw_text: str, failures: list[str]) -> str:
    if BEGIN_MARKER not in raw_text or END_MARKER not in raw_text:
        failures.append("missing Production Card Begin/End marker")
        return raw_text.strip()
    start = raw_text.index(BEGIN_MARKER) + len(BEGIN_MARKER)
    end = raw_text.index(END_MARKER)
    if end <= start:
        failures.append("Production Card markers are in the wrong order")
        return raw_text.strip()
    return raw_text[start:end].strip()


def field_pattern(field: str) -> re.Pattern[str]:
    return re.compile(rf"(?m)^{re.escape(field)}：")


def section(text: str, field: str) -> str:
    fields = "|".join(re.escape(f) for f in REQUIRED_FIELDS)
    match = re.search(
        rf"(?ms)^{re.escape(field)}：\s*(.*?)(?=^(?:{fields})：|\Z)",
        text,
    )
    return match.group(1).strip() if match else ""


def count_numbered_items(value: str) -> int:
    return len(re.findall(r"(?m)^\s*\d+\.", value))


def is_valid_zhihu_question_url(value: str) -> bool:
    return bool(re.search(r"https://www\.zhihu\.com/question/\d+", value))


def read_file(path: str) -> str:
    try:
        return (ROOT / path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def check_runtime_version(failures: list[str]) -> None:
    version_files = [
        "docs/08_总AI执行中心.md",
        "docs/知乎OS执行协议.md",
        "templates/知乎OS总控提示词.md",
        "runtime/ACTIVE_MANIFEST.md",
        "runtime/知乎结构库快照.md",
        "skills/Skill006_知乎生产卡生成器.md",
        "templates/Production Card模板.md",
    ]
    missing = []
    for file_name in version_files:
        content = read_file(file_name)
        if EXPECTED_RUNTIME_VERSION not in content and EXPECTED_STRUCTURE_VERSION_PREFIX not in content:
            missing.append(file_name)
    if missing:
        failures.append(
            "FAIL-RUNTIME-VERSION-MISMATCH: version marker missing in "
            + ", ".join(missing)
        )


def active_structure_ids() -> set[str]:
    content = read_file("runtime/知乎结构库快照.md")
    ids = set(re.findall(r"^## (ACTIVE-[^｜\n]+)｜", content, flags=re.M))
    ids.update(re.findall(r"结构版本号：(STRUCT-V3\.0-TEACHER-[A-Z0-9]+)", content))
    return ids


def validate_segments(text: str, failures: list[str]) -> None:
    construction = section(text, "分段施工说明")
    segment_matches = re.findall(
        r"(?ms)^\s*\d+\.\s*段落目标：\s*(.*?)(?=^\s*\d+\.\s*段落目标：|\Z)",
        construction,
    )
    if len(segment_matches) < 5:
        failures.append("FAIL-CARD-ABSTRACT: 分段施工说明 must contain at least 5 segments")
        return

    for index, segment in enumerate(segment_matches, start=1):
        for subfield in ["具体内容", "现实场景或例子", "推进关系"]:
            match = re.search(rf"(?m)^\s*{subfield}：\s*(.+)", segment)
            if not match or len(match.group(1).strip()) < 8:
                code = "FAIL-CARD-NO-SCENE" if subfield == "现实场景或例子" else "FAIL-CARD-ABSTRACT"
                failures.append(f"{code}: segment {index} missing concrete {subfield}")
            elif subfield == "推进关系":
                relation = match.group(1).strip()
                if relation in ABSTRACT_ONLY_TOKENS:
                    failures.append(
                        f"FAIL-CARD-EXPLANATION-TARGET-DRIFT: segment {index} 推进关系 is not a concrete explanation step"
                    )
        goal_match = re.search(r"(?m)^(.+?)(?:\n|$)", segment.strip())
        goal_text = goal_match.group(1).strip() if goal_match else ""
        if goal_text in ABSTRACT_ONLY_TOKENS:
            failures.append(f"FAIL-CARD-ABSTRACT: segment {index} uses abstract-only label")


def validate_explanation_target(text: str, structure_instance: str, failures: list[str]) -> None:
    for field in EXPLANATION_TARGET_REQUIREMENTS:
        if len(section(text, field)) < 12 and field not in {"因果追问链", "因果追问终点"}:
            failures.append(f"FAIL-CARD-EXPLANATION-TARGET-DRIFT: {field} is too thin")

    true_confusion = section(text, "读者真实困惑")
    original_understanding = section(text, "读者原始理解")
    core_judgment = section(text, "唯一核心判断")
    if true_confusion and original_understanding and true_confusion.strip() == original_understanding.strip():
        failures.append("FAIL-CARD-EXPLANATION-TARGET-DRIFT: 读者真实困惑 must differ from 读者原始理解")
    if core_judgment and len(core_judgment) < 18:
        failures.append("FAIL-CARD-EXPLANATION-TARGET-DRIFT: 唯一核心判断 must state the final judgment")

    causal_chain_match = re.search(
        r"(?ms)^因果追问链：\s*(.*?)(?=^因果追问终点：|\Z)",
        structure_instance,
    )
    causal_chain = causal_chain_match.group(1).strip() if causal_chain_match else ""
    causal_items = [
        item.strip()
        for item in re.findall(r"(?m)^\s*\d+\.\s*(.+)", causal_chain)
        if item.strip()
    ]
    if len(causal_items) < 3:
        failures.append("FAIL-CARD-NO-CAUSAL-CHAIN: causal chain must contain at least 3 numbered steps")
    for index, item in enumerate(causal_items, start=1):
        if len(item) < 8:
            failures.append(f"FAIL-CARD-EXPLANATION-TARGET-DRIFT: causal step {index} is too thin")
        if item in ABSTRACT_ONLY_TOKENS:
            failures.append(f"FAIL-CARD-EXPLANATION-TARGET-DRIFT: causal step {index} is abstract-only")

    endpoint_match = re.search(r"(?m)^因果追问终点：\s*(.{8,})", structure_instance)
    if not endpoint_match:
        failures.append("FAIL-CARD-NO-CAUSAL-CHAIN: missing causal endpoint")
    else:
        endpoint = endpoint_match.group(1).strip()
        if endpoint in ABSTRACT_ONLY_TOKENS:
            failures.append("FAIL-CARD-EXPLANATION-TARGET-DRIFT: causal endpoint is abstract-only")


def main() -> int:
    failures: list[str] = []
    raw = read_input()
    text = extract_card(raw, failures)

    if not text:
        failures.append("Production Card is empty")

    for field in REQUIRED_FIELDS:
        if not field_pattern(field).search(text):
            failures.append(f"missing field: {field}")

    question_url = section(text, "问题链接")
    if not is_valid_zhihu_question_url(question_url):
        failures.append("问题链接 must contain a valid https://www.zhihu.com/question/{id} URL")

    structure_id = section(text, "ACTIVE结构ID").splitlines()[0].strip() if section(text, "ACTIVE结构ID") else ""
    structure_version = section(text, "结构版本").splitlines()[0].strip() if section(text, "结构版本") else ""
    valid_structures = active_structure_ids()
    if structure_id not in valid_structures and structure_version not in valid_structures:
        failures.append("FAIL-STRUCTURE-NOT-ACTIVE: card does not reference an ACTIVE runtime structure")
    if structure_version and not structure_version.startswith(EXPECTED_STRUCTURE_VERSION_PREFIX):
        failures.append("FAIL-STRUCTURE-INVENTED: structure version is not a V3 teacher structure")
    if "STRUCT-V2.1" in text:
        failures.append("FAIL-STRUCTURE-INVENTED: STRUCT-V2.1 is not allowed")

    structure_instance = section(text, "结构实例化")
    for field in STRUCTURE_INSTANCE_FIELDS:
        match = re.search(rf"(?m)^{re.escape(field)}：\s*(.+)", structure_instance)
        if not match or len(match.group(1).strip()) < 8:
            failures.append(f"FAIL-CARD-ABSTRACT: 结构实例化 missing concrete {field}")

    validate_explanation_target(text, structure_instance, failures)

    validate_segments(text, failures)

    writing_constraints = section(text, "表达约束")
    for item in CLAUDE_DIRECT_OUTPUT_REQUIREMENTS:
        if item not in writing_constraints:
            failures.append(f"表达约束 missing Claude direct-output requirement: {item}")
    for item in ["两稿制", "首屏 150 字"]:
        if item not in writing_constraints:
            failures.append(f"表达约束 missing requirement: {item}")

    for token in FORBIDDEN_CARD_TOKENS:
        if token in text:
            failures.append(f"forbidden backstage token present: {token}")

    if count_numbered_items(section(text, "事实和安全边界")) < 3:
        failures.append("事实和安全边界 must contain at least 3 numbered items")

    check_runtime_version(failures)

    if failures:
        print("Fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
