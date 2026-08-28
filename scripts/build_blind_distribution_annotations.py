#!/usr/bin/env python3
import csv
import hashlib
import re
from pathlib import Path


TEXT_SOURCES = [
    Path("l2_variable_records.md"),
    Path("知乎TOP10事实包_V1_给GPT复盘.md"),
]


def make_blind_id(article_id):
    digest = hashlib.sha1(article_id.encode("utf-8")).hexdigest()[:10].upper()
    return f"BLIND-{digest}"


def clean_block(text):
    text = re.sub(r"\n{3,}", "\n\n", text.strip())
    return text


def extract_section(text, start_pattern, next_pattern=r"\n#{2,4} "):
    match = re.search(start_pattern, text)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(next_pattern, text[start:])
    end = start + next_heading.start() if next_heading else len(text)
    return clean_block(text[start:end])


def extract_l2_snapshot(text, article_id):
    section = extract_section(
        text,
        rf"### 记录 \d+｜{re.escape(article_id)}\n",
        next_pattern=r"\n### 记录 \d+｜",
    )
    if not section:
        return ""
    title_match = re.search(r"- 标题：(.+)", section)
    question_text = title_match.group(1).strip() if title_match else ""
    parts = []
    for heading in ("首屏", "结构", "结尾"):
        block = extract_section(section, rf"#### {heading}\n")
        if block:
            parts.append(f"{heading}：\n{block}")
    return question_text, clean_block("\n\n".join(parts))


def extract_top_fact_snapshot(text, title):
    section = extract_section(text, rf"## 正文快照｜\d+｜{re.escape(title)}\n")
    if not section:
        return ""
    lines = []
    for line in section.splitlines():
        if line.startswith("正文采集状态："):
            break
        if line.strip():
            lines.append(line)
    return title, clean_block("\n".join(lines))


def load_text_snapshots():
    snapshots = {}
    for source in TEXT_SOURCES:
        if not source.exists():
            continue
        text = source.read_text(encoding="utf-8")
        snapshots[source.as_posix()] = text
    return snapshots


def resolve_text(row, snapshots):
    title = row["title"]
    article_id = row["article_id"]
    for path, text in snapshots.items():
        if path.endswith("l2_variable_records.md"):
            result = extract_l2_snapshot(text, article_id)
            if result:
                question_text, answer_text = result
                return question_text or title, answer_text, "HISTORICAL_SNAPSHOT", path
    for path, text in snapshots.items():
        if path.endswith("知乎TOP10事实包_V1_给GPT复盘.md"):
            result = extract_top_fact_snapshot(text, title)
            if result:
                question_text, answer_text = result
                return question_text or title, answer_text, "HISTORICAL_SNAPSHOT", path
    return title, "", "TEXT_MISSING", ""


def main():
    source = Path("reports/distribution_matched_pairs_EXP008.csv")
    blind_out = Path("data/distribution_text_annotations_blind.csv")
    map_out = Path("data/distribution_text_annotations_blind_map.csv")
    if not source.exists():
        raise SystemExit(f"Missing source: {source}")

    with source.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    snapshots = load_text_snapshots()

    blind_fields = [
        "blind_id",
        "title",
        "question_text",
        "answer_text",
        "text_source_status",
        "text_source_path",
        "audience_scope",
        "audience_scope_evidence",
        "conflict_strength",
        "conflict_strength_evidence",
        "emotional_charge",
        "emotional_charge_evidence",
        "first_sentence_judgment",
        "first_sentence_evidence",
        "first_100_interest_conflict",
        "first_100_evidence",
        "annotation_status",
        "notes",
    ]
    map_fields = [
        "blind_id",
        "article_id",
        "pair_id",
        "pair_role",
        "matched_with_article_id",
    ]

    blind_rows = []
    map_rows = []
    for row in rows:
        blind_id = make_blind_id(row["article_id"])
        question_text, answer_text, text_source_status, text_source_path = resolve_text(row, snapshots)
        blind_rows.append(
            {
                "blind_id": blind_id,
                "title": row["title"],
                "question_text": question_text,
                "answer_text": answer_text,
                "text_source_status": text_source_status,
                "text_source_path": text_source_path,
                "audience_scope_evidence": "PENDING",
                "conflict_strength_evidence": "PENDING",
                "emotional_charge_evidence": "PENDING",
                "first_sentence_evidence": "PENDING",
                "first_100_evidence": "PENDING",
                "annotation_status": "PENDING",
                "notes": "Blind text-derived annotation only; do not use performance data while coding. Do not code first sentence or first 100 chars when answer_text is empty.",
            }
        )
        map_rows.append(
            {
                "blind_id": blind_id,
                "article_id": row["article_id"],
                "pair_id": row["pair_id"],
                "pair_role": row["pair_role"],
                "matched_with_article_id": row["matched_with_article_id"],
            }
        )

    with blind_out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=blind_fields)
        writer.writeheader()
        writer.writerows(blind_rows)

    with map_out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=map_fields)
        writer.writeheader()
        writer.writerows(map_rows)

    print(f"blind_rows={len(blind_rows)}")
    print(f"text_rows={sum(1 for row in blind_rows if row['answer_text'])}")
    print(f"missing_text_rows={sum(1 for row in blind_rows if not row['answer_text'])}")
    print(f"blind_output={blind_out}")
    print(f"map_output={map_out}")


if __name__ == "__main__":
    main()
