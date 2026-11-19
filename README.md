 # Boston Short-Term Rentals: Pricing

DS 5110, Fall 2026, Northeastern University. Instructor: Jonathan Mwaura.

Team: Ehsanul, Padma, Sandeep

Track: Pricing

## Question
What drives nightly prices of short-term rentals in Boston, and how much of the variation in price can location alone explain? 

We will answer it with a linear regression on log nightly price, using neighbourhood_cleansed alone and then adding room_type and listing features, from listings.csv.gz. Our target population is public Boston Airbnb listings that appear in the Inside Airbnb snapshots, not all short-term rentals in Boston.

## What this data cannot answer

This data can show how much of the variation in daily price neighbourhood explains among listings in the snapshots. It cannot show what causes prices, or what guests pay.

1. **It is a scrape, not all of Boston.** It leaves out listings Airbnb hides, removes, or never shows, so our R² describes only listings in the snapshots.

2. **Price is a daily price, not what guests paid.** The data dictionary says only "daily price in local currency," so we cannot claim a coefficient tells us what guests pay.

3. **"Location alone" depends on how we measure location.** The data has a neighbourhood label and latitude and longitude, so one R² number is not the effect of location.

4. **Neighbourhood is confounded with room type and size.** Entire homes are concentrated downtown, so we cannot claim a neighbourhood or room type causes a price difference.

## What it finds

To be filled in at the final milestone.

## How to run

You need Python 3.12 or newer (the pinned packages require it), `make` and `curl`.

```bash
git clone https://github.com/padmabellamkonda/ds5110-project-pricing.git
cd ds5110-project-pricing
make env    # create .venv and install the pinned requirements.txt
make data   # download the frozen snapshots into data/raw/ and verify them against MANIFEST.sha256
```

`make data` is safe to re-run: it only downloads files that are missing, stops at the first failed download, and ends by checking every file's SHA-256. `make all` currently runs `data` only; `audit`, `model` and `site` are added at later milestones.

# Team 

Roles by phase (from the project rotation):

| Student | Nov 17 to 23 | Nov 23 to Dec 7 | Dec 7 to 17 |
|---|---|---|---|
| Ehsanul | Data lead | Model lead | Delivery lead |
| Padma | Model lead | Delivery lead | Data lead |
| Sandeep | Delivery lead | Data lead | Model lead |

## Week of Nov 17 to 23 

| Student | Role | Contributions Summary | Links
|---|---|---|---|
| Ehsan | Data Lead | Verified Inside Airbnb Boston snapshots (`2026-06-15` and `2026-09-19`), validated SHA-256 checksums against `v0.1-data`, configured `.gitignore` and `data/` layout, and reviewed PR #1. | [PR #1 Review](https://github.com/padmabellamkonda/ds5110-project-pricing/pull/1), [Data Release v0.1-data](https://github.com/padmabellamkonda/ds5110-project-pricing/releases/tag/v0.1-data) |
| Padma | Model Lead | Added readme, answered what the data cannot answer, answered the proposal question, added contribution log to track, reviewed PRs | [PR #4 Review] (https://github.com/padmabellamkonda/ds5110-project-pricing/pull/4), merged previous branch
| Sandeep | Delivery Lead | Built the repo skeleton: pinned `requirements.txt`, folder stubs for `sql/`, `src/`, `tests/` and `docs/`, and the Makefile `env` and `all` targets. Reviewed PR #1. Filled in the README run instructions, AI use statement and attribution. | [PR #2](https://github.com/padmabellamkonda/ds5110-project-pricing/pull/2), [commit 2043219](https://github.com/padmabellamkonda/ds5110-project-pricing/commit/2043219cfa69cf1018239f573c2bc47f813d9aa3), [PR #1 review](https://github.com/padmabellamkonda/ds5110-project-pricing/pull/1#pullrequestreview-5948488321) |

## Week of Nov 24 to 30 

| Student |
|---|---|---|---|
| Ehsanul | 
| Padma | 
| Sandeep |

## Week of Dec 1 to 7 

| Student |
|---|---|---|---|
| Ehsanul | 
| Padma | 
| Sandeep |

## Week of Dec 8 to 14

| Student |
|---|---|---|---|
| Ehsanul | 
| Padma | 
| Sandeep |

## Week of Dec 15 to 17 

| Student |
|---|---|---|---|
| Ehsanul | 
| Padma | 
| Sandeep |

## Data

Inside Airbnb, Boston, https://insideairbnb.com/get-the-data/. Licensed CC BY 4.0. See data/README.md for the data card.

## Use of AI assistants

- **Claude Code (Anthropic):** used by Sandeep for the delivery work: drafting the repo skeleton, the Makefile targets and the README run instructions, and for checking the team repository's state on GitHub. Sandeep reviewed and edited the output and is responsible for it.

## Attribution

Data: [Inside Airbnb](https://insideairbnb.com/get-the-data/), Boston, licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). We downloaded the 2026-06-15 and 2026-09-19 snapshots and will clean and transform them; Inside Airbnb does not endorse this project.
