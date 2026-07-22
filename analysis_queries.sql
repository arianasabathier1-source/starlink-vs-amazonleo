-- Analysis queries for Starlink vs Amazon Leo competitive analysis

-- 1. Deployment gap over time (satellites in orbit, both companies, chronological)
SELECT date, company, satellites_in_orbit, satellites_operational
FROM satellite_timeline
ORDER BY date;

-- 2. Current snapshot: latest data point per company
SELECT company, MAX(date) AS latest_date, satellites_in_orbit, satellites_operational
FROM satellite_timeline
GROUP BY company;

-- 3. Deployment velocity: satellites added per period (window function)
SELECT
    company,
    date,
    satellites_in_orbit,
    satellites_in_orbit - LAG(satellites_in_orbit) OVER (
        PARTITION BY company ORDER BY date
    ) AS satellites_added_since_prior_snapshot
FROM satellite_timeline
ORDER BY company, date;

-- 4. Years-to-scale comparison: how long each company took to reach comparable milestones
-- (requires manual mapping since Starlink's "day zero" is 2019-05-24 and Amazon Leo's is 2025-04-28,
--  the first PRODUCTION launch for each — apples-to-apples on production deployment, not prototypes)
SELECT
    company,
    date,
    satellites_in_orbit,
    CAST(
        julianday(date) - julianday(
            CASE company
                WHEN 'Starlink' THEN '2019-05-24'
                WHEN 'Amazon Leo' THEN '2025-04-28'
            END
        ) AS INTEGER
    ) AS days_since_production_start
FROM satellite_timeline
ORDER BY company, days_since_production_start;

-- 5. Pricing tier comparison (only rows with announced pricing)
SELECT company, plan_name, monthly_price_usd, download_speed_mbps, hardware_cost_usd
FROM pricing_comparison
WHERE monthly_price_usd IS NOT NULL
ORDER BY company, monthly_price_usd;

-- 6. Consumer decision factors, flattened for a Tableau text/heatmap table
SELECT factor, starlink_position, amazon_leo_position, weight_rationale
FROM consumer_decision_factors;

-- 7. Company overview key facts, flattened
SELECT metric, starlink, amazon_leo, notes
FROM company_overview;
