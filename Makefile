.PHONY: data

RELEASE_URL = https://github.com/padmabellamkonda/ds5110-project-pricing/releases/download/v0.1-data

SHA_CHECK := $(shell command -v sha256sum >/dev/null 2>&1 && echo "sha256sum -c" || echo "shasum -a 256 -c")

FILES = 2026-06-15_listings.csv.gz 2026-06-15_calendar.csv.gz 2026-06-15_reviews.csv.gz 2026-06-15_neighbourhoods.geojson \
        2026-09-19_listings.csv.gz 2026-09-19_calendar.csv.gz 2026-09-19_reviews.csv.gz 2026-09-19_neighbourhoods.geojson

data:
	mkdir -p data/raw
	@for file in $(FILES); do \
		if [ ! -f "data/raw/$$file" ]; then \
			echo "Downloading $$file..."; \
			curl -fL "$(RELEASE_URL)/$$file" -o "data/raw/$$file"; \
		fi; \
	done
	$(SHA_CHECK) MANIFEST.sha256
