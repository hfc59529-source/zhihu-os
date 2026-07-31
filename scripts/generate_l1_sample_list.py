#!/usr/bin/env python3
import csv
from collections import defaultdict
from pathlib import Path


INPUT = Path("data/l0_content_assets.csv")
OUTPUT = Path("data/l1_sample_list.csv")
REPORT = Path("reports/l1_sample_report.md")


def to_number(value):
    if value == "":
        return None
    text = value.replace(",", "").strip()
    if text.endswith("万"):
        return float(text[:-1]) * 10000
    return float(text)


def earnings_per_1k(row):
    views = to_number(row.get("views", ""))
    earnings = to_number(row.get("earnings", ""))
    if not views or earnings is None:
        return None
    return earnings / views * 1000


def is_recent(row):
    published = row["published_at"]
    return (
        "小时前" in published
        or "07-27" in published
        or "07-26" in published
        or "07-25" in published
        or "07-24" in published
        or "07-23" in published
        or "07-22" in published
        or "07-21" in published
    )


def add_samples(sample_reasons, rows, reason, sort_field, limit=5, reverse=True):
    sortable = []
    for row in rows:
        value = to_number(row.get(sort_field, ""))
        if value is not None:
            sortable.append((value, row))
    selected = sorted(sortable, key=lambda item: item[0], reverse=reverse)[:limit]
    for _, row in selected:
        sample_reasons[row["article_id"]].add(reason)
    return [row["article_id"] for _, row in selected]


def add_ratio_samples(sample_reasons, rows, reason, limit=20):
    sortable = []
    for row in rows:
        value = earnings_per_1k(row)
        if value is not None:
            sortable.append((value, row))
    selected = sorted(sortable, key=lambda item: item[0], reverse=True)[:limit]
    for _, row in selected:
        sample_reasons[row["article_id"]].add(reason)
    return [row["article_id"] for _, row in selected]


