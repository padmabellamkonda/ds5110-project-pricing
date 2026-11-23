import json
from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
OUT_MD = Path("docs/data_audit.md")
SNAPSHOTS = ["2026-06-15", "2026-09-19"]

CORE_COLS = [
    "price",
    "neighbourhood_cleansed",
    "room_type",
    "property_type",
    "accommodates",
    "bedrooms",
    "bathrooms",
    "minimum_nights",
    "maximum_nights",
    "review_scores_rating",
    "number_of_reviews",
]

# Approximate Boston bounding box
LAT_MIN, LAT_MAX = 42.22, 42.40
LON_MIN, LON_MAX = -71.20, -70.92


def parse_price(series: pd.Series) -> pd.Series:
    cleaned = (
        series.astype("string")
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    return pd.to_numeric(cleaned, errors="coerce")


def audit_snapshot(snap: str) -> dict:
    listings_path = RAW_DIR / f"{snap}_listings.csv.gz"
    calendar_path = RAW_DIR / f"{snap}_calendar.csv.gz"
    reviews_path = RAW_DIR / f"{snap}_reviews.csv.gz"
    geo_path = RAW_DIR / f"{snap}_neighbourhoods.geojson"

    listings = pd.read_csv(listings_path, low_memory=False)
    calendar = pd.read_csv(calendar_path, usecols=["listing_id", "date"], low_memory=False)
    reviews = pd.read_csv(reviews_path, usecols=["id", "listing_id"], low_memory=False)
    with open(geo_path, "r", encoding="utf-8") as f:
        geo = json.load(f)

    geo_neighbourhoods = {
        feat.get("properties", {}).get("neighbourhood")
        for feat in geo.get("features", [])
        if feat.get("properties", {}).get("neighbourhood")
    }

    # Price parsing & anomalies
    price_num = parse_price(listings["price"])
    valid_pos_price = price_num[price_num > 0]

    # Coordinate & neighbourhood checks
    lat_ok = listings["latitude"].between(LAT_MIN, LAT_MAX)
    lon_ok = listings["longitude"].between(LON_MIN, LON_MAX)
    out_of_bbox = int((~(lat_ok & lon_ok)).sum())
    listing_hoods = set(listings["neighbourhood_cleansed"].dropna().unique())

    # Calendar checks
    cal_dups = int(calendar.duplicated(subset=["listing_id", "date"]).sum())
    cal_orphan_listings = int((~calendar["listing_id"].isin(listings["id"])).sum())

    # Missingness table for core columns
    miss_rows = []
    for col in CORE_COLS:
        if col in listings.columns:
            null_pct = listings[col].isna().mean() * 100
            raw_dtype = str(listings[col].dtype)
            parsed_dtype = "float64 (parsed $)" if col == "price" else raw_dtype
            miss_rows.append((col, raw_dtype, parsed_dtype, f"{null_pct:.2f}%"))
        else:
            miss_rows.append((col, "MISSING", "N/A", "100.00%"))

    return {
        "snap": snap,
        "listings_rows": len(listings),
        "listings_unique_id": int(listings["id"].nunique()),
        "calendar_rows": len(calendar),
        "calendar_unique_key": len(calendar) - cal_dups,
        "calendar_dups": cal_dups,
        "calendar_min_date": str(calendar["date"].min()),
        "calendar_max_date": str(calendar["date"].max()),
        "calendar_orphan_rows": cal_orphan_listings,
        "reviews_rows": len(reviews),
        "reviews_unique_id": int(reviews["id"].nunique()),
        "geo_features": len(geo.get("features", [])),
        "price_nulls": int(price_num.isna().sum()),
        "price_zero": int((price_num == 0).sum()),
        "price_gt_2500": int((price_num > 2500).sum()),
        "price_gt_10000": int((price_num > 10000).sum()),
        "price_median": float(valid_pos_price.median()),
        "price_iqr": float(valid_pos_price.quantile(0.75) - valid_pos_price.quantile(0.25)),
        "out_of_bbox": out_of_bbox,
        "hoods_in_listings_not_geo": sorted(listing_hoods - geo_neighbourhoods),
        "hoods_in_geo_not_listings": sorted(geo_neighbourhoods - listing_hoods),
        "miss_rows": miss_rows,
        "columns": set(listings.columns),
        "listing_ids": set(listings["id"].dropna()),
    }


def main() -> None:
    results = {snap: audit_snapshot(snap) for snap in SNAPSHOTS}
    s1, s2 = results["2026-06-15"], results["2026-09-19"]

    overlap_ids = len(s1["listing_ids"] & s2["listing_ids"])
    only_s1 = len(s1["listing_ids"] - s2["listing_ids"])
    only_s2 = len(s2["listing_ids"] - s1["listing_ids"])
    cols_only_s1 = sorted(s1["columns"] - s2["columns"])
    cols_only_s2 = sorted(s2["columns"] - s1["columns"])

    lines = [
        "# Boston Inside Airbnb Data Audit (`2026-06-15` vs. `2026-09-19`)",
        "",
        "Generated automatically by `src/audit.py` from verified raw snapshots in `data/raw/`.",
        "",
        "## 1. Snapshot & Row-Count Summary",
        "",
        "| Snapshot | Table / File | Total Rows / Features | Unique Primary Key Count | Duplicate PKs |",
        "| :--- | :--- | ---: | ---: | ---: |",
    ]

    for snap in SNAPSHOTS:
        r = results[snap]
        lines.extend([
            f"| `{snap}` | `listings.csv.gz` (`id`) | {r['listings_rows']:,} | {r['listings_unique_id']:,} | {r['listings_rows'] - r['listings_unique_id']:,} |",
            f"| `{snap}` | `calendar.csv.gz` (`listing_id, date`) | {r['calendar_rows']:,} | {r['calendar_unique_key']:,} | {r['calendar_dups']:,} |",
            f"| `{snap}` | `reviews.csv.gz` (`id`) | {r['reviews_rows']:,} | {r['reviews_unique_id']:,} | {r['reviews_rows'] - r['reviews_unique_id']:,} |",
            f"| `{snap}` | `neighbourhoods.geojson` | {r['geo_features']:,} | {r['geo_features']:,} | 0 |",
        ])

    lines.extend([
        "",
        "## 2. Missingness & Data Type Audit (`listings.csv.gz`)",
        "",
        "| Column | Raw Dtype | Parsed Dtype | `2026-06-15` Null % | `2026-09-19` Null % |",
        "| :--- | :--- | :--- | ---: | ---: |",
    ])

    s2_miss_map = {row[0]: row[3] for row in s2["miss_rows"]}
    for col, raw_dt, parsed_dt, null_s1 in s1["miss_rows"]:
        lines.append(f"| `{col}` | `{raw_dt}` | `{parsed_dt}` | {null_s1} | {s2_miss_map[col]} |")

    lines.extend([
        "",
        "## 3. Anomaly, Spatial & Referential Integrity Checks",
        "",
        "| Metric | `2026-06-15` | `2026-09-19` |",
        "| :--- | ---: | ---: |",
        f"| Unparseable / Null `price` rows | {s1['price_nulls']:,} | {s2['price_nulls']:,} |",
        f"| Zero-dollar (`$0`) `price` rows | {s1['price_zero']:,} | {s2['price_zero']:,} |",
        f"| High-price outliers (`> $2,500/night`) | {s1['price_gt_2500']:,} | {s2['price_gt_2500']:,} |",
        f"| Extreme-price outliers (`> $10,000/night`) | {s1['price_gt_10000']:,} | {s2['price_gt_10000']:,} |",
        f"| Median nightly `price` (`price > 0`) | ${s1['price_median']:,.2f} | ${s2['price_median']:,.2f} |",
        f"| IQR nightly `price` (`price > 0`) | ${s1['price_iqr']:,.2f} | ${s2['price_iqr']:,.2f} |",
        f"| Listings outside Boston bounding box | {s1['out_of_bbox']:,} | {s2['out_of_bbox']:,} |",
        f"| `calendar` date range | `{s1['calendar_min_date']}` to `{s1['calendar_max_date']}` | `{s2['calendar_min_date']}` to `{s2['calendar_max_date']}` |",
        f"| `calendar` rows missing parent `listings.id` | {s1['calendar_orphan_rows']:,} | {s2['calendar_orphan_rows']:,} |",
        "",
        f"- **Neighbourhood parity (`2026-06-15`):** in listings but not GeoJSON = `{s1['hoods_in_listings_not_geo']}`; in GeoJSON but not listings = `{s1['hoods_in_geo_not_listings']}`",
        f"- **Neighbourhood parity (`2026-09-19`):** in listings but not GeoJSON = `{s2['hoods_in_listings_not_geo']}`; in GeoJSON but not listings = `{s2['hoods_in_geo_not_listings']}`",
        "",
        "## 4. Cross-Snapshot Drift (`2026-06-15` vs. `2026-09-19`)",
        "",
        f"- **Retained listings (present in both snapshots):** {overlap_ids:,}",
        f"- **Churned listings (only in `2026-06-15`):** {only_s1:,}",
        f"- **New listings (only in `2026-09-19`):** {only_s2:,}",
        f"- **Columns only in `2026-06-15`:** `{cols_only_s1}`",
        f"- **Columns only in `2026-09-19`:** `{cols_only_s2}`",
        "",
        "## 5. Canonical Cleaning & Filtering Rules for Milestone 3",
        "",
        "1. **Target (`price`) parsing:** Strip leading `$` and `,`, cast to `float64`, and exclude rows where `price` is null or `<= 0` from supervised price-modeling splits.",
        "2. **Extreme outlier handling:** Flag `price > $2,500/night` for sensitivity analysis (log-price target `log(price)` is primary; raw-dollar sensitivity excludes `> $10,000/night` errors).",
        "3. **Spatial & neighbourhood validation:** Require `neighbourhood_cleansed` to match canonical Boston neighbourhoods in `neighbourhoods.geojson` and coordinates to fall within `[42.22, 42.40]` lat and `[-71.20, -70.92]` lon.",
        "4. **Missing predictor imputation:** Impute numeric structural features (`bedrooms`, `bathrooms`, `review_scores_rating`) within `(neighbourhood_cleansed, room_type)` strata alongside missingness indicator flags.",
    ])

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
