#!/usr/bin/env python3
"""Consistency Engine V2.0 - 收益目标 + 行为目标最终验收.

使用：
  python3 scripts/validate_consistency_engine.py article.txt card.txt
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


MONETIZATION_GOALS = [
    "阅读收益（广告/致知）",
    "咨询转化",
    "好物带货",
    "产品付费（盐选/数字产品）",
    "账号积累（关注、长期资产）",
]

BEHAVIOR_GOALS = [
    "点开",
    "完读",
    "点赞",
    "收藏",
    "评论",
    "转发",
    "关注",
    "点击链接",
    "咨询/私信",
    "购买",
]

BASIC_DIMENSIONS = [
    "问题回应",
    "推理完整",
    "阅读顺畅",
    "可信度",
]

FIELD_ALIASES = {
    "行为动作理由": ["行为动作理由", "目标动作理由"],
    "行为触发机制": ["行为触发机制", "目标触发机制"],
    "触发机制位置": ["触发机制位置", "结果出现位置"],
}

ALIGNMENT_RULES = {
    "阅读收益（广告/致知）": {"点开", "完读", "点赞", "收藏", "评论", "转发", "关注"},
    "咨询转化": {"咨询/私信", "关注", "点击链接"},
    "好物带货": {"购买", "点击链接", "咨询/私信"},
    "产品付费（盐选/数字产品）": {"购买", "点击链接", "咨询/私信", "收藏"},
    "账号积累（关注、长期资产）": {"关注", "点赞", "收藏", "评论", "转发", "完读"},
}

CHECKED_MARKERS = ("☑", "✅", "[x]", "[X]")
UNCHECKED_MARKERS = ("☐", "[ ]")


@dataclass
class ConsistencyReport:
    """一致性检查报告。"""

    overall: str
    monetization_goal: str
    revenue_path: str
    target_user: str
    primary_goal: str
    checks: dict[str, str]
    failures: list[str]
    ai_review_required: bool
    card_fields: dict[str, object]


def normalize_line_value(value: str) -> str:
    """去掉选项后的解释括号，保留正式枚举值。"""
    cleaned = value.strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned


def extract_card(raw_text: str) -> str:
    begin = "===Production Card Begin==="
    end = "===Production Card End==="
    if begin in raw_text and end in raw_text:
        start = raw_text.index(begin) + len(begin)
        stop = raw_text.index(end)
        if stop > start:
            return raw_text[start:stop].strip()
    return raw_text.strip()


def section(text: str, heading: str) -> str:
    lines = text.splitlines()
    start_index: int | None = None
    for index, line in enumerate(lines):
        if line.strip() == f"{heading}：":
            start_index = index + 1
            break
    if start_index is None:
        return ""

    collected: list[str] = []
    for line in lines[start_index:]:
        if re.match(r"^[A-Za-z0-9_ /（）()一-龥]+：\s*$", line.strip()):
            break
        collected.append(line)
    return "\n".join(collected).strip()


def field_value(text: str, field: str) -> str:
    return section(text, field)


def aliased_field_value(text: str, canonical_field: str) -> str:
    for alias in FIELD_ALIASES[canonical_field]:
        value = field_value(text, alias)
        if value:
            return value
    return ""


def is_checked_line(line: str) -> bool:
    stripped = line.strip()
    return any(stripped.startswith(marker) for marker in CHECKED_MARKERS)


def is_unchecked_line(line: str) -> bool:
    stripped = line.strip()
    return any(stripped.startswith(marker) for marker in UNCHECKED_MARKERS)


def option_value_from_line(line: str) -> str:
    stripped = line.strip()
    for marker in CHECKED_MARKERS + UNCHECKED_MARKERS:
        if stripped.startswith(marker):
            return normalize_line_value(stripped[len(marker) :])
    return ""


def checked_options(text: str, heading: str) -> list[str]:
    values = []
    for line in section(text, heading).splitlines():
        if is_checked_line(line):
            values.append(option_value_from_line(line))
    return values


def known_options_in_section(text: str, heading: str) -> list[str]:
    values = []
    for line in section(text, heading).splitlines():
        if is_checked_line(line) or is_unchecked_line(line):
            values.append(option_value_from_line(line))
    return values


def read_card_content(card_text: str) -> dict[str, object]:
    """从 Production Card 中提取 Consistency Engine V2.0 字段。"""
    text = extract_card(card_text)
    monetization_goals = checked_options(text, "Monetization Goal")
    behavior_goals = checked_options(text, "Primary Behavior Goal")
    forbidden_items = checked_options(text, "禁止牺牲项")

    return {
        "monetization_goals": monetization_goals,
        "primary_goals": behavior_goals,
        "monetization_goal": monetization_goals[0] if len(monetization_goals) == 1 else "",
        "primary_goal": behavior_goals[0] if len(behavior_goals) == 1 else "",
        "revenue_path": field_value(text, "收益链路描述"),
        "target_user": field_value(text, "目标用户"),
        "behavior_reason": aliased_field_value(text, "行为动作理由"),
        "trigger_mechanism": aliased_field_value(text, "行为触发机制"),
        "trigger_position": aliased_field_value(text, "触发机制位置"),
        "forbidden_items": forbidden_items,
        "known_monetization_options": known_options_in_section(text, "Monetization Goal"),
        "known_behavior_options": known_options_in_section(text, "Primary Behavior Goal"),
    }


def blank_or_placeholder(value: object) -> bool:
    text = str(value or "").strip()
    if not text:
        return True
    placeholder_patterns = [
        r"^（.*）$",
        r"^\(.*\)$",
        r"^TODO$",
        r"^待填$",
        r"^待补充$",
    ]
    return any(re.match(pattern, text, flags=re.I) for pattern in placeholder_patterns)


def validate_goal_uniqueness(
    selected: list[str],
    allowed: list[str],
    missing_code: str,
    not_unique_code: str,
    unknown_code: str,
    label: str,
    failures: list[str],
    checks: dict[str, str],
) -> None:
    if not selected:
        failures.append(f"{missing_code}: {label} 未勾选")
        checks[label] = "FAIL"
        return
    if len(selected) != 1:
        failures.append(f"{not_unique_code}: 找到 {len(selected)} 个已勾选项（应为 1 个）")
        checks[label] = "FAIL"
        return
    if selected[0] not in allowed:
        failures.append(f"{unknown_code}: {selected[0]} 不在允许列表中")
        checks[label] = "FAIL"
        return
    checks[label] = "PASS"


def validate_alignment(monetization_goal: str, behavior_goal: str) -> bool:
    allowed = ALIGNMENT_RULES.get(monetization_goal, set())
    return behavior_goal in allowed


def validate_hard_rules(card_text: str, article_text: str) -> tuple[list[str], dict[str, str], dict[str, object]]:
    """执行 V2.0 硬规则检查。"""
    failures: list[str] = []
    checks: dict[str, str] = {}
    card_fields = read_card_content(card_text)

    validate_goal_uniqueness(
        card_fields["monetization_goals"],
        MONETIZATION_GOALS,
        "MONETIZATION-GOAL-MISSING",
        "MONETIZATION-GOAL-NOT-UNIQUE",
        "MONETIZATION-GOAL-UNKNOWN",
        "Monetization Goal",
        failures,
        checks,
    )

    validate_goal_uniqueness(
        card_fields["primary_goals"],
        BEHAVIOR_GOALS,
        "PRIMARY-GOAL-MISSING",
        "PRIMARY-GOAL-NOT-UNIQUE",
        "PRIMARY-GOAL-UNKNOWN",
        "Primary Behavior Goal",
        failures,
        checks,
    )

    if blank_or_placeholder(card_fields["revenue_path"]):
        failures.append("REVENUE-PATH-MISSING: 收益链路描述未填写")
        checks["Revenue Path"] = "FAIL"
    else:
        checks["Revenue Path"] = "PASS"

    if blank_or_placeholder(card_fields["target_user"]):
        failures.append("TARGET-USER-MISSING: 目标用户未填写")
        checks["Target User"] = "FAIL"
    else:
        checks["Target User"] = "PASS"

    required_behavior_fields = {
        "行为动作理由": "behavior_reason",
        "行为触发机制": "trigger_mechanism",
        "触发机制位置": "trigger_position",
    }
    for label, key in required_behavior_fields.items():
        if blank_or_placeholder(card_fields[key]):
            failures.append(f"GOAL-FIELD-INCOMPLETE: {label} 未填写")
            checks[label] = "FAIL"
        else:
            checks[label] = "PASS"

    forbidden_items = card_fields["forbidden_items"]
    if not forbidden_items:
        failures.append("FORBIDDEN-ITEMS-MISSING: 未标记禁止牺牲项")
        checks["Forbidden Items"] = "FAIL"
    else:
        checks["Forbidden Items"] = "PASS"

    monetization_goal = str(card_fields["monetization_goal"])
    behavior_goal = str(card_fields["primary_goal"])
    if monetization_goal and behavior_goal:
        if validate_alignment(monetization_goal, behavior_goal):
            checks["Behavior-Revenue Alignment"] = "PASS"
        else:
            failures.append(
                "BEHAVIOR-REVENUE-MISALIGNED: "
                f"{monetization_goal} 与 {behavior_goal} 没有硬规则认可的转化路径"
            )
            checks["Behavior-Revenue Alignment"] = "FAIL"
    else:
        checks["Behavior-Revenue Alignment"] = "SKIP"

    for dim in BASIC_DIMENSIONS:
        if dim in article_text or dim in card_text:
            checks[f"Basic: {dim}"] = "PENDING"
        else:
            failures.append(f"BASIC-DIMENSION-MISSING: {dim} 在 Card 或 Article 中无记录")
            checks[f"Basic: {dim}"] = "FAIL"

    unhandled_fails = re.findall(r"(?m)^.*?：\s*FAIL(?!\s*→).*$", article_text)
    if unhandled_fails:
        failures.append(f"UNHANDLED-FAIL: 存在 {len(unhandled_fails)} 个未处理的失败记录")
        checks["Unhandled Failures"] = "FAIL"
    else:
        checks["Unhandled Failures"] = "PASS"

    return failures, checks, card_fields


def generate_ai_review_checklist(card_fields: dict[str, object]) -> str:
    monetization_goal = card_fields.get("monetization_goal", "未知")
    behavior_goal = card_fields.get("primary_goal", "未知")

    return f"""
