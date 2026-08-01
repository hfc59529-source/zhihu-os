#!/usr/bin/env python3
"""Tests for Consistency Engine V2.0 validator."""

from __future__ import annotations

import unittest

from validate_consistency_engine import validate_hard_rules


ARTICLE = """
问题回应：PENDING
推理完整：PENDING
阅读顺畅：PENDING
可信度：PENDING

正文示例：
这篇回答围绕问题展开，解释读者为什么会卡住，并给出可执行判断。
"""


def card(
    monetization_marker: str = "☑",
    behavior_marker: str = "☑",
    forbidden_marker: str = "☑",
    monetization_goal: str = "阅读收益（广告/致知）",
    behavior_goal: str = "完读",
    revenue_path: str = "点开后被首屏反差留住，继续读到结尾并产生互动，形成阅读收益。",
    target_user: str = "对这个问题有现实困惑、需要快速看懂判断标准的知乎用户。",
    behavior_fields: str | None = None,
    extra_behavior_checked: str = "",
    include_monetization: bool = True,
) -> str:
    if behavior_fields is None:
        behavior_fields = """
行为动作理由：
用户会因为推理链完整、结尾有可迁移判断而愿意读完。

行为触发机制：
正文必须在中段持续制造因果追问，并在结尾回收核心判断。

触发机制位置：
主要落在第 2-5 段，结尾完成回收。
"""

    monetization_lines = [
        f"{monetization_marker} {monetization_goal}",
        "☐ 咨询转化",
        "☐ 好物带货",
        "☐ 产品付费（盐选/数字产品）",
        "☐ 账号积累（关注、长期资产）",
    ]
    if not include_monetization:
        monetization_lines[0] = f"☐ {monetization_goal}"

    behavior_lines = [
        "☐ 点开",
        f"{behavior_marker} {behavior_goal}",
        "☐ 点赞",
        "☐ 收藏",
        "☐ 评论",
        "☐ 转发",
        "☐ 关注",
        "☐ 点击链接",
        "☐ 咨询/私信",
        "☐ 购买",
    ]
    if extra_behavior_checked:
        behavior_lines.append(f"☑ {extra_behavior_checked}")

    return f"""
===Production Card Begin===
Claude版 Production Card

问题：
测试问题
问题链接：
https://www.zhihu.com/question/123456
平台：
知乎
题型：
认知判断

收益目标定义：

Monetization Goal：
（这篇文章最终要完成的商业目标）
{chr(10).join(monetization_lines)}

收益链路描述：
{revenue_path}

目标用户：
{target_user}

行为目标定义：

Primary Behavior Goal：
（为了完成收益目标，需要用户先产生什么行为）
{chr(10).join(behavior_lines)}
{behavior_fields}

禁止牺牲项：
（本文不能为了达成目标而降低的维度）
{forbidden_marker} 问题回应
☐ 推理完整
☐ 阅读顺畅
☐ 可信度
===Production Card End===
"""


def failure_codes(failures: list[str]) -> set[str]:
    return {failure.split(":", 1)[0] for failure in failures}


class ValidateConsistencyEngineTests(unittest.TestCase):
    def assert_passes(self, card_text: str) -> None:
        failures, checks, fields = validate_hard_rules(card_text, ARTICLE)
        self.assertEqual([], failures)
        self.assertEqual("PASS", checks["Monetization Goal"])
        self.assertEqual("PASS", checks["Primary Behavior Goal"])
        self.assertEqual("PASS", checks["Behavior-Revenue Alignment"])
        self.assertTrue(fields["monetization_goal"])
        self.assertTrue(fields["primary_goal"])

    def test_v32_valid_card_passes(self) -> None:
        self.assert_passes(card())

    def test_unchecked_options_do_not_count(self) -> None:
        failures, checks, fields = validate_hard_rules(card(), ARTICLE)
        self.assertEqual([], failures)
        self.assertEqual(["完读"], fields["primary_goals"])

    def test_checked_marker_variants_are_supported(self) -> None:
        self.assert_passes(
            card(
                monetization_marker="✅",
                behavior_marker="[X]",
                forbidden_marker="[x]",
            )
        )

    def test_multiple_primary_goals_fail(self) -> None:
        failures, _, _ = validate_hard_rules(card(extra_behavior_checked="收藏"), ARTICLE)
        self.assertIn("PRIMARY-GOAL-NOT-UNIQUE", failure_codes(failures))

    def test_missing_primary_goal_fails(self) -> None:
        failures, _, _ = validate_hard_rules(card(behavior_marker="☐"), ARTICLE)
        self.assertIn("PRIMARY-GOAL-MISSING", failure_codes(failures))

    def test_new_behavior_goal_is_recognized(self) -> None:
        self.assert_passes(
            card(
                monetization_goal="好物带货",
                behavior_goal="点击链接",
                revenue_path="识别需求后建立产品信任，引导用户点击链接并进入购买页面。",
            )
        )

    def test_v31_field_aliases_are_compatible(self) -> None:
        legacy_fields = """
目标动作理由：
用户会因为观点被准确表达而愿意点赞。

目标触发机制：
正文必须出现准确命名情绪和立场确认。

结果出现位置：
主要落在第 1 段和结尾。
"""
        self.assert_passes(card(behavior_goal="点赞", behavior_fields=legacy_fields))

    def test_forbidden_items_missing_fails(self) -> None:
        failures, _, _ = validate_hard_rules(card(forbidden_marker="☐"), ARTICLE)
        self.assertIn("FORBIDDEN-ITEMS-MISSING", failure_codes(failures))

    def test_monetization_goal_missing_fails(self) -> None:
        failures, _, _ = validate_hard_rules(card(include_monetization=False), ARTICLE)
        self.assertIn("MONETIZATION-GOAL-MISSING", failure_codes(failures))

    def test_behavior_revenue_misaligned_fails(self) -> None:
        failures, _, _ = validate_hard_rules(
            card(monetization_goal="好物带货", behavior_goal="评论"),
            ARTICLE,
        )
        self.assertIn("BEHAVIOR-REVENUE-MISALIGNED", failure_codes(failures))


if __name__ == "__main__":
    unittest.main()
