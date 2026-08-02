#!/usr/bin/env python3
"""Static question type vs performance analysis for Zhihu records."""

from __future__ import annotations

import csv
import re
import statistics
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reports" / "ZH-Question-Type-Performance-Analysis-V1.md"


@dataclass
class Article:
    article_id: str
    title: str
    publish_date: str
    reads: int | None
    revenue: float | None
    source: str


def parse_number(value: str | None) -> float | None:
    if value is None:
        return None
    text = value.strip().replace(",", "")
    if not text or text.upper() == "UNKNOWN":
        return None
    mult = 1.0
    if "万" in text:
        mult = 10000.0
        text = text.replace("万", "")
    m = re.search(r"-?\d+(?:\.\d+)?", text)
    if not m:
        return None
    return float(m.group(0)) * mult


def parse_reads(value: str | None) -> int | None:
    number = parse_number(value)
    if number is None:
        return None
    return int(round(number))


def normalize_date(value: str | None) -> str:
    if not value:
        return ""
    text = value.strip()
    m = re.search(r"20\d{2}-\d{2}-\d{2}", text)
    if m:
        return m.group(0)
    m = re.search(r"(\d{2})-(\d{2})", text)
    if m:
        return f"2026-{m.group(1)}-{m.group(2)}"
    return text


def classify(title: str) -> str:
    why_patterns = [
        r"为什么",
        r"为何",
        r"为啥",
        r"原因是什么",
        r"是什么让",
        r"怎么会",
    ]
    how_patterns = [
        r"怎么办",
        r"怎么做",
        r"怎么才能",
        r"怎么判断",
        r"如何",
        r"有哪些",
        r"该不该",
        r"要不要",
        r"怎么选",
        r"怎么改",
        r"怎么破局",
    ]
    has_why = any(re.search(p, title) for p in why_patterns)
    has_how = any(re.search(p, title) for p in how_patterns)
    if has_why and has_how:
        return "MIXED"
    if has_why:
        return "WHY"
    if has_how:
        return "HOW"
    return "MIXED"


def load_csv_records(path: Path, source: str) -> list[Article]:
    if not path.exists():
        return []
    rows: list[Article] = []
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            article_id = (
                row.get("article_id")
                or row.get("run_id")
                or row.get("answer_id")
                or row.get("url")
                or row.get("question")
                or ""
            ).strip()
            title = (row.get("title") or row.get("question") or row.get("内容") or "").strip()
            if not title:
                continue
            reads = parse_reads(row.get("views") or row.get("reading") or row.get("累计阅读") or row.get("阅读"))
            revenue = parse_number(row.get("earnings") or row.get("salt_income") or row.get("累计收益") or row.get("收益"))
            publish_date = normalize_date(row.get("published_at") or row.get("发布时间") or row.get("data_cycle"))
            rows.append(Article(article_id, title, publish_date, reads, revenue, source))
    return rows


def load_review_capture(path: Path) -> list[Article]:
    if not path.exists():
        return []
    rows: list[Article] = []
    section = None
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("## 04"):
            section = "reads"
            continue
        if stripped.startswith("## 05"):
            section = "revenue"
            continue
        if stripped.startswith("## 06"):
            section = None
        if not stripped.startswith("|") or "---" in stripped:
            continue
        parts = [p.strip() for p in stripped.strip("|").split("|")]
        if section == "reads" and len(parts) >= 8 and parts[0] != "发布时间":
            rows.append(
                Article(
                    article_id=f"answer_{parts[1]}",
                    title=parts[2],
                    publish_date=normalize_date(parts[0]),
                    reads=parse_reads(parts[3]),
                    revenue=None,
                    source="reports/zhihu_review_capture_20260731.md#04",
                )
            )
        elif section == "revenue" and len(parts) >= 7 and parts[0] != "内容":
            rows.append(
                Article(
                    article_id=f"title:{parts[0]}",
                    title=parts[0],
                    publish_date=normalize_date(parts[2]),
                    reads=parse_reads(parts[5]),
                    revenue=parse_number(parts[6]),
                    source="reports/zhihu_review_capture_20260731.md#05",
                )
            )
    return rows


def better(existing: Article, candidate: Article) -> Article:
    reads = max(x for x in [existing.reads, candidate.reads] if x is not None) if (existing.reads is not None or candidate.reads is not None) else None
    revenue_values = [x for x in [existing.revenue, candidate.revenue] if x is not None]
    revenue = max(revenue_values) if revenue_values else None
    publish_date = existing.publish_date or candidate.publish_date
    article_id = existing.article_id if not existing.article_id.startswith("title:") else candidate.article_id
    source = existing.source if existing.source == candidate.source else f"{existing.source}; {candidate.source}"
    return Article(article_id, existing.title, publish_date, reads, revenue, source)