## AI 审核检查清单

Monetization Goal: {monetization_goal}
Primary Behavior Goal: {behavior_goal}

### 1. 收益目标合理性
- [ ] 收益目标是否匹配题目和作者能力？
- [ ] 收益链路是否可信、完整、可执行？
  收益链路：{card_fields.get('revenue_path', '未填')}

### 2. 行为目标对齐
- [ ] 用户行为是否真的能推进收益目标？
- [ ] 是否存在更适合该收益目标的 Behavior Goal？

### 3. 机制真实性
- [ ] 行为触发机制是否真正进入正文？
  触发机制：{card_fields.get('trigger_mechanism', '未填')}
- [ ] 触发机制是否出现在指定位置？
  指定位置：{card_fields.get('trigger_position', '未填')}

### 4. 收益链路可执行性
- [ ] 正文是否完成收益链路中的每一步？
- [ ] 最后一跳转化是否存在断层？

### 5. 维度冲突
- [ ] 是否为了收益目标牺牲禁止牺牲项？
- [ ] 基础维度是否互相支持？

### 6. 目标实现质量
- [ ] 正文促成目标行为的强度是否至少达到“中”？

### 7. 失败段落定位
- [ ] 如有失败，具体是哪一段出现问题？
- [ ] 是内容问题、表达问题，还是收益链路问题？
"""


def format_output(report: ConsistencyReport) -> str:
    output = f"""
