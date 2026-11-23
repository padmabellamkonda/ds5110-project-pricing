# Boston Inside Airbnb Data Audit (`2026-06-15` vs. `2026-09-19`)

Generated automatically by `src/audit.py` from verified raw snapshots in `data/raw/`.

## 1. Snapshot & Row-Count Summary

| Snapshot | Table / File | Total Rows / Features | Unique Primary Key Count | Duplicate PKs |
| :--- | :--- | ---: | ---: | ---: |
| `2026-06-15` | `listings.csv.gz` (`id`) | 4,378 | 4,378 | 0 |
| `2026-06-15` | `calendar.csv.gz` (`listing_id, date`) | 1,611,110 | 1,611,110 | 0 |
| `2026-06-15` | `reviews.csv.gz` (`id`) | 252,910 | 252,910 | 0 |
| `2026-06-15` | `neighbourhoods.geojson` | 26 | 26 | 0 |
| `2026-09-19` | `listings.csv.gz` (`id`) | 4,368 | 4,368 | 0 |
| `2026-09-19` | `calendar.csv.gz` (`listing_id, date`) | 1,594,327 | 1,594,327 | 0 |
| `2026-09-19` | `reviews.csv.gz` (`id`) | 267,731 | 266,845 | 886 |
| `2026-09-19` | `neighbourhoods.geojson` | 26 | 26 | 0 |

## 2. Missingness & Data Type Audit (`listings.csv.gz`)

| Column | Raw Dtype | Parsed Dtype | `2026-06-15` Null % | `2026-09-19` Null % |
| :--- | :--- | :--- | ---: | ---: |
| `price` | `str` | `float64 (parsed $)` | 15.65% | 20.19% |
| `neighbourhood_cleansed` | `str` | `str` | 0.00% | 0.00% |
| `room_type` | `str` | `str` | 0.00% | 0.00% |
| `property_type` | `str` | `str` | 0.00% | 0.00% |
| `accommodates` | `int64` | `int64` | 0.00% | 0.00% |
| `bedrooms` | `float64` | `float64` | 28.80% | 0.00% |
| `bathrooms` | `float64` | `float64` | 23.53% | 100.00% |
| `minimum_nights` | `int64` | `int64` | 0.00% | 0.89% |
| `maximum_nights` | `int64` | `int64` | 0.00% | 0.89% |
| `review_scores_rating` | `float64` | `float64` | 20.58% | 18.06% |
| `number_of_reviews` | `int64` | `int64` | 0.00% | 0.00% |

## 3. Anomaly, Spatial & Referential Integrity Checks

| Metric | `2026-06-15` | `2026-09-19` |
| :--- | ---: | ---: |
| Unparseable / Null `price` rows | 685 | 882 |
| Zero-dollar (`$0`) `price` rows | 0 | 0 |
| High-price outliers (`> $2,500/night`) | 13 | 4 |
| Extreme-price outliers (`> $10,000/night`) | 0 | 0 |
| Median nightly `price` (`price > 0`) | $278.85 | $253.33 |
| IQR nightly `price` (`price > 0`) | $269.00 | $246.90 |
| Listings outside Boston bounding box | 0 | 0 |
| `calendar` date range | `2026-06-15` to `2027-07-05` | `2026-09-19` to `2027-09-19` |
| `calendar` rows missing parent `listings.id` | 13,140 | 0 |

- **Neighbourhood parity (`2026-06-15`):** in listings but not GeoJSON = `[]`; in GeoJSON but not listings = `['Harbor Islands']`
- **Neighbourhood parity (`2026-09-19`):** in listings but not GeoJSON = `[]`; in GeoJSON but not listings = `['Harbor Islands']`

## 4. Cross-Snapshot Drift (`2026-06-15` vs. `2026-09-19`)

- **Retained listings (present in both snapshots):** 3,960
- **Churned listings (only in `2026-06-15`):** 418
- **New listings (only in `2026-09-19`):** 408
- **Columns only in `2026-06-15`:** `[]`
- **Columns only in `2026-09-19`:** `[]`

## 5. Canonical Cleaning & Filtering Rules for Milestone 3

1. **Target (`price`) parsing:** Strip leading `$` and `,`, cast to `float64`, and exclude rows where `price` is null or `<= 0` from supervised price-modeling splits.
2. **Extreme outlier handling:** Flag `price > $2,500/night` for sensitivity analysis (log-price target `log(price)` is primary; raw-dollar sensitivity excludes `> $10,000/night` errors).
3. **Spatial & neighbourhood validation:** Require `neighbourhood_cleansed` to match canonical Boston neighbourhoods in `neighbourhoods.geojson` and coordinates to fall within `[42.22, 42.40]` lat and `[-71.20, -70.92]` lon.
4. **Missing predictor imputation:** Impute numeric structural features (`bedrooms`, `bathrooms`, `review_scores_rating`) within `(neighbourhood_cleansed, room_type)` strata alongside missingness indicator flags.