def collect_articles() -> list[Article]:
    candidates: list[Article] = []
    candidates.extend(load_csv_records(ROOT / "data" / "l0_content_assets.csv", "data/l0_content_assets.csv"))
    candidates.extend(load_csv_records(ROOT / "data" / "l1_sample_list.csv", "data/l1_sample_list.csv"))
    candidates.extend(load_csv_records(ROOT / "runtime" / "logs" / "publish_results.csv", "runtime/logs/publish_results.csv"))
    candidates.extend(load_review_capture(ROOT / "reports" / "zhihu_review_capture_20260731.md"))

    by_title: dict[str, Article] = {}
    for article in candidates:
        if article.reads is None:
            continue
        key = re.sub(r"\s+", "", article.title)
        if key in by_title:
            by_title[key] = better(by_title[key], article)
        else:
            by_title[key] = article
    return sorted(by_title.values(), key=lambda a: (a.publish_date, a.title))


def avg(values: list[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def fmt_number(value: float | int | None, digits: int = 2) -> str:
    if value is None:
        return ""
    if isinstance(value, int) or float(value).is_integer():
        return str(int(value))
    return f"{value:.{digits}f}"


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |"]
    out.append("|" + "|".join(["---"] * len(headers)) + "|")
    for row in rows:
        out.append("| " + " | ".join(row) + " |")
    return "\n".join(out)


def sample_rows(articles: list[Article]) -> list[list[str]]:
    return [
        [
            article.article_id,
            article.title.replace("|", " "),
            article.publish_date,
            fmt_number(article.reads),
            fmt_number(article.revenue),
        ]
        for article in articles
    ]


def main() -> None:
    articles = collect_articles()
    typed = [(article, classify(article.title)) for article in articles]
    groups = {
        qtype: [article for article, article_type in typed if article_type == qtype]
        for qtype in ["WHY", "HOW", "MIXED"]
    }

    stats_rows: list[list[str]] = []
    for qtype in ["WHY", "HOW"]:
        group = groups[qtype]
        reads = [a.reads for a in group if a.reads is not None]
        revenues = [a.revenue for a in group if a.revenue is not None]
        stats_rows.append(
            [
                qtype,
                str(len(group)),
                fmt_number(avg([float(x) for x in reads])),
                fmt_number(float(statistics.median(reads)) if reads else None),
                fmt_number(avg(revenues)),
            ]
        )

    why_avg = avg([float(a.reads) for a in groups["WHY"] if a.reads is not None])
    how_avg = avg([float(a.reads) for a in groups["HOW"] if a.reads is not None])
    conclusion = "SUPPORTED" if why_avg is not None and how_avg is not None and why_avg > how_avg else "NOT SUPPORTED"

    top_why = sorted(groups["WHY"], key=lambda a: a.reads or -1, reverse=True)[:10]
    top_how = sorted(groups["HOW"], key=lambda a: a.reads or -1, reverse=True)[:10]
    worst_why = sorted(groups["WHY"], key=lambda a: a.reads or 10**18)[:10]
    worst_how = sorted(groups["HOW"], key=lambda a: a.reads or 10**18)[:10]

    lines = [
        "# ZH-Question-Type-Performance-Analysis-V1",
        "",
        "Objective: Why > How",
        "",
        "## Dataset",
        "",
        markdown_table(
            ["Scope", "Count"],
            [
                ["All records with reads", str(len(articles))],
                ["WHY", str(len(groups["WHY"]))],
                ["HOW", str(len(groups["HOW"]))],
                ["MIXED excluded", str(len(groups["MIXED"]))],
            ],
        ),
        "",
        "## Stats",
        "",
        markdown_table(["Type", "Count", "Avg Reads", "Median Reads", "Avg Revenue"], stats_rows),
        "",
        "## Top Why",
        "",
        markdown_table(["Article_ID", "Title", "Publish_Date", "Reads", "Revenue"], sample_rows(top_why)),
        "",
        "## Top How",
        "",
        markdown_table(["Article_ID", "Title", "Publish_Date", "Reads", "Revenue"], sample_rows(top_how)),
        "",
        "## Worst Why",
        "",
        markdown_table(["Article_ID", "Title", "Publish_Date", "Reads", "Revenue"], sample_rows(worst_why)),
        "",
        "## Worst How",
        "",
        markdown_table(["Article_ID", "Title", "Publish_Date", "Reads", "Revenue"], sample_rows(worst_how)),
        "",
        "## Conclusion",
        "",
        conclusion,
        "",
    ]
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(OUTPUT.relative_to(ROOT))
    print(conclusion)


if __name__ == "__main__":
    main()
