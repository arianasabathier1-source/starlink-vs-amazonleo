# Building the Tableau Dashboard

Tableau isn't something I can drive directly from here, so this folder gives you
everything you need to build it in ~20 minutes.

## 1. Connect your data sources
Open Tableau Desktop (or Tableau Public) → **Connect → Text File** → select:
- `tableau_satellite_timeline.csv` (primary — this is the one that drives the main visuals)
- `../data/pricing_comparison.csv`
- `../data/consumer_decision_factors.csv`
- `../data/company_overview.csv`

If you'd rather connect directly to the SQL layer instead of flat files:
**Connect → More… → SQLite ODBC** (or use the free SQLite Tableau connector) and
point it at `../data/warehouse.db`. That gives you all four tables plus the option
to write live calculated fields against them.

## 2. Recommended dashboard layout (4 sheets → 1 dashboard)

**Sheet 1 — "The Deployment Gap" (line chart)**
- Columns: `date` | Rows: `satellites_in_orbit` | Color: `company`
- This is your hero visual. Starlink at ~10,800 vs. Amazon Leo at ~394 tells the
  whole first-mover story in one look.

**Sheet 2 — "Apples to Apples" (line chart, normalized)**
- Create a calculated field `days_since_production_start` (see `sql/analysis_queries.sql`
  query #4 for the logic — replicate it as a Tableau calculated field using
  `DATEDIFF` from each company's first production launch date).
- This reframes the comparison fairly: Amazon Leo is ~15 months into deployment,
  not 7 years behind — it's a much closer race on velocity than raw totals suggest.

**Sheet 3 — "Pricing Reality Check" (bar chart)**
- From `pricing_comparison.csv`, filter to non-null `monthly_price_usd`.
- Note Amazon Leo has zero published consumer pricing as of July 2026 — worth
  calling out as a visible gap on the dashboard itself, not just a footnote.

**Sheet 4 — "Why Would You Choose an Unknown Provider?" (highlight table / heat map)**
- From `consumer_decision_factors.csv`: rows = `factor`, columns = `starlink_position`
  and `amazon_leo_position`, using text with conditional color (green = advantage,
  yellow = neutral/unknown, red = disadvantage). This is the consulting-style
  "who wins the room" slide.

## 3. Dashboard assembly
- New Dashboard → drag all 4 sheets onto a 1200x800 canvas
- Add a title: "Starlink vs Amazon Leo: Competitive Positioning, July 2026"
- Add a text box footnote citing that Amazon Leo figures are approximate given
  rapid weekly deployment and inconsistent third-party tracker counts
- Publish to Tableau Public or Tableau Server, then link it from the README

## 4. Suggested filters/interactivity
- Date range slider on Sheet 1 and 2
- Company multi-select filter dropdown, applied across all sheets
