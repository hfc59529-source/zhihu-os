#!/usr/bin/env python3
import argparse
import csv
import re
from collections import Counter
from pathlib import Path


INPUT = Path("data/l0_content_assets.csv")

STOPWORDS = set("为什么什么到底一个一些越来越是不是有没有如何怎么哪些以及还是我们他们你我他她的了在和与或就都很也更不没会能")
DOMAIN_KEYWORDS = [
    "领导",
    "员工",
    "培养",
    "提拔",
    "晋升",
    "管理",
    "中层",
    "组织",
    "公司",
    "老板",
    "风险",
    "责任",
    "信任",
    "利益",
    "基层",
    "职场",
    "能力",
    "离职",
    "跳槽",
    "成本",
]


def to_number(value):
    if value == "":
        return None
    text = value.replace(",", "").strip()
    if text.endswith("万"):
        return float(text[:-1]) * 10000
    if text.endswith(("k", "K")):
        return float(text[:-1]) * 1000
    return float(text)


def tokenize(text):
    text = re.sub(r"\s+", "", text)
    tokens = []
    for size in (2, 3, 4):
        tokens.extend(text[index : index + size] for index in range(max(0, len(text) - size + 1)))
    tokens.extend(char for char in text if "\u4e00" <= char <= "\u9fff" and char not in STOPWORDS)
    return Counter(tokens)


def similarity(query_tokens, title):
    title_tokens = tokenize(title)
    if not query_tokens or not title_tokens:
        return 0
    overlap = sum(min(count, title_tokens[token]) for token, count in query_tokens.items())
    keyword_hits = sum(1 for word in DOMAIN_KEYWORDS if word in title and query_tokens.get(word, 0))
    return overlap / max(1, sum(query_tokens.values())) + keyword_hits * 0.12


def fmt_number(value):
    number = to_number(value)
    if number is None:
        return ""
    if number >= 10000:
        return f"{number / 10000:.1f}万"
    return str(int(number) if number.is_integer() else round(number, 2))


def top_row(rows, field):
    sortable = [(to_number(row.get(field, "")), row) for row in rows if to_number(row.get(field, "")) is not None]
    return max(sortable, key=lambda item: item[0])[1] if sortable else None


def low_earnings_row(rows):
    sortable = []
    for row in rows:
        earnings = to_number(row.get("earnings", ""))
        views = to_number(row.get("views", ""))
        if earnings is not None and views is not None:
            sortable.append((earnings, -views, row))
    return min(sortable, key=lambda item: (item[0], item[1]))[2] if sortable else None


def known_values(rows, field):
    values = [
        row.get(field, "")
        for row in rows
        if row.get(field, "") not in {"", "UNKNOWN"}
    ]
    return Counter(values).most_common(5)


def row_line(row, include_score=False):
    parts = [row["title"]]
    if include_score:
        parts.append(f"相似度 {row['_score']:.2f}")
    parts.extend([
        f"阅读 {fmt_number(row.get('views', '')) or '未知'}",
        f"收益 {fmt_number(row.get('earnings', '')) or '未知'}",
        f"千阅收益 {row.get('earnings_per_1k_views') or '未知'}",
        f"分层 {row.get('result_layer') or '未分层'}",
    ])
    return "；".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Search L0 historical Zhihu assets before COMPILE generates Execution IR.")
    parser.add_argument("question", help="知乎问题标题")
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rows = list(csv.DictReader(INPUT.open(newline="", encoding="utf-8")))
    query_tokens = tokenize(args.question)
    scored = []
    for row in rows:
        score = similarity(query_tokens, row.get("title", ""))
        if score > 0:
            item = row.copy()
            item["_score"] = score
            scored.append(item)
    matches = sorted(
        scored,
        key=lambda row: (
            row["_score"],
            to_number(row.get("earnings", "")) or -1,
            to_number(row.get("views", "")) or -1,
        ),
        reverse=True,
    )[: args.limit]

    highest_earnings = top_row(matches, "earnings")
    highest_ratio = top_row(matches, "earnings_per_1k_views")
    lowest = low_earnings_row(matches)
    structures = known_values(matches, "structure_used")
    variables = known_values(matches, "primary_variable")
    mechanisms = known_values(matches, "core_mechanism")
    earnings_known = [row for row in matches if row.get("earnings", "") != ""]
    high_view_low_earnings = [row for row in matches if "C" in row.get("result_layer", "")]

    lines = [
        "==========历史资产命中==========",
        f"输入问题：{args.question}",
        f"检索范围：L0内容资产 {len(rows)}篇",
        f"历史命中：{len(matches)}篇",
        "",
        "最相似：",
    ]
    if matches:
        lines.extend(f"- {row_line(row, True)}" for row in matches[:5])
    else:
        lines.append("- 无")

    lines.extend(["", "最高收益："])
    lines.append(f"- {row_line(highest_earnings)}" if highest_earnings else "- 收益证据不足")
    lines.extend(["", "最高千阅读："])
    lines.append(f"- {row_line(highest_ratio)}" if highest_ratio else "- 千阅读收益证据不足")
    lines.extend(["", "最低收益："])
    lines.append(f"- {row_line(lowest)}" if lowest else "- 收益证据不足")

    lines.extend(["", "推荐结构："])
    if structures:
        lines.extend(f"- {value}：{count}篇命中" for value, count in structures)
    else:
        lines.append("- UNKNOWN：历史标签证据不足，需由ACTIVE结构库决定")

    lines.extend(["", "推荐变量："])
    if variables:
        lines.extend(f"- {value}：{count}篇命中" for value, count in variables)
    else:
        lines.append("- UNKNOWN：历史标签证据不足，需由ACTIVE变量/参数判断")

    lines.extend(["", "共同机制："])
    if mechanisms:
        lines.extend(f"- {value}：{count}篇命中" for value, count in mechanisms)
    else:
        lines.append("- UNKNOWN：历史机制标签不足")

    risk = []
    if not matches:
        risk.append("历史相似样本不足，不能把历史资产作为主证据。")
    if len(earnings_known) < 3:
        risk.append("命中样本收益覆盖不足，收益判断仅作弱参考。")
    if high_view_low_earnings:
        risk.append(f"存在{len(high_view_low_earnings)}篇C层高阅读低收益样本，需警惕只做阅读不做收益。")
    if not structures or not variables:
        risk.append("结构/变量字段仍为UNKNOWN，不能替代ACTIVE结构与变量选择。")
    if not risk:
        risk.append("无明显历史风险；仍需通过ACTIVE与17维参数审计。")

    lines.extend(["", "历史风险："])
    lines.extend(f"- {item}" for item in risk)
    lines.extend([
        "",
        "是否建议进入COMPILE：YES" if matches else "是否建议进入COMPILE：NO",
        "使用边界：历史资产只提供证据摘要；不得直接升级ACTIVE，不得替代runtime ACTIVE快照。",
    ])

    output = "\n".join(lines) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    print(output, end="")


if __name__ == "__main__":
    main()
