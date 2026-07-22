-- Analysis queries for Starlink vs Amazon Leo — PostgreSQL version
-- (Postgres lets you subtract two DATE values directly to get an integer number of days —
--  no julianday() conversion needed like in SQLite)

-- 1. Deployment gap over time
SELECT date, company, satellites_in_orbit, satellites_operational
FROM satellite_timeline
ORDER BY date;

-- 2. Current snapshot per company
SELECT DISTINCT ON (company) company, date, satellites_in_orbit, satellites_operational
FROM satellite_timeline
ORDER BY company, date DESC;

-- 3. Deployment velocity (window function — same LAG() pattern as SQLite)
SELECT
    company,
    date,
    satellites_in_orbit,
    satellites_in_orbit - LAG(satellites_in_orbit) OVER (
        PARTITION BY company ORDER BY date
    ) AS satellites_added_since_prior_snapshot
FROM satellite_timeline
ORDER BY company, date;

-- 4. Normalized "days since first production launch" — THE key story query
SELECT
    company,
    date,
    satellites_in_orbit,
    date - (CASE company
                WHEN 'Starlink' THEN DATE '2019-05-24'
                WHEN 'Amazon Leo' THEN DATE '2025-04-28'
            END) AS days_since_production_start
FROM satellite_timeline
ORDER BY company, days_since_production_start;

-- 5. Pricing comparison (announced pricing only)
SELECT company, plan_name, monthly_price_usd, download_speed_mbps, hardware_cost_usd
FROM pricing_comparison
WHERE monthly_price_usd IS NOT NULL
ORDER BY company, monthly_price_usd;

-- 6. Consumer decision factors
SELECT factor, starlink_position, amazon_leo_position, weight_rationale
FROM consumer_decision_factors;

-- 7. Company overview facts
SELECT metric, starlink, amazon_leo, notes
FROM company_overview;
