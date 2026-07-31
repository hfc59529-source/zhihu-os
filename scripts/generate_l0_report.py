#!/usr/bin/env python3
import csv
from collections import Counter
from pathlib import Path


INPUT = Path("data/l0_content_assets.csv")
OUTPUT = Path("reports/l0_asset_report.md")


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


if __name__ == "__main__":
    main()
