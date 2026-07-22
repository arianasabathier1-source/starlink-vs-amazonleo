-- Starlink vs Amazon Leo Competitive Analysis
-- Database schema (SQLite-compatible; portable to Postgres/MySQL with minor type changes)

DROP TABLE IF EXISTS satellite_timeline;
CREATE TABLE satellite_timeline (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    company TEXT NOT NULL,
    satellites_in_orbit INTEGER,
    satellites_operational INTEGER,
    cumulative_launched INTEGER,
    milestone_note TEXT
);

DROP TABLE IF EXISTS company_overview;
CREATE TABLE company_overview (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric TEXT NOT NULL,
    starlink TEXT,
    amazon_leo TEXT,
    notes TEXT
);

DROP TABLE IF EXISTS pricing_comparison;
CREATE TABLE pricing_comparison (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    plan_name TEXT,
    monthly_price_usd REAL,
    download_speed_mbps TEXT,
    hardware_cost_usd REAL,
    hardware_model TEXT,
    notes TEXT
);

DROP TABLE IF EXISTS consumer_decision_factors;
CREATE TABLE consumer_decision_factors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    factor TEXT NOT NULL,
    starlink_position TEXT,
    amazon_leo_position TEXT,
    weight_rationale TEXT
);
