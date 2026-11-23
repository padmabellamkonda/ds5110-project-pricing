.PHONY: all data env audit

RELEASE_URL = https://github.com/padmabellamkonda/ds5110-project-pricing/releases/download/v0.1-data

SHA_CHECK := $(shell command -v sha256sum >/dev/null 2>&1 && echo "sha256sum -c" || echo "shasum -a 256 -c")

FILES = 2026-06-15_listings.csv.gz 2026-06-15_calendar.csv.gz 2026-06-15_reviews.csv.gz 2026-06-15_neighbourhoods.geojson \
        2026-09-19_listings.csv.gz 2026-09-19_calendar.csv.gz 2026-09-19_reviews.csv.gz 2026-09-19_neighbourhoods.geojson

PYTHON := $(shell command -v python3 >/dev/null 2>&1 && echo "python3" || echo "python")

all: data audit

env:
	$(PYTHON) -m venv .venv
	.venv/bin/pip install -r requirements.txt

data:
	mkdir -p data/raw
	@for file in $(FILES); do \
		if [ ! -f "data/raw/$$file" ]; then \
			echo "Downloading $$file..."; \
			curl -fL "$(RELEASE_URL)/$$file" -o "data/raw/$$file.part" || { rm -f "data/raw/$$file.part"; echo "ERROR: could not download $$file from $(RELEASE_URL)"; exit 1; }; \
			mv "data/raw/$$file.part" "data/raw/$$file"; \
		fi; \
	done
	$(SHA_CHECK) MANIFEST.sha256

audit: data
	$(PYTHON) src/audit.py
