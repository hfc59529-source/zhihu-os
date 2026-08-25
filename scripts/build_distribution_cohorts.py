#!/usr/bin/env python3
import argparse
import csv
from datetime import date, datetime
from pathlib import Path
from statistics import median


CURRENT_DATE = date(2026, 8, 25)


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


def parse_publish_date(value, current_date):
    if not value:
        return None
    value = value.strip()
    for prefix in ("发布于 ", "编辑于 "):
        if value.startswith(prefix):
            value = value[len(prefix) :]
            break
    if "小时前" in value or "昨天" in value:
        return None
    try:
        month, day = value.split("-")
        return date(current_date.year, int(month), int(day))
    except ValueError:
        return None


def classify_age(days):
    if days is None:
        return "UNKNOWN"
    if days <= 7:
        return "0_7D"
    if days <= 21:
        return "8_21D"
    if days <= 45:
        return "22_45D"
    return "46D_PLUS"


def enrich_rows(rows, current_date):
    enriched = []
    for row, views, earnings, rpm in rows:
        published_date = parse_publish_date(row.get("published_at", ""), current_date)
        age_days = (current_date - published_date).days if published_date else None
        views_per_day = views / max(age_days or 1, 1)
        likes = parse_float(row.get("likes")) or 0
        comments = parse_float(row.get("comments")) or 0
        favorites = parse_float(row.get("favorites")) or 0
        enriched.append(
            {
                "row": row,
                "article_id": row.get("article_id", ""),
                "title": row.get("title", ""),
                "views": views,
                "earnings": earnings,
                "rpm": rpm,
                "published_at": row.get("published_at", ""),
                "published_date": published_date.isoformat() if published_date else "",
                "exposure_age_days": age_days if age_days is not None else "",
                "age_bucket": classify_age(age_days),
                "views_per_day": views_per_day,
                "like_rate": likes / views,
                "comment_rate": comments / views,
                "favorite_rate": favorites / views,
                "url": row.get("url", ""),
            }
        )
    return enriched


def monetization_distance(a, b):
    high = max(a["rpm"], b["rpm"])
    low = min(a["rpm"], b["rpm"])
    return (high - low) / high if high else 1


def age_distance(a, b):
    if a["exposure_age_days"] == "" or b["exposure_age_days"] == "":
        return 999
    return abs(a["exposure_age_days"] - b["exposure_age_days"])


def build_matched_pairs(rows, min_views, min_pair_views_ratio, max_rpm_delta, max_age_days_delta):
    stable = [r for r in rows if r["views"] >= min_views]
    pairs = []
    used = set()
    pair_no = 1
    for high in sorted(stable, key=lambda r: r["views_per_day"], reverse=True):
        if high["article_id"] in used:
            continue
        candidates = []
        for low in stable:
            if low["article_id"] == high["article_id"] or low["article_id"] in used:
                continue
            if high["views"] / max(low["views"], 1) < min_pair_views_ratio:
                continue
            if monetization_distance(high, low) > max_rpm_delta:
                continue
            if age_distance(high, low) > max_age_days_delta:
                continue
            candidates.append(
                (
                    monetization_distance(high, low),
                    age_distance(high, low),
                    -high["views"] / max(low["views"], 1),
                    low,
                )
            )
        if not candidates:
            continue
        _, _, _, low = sorted(candidates, key=lambda item: item[:3])[0]
        pair_id = f"PAIR-{pair_no:02d}"
        pairs.append((pair_id, "A_MATCHED_HIGH_PLAY", high, low))
        pairs.append((pair_id, "B_MATCHED_LOW_PLAY", low, high))
        used.add(high["article_id"])
        used.add(low["article_id"])
        pair_no += 1
    return pairs


def write_matched_pairs(path, pairs):
    fieldnames = [
        "pair_id",
        "pair_role",
        "article_id",
        "title",
        "views",
        "earnings",
        "earnings_per_1k_views",
        "published_at",
        "published_date",
        "exposure_age_days",
        "age_bucket",
        "views_per_day",
        "matched_with_article_id",
        "views_ratio",
        "rpm_delta_ratio",
        "age_days_delta",
        "like_rate",
        "comment_rate",
        "favorite_rate",
        "evidence_status",
        "url",
    ]
    output_rows = []
    for pair_id, role, row, other in pairs:
        output_rows.append(
            {
                "pair_id": pair_id,
                "pair_role": role,
                "article_id": row["article_id"],
                "title": row["title"],
                "views": int(row["views"]),
                "earnings": row["earnings"],
                "earnings_per_1k_views": round(row["rpm"], 2),
                "published_at": row["published_at"],
                "published_date": row["published_date"],
                "exposure_age_days": row["exposure_age_days"],
                "age_bucket": row["age_bucket"],
                "views_per_day": round(row["views_per_day"], 2),
                "matched_with_article_id": other["article_id"],
                "views_ratio": round(max(row["views"], other["views"]) / max(min(row["views"], other["views"]), 1), 2),
                "rpm_delta_ratio": round(monetization_distance(row, other), 4),
                "age_days_delta": age_distance(row, other),
                "like_rate": round(row["like_rate"], 4),
                "comment_rate": round(row["comment_rate"], 4),
                "favorite_rate": round(row["favorite_rate"], 4),
                "evidence_status": "WEAK_MATCHED_CANDIDATE",
                "url": row["url"],
            }
        )
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def main():
    parser = argparse.ArgumentParser(
        description="Build EXP008 Distribution Model matched-pair candidates from L0 assets."
    )
    parser.add_argument("--input", default="data/l0_content_assets.csv")
    parser.add_argument("--output", default="reports/distribution_matched_pairs_EXP008.csv")
    parser.add_argument("--min-views", type=float, default=150)
    parser.add_argument("--min-pair-views-ratio", type=float, default=2.0)
    parser.add_argument("--max-rpm-delta", type=float, default=0.45)
    parser.add_argument("--max-age-days-delta", type=int, default=14)
    parser.add_argument("--current-date", default=CURRENT_DATE.isoformat())
    args = parser.parse_args()

    current_date = datetime.strptime(args.current_date, "%Y-%m-%d").date()
    rows = enrich_rows(load_rows(Path(args.input)), current_date)
    stable_rows = [r for r in rows if r["views"] >= args.min_views]
    if not rows:
        raise SystemExit("No eligible rows found.")

    pairs = build_matched_pairs(
        rows,
        args.min_views,
        args.min_pair_views_ratio,
        args.max_rpm_delta,
        args.max_age_days_delta,
    )

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    write_matched_pairs(out, pairs)

    print(f"eligible_rows={len(rows)}")
    print(f"stable_rows_min_views_{int(args.min_views)}={len(stable_rows)}")
    print(f"views_median_stable={median(r['views'] for r in stable_rows):.1f}")
    print(f"rpm_median_stable={median(r['rpm'] for r in stable_rows):.2f}")
    print(f"matched_pairs={len(pairs) // 2}")
    print(f"output={out}")


if __name__ == "__main__":
    main()
