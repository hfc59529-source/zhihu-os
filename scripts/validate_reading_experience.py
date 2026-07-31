#!/usr/bin/env python3
"""Programmatic RR reading-experience checks for Zhihu articles.

This script only reports measurable signals. Semantic checks such as unique
main judgment, whether a scene truly aids understanding, or ordinary-reader
comprehension must remain in AI QA.

Usage:
  python3 scripts/validate_reading_experience.py article.txt
  cat article.txt | python3 scripts/validate_reading_experience.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


SCENE_TOKENS = [
    "领导", "老板", "同事", "员工", "客户", "会议", "开会", "纪要", "邮件", "工作群",
    "群里", "汇报", "项目", "绩效", "复盘", "执行", "签字", "确认", "办公室",
]

ACTION_TOKENS = [
    "开口", "沉默", "点头", "回复", "转发", "确认", "签字", "执行", "汇报", "修改",
    "追责", "抄送", "推进", "补充", "低头", "看电脑", "发出来",
]

ABSTRACT_TOKENS = [
    "权力", "资源", "责任", "成本", "收益", "利益", "博弈", "共识", "风险", "边界",
    "结构", "机制", "传导", "激励", "组织", "认知", "变量", "规律", "配置", "分配",
]

CAUSE_TOKENS = [
    "因为", "所以", "因此", "于是", "导致", "这意味着", "进一步说", "真正的问题是",
    "本质上", "归根结底", "换句话说",
]

TRAINING_PATTERNS = [
    r"第一步", r"第二步", r"第三步", r"机制一", r"机制二", r"机制三",
    r"第一[，、]", r"第二[，、]", r"第三[，、]",
]


def read_input() -> str:
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).read_text(encoding="utf-8")
    return sys.stdin.read()


def split_paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[。！？!?])", text) if s.strip()]


def has_any(text: str, tokens: list[str]) -> bool:
    return any(token in text for token in tokens)


def max_streak(flags: list[bool]) -> int:
    best = 0
    current = 0
    for flag in flags:
        if flag:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def count_windows(text: str, tokens: list[str], window_size: int, threshold: int) -> int:
    compact = re.sub(r"\s+", "", text)
    if not compact:
        return 0
    hits = 0
    for start in range(0, max(1, len(compact) - window_size + 1), max(1, window_size // 2)):
        window = compact[start : start + window_size]
        count = sum(window.count(token) for token in tokens)
        if count >= threshold:
            hits += 1
    return hits


def paragraph_length_cv(paragraphs: list[str]) -> float:
    lengths = [len(re.sub(r"\s+", "", p)) for p in paragraphs if p.strip()]
    if not lengths:
        return 0.0
    mean = sum(lengths) / len(lengths)
    if mean == 0:
        return 0.0
    variance = sum((item - mean) ** 2 for item in lengths) / len(lengths)
    return (variance ** 0.5) / mean


def main() -> int:
    text = read_input()
    paragraphs = split_paragraphs(text)
    sentences = split_sentences(text)

    no_scene_flags = [not has_any(p, SCENE_TOKENS + ACTION_TOKENS) for p in paragraphs]
    explanation_flags = [has_any(p, CAUSE_TOKENS) for p in paragraphs]
    abstract_flags = [has_any(p, ABSTRACT_TOKENS) and not has_any(p, SCENE_TOKENS + ACTION_TOKENS) for p in paragraphs]

    long_60 = [s for s in sentences if len(re.sub(r"\s+", "", s)) > 60]
    long_80 = [s for s in sentences if len(re.sub(r"\s+", "", s)) > 80]
    scene_count = sum(1 for p in paragraphs if has_any(p, SCENE_TOKENS))
    action_count = sum(1 for p in paragraphs if has_any(p, ACTION_TOKENS))
    training_hits = sum(len(re.findall(pattern, text)) for pattern in TRAINING_PATTERNS)
    abstract_windows = count_windows(text, ABSTRACT_TOKENS, 150, 6)
    one_sentence_paragraphs = sum(1 for p in paragraphs if len(split_sentences(p)) <= 1)
    cv = paragraph_length_cv(paragraphs)
    title_count = sum(1 for line in text.splitlines() if line.strip().startswith("#"))

    risks: list[str] = []
    if max_streak(no_scene_flags) >= 3:
        risks.append("HIGH: 连续 3 段没有人物、动作、场景或具体对象")
    if max_streak(explanation_flags) >= 3:
        risks.append("HIGH: 连续 3 段均以因果解释为主")
    if abstract_windows:
        risks.append("HIGH: 存在连续 150 字内 6 个以上抽象概念")
    if len(long_60) > 5 or len(long_80) > 2:
        risks.append("MEDIUM: 长句疲劳")
    if len(re.sub(r'\\s+', '', text)) >= 1500 and scene_count < 2:
        risks.append("MEDIUM: 1500 字以上正文少于 2 个现实场景")
    if training_hits >= 3:
        risks.append("MEDIUM: 培训式表达频率偏高")
    if paragraphs and one_sentence_paragraphs / len(paragraphs) > 0.7:
        risks.append("MEDIUM: 一句话一段比例过高")
    if paragraphs and cv < 0.25 and len(paragraphs) >= 8:
        risks.append("MEDIUM: 段落长度高度接近")

    print("# RR Programmatic Report")
    print(f"paragraphs: {len(paragraphs)}")
    print(f"sentences: {len(sentences)}")
    print(f"scene_paragraphs: {scene_count}")
    print(f"action_paragraphs: {action_count}")
    print(f"max_no_scene_streak: {max_streak(no_scene_flags)}")
    print(f"max_explanation_streak: {max_streak(explanation_flags)}")
    print(f"max_abstract_no_scene_streak: {max_streak(abstract_flags)}")
    print(f"long_sentences_gt_60: {len(long_60)}")
    print(f"long_sentences_gt_80: {len(long_80)}")
    print(f"abstract_dense_windows: {abstract_windows}")
    print(f"training_expression_hits: {training_hits}")
    print(f"one_sentence_paragraph_ratio: {one_sentence_paragraphs / len(paragraphs):.2f}" if paragraphs else "one_sentence_paragraph_ratio: 0.00")
    print(f"paragraph_length_cv: {cv:.2f}")
    print(f"title_count: {title_count}")
    print("risks:")
    if risks:
        for risk in risks:
            print(f"- {risk}")
    else:
        print("- none")

    return 1 if any(risk.startswith("HIGH") for risk in risks) else 0


if __name__ == "__main__":
    raise SystemExit(main())
