#!/usr/bin/env python3
import csv
from pathlib import Path


def main():
    source = Path("reports/distribution_matched_pairs_EXP008.csv")
    target = Path("data/distribution_model_annotations.csv")
    if not source.exists():
        raise SystemExit(f"Missing source: {source}")
    with source.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    fieldnames = [
        "pair_id",
        "pair_role",
        "article_id",
        "title",
        "views",
        "earnings",
        "earnings_per_1k_views",
        "exposure_age_days",
        "views_per_day",
        "question_attention_level",
        "question_attention_evidence",
        "question_stage_at_publish",
        "question_stage_evidence",
        "existing_answer_count",
        "existing_answer_count_evidence",
        "high_like_occupied",
        "high_like_occupied_evidence",
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
        "like_rate",
        "comment_rate",
        "favorite_rate",
        "post_outcome_role",
        "primary_hypothesis",
        "annotation_status",
        "notes",
    ]
    seeded = []
    for row in rows:
        seeded.append(
            {
                "pair_id": row["pair_id"],
                "pair_role": row["pair_role"],
                "article_id": row["article_id"],
                "title": row["title"],
                "views": row["views"],
                "earnings": row["earnings"],
                "earnings_per_1k_views": row["earnings_per_1k_views"],
                "exposure_age_days": row["exposure_age_days"],
                "views_per_day": row["views_per_day"],
                "question_attention_evidence": "UNKNOWN",
                "question_stage_evidence": "UNKNOWN",
                "existing_answer_count_evidence": "UNKNOWN",
                "high_like_occupied_evidence": "UNKNOWN",
                "audience_scope_evidence": "PENDING",
                "conflict_strength_evidence": "PENDING",
                "emotional_charge_evidence": "PENDING",
                "first_sentence_evidence": "UNKNOWN",
                "first_100_evidence": "UNKNOWN",
                "like_rate": row["like_rate"],
                "comment_rate": row["comment_rate"],
                "favorite_rate": row["favorite_rate"],
                "post_outcome_role": "OUTCOME_OR_MEDIATOR",
                "annotation_status": "PENDING",
                "notes": "Seeded from matched pairs; do not infer publish-time question context from current Zhihu state.",
            }
        )
    with target.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(seeded)
    print(f"seeded_rows={len(seeded)}")
    print(f"output={target}")


if __name__ == "__main__":
    main()
