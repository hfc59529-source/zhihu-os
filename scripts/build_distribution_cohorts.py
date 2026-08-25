#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path
from statistics import median


def parse_float(value):
    if value is None:
        return None
    value = str(value).strip()
    if not value or value.upper() == "UNKNOWN":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def load_rows(path):
    rows = []
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if row.get("content_type") != "回答":
                continue
            views = parse_float(row.get("views"))
            earnings = parse_float(row.get("earnings"))
            rpm = parse_float(row.get("earnings_per_1k_views"))
            if views is None or earnings is None or views <= 0 or earnings <= 0:
                continue
            if rpm is None:
                rpm = earnings / views * 1000
            rows.append((row, views, earnings, rpm))
    return rows


def main():
    parser = argparse.ArgumentParser(
        description="Build EXP008 Distribution Model cohort candidates from L0 assets."
    )
    parser.add_argument("--input", default="data/l0_content_assets.csv")
    parser.add_argument("--output", default="reports/distribution_cohort_candidates_EXP008.csv")
    parser.add_argument("--min-views", type=float, default=20)
    args = parser.parse_args()

    rows = [r for r in load_rows(Path(args.input)) if r[1] >= args.min_views]
    if not rows:
        raise SystemExit("No eligible rows found.")

    view_cutoff = median(r[1] for r in rows)
    rpm_cutoff = median(r[3] for r in rows)

    output_rows = []
    for row, views, earnings, rpm in rows:
        high_play = views >= view_cutoff
        high_m = rpm >= rpm_cutoff
        if high_m and high_play:
            cohort = "A_HIGH_M_HIGH_PLAY"
        elif high_m and not high_play:
            cohort = "B_HIGH_M_LOW_PLAY"
        elif not high_m and high_play:
            cohort = "C_LOW_M_HIGH_PLAY"
        else:
            continue
        like_rate = parse_float(row.get("likes")) or 0
        comment_rate = parse_float(row.get("comments")) or 0
        favorite_rate = parse_float(row.get("favorites")) or 0
        output_rows.append(
            {
                "article_id": row.get("article_id", ""),
                "title": row.get("title", ""),
                "cohort": cohort,
                "views": int(views),
                "earnings": earnings,
                "earnings_per_1k_views": round(rpm, 2),
                "like_rate": round(like_rate / views, 4),
                "comment_rate": round(comment_rate / views, 4),
                "favorite_rate": round(favorite_rate / views, 4),
                "published_at": row.get("published_at", ""),
                "url": row.get("url", ""),
            }
        )

    output_rows.sort(
        key=lambda r: (
            {"A_HIGH_M_HIGH_PLAY": 0, "B_HIGH_M_LOW_PLAY": 1, "C_LOW_M_HIGH_PLAY": 2}[r["cohort"]],
            -r["earnings_per_1k_views"],
            -r["views"],
        )
    )

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "article_id",
        "title",
        "cohort",
        "views",
        "earnings",
        "earnings_per_1k_views",
        "like_rate",
        "comment_rate",
        "favorite_rate",
        "published_at",
        "url",
    ]
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"eligible_rows={len(rows)}")
    print(f"view_cutoff_median={view_cutoff}")
    print(f"rpm_cutoff_median={rpm_cutoff:.2f}")
    print(f"candidate_rows={len(output_rows)}")
    print(f"output={out}")


if __name__ == "__main__":
    main()
