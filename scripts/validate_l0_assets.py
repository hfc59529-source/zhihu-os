#!/usr/bin/env python3
import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

REQUIRED_FIELDS = [
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

NUMERIC_FIELDS = ["views", "likes", "comments", "favorites", "earnings", "earnings_per_1k_views"]
EVIDENCE_LEVELS = {"RAW", "CANDIDATE", "REVIEW", "ACTIVE"}
HISTORICAL_RULE_STATUSES = {"未提取", "候选规律", "05.5验证中", "已进入ACTIVE"}
DEEP_REVIEW_VALUES = {"是", "否"}


def parse_number(value):
    if value == "":
        return None
    text = value.replace(",", "").strip()
    multipliers = {"万": 10000, "k": 1000, "K": 1000}
    for suffix, multiplier in multipliers.items():
        if text.endswith(suffix):
            return float(text[: -len(suffix)]) * multiplier
    return float(text)


def main():
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "data/l0_content_assets.csv")
    rows = list(csv.DictReader(path.open(newline="", encoding="utf-8")))
    fields = rows[0].keys() if rows else csv.DictReader(path.open(newline="", encoding="utf-8")).fieldnames

    missing_fields = [field for field in REQUIRED_FIELDS if field not in (fields or [])]
    duplicate_ids = sorted({row["article_id"] for row in rows if row["article_id"] and sum(r["article_id"] == row["article_id"] for r in rows) > 1})
    missing_required_values = [
        (idx + 2, field)
        for idx, row in enumerate(rows)
        for field in ["article_id", "title", "content_type", "published_at", "status", "sample_level", "source", "collected_at"]
        if row.get(field, "") == ""
    ]

    numeric_errors = []
    for idx, row in enumerate(rows):
        for field in NUMERIC_FIELDS:
            try:
                parse_number(row.get(field, ""))
            except ValueError:
                numeric_errors.append((idx + 2, field, row.get(field, "")))

    enum_errors = []
    for idx, row in enumerate(rows):
        evidence_level = row.get("evidence_level", "")
        if evidence_level not in EVIDENCE_LEVELS:
            enum_errors.append((idx + 2, "evidence_level", evidence_level))
        rule_status = row.get("historical_rule_status", "")
        if rule_status not in HISTORICAL_RULE_STATUSES:
            enum_errors.append((idx + 2, "historical_rule_status", rule_status))
        deep_review = row.get("deep_review", "")
        if deep_review not in DEEP_REVIEW_VALUES:
            enum_errors.append((idx + 2, "deep_review", deep_review))

    type_counts = Counter(row.get("content_type", "") or "<EMPTY>" for row in rows)
    null_counts = {
        field: sum(1 for row in rows if row.get(field, "") == "")
        for field in REQUIRED_FIELDS
    }
    null_by_type = defaultdict(lambda: Counter())
    for row in rows:
        content_type = row.get("content_type", "") or "<EMPTY>"
        for field in REQUIRED_FIELDS:
            if row.get(field, "") == "":
                null_by_type[field][content_type] += 1

    anomaly_warnings = []
    for row_index, row in enumerate(rows, start=2):
        content_type = row.get("content_type", "")
        if content_type in {"回答", "文章", "视频"} and row.get("favorites", "") == "":
            anomaly_warnings.append((row_index, "favorites", content_type, row.get("article_id", "")))
        if row.get("views", "") == "":
            anomaly_warnings.append((row_index, "views", content_type, row.get("article_id", "")))

    print(f"file: {path}")
    print(f"rows: {len(rows)}")
    print(f"missing_fields: {missing_fields or 'OK'}")
    print(f"duplicate_article_ids: {duplicate_ids or 'OK'}")
    print(f"missing_required_values: {missing_required_values or 'OK'}")
    print(f"numeric_sortable: {'OK' if not numeric_errors else numeric_errors}")
    print(f"enum_values: {'OK' if not enum_errors else enum_errors}")
    print("content_types:")
    for content_type, count in sorted(type_counts.items()):
        print(f"  {content_type}: {count}")
    print("null_counts:")
    for field in REQUIRED_FIELDS:
        count = null_counts[field]
        if count:
            by_type = ", ".join(f"{content_type}:{type_count}" for content_type, type_count in sorted(null_by_type[field].items()))
            print(f"  {field}: {count} ({by_type})")
    print(f"anomaly_warnings: {anomaly_warnings or 'OK'}")

    if missing_fields or duplicate_ids or missing_required_values or numeric_errors or enum_errors or anomaly_warnings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
