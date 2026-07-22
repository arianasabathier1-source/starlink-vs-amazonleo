# Starlink vs. Amazon Leo: A Competitive Analysis

A data-driven competitive analysis of SpaceX's Starlink and Amazon's Leo
(used-to-be Project Kuiper) satellite internet constellations. 

**Data current as of: July 20, 2026**

## Why this project

I grew up hearing about fiber optics and networking from my dad, and space + satellites from my mom's side, so when Starlink and Amazon Leo both started making headlines this year, I couldn't help but dig in. Two of the most resourced companies on the planet are racing to build competing satellite internet networks, and the numbers alone are wild: Starlink has a 7-year head start and over 10 million subscribers, while Amazon Leo is leaning on Amazon's balance sheet, retail reach, and a regulatory deadline it's already about to miss. I wanted to actually run the numbers myself instead of just reading takes on it --- figure out what's true + exciting, and what each company is probably thinking about the other one right now (from a superficial standpoint).

## Dashboard

![Full Dashboard](tableau/full_dashboard.png)

### Individual Views

**Deployment Velocity (Normalized)**
![Deployment Velocity](tableau/deployment_velocity.png)

**Raw Deployment Gap**
![Raw Deployment Gap](tableau/raw_deployment_gap.png)

**Pricing & Commercial Readiness**
![Pricing Readiness](tableau/pricing_readiness.png)

**Consumer Decision Factors**
![Consumer Decision Factors](tableau/consumer_decision_factors.png)

## What's in this repo

```
├── data/                          # Source CSVs (satellite counts, pricing, company facts, consumer factors)
├── sql/
│   ├── schema.sql                 # Table definitions
│   └── analysis_queries.sql       # All analysis queries (deployment velocity, pricing, etc.)
├── analysis/
│   ├── run_analysis.py            # Loads CSVs → SQLite, runs queries, generates charts
│   └── insights.md                # Written analysis and takeaways
├── charts/                        # Generated PNG charts
├── tableau/
│   ├── tableau_satellite_timeline.csv   # Flat export ready for Tableau
│   └── dashboard_guide.md         # Step-by-step Tableau build instructions
└── requirements.txt
```

## Quickstart (SQLite version — no server required)

```bash
pip install -r requirements.txt
python3 analysis/run_analysis.py
```

This rebuilds `data/warehouse.db` (SQLite), regenerates the charts in
`charts/`, and re-exports the Tableau-ready CSV in `tableau/`.

## Quickstart (real Postgres server, for a live Tableau connection)

1. Install [Postgres.app](https://postgresapp.com) and click "Initialize" to start a server.
2. Create the database and load the data:
```bash
createdb starlink_analysis
psql -d starlink_analysis -f sql/postgres_schema.sql
psql -d starlink_analysis -f sql/postgres_load.sql
```
3. In Tableau Desktop: **Connect → PostgreSQL** → Server: `localhost`, Port: `5432`,
   Database: `starlink_analysis`, your Mac username, no password (Postgres.app's
   default is trust-based local auth). All four tables will show up ready to drag
   onto the canvas — no CSV import needed, and any time you re-run
   `postgres_load.sql` with fresh data, hitting "Refresh" in Tableau pulls it live.

## Headline numbers (July 2026)

| Metric | Starlink | Amazon Leo |
|---|---|---|
| Satellites in orbit | ~10,844 | ~394 |
| First production launch | May 24, 2019 | April 28, 2025 |
| Consumer service live? | Yes (since Oct 2020) | No — enterprise beta only |
| Global subscribers | 10,000,000+ | 0 (pre-commercial) |
| Published consumer pricing | $55–$130/mo | Not yet announced |
| Planned constellation | ~12,000 (current licensed phase) | 7,727 (3,236 Gen1 + 4,500 Gen2) |
| Regulatory status | On pace | Requested FCC deadline extension |

## The core strategic question

**Why would a consumer choose a satellite internet provider they've never
heard of over one with a decade of track record and 10 million existing
customers?**

See [`analysis/insights.md`](analysis/insights.md) for the full breakdown, but
the short version: Amazon Leo's near-term advantage isn't going to come from
out-launching SpaceX. It'll come from distribution (Prime bundling, Amazon
retail placement), enterprise credibility spillover (JetBlue, Delta, AT&T
deals landing before the consumer product does), and solving Starlink's
known pain points (congestion pricing, customer service) rather than
competing head-on with satellite count.

## Charts

- `charts/satellite_deployment_over_time.png` — raw deployment gap
- `charts/deployment_velocity_normalized.png` — apples-to-apples, both companies measured from their own day-zero
- `charts/starlink_pricing.png` — current published pricing tiers

## Data sources & caveats

All figures pulled from public trackers (Jonathan McDowell's satellite
catalog, KeepTrack, Orbital Radar), FCC filings, Amazon and SpaceX public
statements, and industry press (Light Reading, SatelliteInternet.com,
CableTV.com) as of July 2026. Third-party trackers disagree by tens to
hundreds of satellites at any given moment due to launch-to-catalog lag —
treat exact counts as directionally accurate rather than precise to the
unit, especially for Amazon Leo, where deployment is changing weekly.

## Pushing this to GitHub

This folder is already a git repo (see below). To push it to your own
GitHub account:

```bash
git remote add origin https://github.com/<your-username>/starlink-vs-amazonleo.git
git branch -M main
git push -u origin main
```
