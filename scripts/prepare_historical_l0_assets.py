#!/usr/bin/env python3
import csv
from pathlib import Path


INPUT = Path("data/l0_content_assets.csv")

BASE_FIELDS = [
    "article_id",
    "title",
    "content_type",
    "published_at",
    "url",
    "views",
    "likes",
    "comments",
    "favorites",
    "earnings",
    "earnings_per_1k_views",
    "historical_batch",
    "historical_source",
    "historical_completeness",
    "question_type",
    "structure_used",
    "primary_variable",
    "first_screen_type",
    "core_mechanism",
    "result_layer",
    "deep_review",
    "historical_rule_status",
    "evidence_level",
    "status",
    "sample_level",
    "upgrade_reason",
    "source",
    "collected_at",
    "notes",
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


def ratio(row):
    views = to_number(row.get("views", ""))
    earnings = to_number(row.get("earnings", ""))
    if not views or earnings is None:
        return ""
    return f"{earnings / views * 1000:.2f}"


def ranked_ids(rows, key, limit=20, reverse=True, exclude=None):
    exclude = exclude or set()
    sortable = []
    for row in rows:
        if row["article_id"] in exclude:
            continue
        value = key(row)
        if value is not None:
            sortable.append((value, row["article_id"]))
    return {article_id for _, article_id in sorted(sortable, reverse=reverse)[:limit]}


def main():
    rows = list(csv.DictReader(INPUT.open(newline="", encoding="utf-8")))
    current_fields = list(rows[0].keys()) if rows else BASE_FIELDS
    fieldnames = BASE_FIELDS + [field for field in current_fields if field not in BASE_FIELDS]

    for index, row in enumerate(rows):
        row.setdefault("historical_batch", f"HIST-{index // 50 + 1:02d}")
        row.setdefault("historical_source", row.get("source", ""))
        row.setdefault("historical_completeness", "")
        row.setdefault("question_type", "UNKNOWN")
        row.setdefault("structure_used", "UNKNOWN")
        row.setdefault("primary_variable", "UNKNOWN")
        row.setdefault("first_screen_type", "UNKNOWN")
        row.setdefault("core_mechanism", "UNKNOWN")
        row.setdefault("result_layer", "")
        row.setdefault("deep_review", "否")
        row.setdefault("historical_rule_status", "未提取")
        row.setdefault("evidence_level", "RAW")
        row["earnings_per_1k_views"] = ratio(row)

        has_result = row.get("views", "") != "" and row.get("earnings", "") != ""
        has_tags = all(row.get(field, "") not in {"", "UNKNOWN"} for field in [
            "question_type",
            "structure_used",
            "primary_variable",
            "first_screen_type",
            "core_mechanism",
        ])
        if has_result and has_tags:
            row["historical_completeness"] = "结果+标签完整"
        elif has_result:
            row["historical_completeness"] = "结果完整/标签待补"
        elif row.get("views", "") != "":
            row["historical_completeness"] = "阅读完整/收益待补"
        else:
            row["historical_completeness"] = "待补齐"

    high_earnings = ranked_ids(rows, lambda row: to_number(row.get("earnings", "")), 20)
    high_ratio = ranked_ids(rows, lambda row: to_number(row.get("earnings_per_1k_views", "")), 20)
    high_read_low_earnings = ranked_ids(
        rows,
        lambda row: to_number(row.get("views", "")) if to_number(row.get("earnings", "")) is not None else None,
        20,
        True,
        high_earnings,
    )
    low_result = ranked_ids(
        rows,
        lambda row: (
            -to_number(row.get("earnings", "")),
            -to_number(row.get("views", "")),
        ) if to_number(row.get("earnings", "")) is not None and to_number(row.get("views", "")) is not None else None,
        20,
    )

    for row in rows:
        layers = []
        if row["article_id"] in high_earnings:
            layers.append("A")
        if row["article_id"] in high_ratio:
            layers.append("B")
        if row["article_id"] in high_read_low_earnings:
            layers.append("C")
        if row["article_id"] in low_result:
            layers.append("D")
        row["result_layer"] = "+".join(layers)
        if layers:
            row["deep_review"] = "是"

    with INPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})

    print(f"prepared {len(rows)} rows in {INPUT}")


if __name__ == "__main__":
    main()
