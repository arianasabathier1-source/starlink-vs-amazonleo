-- Starlink vs Amazon Leo Competitive Analysis
-- PostgreSQL schema (for use with Postgres.app / any Postgres server)

DROP TABLE IF EXISTS satellite_timeline;
CREATE TABLE satellite_timeline (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    company TEXT NOT NULL,
    satellites_in_orbit INTEGER,
    satellites_operational INTEGER,
    cumulative_launched INTEGER,
    milestone_note TEXT
);

DROP TABLE IF EXISTS company_overview;
CREATE TABLE company_overview (
    id SERIAL PRIMARY KEY,
    metric TEXT NOT NULL,
    starlink TEXT,
    amazon_leo TEXT,
    notes TEXT
);

DROP TABLE IF EXISTS pricing_comparison;
CREATE TABLE pricing_comparison (
    id SERIAL PRIMARY KEY,
    company TEXT NOT NULL,
    plan_name TEXT,
    monthly_price_usd NUMERIC,
    download_speed_mbps TEXT,
    hardware_cost_usd NUMERIC,
    hardware_model TEXT,
    notes TEXT
);

DROP TABLE IF EXISTS consumer_decision_factors;
CREATE TABLE consumer_decision_factors (
    id SERIAL PRIMARY KEY,
    factor TEXT NOT NULL,
    starlink_position TEXT,
    amazon_leo_position TEXT,
    weight_rationale TEXT
);
