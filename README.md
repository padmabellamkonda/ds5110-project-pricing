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

make data   # download the frozen snapshot into data/raw/

# Team contribution log

Roles by phase (from the project rotation):

| Student | Nov 17 to 23 | Nov 23 to Dec 7 | Dec 7 to 17 |
|---|---|---|---|
| Ehsanul | Data lead | Model lead | Delivery lead |
| Padma | Model lead | Delivery lead | Data lead |
| Sandeep | Delivery lead | Data lead | Model lead |

## Week of Nov 17 to 23 

| Student |
|---|---|---|---|
| Ehsanul | 
| Padma | 
| Sandeep |

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


## Attribution


Data: Inside Airbnb (CC BY 4.0).
