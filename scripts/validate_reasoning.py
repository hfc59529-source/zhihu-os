#!/usr/bin/env python3
"""Validate a generated Zhihu article against Reasoning Protocol V1.0.

Usage:
  python3 scripts/validate_reasoning.py article.txt
  cat article.txt | python3 scripts/validate_reasoning.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ABSOLUTE_TOKENS = [
    "一定",
    "全部",
    "永远",
    "必然",
    "所有",
    "任何时候",
    "只要",
    "都会",
    "从来不会",
]

AI_PHRASES = [
    "本质就是",
    "本质上",
    "说白了",
    "归根结底",
    "真正的",
    "真正的问题是",
    "完全不是",
    "全部都是",
    "永远如此",
    "组织不会",
    "领导都会",
]

NUMBERED_LAYER_PATTERNS = [
    re.compile(r"第[一二三四五六七八九十]+层"),
    re.compile(r"第[一二三四五六七八九十]+个(?:原因|建议|前提|问题|机制|逻辑)"),
    re.compile(r"[一二三四五六七八九十]个(?:原因|建议|前提|问题|机制|逻辑)"),
]

LOW_CREDIBILITY_SCENES = [
    "所有领导",
    "每个老板",
    "全公司都",
    "一夜之间",
    "突然所有人",
    "普通员工掌握公司战略",
    "员工知道所有决策",
    "领导完全站在员工角度",
]

BACKSTAGE_TERMS = [
    "过程控制权",
    "利益结构",
    "风险传导",
    "博弈关系",
    "权力资源",
    "认知升级",
    "责任边界重构",
    "责任边界",
    "利益关系层",
    "人性博弈层",
    "认知升级层",
    "机制层",
    "PD-03",
    "PD-04",
    "PD-05",
    "PD-06",
    "PD-08",
]

PARAMETER_SECTION_PATTERNS = [
    re.compile(r"(?m)^#+\s*(?:PD|RR|RE|BT)-\d+"),
    re.compile(r"(?m)^(?:PD|RR|RE|BT)-\d+"),
    re.compile(r"(?m)^#+\s*(?:机制层|利益关系层|人性博弈层|认知升级层)"),
]

THREE_PARTY_ANALYSIS_PATTERNS = [
    re.compile(r"领导为什么"),
    re.compile(r"前接手者为什么"),
    re.compile(r"同事为什么"),
    re.compile(r"你为什么"),
]

MECHANISM_TOKENS = [
    "因为",
    "原因",
    "机制",
    "导致",
    "所以",
    "成本",
    "收益",
    "利益",
    "风险",
    "责任",
    "权力",
    "资源",
    "选择权",
    "评价权",
    "决策权",
]

SCENE_TOKENS = [
    "开会",
    "会议",
    "加班",
    "汇报",
    "晋升",
    "裁员",
    "KPI",
    "绩效",
    "同事",
    "老板",
    "领导",
    "工作群",
    "请假",
    "离职",
    "面试",
    "项目",
    "客户",
    "岗位",
    "工资",
]

CONCLUSION_HINTS = [
    "所以",
    "结论",
    "这意味着",
    "你要明白",
    "真正的问题",
    "关键不是",
    "核心不是",
    "核心在于",
]

CONCEPT_PATTERNS = [
    re.compile(r"([\u4e00-\u9fff]{2,8})(?:模型|机制|模式|系统|框架|账户|逻辑|结构|效应|路径)"),
    re.compile(r"“([^”]{2,12})”"),
    re.compile(r"「([^」]{2,12})」"),
]

COMMON_CONCEPT_WHITELIST = {
    "Production Card",
    "Claude",
    "知乎",
    "老板",
    "领导",
    "员工",
    "组织",
    "公司",
    "岗位",
    "绩效",
    "晋升",
    "汇报",
    "加班",
}


def read_input() -> str:
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).read_text(encoding="utf-8")
    return sys.stdin.read()


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def find_token_hits(text: str, tokens: list[str]) -> list[str]:
    hits: list[str] = []
    for token in tokens:
        for match in re.finditer(re.escape(token), text):
            hits.append(f"L{line_number(text, match.start())}: {token}")
    return hits


def split_paragraphs(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]


def extract_concepts(text: str) -> list[str]:
    concepts: list[str] = []
    for pattern in CONCEPT_PATTERNS:
        for match in pattern.finditer(text):
            concept = match.group(1).strip()
            if concept in COMMON_CONCEPT_WHITELIST:
                continue
            if len(concept) < 2:
                continue
            concepts.append(concept)
    return sorted(set(concepts))


def numbered_layer_failures(text: str) -> list[str]:
    hits: list[str] = []
    for pattern in NUMBERED_LAYER_PATTERNS:
        for match in pattern.finditer(text):
            hits.append(f"L{line_number(text, match.start())}: {match.group(0)}")
    if len(hits) >= 2:
        return hits
    return []


def consecutive_concept_definition_failures(paragraphs: list[str]) -> list[str]:
    failures: list[str] = []
    streak = 0
    start_idx = 0
    definition_markers = [
        "叫做",
        "就是",
        "意味着",
        "指的是",
        "可以理解为",
        "本质上",
        "真正的问题是",
    ]
    for idx, paragraph in enumerate(paragraphs, start=1):
        concepts = extract_concepts(paragraph)
        is_definition = bool(concepts) and any(marker in paragraph for marker in definition_markers)
        if is_definition:
            if streak == 0:
                start_idx = idx
            streak += 1
            if streak >= 2:
                failures.append(f"P{start_idx}-P{idx}: consecutive concept definitions")
        else:
            streak = 0
    return failures


def abstract_streak_failures(paragraphs: list[str]) -> list[str]:
    failures: list[str] = []
    streak = 0
    start_idx = 0
    for idx, paragraph in enumerate(paragraphs, start=1):
        has_mechanism = has_mechanism_support(paragraph)
        has_scene = any(token in paragraph for token in SCENE_TOKENS)
        is_abstract = has_mechanism and not has_scene
        if is_abstract:
            if streak == 0:
                start_idx = idx
            streak += 1
            if streak >= 3:
                failures.append(f"P{start_idx}-P{idx}: three or more abstract/mechanism paragraphs without scene support")
        else:
            streak = 0
    return failures


def count_concept_levels(concepts: list[str]) -> tuple[int, int, int]:
    level_1 = sum(1 for item in concepts if len(item) >= 7)
    level_2 = sum(1 for item in concepts if 4 <= len(item) <= 6)
    level_3 = sum(1 for item in concepts if len(item) <= 3)
    return level_1, level_2, level_3


def has_mechanism_support(paragraph: str) -> bool:
    return any(token in paragraph for token in MECHANISM_TOKENS)


def mechanism_failures(text: str) -> list[str]:
    failures: list[str] = []
    paragraphs = split_paragraphs(text)
    for idx, paragraph in enumerate(paragraphs, start=1):
        has_conclusion = any(token in paragraph for token in CONCLUSION_HINTS)
        if has_conclusion and not has_mechanism_support(paragraph):
            failures.append(f"P{idx}: conclusion-like paragraph lacks mechanism tokens")
    return failures


def role_failures(text: str) -> list[str]:
    patterns = [
        "领导站在员工角度",
        "老板站在员工角度",
        "员工知道组织",
        "员工掌握组织",
        "员工知道公司战略",
        "员工掌握公司战略",
        "组织觉得",
        "组织害怕",
        "组织喜欢",
    ]
    return find_token_hits(text, patterns)


def parameter_section_failures(text: str) -> list[str]:
    hits: list[str] = []
    for pattern in PARAMETER_SECTION_PATTERNS:
        for match in pattern.finditer(text):
            hits.append(f"L{line_number(text, match.start())}: {match.group(0)}")
    return hits


def three_party_analysis_failures(text: str) -> list[str]:
    hits: list[str] = []
    for pattern in THREE_PARTY_ANALYSIS_PATTERNS:
        for match in pattern.finditer(text):
            hits.append(f"L{line_number(text, match.start())}: {match.group(0)}")
    if len(hits) >= 3:
        return hits
    return []


def main() -> int:
    text = read_input().strip()
    failures: list[str] = []
    warnings: list[str] = []

    if not text:
        failures.append("article is empty")

    absolute_hits = find_token_hits(text, ABSOLUTE_TOKENS)
    if absolute_hits:
        failures.append("absolute reasoning tokens present: " + "; ".join(absolute_hits[:12]))

    ai_phrase_hits = find_token_hits(text, AI_PHRASES)
    if ai_phrase_hits:
        failures.append("AI phrase tokens present: " + "; ".join(ai_phrase_hits[:12]))

    not_but_hits = re.findall(r"不是[^。\n]{0,30}而是", text)
    if not_but_hits:
        failures.append("possible pseudo-contrarian pattern present: " + "; ".join(not_but_hits[:5]))

    scene_hits = find_token_hits(text, LOW_CREDIBILITY_SCENES)
    if scene_hits:
        failures.append("low-credibility scene tokens present: " + "; ".join(scene_hits[:12]))

    backstage_hits = find_token_hits(text, BACKSTAGE_TERMS)
    if backstage_hits:
        failures.append("backstage/system terms visible in article: " + "; ".join(backstage_hits[:12]))

    parameter_sections = parameter_section_failures(text)
    if parameter_sections:
        failures.append("parameter-like sectioning visible in article: " + "; ".join(parameter_sections[:12]))

    three_party_gaps = three_party_analysis_failures(text)
    if three_party_gaps:
        failures.append("three-party psychology analysis pattern present: " + "; ".join(three_party_gaps[:12]))

    mechanism_gaps = mechanism_failures(text)
    if mechanism_gaps:
        failures.append("mechanism support gaps: " + "; ".join(mechanism_gaps[:12]))

    paragraphs = split_paragraphs(text)

    layer_gaps = numbered_layer_failures(text)
    if layer_gaps:
        failures.append("RE-08 numbered layer/list structure present: " + "; ".join(layer_gaps[:12]))

    definition_gaps = consecutive_concept_definition_failures(paragraphs)
    if definition_gaps:
        failures.append("RE-08 consecutive concept definitions present: " + "; ".join(definition_gaps[:12]))

    abstract_gaps = abstract_streak_failures(paragraphs)
    if abstract_gaps:
        failures.append("Reasoning Protocol reality-first violation: " + "; ".join(abstract_gaps[:12]))

    role_gaps = role_failures(text)
    if role_gaps:
        failures.append("role consistency violations: " + "; ".join(role_gaps[:12]))

    concepts = extract_concepts(text)
    level_1, level_2, level_3 = count_concept_levels(concepts)
    if level_1 > 1 or level_2 > 3 or level_3 > 5:
        failures.append(
            "concept budget exceeded: "
            f"level1={level_1}/1, level2={level_2}/3, level3={level_3}/5; "
            f"concepts={', '.join(concepts[:20])}"
        )
    elif concepts:
        warnings.append(
            "concept budget observed: "
            f"level1={level_1}/1, level2={level_2}/3, level3={level_3}/5; "
            f"concepts={', '.join(concepts[:20])}"
        )

    if failures:
        print("Fail")
        for failure in failures:
            print(f"- {failure}")
        for warning in warnings:
            print(f"- warning: {warning}")
        return 1

    print("Pass")
    for warning in warnings:
        print(f"- warning: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