def main():
    rows = list(csv.DictReader(INPUT.open(newline="", encoding="utf-8")))
    by_id = {row["article_id"]: row for row in rows}
    sample_reasons = defaultdict(set)
    candidates_by_group = {}

    candidates_by_group["高阅读TOP5"] = add_samples(sample_reasons, rows, "高阅读TOP5", "views", 5)
    candidates_by_group["高收藏TOP5"] = add_samples(sample_reasons, rows, "高收藏TOP5", "favorites", 5)
    candidates_by_group["高收益TOP5"] = add_samples(sample_reasons, rows, "高收益TOP5", "earnings", 5)
    candidates_by_group["A层-高收益TOP20"] = add_samples(sample_reasons, rows, "A层-高收益TOP20", "earnings", 20)
    candidates_by_group["B层-高千阅读收益TOP20"] = add_ratio_samples(sample_reasons, rows, "B层-高千阅读收益TOP20", 20)

    recent_rows = [row for row in rows if is_recent(row)]
    candidates_by_group["最近7天TOP5"] = add_samples(sample_reasons, recent_rows, "最近7天TOP5", "views", 5)

    abnormal_candidates = []
    for row in rows:
        views = to_number(row["views"])
        favorites = to_number(row["favorites"])
        if views and favorites is not None and views >= 50:
            abnormal_candidates.append((favorites / views, row))
    abnormal_selected = sorted(abnormal_candidates, key=lambda item: item[0], reverse=True)[:5]
    candidates_by_group["异常样本TOP5-高收藏率"] = [row["article_id"] for _, row in abnormal_selected]
    for _, row in abnormal_selected:
        sample_reasons[row["article_id"]].add("异常样本TOP5-高收藏率")

    low_view_high_earnings = []
    for row in rows:
        views = to_number(row["views"])
        earnings = to_number(row["earnings"])
        if views and earnings is not None:
            low_view_high_earnings.append((earnings / views, row))
    low_view_high_earnings_selected = sorted(low_view_high_earnings, key=lambda item: item[0], reverse=True)[:5]
    candidates_by_group["低阅读高收益TOP5"] = [row["article_id"] for _, row in low_view_high_earnings_selected]
    for _, row in low_view_high_earnings_selected:
        sample_reasons[row["article_id"]].add("低阅读高收益TOP5")

    high_earnings_ids = set(candidates_by_group["A层-高收益TOP20"])
    high_read_low_earnings_candidates = []
    for row in rows:
        if row["article_id"] in high_earnings_ids:
            continue
        views = to_number(row.get("views", ""))
        earnings = to_number(row.get("earnings", ""))
        if views is not None and earnings is not None:
            high_read_low_earnings_candidates.append((views, row))
    high_read_low_earnings_selected = sorted(high_read_low_earnings_candidates, key=lambda item: item[0], reverse=True)[:20]
    candidates_by_group["C层-高阅读低收益TOP20"] = [row["article_id"] for _, row in high_read_low_earnings_selected]
    for _, row in high_read_low_earnings_selected:
        sample_reasons[row["article_id"]].add("C层-高阅读低收益TOP20")

    low_result_candidates = []
    for row in rows:
        views = to_number(row.get("views", ""))
        earnings = to_number(row.get("earnings", ""))
        if views is not None and earnings is not None:
            low_result_candidates.append((views, earnings, row))
    low_result_selected = sorted(low_result_candidates, key=lambda item: (item[1], item[0]))[:20]
    candidates_by_group["D层-低阅读低收益TOP20"] = [row["article_id"] for _, _, row in low_result_selected]
    for _, _, row in low_result_selected:
        sample_reasons[row["article_id"]].add("D层-低阅读低收益TOP20")

    headers = [
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
        "result_layer",
        "evidence_level",
        "sample_level",
        "upgrade_reason",
        "notes",
    ]

    sampled_rows = []
    for article_id, reasons in sorted(sample_reasons.items(), key=lambda item: by_id[item[0]]["published_at"], reverse=True):
        row = by_id[article_id].copy()
        row["sample_level"] = "L1"
        row["upgrade_reason"] = "；".join(sorted(reasons))
        ratio = earnings_per_1k(row)
        if ratio is not None and not row.get("earnings_per_1k_views"):
            row["earnings_per_1k_views"] = f"{ratio:.2f}"
        sampled_rows.append(row)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in sampled_rows:
            writer.writerow({field: row.get(field, "") for field in headers})

    earnings_count = sum(1 for row in rows if row.get("earnings", "") != "")
    candidate_total = sum(len(article_ids) for article_ids in candidates_by_group.values())
    duplicate_hits = [
        {
            "article_id": article_id,
            "title": by_id[article_id]["title"],
            "rules": "；".join(sorted(reasons)),
        }
        for article_id, reasons in sorted(sample_reasons.items())
        if len(reasons) > 1
    ]

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    report_lines = [
        "# L1 Sample Report",
        "",
        "本报告只基于 L0 内容资产总账生成，不读取正文、评论、同题高赞或变量层数据。",
        "",
        "## 候选数量",
        "",
    ]
    for group, article_ids in candidates_by_group.items():
        report_lines.append(f"- {group}: {len(article_ids)}")
    report_lines.extend([
        f"- 候选总数: {candidate_total}",
        f"- 去重后唯一文章: {len(sampled_rows)}",
        "",
        "## 收益覆盖率",
        "",
        f"- 已有 earnings: {earnings_count} / {len(rows)}",
        f"- 覆盖率: {earnings_count / len(rows) * 100:.2f}%",
        f"- 状态: {'正式样本' if earnings_count >= 10 else '临时样本'}",
        "",
        "## 重复命中",
        "",
    ])
    if duplicate_hits:
        report_lines.extend([
            "| article_id | 标题 | 命中规则 |",
            "| --- | --- | --- |",
        ])
        for item in duplicate_hits:
            report_lines.append(f"| {item['article_id']} | {item['title']} | {item['rules']} |")
    else:
        report_lines.append("无重复命中。")
    report_lines.extend([
        "",
        "## 最终样本",
        "",
        "| article_id | 标题 | earnings | views | favorites | 命中规则 |",
        "| --- | --- | --- | --- | --- | --- |",
    ])
    for row in sampled_rows:
        report_lines.append(
            f"| {row['article_id']} | {row['title']} | {row.get('earnings', '')} | "
            f"{row.get('views', '')} | {row.get('favorites', '')} | {row.get('upgrade_reason', '')} |"
        )
    report_lines.extend([
        "",
        "## 下一步",
        "",
        "- 已分层样本可以进入05单篇复盘；未分层样本继续优先补充 article_id + earnings。",
        "- 题型、结构、变量、首屏、机制字段无法判断时保持 UNKNOWN，不阻塞下一批回填。",
        "- 历史样本复盘产出的规律先进入05.5验证库，不直接升级 ACTIVE。",
    ])
    REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(f"wrote {OUTPUT}")
    print(f"wrote {REPORT}")
    print(f"rows: {len(sampled_rows)}")
    if earnings_count == 0:
        print("blocked_groups: 高收益TOP5, 低阅读高收益TOP5 (earnings field is empty in L0)")
    elif earnings_count < 10:
        print(f"partial_earnings_warning: only {earnings_count} rows have earnings; earnings-based groups are provisional")
    else:
        print("blocked_groups: none")


if __name__ == "__main__":
    main()
