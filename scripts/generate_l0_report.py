#!/usr/bin/env python3
import csv
from collections import Counter
from pathlib import Path


INPUT = Path("data/l0_content_assets.csv")
OUTPUT = Path("reports/l0_asset_report.md")
BASELINE_OUTPUT = Path("reports/historical_baseline_report.md")


def to_number(value):
    if value == "":
        return None
    text = value.replace(",", "").strip()
    if text.endswith("万"):
        return float(text[:-1]) * 10000
    return float(text)


def top_rows(rows, field, limit=10):
    sortable = []
    for row in rows:
        value = to_number(row.get(field, ""))
        if value is not None:
            sortable.append((value, row))
    return sorted(sortable, key=lambda item: item[0], reverse=True)[:limit]


def percentile(values, pct):
    nums = sorted(v for v in values if v is not None)
    if not nums:
        return None
    if len(nums) == 1:
        return nums[0]
    rank = (len(nums) - 1) * pct
    low = int(rank)
    high = min(low + 1, len(nums) - 1)
    weight = rank - low
    return nums[low] * (1 - weight) + nums[high] * weight


def metric_values(rows, field):
    return [to_number(row.get(field, "")) for row in rows if to_number(row.get(field, "")) is not None]


def ratio_values(rows, numerator_fields):
    values = []
    for row in rows:
        views = to_number(row.get("views", ""))
        if not views:
            continue
        total = 0
        usable = True
        for field in numerator_fields:
            value = to_number(row.get(field, ""))
            if value is None:
                usable = False
                break
            total += value
        if usable:
            values.append(total / views)
    return values


def bucket_count(values, buckets):
    rows = []
    for label, lower, upper in buckets:
        count = 0
        for value in values:
            if value is None:
                continue
            if upper is None:
                if value >= lower:
                    count += 1
            elif lower <= value < upper:
                count += 1
        rows.append({"区间": label, "数量": count})
    return rows


def fmt(value, digits=2):
    if value is None:
        return ""
    if abs(value) >= 100:
        return f"{value:.0f}"
    return f"{value:.{digits}f}"


def percentile_rows(rows, metrics):
    output = []
    for label, field in metrics:
        values = metric_values(rows, field)
        output.append({
            "指标": label,
            "样本数": len(values),
            "P50": fmt(percentile(values, 0.50)),
            "P75": fmt(percentile(values, 0.75)),
            "P90": fmt(percentile(values, 0.90)),
            "P95": fmt(percentile(values, 0.95)),
            "MAX": fmt(max(values) if values else None),
        })
    return output


def ratio_percentile_rows(rows):
    ratios = [
        ("点赞率", ratio_values(rows, ["likes"])),
        ("收藏率", ratio_values(rows, ["favorites"])),
        ("评论率", ratio_values(rows, ["comments"])),
        ("互动率", ratio_values(rows, ["likes", "favorites", "comments"])),
    ]
    return [
        {
            "指标": label,
            "样本数": len(values),
            "P50": fmt(percentile(values, 0.50) * 100 if values else None),
            "P75": fmt(percentile(values, 0.75) * 100 if values else None),
            "P90": fmt(percentile(values, 0.90) * 100 if values else None),
            "P95": fmt(percentile(values, 0.95) * 100 if values else None),
            "MAX": fmt(max(values) * 100 if values else None),
        }
        for label, values in ratios
    ]


