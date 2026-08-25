#!/usr/bin/env python3
import csv
import hashlib
from pathlib import Path


def make_blind_id(article_id):
    digest = hashlib.sha1(article_id.encode("utf-8")).hexdigest()[:10].upper()
    return f"BLIND-{digest}"


def main():
    source = Path("reports/distribution_matched_pairs_EXP008.csv")
    blind_out = Path("data/distribution_text_annotations_blind.csv")
    map_out = Path("data/distribution_text_annotations_blind_map.csv")
    if not source.exists():
        raise SystemExit(f"Missing source: {source}")

    with source.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    blind_fields = [
        "blind_id",
        "article_id",
        "title",
        "question_text",
        "answer_text",
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
        blind_rows.append(
            {
                "blind_id": blind_id,
                "article_id": row["article_id"],
                "title": row["title"],
                "audience_scope_evidence": "PENDING",
                "conflict_strength_evidence": "PENDING",
                "emotional_charge_evidence": "PENDING",
                "first_sentence_evidence": "PENDING",
                "first_100_evidence": "PENDING",
                "annotation_status": "PENDING",
                "notes": "Blind text-derived annotation only; do not use performance data while coding.",
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
    print(f"blind_output={blind_out}")
    print(f"map_output={map_out}")


if __name__ == "__main__":
    main()
