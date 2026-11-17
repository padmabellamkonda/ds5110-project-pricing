# Data card

## Source
- **Publisher:** Inside Airbnb (Murray Cox)
- **URL:** https://insideairbnb.com/get-the-data/ (Boston, Massachusetts, United States section)
- **Collection Method:** Automated public web scrape of Airbnb listing pages in Boston, MA. Because this is a point-in-time scrape rather than a random sample, hidden, unlisted, or removed properties are excluded.

## Snapshots
- **Build Snapshot (Training/Development):** June 15, 2026
- **Test Snapshot (Later Validation):** September 19, 2026

## License
- **License:** Creative Commons Attribution 4.0 International (CC BY 4.0).
- **Attribution Requirements:** Requires giving clear credit to Inside Airbnb (in `README.md` and on the final GitHub Pages site), providing a link to the CC BY 4.0 license, and noting if any modifications were made to the data.

## Files
- `2026-06-15_listings.csv.gz` & `2026-09-19_listings.csv.gz`: One row per listing (~[X,XXX] rows, ~75 columns); primary source for nightly `price` (stored as text), `neighbourhood_cleansed`, `room_type`, `bedrooms`, and host metadata.
- `2026-06-15_calendar.csv.gz` & `2026-09-19_calendar.csv.gz`: One row per listing per date (~[X,XXX,XXX] rows); used to inspect 365-day forward pricing and availability patterns.
- `2026-06-15_reviews.csv.gz` & `2026-09-19_reviews.csv.gz`: One row per guest review (~[XX,XXX] rows); used for text-based feature extraction/checks alongside listing descriptions.
- `2026-06-15_neighbourhoods.geojson` & `2026-09-19_neighbourhoods.geojson`: One polygon per Boston neighborhood (~25 features); used for spatial grouping and optional neighborhood price mapping.

## Known limits
- **Advertised Base Price vs. Realized Price:** The `price` column in `listings.csv.gz` records the host's listed base rate on the day of the scrape, not the final transaction price paid by guests (which varies dynamically and omits cleaning and service fees).
- **Spatial & Property-Type Confounding:** Entire homes are heavily concentrated in downtown Boston neighborhoods, making neighborhood location and room type strongly confounded when modeling price drivers.

## Checksums
- **Location:** `MANIFEST.sha256` in the repository root.
- **Verification:** Run `make data` from the repository root (which runs `sha256sum -c MANIFEST.sha256` on Linux/Windows or `shasum -a 256 -c MANIFEST.sha256` on macOS) to verify the SHA-256 hashes of all files in `data/raw/`.
