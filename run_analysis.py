"""
Starlink vs Amazon Leo — Competitive Analysis Pipeline
--------------------------------------------------------
1. Loads CSV source data into a local SQLite database (data/warehouse.db)
2. Runs the analysis queries defined in sql/analysis_queries.sql
3. Generates chart images for the Tableau dashboard / README
4. Writes a flattened export CSV that Tableau can connect to directly

Run with: python3 analysis/run_analysis.py
"""

import sqlite3
import csv
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
SQL_DIR = os.path.join(ROOT, "sql")
CHARTS_DIR = os.path.join(ROOT, "charts")
TABLEAU_DIR = os.path.join(ROOT, "tableau")
DB_PATH = os.path.join(DATA_DIR, "warehouse.db")


def load_csv_to_table(conn, csv_path, table_name):
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        cols = reader.fieldnames

    placeholders = ",".join("?" for _ in cols)
    col_list = ",".join(cols)
    conn.executemany(
        f"INSERT INTO {table_name} ({col_list}) VALUES ({placeholders})",
        [tuple(row[c] for c in cols) for row in rows],
    )
    conn.commit()
    print(f"Loaded {len(rows)} rows into {table_name}")


def build_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)

    with open(os.path.join(SQL_DIR, "schema.sql")) as f:
        conn.executescript(f.read())

    load_csv_to_table(conn, os.path.join(DATA_DIR, "satellite_timeline.csv"), "satellite_timeline")
    load_csv_to_table(conn, os.path.join(DATA_DIR, "company_overview.csv"), "company_overview")
    load_csv_to_table(conn, os.path.join(DATA_DIR, "pricing_comparison.csv"), "pricing_comparison")
    load_csv_to_table(conn, os.path.join(DATA_DIR, "consumer_decision_factors.csv"), "consumer_decision_factors")

    return conn


def chart_satellite_deployment(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT date, company, satellites_in_orbit
        FROM satellite_timeline
        ORDER BY date
    """)
    rows = cur.fetchall()

    starlink = [(r[0], r[2]) for r in rows if r[1] == "Starlink"]
    kuiper = [(r[0], r[2]) for r in rows if r[1] == "Amazon Leo"]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot([r[0] for r in starlink], [r[1] for r in starlink], marker="o", label="Starlink", color="#1c3f95", linewidth=2)
    ax.plot([r[0] for r in kuiper], [r[1] for r in kuiper], marker="o", label="Amazon Leo", color="#ff9900", linewidth=2)
    ax.set_title("Satellites in Orbit Over Time: Starlink vs Amazon Leo", fontsize=13, fontweight="bold")
    ax.set_ylabel("Satellites in orbit")
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))
    ax.tick_params(axis="x", rotation=45)
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    out_path = os.path.join(CHARTS_DIR, "satellite_deployment_over_time.png")
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"Saved {out_path}")


def chart_deployment_velocity(conn):
    """Compares each company's growth curve starting from their own production-deployment day zero."""
    cur = conn.cursor()
    cur.execute("""
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
            ) AS days_since_start
        FROM satellite_timeline
        WHERE date >= CASE company WHEN 'Starlink' THEN '2019-05-24' ELSE '2025-04-28' END
        ORDER BY company, days_since_start
    """)
    rows = cur.fetchall()
    starlink = [(r[3], r[2]) for r in rows if r[0] == "Starlink"]
    kuiper = [(r[3], r[2]) for r in rows if r[0] == "Amazon Leo"]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot([r[0] for r in starlink], [r[1] for r in starlink], marker="o", label="Starlink (from first production launch)", color="#1c3f95", linewidth=2)
    ax.plot([r[0] for r in kuiper], [r[1] for r in kuiper], marker="o", label="Amazon Leo (from first production launch)", color="#ff9900", linewidth=2)
    ax.set_title("Apples-to-Apples: Satellites Deployed Since Each Company's\nFirst PRODUCTION Launch (Day Zero Normalized)", fontsize=12, fontweight="bold")
    ax.set_xlabel("Days since first production satellite launch")
    ax.set_ylabel("Satellites in orbit")
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    out_path = os.path.join(CHARTS_DIR, "deployment_velocity_normalized.png")
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"Saved {out_path}")


def chart_pricing(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT plan_name, monthly_price_usd
        FROM pricing_comparison
        WHERE company = 'Starlink' AND monthly_price_usd IS NOT NULL
        ORDER BY monthly_price_usd
    """)
    rows = cur.fetchall()
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar([r[0] for r in rows], [r[1] for r in rows], color="#1c3f95")
    ax.set_title("Starlink Current Pricing by Plan\n(Amazon Leo: pricing not yet announced as of Jul 2026)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Monthly price (USD)")
    ax.tick_params(axis="x", rotation=20)
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 1, f"${b.get_height():.0f}", ha="center", fontsize=9)
    fig.tight_layout()
    out_path = os.path.join(CHARTS_DIR, "starlink_pricing.png")
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"Saved {out_path}")


def export_tableau_flat_file(conn):
    """Builds one wide, Tableau-friendly CSV joining timeline + a company key so Tableau
    can build the dashboard without needing to understand the relational schema."""
    cur = conn.cursor()
    cur.execute("""
        SELECT date, company, satellites_in_orbit, satellites_operational, cumulative_launched, milestone_note
        FROM satellite_timeline
        ORDER BY date
    """)
    rows = cur.fetchall()
    out_path = os.path.join(TABLEAU_DIR, "tableau_satellite_timeline.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "company", "satellites_in_orbit", "satellites_operational", "cumulative_launched", "milestone_note"])
        writer.writerows(rows)
    print(f"Saved Tableau extract: {out_path}")


def print_summary(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT company, satellites_in_orbit, satellites_operational, date
        FROM satellite_timeline s1
        WHERE date = (SELECT MAX(date) FROM satellite_timeline s2 WHERE s2.company = s1.company)
    """)
    print("\n=== CURRENT SNAPSHOT ===")
    for row in cur.fetchall():
        print(f"{row[0]}: {row[1]} in orbit, {row[2]} operational (as of {row[3]})")


if __name__ == "__main__":
    conn = build_database()
    os.makedirs(CHARTS_DIR, exist_ok=True)
    chart_satellite_deployment(conn)
    chart_deployment_velocity(conn)
    chart_pricing(conn)
    export_tableau_flat_file(conn)
    print_summary(conn)
    conn.close()
    print("\nDone. Database at data/warehouse.db, charts in charts/, Tableau extract in tableau/")