╔════════════════════════════════════════════════════════════╗
║         Consistency Engine 最终验收报告 V2.0               ║
╚════════════════════════════════════════════════════════════╝

Overall：{report.overall}

Monetization Goal：{report.monetization_goal or 'UNKNOWN'}
收益链路：{report.revenue_path or 'UNKNOWN'}
目标用户：{report.target_user or 'UNKNOWN'}
Primary Behavior Goal：{report.primary_goal or 'UNKNOWN'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

收益层检查：
  Monetization Goal Clarity：{report.checks.get('Monetization Goal', 'N/A')}
  Revenue Path：{report.checks.get('Revenue Path', 'N/A')}
  Target User：{report.checks.get('Target User', 'N/A')}
  Behavior-Revenue Alignment：{report.checks.get('Behavior-Revenue Alignment', 'N/A')}

行为层检查：
  Primary Behavior Goal：{report.checks.get('Primary Behavior Goal', 'N/A')}
  行为动作理由：{report.checks.get('行为动作理由', 'N/A')}
  行为触发机制：{report.checks.get('行为触发机制', 'N/A')}
  触发机制位置：{report.checks.get('触发机制位置', 'N/A')}
  Forbidden Items：{report.checks.get('Forbidden Items', 'N/A')}

基础维度检查：
"""

    for dim in BASIC_DIMENSIONS:
        result = report.checks.get(f"Basic: {dim}", "N/A")
        output += f"  {dim}：{result}\n"

    output += f"\nOther：{report.checks.get('Unhandled Failures', 'N/A')}\n"

    if report.failures:
        output += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

硬规则失败（{len(report.failures)} 项）：

"""
        for failure in report.failures:
            output += f"  ✗ {failure}\n"

    if report.ai_review_required:
        output += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AI 审核项（需要人工或 AI 语义判断）：
"""
        output += generate_ai_review_checklist(report.card_fields)

    return output


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 0

    article_path = Path(sys.argv[1])
    card_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    try:
        article_text = article_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: {article_path} not found")
        return 1

    card_text = ""
    if card_path:
        try:
            card_text = card_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            print(f"Warning: {card_path} not found, skipping card validation")

    failures, checks, card_fields = validate_hard_rules(card_text, article_text)
    report = ConsistencyReport(
        overall="FAIL" if failures else "PENDING",
        monetization_goal=str(card_fields.get("monetization_goal", "")),
        revenue_path=str(card_fields.get("revenue_path", "")),
        target_user=str(card_fields.get("target_user", "")),
        primary_goal=str(card_fields.get("primary_goal", "")),
        checks=checks,
        failures=failures,
        ai_review_required=not failures,
        card_fields=card_fields,
    )

    print(format_output(report))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
