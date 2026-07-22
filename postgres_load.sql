-- Run this with: psql -d starlink_analysis -f sql/postgres_load.sql
-- (run from the project root folder, so the relative CSV paths resolve correctly)

\copy satellite_timeline(date,company,satellites_in_orbit,satellites_operational,cumulative_launched,milestone_note) FROM 'data/satellite_timeline.csv' WITH (FORMAT csv, HEADER true)

\copy company_overview(metric,starlink,amazon_leo,notes) FROM 'data/company_overview.csv' WITH (FORMAT csv, HEADER true)

\copy pricing_comparison(company,plan_name,monthly_price_usd,download_speed_mbps,hardware_cost_usd,hardware_model,notes) FROM 'data/pricing_comparison.csv' WITH (FORMAT csv, HEADER true)

\copy consumer_decision_factors(factor,starlink_position,amazon_leo_position,weight_rationale) FROM 'data/consumer_decision_factors.csv' WITH (FORMAT csv, HEADER true)

-- Quick sanity check after loading
SELECT 'satellite_timeline' AS table_name, COUNT(*) FROM satellite_timeline
UNION ALL
SELECT 'company_overview', COUNT(*) FROM company_overview
UNION ALL
SELECT 'pricing_comparison', COUNT(*) FROM pricing_comparison
UNION ALL
SELECT 'consumer_decision_factors', COUNT(*) FROM consumer_decision_factors;
