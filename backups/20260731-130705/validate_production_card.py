#!/usr/bin/env python3
"""Validate Claude版 Production Card.

Usage:
  python3 scripts/validate_production_card.py card.txt
  cat card.txt | python3 scripts/validate_production_card.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_FIELDS = [
    "问题",
    "问题链接",
    "平台",
    "题型",
    "L1冻结卡",
    "唯一主变量",
    "辅助变量",
    "变量证据",
    "问题理解调用",
    "认知奖励目标",
    "质量参数调用",
    "本篇重点执行",
    "核心机制",
    "正文结构",
    "禁止推导",
    "结尾任务",
    "写作约束",
]

FORBIDDEN_TOKENS = [
    "MASTER",
    "ACTIVE",
    "Notion",
    "命中页",
    "未命中",
    "审计",
    "协议版本",
    "知识调用",
    "调度",
    "制作过程",
    "分析过程",
]

ALLOWED_SUBFIELDS = {
    "来源",
    "调用理由",
    "证据等级",
    "是否默认=是；",
    "适用于=知乎正文；",
    "调用阶段=正文生成；",
    "优先级=P1/P2/P3。",
}

BEGIN_MARKER = "===Production Card Begin==="
END_MARKER = "===Production Card End==="
CLAUDE_DIRECT_OUTPUT_REQUIREMENTS = [
    "直接生成一篇可发布的知乎回答",
    "不要反问",
    "不要改卡",
    "不要要求用户确认篇幅或素材",
    "只输出正文",
    "不输出分析",
    "不输出",
    "卡片",
    "生成说明",
    "自检结果",
]


def read_input() -> str:
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).read_text(encoding="utf-8")
    return sys.stdin.read()


def extract_card(raw_text: str, failures: list[str]) -> str:
    if BEGIN_MARKER not in raw_text:
        failures.append("missing Production Card Begin marker")
    if END_MARKER not in raw_text:
        failures.append("missing Production Card End marker")
    if failures:
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
    if field == "变量证据":
        match = re.search(r"(?ms)^变量证据：\s*(.*?)(?=^问题理解调用：|\Z)", text)
        return match.group(1).strip() if match else ""

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


def main() -> int:
    failures: list[str] = []
    text = extract_card(read_input(), failures)

    if not text:
        failures.append("Production Card is empty")

    for field in REQUIRED_FIELDS:
        if not field_pattern(field).search(text):
            failures.append(f"missing field: {field}")

    question_url = section(text, "问题链接")
    if not is_valid_zhihu_question_url(question_url):
        failures.append("问题链接 must contain a valid https://www.zhihu.com/question/{id} URL")

    main_variable = section(text, "唯一主变量")
    main_variable_lines = [
        line.strip()
        for line in main_variable.splitlines()
        if line.strip() and not line.strip().startswith("-")
    ]
    if len(main_variable_lines) != 1:
        failures.append("唯一主变量 must contain exactly 1 item")

    l1_freeze = section(text, "L1冻结卡")
    if not l1_freeze:
        failures.append("L1冻结卡 is empty")
    for item in ["题型", "结构版本号", "冻结证据清单", "禁止后改项"]:
        if item not in l1_freeze:
            failures.append(f"L1冻结卡 missing item: {item}")
    frozen_evidence = re.search(r"(?ms)冻结证据清单：\s*(.*?)(?=^禁止后改项：|\Z)", l1_freeze)
    if count_numbered_items(frozen_evidence.group(1) if frozen_evidence else "") < 3:
        failures.append("L1冻结卡 冻结证据清单 must contain at least 3 items")

    aux_count = count_numbered_items(section(text, "辅助变量"))
    if aux_count > 3:
        failures.append("辅助变量 must be <= 3")

    core = section(text, "核心机制")
    if not core:
        failures.append("核心机制 is empty or not sourced")

    evidence = section(text, "变量证据")
    if not evidence:
        failures.append("变量证据 is empty")
    for item in ["唯一主变量", "来源", "调用理由", "证据等级"]:
        if item not in evidence:
            failures.append(f"变量证据 missing item: {item}")

    question_understanding = section(text, "问题理解调用")
    if not question_understanding:
        failures.append("问题理解调用 is empty")
    for item in ["问题分类", "用户意图", "用户隐藏约束", "形成机制", "路由结果", "执行规则", "验证指标"]:
        if item not in question_understanding:
            failures.append(f"问题理解调用 missing item: {item}")

    cr_target = section(text, "认知奖励目标")
    if not cr_target:
        failures.append("认知奖励目标 is empty")
    for item in ["主CR", "目标"]:
        if item not in cr_target:
            failures.append(f"认知奖励目标 missing item: {item}")
    if len(re.findall(r"(?m)^主CR：", cr_target)) != 1:
        failures.append("认知奖励目标 must contain exactly 1 主CR")
    cr_codes = re.findall(r"CR-0[1-4]", cr_target)
    if not cr_codes:
        failures.append("认知奖励目标 must specify one CR-01/02/03/04 code")
    if len(set(cr_codes)) > 2:
        failures.append("认知奖励目标 must use at most 1 主CR and 1 辅助CR")
    if "CR｜认知奖励" in cr_target:
        failures.append("认知奖励目标 must not use generic CR｜认知奖励")

    parameter_call = section(text, "质量参数调用")
    if not parameter_call:
        failures.append("质量参数调用 is empty")
    for item in ["强制底线参数", "本篇核心调用参数", "本篇辅助调用参数", "本篇不调用参数", "行为目标", "主要目标"]:
        if item not in parameter_call:
            failures.append(f"质量参数调用 missing item: {item}")
    core_params = re.search(r"(?ms)本篇核心调用参数：\s*(.*?)(?=^本篇辅助调用参数：|\Z)", parameter_call)
    core_count = count_numbered_items(core_params.group(1) if core_params else "")
    if core_count < 3 or core_count > 6:
        failures.append("本篇核心调用参数 must contain 3-6 items")
    aux_params = re.search(r"(?ms)本篇辅助调用参数：\s*(.*?)(?=^本篇不调用参数：|\Z)", parameter_call)
    aux_count = count_numbered_items(aux_params.group(1) if aux_params else "")
    if aux_count < 2 or aux_count > 4:
        failures.append("本篇辅助调用参数 must contain 2-4 items")
    if "关注" in parameter_call:
        failures.append("关注 must not be used as a Zhihu production target")
    if "全部参数" in parameter_call or "均调用" in parameter_call:
        failures.append("质量参数调用 must not claim all parameters are called")

    focus_count = count_numbered_items(section(text, "本篇重点执行"))
    if focus_count < 5:
        failures.append("本篇重点执行 must contain at least 5 items")
    if focus_count > 10:
        failures.append("本篇重点执行 must contain no more than 10 items")

    structure = section(text, "正文结构")
    if count_numbered_items(structure) < 5:
        failures.append("正文结构 must contain at least 5 numbered items")

    writing_constraints = section(text, "写作约束")
    for item in CLAUDE_DIRECT_OUTPUT_REQUIREMENTS:
        if item not in writing_constraints:
            failures.append(f"写作约束 missing Claude direct-output requirement: {item}")
    for item in ["L2 只执行本卡", "两稿制", "首屏 150 字"]:
        if item not in writing_constraints:
            failures.append(f"写作约束 missing freeze/two-draft requirement: {item}")

    if len(text.splitlines()) > 120:
        failures.append("Production Card exceeds one page line budget")

    for token in FORBIDDEN_TOKENS:
        if token in text:
            failures.append(f"forbidden dispatcher token present: {token}")

    if failures:
        print("Fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