def markdown_table(rows, headers):
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def main():
    rows = list(csv.DictReader(INPUT.open(newline="", encoding="utf-8")))
    type_counts = Counter(row["content_type"] for row in rows)
    published_counts = Counter(row["published_at"] for row in rows)
    batch_counts = Counter(row.get("historical_batch", "") or "<EMPTY>" for row in rows)
    completeness_counts = Counter(row.get("historical_completeness", "") or "<EMPTY>" for row in rows)
    evidence_counts = Counter(row.get("evidence_level", "") or "<EMPTY>" for row in rows)
    layer_counts = Counter(layer for row in rows for layer in (row.get("result_layer", "").split("+") if row.get("result_layer") else ["未分层"]))
    earnings_missing = sum(1 for row in rows if row["earnings"] == "")
    fold_count = sum(1 for row in rows if "折叠" in row.get("notes", ""))

    views = [to_number(row["views"]) for row in rows if to_number(row["views"]) is not None]
    likes = [to_number(row["likes"]) for row in rows if to_number(row["likes"]) is not None]
    comments = [to_number(row["comments"]) for row in rows if to_number(row["comments"]) is not None]
    favorites = [to_number(row["favorites"]) for row in rows if to_number(row["favorites"]) is not None]

    report = []
    report.append("# L0 内容资产统计报告")
    report.append("")
    report.append("本报告只使用 L0 内容资产总账字段，不读取正文、评论、同题高赞或变量层数据。")
    report.append("")
    report.append("## 总览")
    report.append("")
    report.append(f"- 内容总数：{len(rows)}")
    report.append(f"- 内容类型：{', '.join(f'{k} {v}' for k, v in sorted(type_counts.items()))}")
    report.append(f"- 收益字段空值：{earnings_missing}/{len(rows)}")
    report.append(f"- 证据等级：{', '.join(f'{k} {v}' for k, v in sorted(evidence_counts.items()))}")
    report.append(f"- 代表复盘候选：{sum(1 for row in rows if row.get('deep_review') == '是')}/{len(rows)}")
    report.append("")
    report.append("## 历史回填批次")
    report.append("")
    report.append(markdown_table(
        [{"批次": k, "数量": v} for k, v in sorted(batch_counts.items())],
        ["批次", "数量"],
    ))
    report.append("")
    report.append("## 历史完整度")
    report.append("")
    report.append(markdown_table(
        [{"完整度": k, "数量": v} for k, v in sorted(completeness_counts.items())],
        ["完整度", "数量"],
    ))
    report.append("")
    report.append("## 结果分层")
    report.append("")
    report.append(markdown_table(
        [{"分层": k, "数量": v} for k, v in sorted(layer_counts.items())],
        ["分层", "数量"],
    ))
    report.append("")
    report.append("## 基础指标")
    report.append("")
    report.append(f"- 平均阅读/浏览：{sum(views) / len(views):.2f}" if views else "- 平均阅读/浏览：不可用")
    report.append(f"- 平均赞同：{sum(likes) / len(likes):.2f}" if likes else "- 平均赞同：不可用")
    report.append(f"- 平均评论：{sum(comments) / len(comments):.2f}" if comments else "- 平均评论：不可用")
    report.append(f"- 平均收藏：{sum(favorites) / len(favorites):.2f}" if favorites else "- 平均收藏：不可用")
    report.append(f"- 阅读中位数：{percentile(views, 0.50):.2f}" if views else "- 阅读中位数：不可用")
    report.append(f"- 阅读 P90：{percentile(views, 0.90):.2f}" if views else "- 阅读 P90：不可用")
    report.append("")
    report.append("## 分位数 Profile")
    report.append("")
    report.append(markdown_table(
        percentile_rows(rows, [
            ("阅读", "views"),
            ("赞同", "likes"),
            ("评论", "comments"),
            ("收藏", "favorites"),
            ("收益", "earnings"),
            ("千阅读收益", "earnings_per_1k_views"),
        ]),
        ["指标", "样本数", "P50", "P75", "P90", "P95", "MAX"],
    ))
    report.append("")
    report.append("## 派生率 Profile（百分比）")
    report.append("")
    report.append(markdown_table(
        ratio_percentile_rows(rows),
        ["指标", "样本数", "P50", "P75", "P90", "P95", "MAX"],
    ))
    report.append("")
    report.append("## 阅读分布")
    report.append("")
    report.append(markdown_table(
        bucket_count(views, [
            ("0-20", 0, 20),
            ("20-50", 20, 50),
            ("50-100", 50, 100),
            ("100-300", 100, 300),
            ("300-1000", 300, 1000),
            ("1000+", 1000, None),
        ]),
        ["区间", "数量"],
    ))
    report.append("")
    report.append("## 内容类型分布")
    report.append("")
    report.append(markdown_table(
        [{"内容类型": k, "数量": v} for k, v in sorted(type_counts.items())],
        ["内容类型", "数量"],
    ))
    report.append("")
    report.append("## 发布时间分布")
    report.append("")
    report.append(markdown_table(
        [{"发布时间": k, "数量": v} for k, v in published_counts.most_common()],
        ["发布时间", "数量"],
    ))
    report.append("")
    report.append("## 阅读/浏览 Top10")
    report.append("")
    report.append(markdown_table(
        [
            {
                "article_id": row["article_id"],
                "类型": row["content_type"],
                "标题": row["title"],
                "阅读": int(value),
                "赞同": row["likes"],
                "评论": row["comments"],
                "收藏": row["favorites"],
            }
            for value, row in top_rows(rows, "views", 10)
        ],
        ["article_id", "类型", "标题", "阅读", "赞同", "评论", "收藏"],
    ))
    report.append("")
    report.append("## 收藏 Top10")
    report.append("")
    report.append(markdown_table(
        [
            {
                "article_id": row["article_id"],
                "类型": row["content_type"],
                "标题": row["title"],
                "收藏": int(value),
                "阅读": row["views"],
                "赞同": row["likes"],
                "评论": row["comments"],
            }
            for value, row in top_rows(rows, "favorites", 10)
        ],
        ["article_id", "类型", "标题", "收藏", "阅读", "赞同", "评论"],
    ))
    report.append("")
    report.append("## L0 结论")
    report.append("")
    report.append("- L0 内容资产总账已具备唯一定位、排序和后续升级能力。")
    report.append("- 历史数据不再另建总表，统一由 L0 承载回填、分层和证据等级字段。")
    report.append("- 下一步可以优先补齐收益缺口，并对 deep_review=是 的代表样本进入05单篇复盘。")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}")

    baseline = []
    baseline.append("# Historical Baseline Report")
    baseline.append("")
    baseline.append("本报告回答：账号历史上什么算高、什么算低，以及新文章应如何放回历史分布判断。只使用 L0 字段，不读取正文或参数库。")
    baseline.append("")
    baseline.append("## Account Profile")
    baseline.append("")
    baseline.append(f"- 内容总数：{len(rows)}")
    baseline.append(f"- 内容类型：{', '.join(f'{k} {v}' for k, v in sorted(type_counts.items()))}")
    baseline.append(f"- 收益覆盖率：{(len(rows) - earnings_missing) / len(rows) * 100:.2f}%")
    baseline.append(f"- 折叠记录数：{fold_count}")
    baseline.append(f"- 阅读 P50 / P75 / P90 / P95 / MAX：{fmt(percentile(views, 0.50))} / {fmt(percentile(views, 0.75))} / {fmt(percentile(views, 0.90))} / {fmt(percentile(views, 0.95))} / {fmt(max(views) if views else None)}")
    baseline.append("")
    baseline.append("## Metric Percentiles")
    baseline.append("")
    baseline.append(markdown_table(
        percentile_rows(rows, [
            ("阅读", "views"),
            ("赞同", "likes"),
            ("评论", "comments"),
            ("收藏", "favorites"),
            ("收益", "earnings"),
            ("千阅读收益", "earnings_per_1k_views"),
        ]),
        ["指标", "样本数", "P50", "P75", "P90", "P95", "MAX"],
    ))
    baseline.append("")
    baseline.append("## Rate Percentiles（百分比）")
    baseline.append("")
    baseline.append(markdown_table(
        ratio_percentile_rows(rows),
        ["指标", "样本数", "P50", "P75", "P90", "P95", "MAX"],
    ))
    baseline.append("")
    baseline.append("## Distribution")
    baseline.append("")
    baseline.append("### 阅读分布")
    baseline.append("")
    baseline.append(markdown_table(
        bucket_count(views, [
            ("0-20", 0, 20),
            ("20-50", 20, 50),
            ("50-100", 50, 100),
            ("100-300", 100, 300),
            ("300-1000", 300, 1000),
            ("1000+", 1000, None),
        ]),
        ["区间", "数量"],
    ))
    baseline.append("")
    baseline.append("### 收藏分布")
    baseline.append("")
    baseline.append(markdown_table(
        bucket_count(favorites, [
            ("0", 0, 1),
            ("1-3", 1, 4),
            ("4-10", 4, 11),
            ("11-50", 11, 51),
            ("50+", 50, None),
        ]),
        ["区间", "数量"],
    ))
    baseline.append("")
    baseline.append("## L1入口定义")
    baseline.append("")
    baseline.append("L1 不是互斥分类，而是代表样本入口。一篇内容可以同时命中多个入口。")
    baseline.append("")
    baseline.append("| 入口 | 用途 |")
    baseline.append("| --- | --- |")
    baseline.append("| Top Performer | 找高表现特征 |")
    baseline.append("| Bottom Performer | 找失败边界 |")
    baseline.append("| Outlier | 找高收藏、低阅读、高收益、折叠等异常机制 |")
    baseline.append("| Recent Production | 观察新流程样本相对历史基线的位置 |")
    baseline.append("")
    baseline.append("## 使用规则")
    baseline.append("")
    baseline.append("- 历史样本只负责发现候选规律，证据状态最高到 CANDIDATE。")
    baseline.append("- 代表样本先做 Blind Review，不先套 ACTIVE / PD / BT 标签。")
    baseline.append("- 候选规律必须用未来新文章的 T24 / T72 / T7D 数据验证后，才可能推进 Parameter 状态。")
    BASELINE_OUTPUT.write_text("\n".join(baseline) + "\n", encoding="utf-8")
    print(f"wrote {BASELINE_OUTPUT}")


if __name__ == "__main__":
    main()
