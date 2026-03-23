#!/usr/bin/env python3
"""
research_db.py — Unified Research Database

Stores ALL autoresearch results in a single SQLite database:
reports, treatments, trials, scores, tumor board reviews, sources.

Usage:
    # Ingest a single report + scores
    python research_db.py ingest report.json --case-id HN-001 --iteration 0

    # Ingest all reports from experiment_reports/
    python research_db.py ingest-all --iteration 0

    # Query the database
    python research_db.py query treatments --top 20
    python research_db.py query trials
    python research_db.py query scores
    python research_db.py query sources --type journal
    python research_db.py query combos
    python research_db.py query supportive
    python research_db.py query board
    python research_db.py query dashboard

    # Export
    python research_db.py export treatments --format csv > treatments.csv
    python research_db.py export full --format json > full_export.json

    # Stats
    python research_db.py stats
"""

import json
import sys
import os
import argparse
import sqlite3
import csv
import io
from datetime import datetime
from pathlib import Path

from evaluate import evaluate_report
from virtual_tumor_board import run_heuristic_board

DB_PATH = "research.db"

# ══════════════════════════════════════════════════════════════════════════════
# SCHEMA
# ══════════════════════════════════════════════════════════════════════════════

SCHEMA = """
-- Benchmark cases (from benchmark_cases.json)
CREATE TABLE IF NOT EXISTS cases (
    case_id         TEXT PRIMARY KEY,
    cancer_type     TEXT NOT NULL,
    stage           TEXT,
    molecular_markers TEXT,  -- JSON array
    patient_age     INTEGER,
    patient_sex     TEXT,
    risk_factors    TEXT,    -- JSON array
    comorbidities   TEXT,    -- JSON array
    performance_status TEXT,
    why_matters     TEXT,
    created_at      TEXT DEFAULT (datetime('now'))
);

-- Research reports (one per case per iteration)
CREATE TABLE IF NOT EXISTS reports (
    report_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id         TEXT NOT NULL,
    iteration       INTEGER NOT NULL DEFAULT 0,
    cancer_type     TEXT,
    stage           TEXT,
    molecular_profile TEXT,  -- JSON array
    generated_date  TEXT,
    report_path     TEXT,
    quality_score   REAL,
    board_score     REAL,
    board_spread    REAL,
    ingested_at     TEXT DEFAULT (datetime('now')),
    UNIQUE(case_id, iteration)
);

-- All treatments across all reports
CREATE TABLE IF NOT EXISTS treatments (
    treatment_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id       INTEGER NOT NULL,
    case_id         TEXT NOT NULL,
    iteration       INTEGER NOT NULL DEFAULT 0,
    rank            INTEGER,
    name            TEXT NOT NULL,
    category        TEXT,
    composite_rating REAL,
    evidence_score  REAL,
    evidence_rationale TEXT,
    survival_score  REAL,
    survival_rationale TEXT,
    accessibility_score REAL,
    accessibility_rationale TEXT,
    safety_score    REAL,
    safety_rationale TEXT,
    biomarker_score REAL,
    biomarker_rationale TEXT,
    mechanism       TEXT,
    study_name      TEXT,
    journal         TEXT,
    study_year      INTEGER,
    sample_size     INTEGER,
    os_treatment    REAL,
    os_control      REAL,
    hazard_ratio    REAL,
    p_value         REAL,
    pfs_treatment   REAL,
    pfs_control     REAL,
    orr_treatment   REAL,
    orr_control     REAL,
    biomarker_requirements TEXT,  -- JSON array
    side_effects    TEXT,         -- JSON array
    availability    TEXT,
    source_urls     TEXT,         -- JSON array
    FOREIGN KEY (report_id) REFERENCES reports(report_id)
);

-- Clinical trials
CREATE TABLE IF NOT EXISTS clinical_trials (
    trial_id_pk     INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id       INTEGER NOT NULL,
    case_id         TEXT NOT NULL,
    iteration       INTEGER NOT NULL DEFAULT 0,
    trial_id        TEXT,
    title           TEXT,
    phase           TEXT,
    status          TEXT,
    sites           TEXT,  -- JSON array
    biomarker_requirements TEXT,  -- JSON array
    early_results   TEXT,
    FOREIGN KEY (report_id) REFERENCES reports(report_id)
);

-- Combination strategies
CREATE TABLE IF NOT EXISTS combinations (
    combo_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id       INTEGER NOT NULL,
    case_id         TEXT NOT NULL,
    iteration       INTEGER NOT NULL DEFAULT 0,
    base_therapy    TEXT,
    combination_partner TEXT,
    evidence_level  TEXT,
    rationale       TEXT,
    FOREIGN KEY (report_id) REFERENCES reports(report_id)
);

-- Supportive care approaches
CREATE TABLE IF NOT EXISTS supportive_care (
    supportive_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id       INTEGER NOT NULL,
    case_id         TEXT NOT NULL,
    iteration       INTEGER NOT NULL DEFAULT 0,
    approach        TEXT,
    evidence        TEXT,
    benefit         TEXT,
    recommendation_level TEXT,
    FOREIGN KEY (report_id) REFERENCES reports(report_id)
);

-- Sources cited
CREATE TABLE IF NOT EXISTS sources (
    source_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id       INTEGER NOT NULL,
    case_id         TEXT NOT NULL,
    iteration       INTEGER NOT NULL DEFAULT 0,
    source_index    INTEGER,
    title           TEXT,
    url             TEXT,
    source_type     TEXT,
    FOREIGN KEY (report_id) REFERENCES reports(report_id)
);

-- Quality evaluation scores
CREATE TABLE IF NOT EXISTS evaluations (
    eval_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id       INTEGER NOT NULL,
    case_id         TEXT NOT NULL,
    iteration       INTEGER NOT NULL DEFAULT 0,
    quality_score   REAL,
    structural_integrity    REAL,
    evidence_depth          REAL,
    tier_coverage           REAL,
    rating_calibration      REAL,
    source_quality          REAL,
    clinical_relevance      REAL,
    combo_supportive        REAL,
    evaluated_at    TEXT,
    FOREIGN KEY (report_id) REFERENCES reports(report_id)
);

-- Tumor board doctor scores
CREATE TABLE IF NOT EXISTS board_reviews (
    review_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id       INTEGER NOT NULL,
    case_id         TEXT NOT NULL,
    iteration       INTEGER NOT NULL DEFAULT 0,
    doctor_id       TEXT,
    doctor_name     TEXT,
    philosophy      TEXT,
    score           REAL,
    notes           TEXT,  -- JSON array
    FOREIGN KEY (report_id) REFERENCES reports(report_id)
);

-- Iteration log (mirrors results.tsv)
CREATE TABLE IF NOT EXISTS iterations (
    iteration_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    iteration       INTEGER NOT NULL,
    mean_score      REAL,
    decision        TEXT,
    note            TEXT,
    strategy_hash   TEXT,
    timestamp       TEXT DEFAULT (datetime('now'))
);

-- Create useful indexes
CREATE INDEX IF NOT EXISTS idx_treatments_case ON treatments(case_id);
CREATE INDEX IF NOT EXISTS idx_treatments_name ON treatments(name);
CREATE INDEX IF NOT EXISTS idx_treatments_rating ON treatments(composite_rating DESC);
CREATE INDEX IF NOT EXISTS idx_treatments_category ON treatments(category);
CREATE INDEX IF NOT EXISTS idx_trials_id ON clinical_trials(trial_id);
CREATE INDEX IF NOT EXISTS idx_sources_url ON sources(url);
CREATE INDEX IF NOT EXISTS idx_reports_case ON reports(case_id);
CREATE INDEX IF NOT EXISTS idx_evaluations_score ON evaluations(quality_score DESC);
"""


def get_db(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Get database connection, creating schema if needed."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


# ══════════════════════════════════════════════════════════════════════════════
# INGEST
# ══════════════════════════════════════════════════════════════════════════════

def ingest_cases(conn: sqlite3.Connection, cases_file: str = "benchmark_cases.json"):
    """Ingest benchmark cases into the database."""
    with open(cases_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    cases = data.get("cases", [])
    for case in cases:
        ctx = case.get("patient_context", {})
        conn.execute("""
            INSERT OR REPLACE INTO cases
            (case_id, cancer_type, stage, molecular_markers, patient_age, patient_sex,
             risk_factors, comorbidities, performance_status, why_matters)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            case["id"],
            case["cancer_type"],
            case["stage"],
            json.dumps(case.get("molecular_markers", [])),
            ctx.get("age"),
            ctx.get("sex"),
            json.dumps(ctx.get("risk_factors", [])),
            json.dumps(ctx.get("comorbidities", [])),
            ctx.get("performance_status"),
            case.get("why_this_case_matters"),
        ))
    conn.commit()
    return len(cases)


def ingest_report(conn: sqlite3.Connection, report_path: str,
                  case_id: str, iteration: int = 0) -> int:
    """Ingest a single report JSON into the database. Returns report_id."""
    with open(report_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    meta = data.get("report_metadata", {})

    # Evaluate
    eval_result = evaluate_report(data)
    board_result = run_heuristic_board(data)

    # Insert report
    cursor = conn.execute("""
        INSERT OR REPLACE INTO reports
        (case_id, iteration, cancer_type, stage, molecular_profile,
         generated_date, report_path, quality_score, board_score, board_spread)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        case_id, iteration,
        meta.get("cancer_type", ""),
        meta.get("stage", ""),
        json.dumps(meta.get("molecular_profile", [])),
        meta.get("generated_date", ""),
        report_path,
        eval_result["quality_score"],
        board_result["board_score"],
        board_result["spread"],
    ))
    report_id = cursor.lastrowid

    # Clear old data for this report (in case of re-ingest)
    for table in ["treatments", "clinical_trials", "combinations",
                  "supportive_care", "sources", "evaluations", "board_reviews"]:
        conn.execute(f"DELETE FROM {table} WHERE case_id=? AND iteration=?",
                     (case_id, iteration))

    # Ingest treatments
    for t in data.get("treatments", []):
        rb = t.get("rating_breakdown", {})
        ev = t.get("key_evidence", {})
        os_data = ev.get("os_months", {}) if isinstance(ev.get("os_months"), dict) else {}
        pfs_data = ev.get("pfs_months", {}) if isinstance(ev.get("pfs_months"), dict) else {}
        orr_data = ev.get("orr_percent", {}) if isinstance(ev.get("orr_percent"), dict) else {}

        conn.execute("""
            INSERT INTO treatments
            (report_id, case_id, iteration, rank, name, category, composite_rating,
             evidence_score, evidence_rationale,
             survival_score, survival_rationale,
             accessibility_score, accessibility_rationale,
             safety_score, safety_rationale,
             biomarker_score, biomarker_rationale,
             mechanism, study_name, journal, study_year, sample_size,
             os_treatment, os_control, hazard_ratio, p_value,
             pfs_treatment, pfs_control, orr_treatment, orr_control,
             biomarker_requirements, side_effects, availability, source_urls)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            report_id, case_id, iteration,
            t.get("rank"), t.get("name"), t.get("category"), t.get("composite_rating"),
            rb.get("evidence_level", {}).get("score"),
            rb.get("evidence_level", {}).get("rationale"),
            rb.get("survival_benefit", {}).get("score"),
            rb.get("survival_benefit", {}).get("rationale"),
            rb.get("accessibility", {}).get("score"),
            rb.get("accessibility", {}).get("rationale"),
            rb.get("safety_profile", {}).get("score"),
            rb.get("safety_profile", {}).get("rationale"),
            rb.get("biomarker_match", {}).get("score"),
            rb.get("biomarker_match", {}).get("rationale"),
            t.get("mechanism_of_action"),
            ev.get("study_name"), ev.get("journal"), ev.get("year"), ev.get("sample_size"),
            os_data.get("treatment"), os_data.get("control"),
            os_data.get("hazard_ratio"), os_data.get("p_value"),
            pfs_data.get("treatment"), pfs_data.get("control"),
            orr_data.get("treatment"), orr_data.get("control"),
            json.dumps(t.get("biomarker_requirements", [])),
            json.dumps(t.get("notable_side_effects", [])),
            t.get("availability"),
            json.dumps(t.get("source_urls", [])),
        ))

    # Ingest clinical trials
    for tr in data.get("clinical_trials", []):
        conn.execute("""
            INSERT INTO clinical_trials
            (report_id, case_id, iteration, trial_id, title, phase, status,
             sites, biomarker_requirements, early_results)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (
            report_id, case_id, iteration,
            tr.get("trial_id"), tr.get("title"), tr.get("phase"), tr.get("status"),
            json.dumps(tr.get("sites", [])),
            json.dumps(tr.get("biomarker_requirements", [])),
            tr.get("early_results"),
        ))

    # Ingest combinations
    for c in data.get("combination_strategies", []):
        conn.execute("""
            INSERT INTO combinations
            (report_id, case_id, iteration, base_therapy, combination_partner,
             evidence_level, rationale)
            VALUES (?,?,?,?,?,?,?)
        """, (
            report_id, case_id, iteration,
            c.get("base_therapy"), c.get("combination_partner"),
            c.get("evidence_level"), c.get("rationale"),
        ))

    # Ingest supportive care
    for s in data.get("supportive_care", []):
        conn.execute("""
            INSERT INTO supportive_care
            (report_id, case_id, iteration, approach, evidence, benefit,
             recommendation_level)
            VALUES (?,?,?,?,?,?,?)
        """, (
            report_id, case_id, iteration,
            s.get("approach"), s.get("evidence"), s.get("benefit"),
            s.get("recommendation_level"),
        ))

    # Ingest sources
    for src in data.get("sources", []):
        conn.execute("""
            INSERT INTO sources
            (report_id, case_id, iteration, source_index, title, url, source_type)
            VALUES (?,?,?,?,?,?,?)
        """, (
            report_id, case_id, iteration,
            src.get("index"), src.get("title"), src.get("url"), src.get("type"),
        ))

    # Ingest evaluation scores
    dims = eval_result.get("dimensions", {})
    conn.execute("""
        INSERT INTO evaluations
        (report_id, case_id, iteration, quality_score,
         structural_integrity, evidence_depth, tier_coverage,
         rating_calibration, source_quality, clinical_relevance,
         combo_supportive, evaluated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        report_id, case_id, iteration, eval_result["quality_score"],
        dims.get("structural_integrity", {}).get("score"),
        dims.get("evidence_depth", {}).get("score"),
        dims.get("tier_coverage", {}).get("score"),
        dims.get("rating_calibration", {}).get("score"),
        dims.get("source_quality", {}).get("score"),
        dims.get("clinical_relevance", {}).get("score"),
        dims.get("combo_supportive_coverage", {}).get("score"),
        eval_result.get("evaluated_at"),
    ))

    # Ingest board reviews
    for dr in board_result.get("individual_results", []):
        conn.execute("""
            INSERT INTO board_reviews
            (report_id, case_id, iteration, doctor_id, doctor_name,
             philosophy, score, notes)
            VALUES (?,?,?,?,?,?,?,?)
        """, (
            report_id, case_id, iteration,
            dr["doctor_id"], dr["doctor_name"],
            dr["philosophy"], dr["score"],
            json.dumps(dr["notes"]),
        ))

    conn.commit()
    return report_id


def ingest_all_reports(conn: sqlite3.Connection, reports_dir: str = "experiment_reports",
                       iteration: int = 0) -> int:
    """Ingest all *_report.json files from the reports directory."""
    count = 0
    report_files = sorted(Path(reports_dir).glob("*_report.json"))

    for rpath in report_files:
        case_id = rpath.stem.replace("_report", "")
        try:
            report_id = ingest_report(conn, str(rpath), case_id, iteration)
            print(f"  Ingested {case_id} -> report_id={report_id}")
            count += 1
        except Exception as e:
            print(f"  ERROR ingesting {case_id}: {e}", file=sys.stderr)

    return count


# ══════════════════════════════════════════════════════════════════════════════
# QUERIES
# ══════════════════════════════════════════════════════════════════════════════

def query_treatments(conn: sqlite3.Connection, top: int = 50, category: str = None):
    """Query top treatments across all cases, ranked by composite rating."""
    sql = """
        SELECT t.name, t.category, t.composite_rating, t.case_id,
               t.evidence_score, t.survival_score, t.safety_score,
               t.study_name, t.sample_size, t.hazard_ratio,
               t.os_treatment, t.availability
        FROM treatments t
        JOIN reports r ON t.report_id = r.report_id
    """
    params = []
    if category:
        sql += " WHERE t.category LIKE ?"
        params.append(f"%{category}%")
    sql += " ORDER BY t.composite_rating DESC LIMIT ?"
    params.append(top)

    rows = conn.execute(sql, params).fetchall()

    print(f"\n{'='*90}")
    print(f"  TOP TREATMENTS ACROSS ALL CASES")
    print(f"{'='*90}")
    print(f"  {'Rating':>6}  {'Treatment':<45} {'Category':<20} {'Case'}")
    print(f"  {'-'*6}  {'-'*45} {'-'*20} {'-'*10}")
    for r in rows:
        print(f"  {r['composite_rating']:>6.1f}  {r['name'][:44]:<45} {(r['category'] or '')[:19]:<20} {r['case_id']}")
    print(f"\n  Total: {len(rows)} treatments\n")
    return rows


def query_trials(conn: sqlite3.Connection):
    """Query all unique clinical trials across cases."""
    rows = conn.execute("""
        SELECT DISTINCT trial_id, title, phase, status,
               GROUP_CONCAT(DISTINCT case_id) as cases,
               early_results
        FROM clinical_trials
        WHERE trial_id IS NOT NULL AND trial_id != ''
        GROUP BY trial_id
        ORDER BY phase DESC, trial_id
    """).fetchall()

    print(f"\n{'='*90}")
    print(f"  CLINICAL TRIALS DATABASE")
    print(f"{'='*90}")
    print(f"  {'Trial ID':<25} {'Phase':<10} {'Status':<20} {'Cases'}")
    print(f"  {'-'*25} {'-'*10} {'-'*20} {'-'*20}")
    for r in rows:
        print(f"  {(r['trial_id'] or '')[:24]:<25} {(r['phase'] or '')[:9]:<10} {(r['status'] or '')[:19]:<20} {r['cases']}")
    print(f"\n  Total unique trials: {len(rows)}\n")
    return rows


def query_scores(conn: sqlite3.Connection):
    """Query evaluation scores across all cases."""
    rows = conn.execute("""
        SELECT e.case_id, e.iteration, e.quality_score,
               e.structural_integrity, e.evidence_depth, e.tier_coverage,
               e.rating_calibration, e.source_quality, e.clinical_relevance,
               e.combo_supportive,
               r.board_score, r.board_spread
        FROM evaluations e
        JOIN reports r ON e.report_id = r.report_id
        ORDER BY e.quality_score DESC
    """).fetchall()

    print(f"\n{'='*90}")
    print(f"  QUALITY SCORES ACROSS ALL CASES")
    print(f"{'='*90}")
    print(f"  {'Case':<10} {'Iter':>4} {'Quality':>8} {'Board':>7} {'Struct':>7} {'EviDep':>7} {'Tiers':>6} {'Rating':>7} {'Source':>7} {'ClinRe':>7} {'Combo':>6}")
    print(f"  {'-'*10} {'-'*4} {'-'*8} {'-'*7} {'-'*7} {'-'*7} {'-'*6} {'-'*7} {'-'*7} {'-'*7} {'-'*6}")
    for r in rows:
        print(f"  {r['case_id']:<10} {r['iteration']:>4} {r['quality_score']:>8.0f} {r['board_score']:>7.1f}"
              f" {r['structural_integrity']:>7.0f} {r['evidence_depth']:>7.0f} {r['tier_coverage']:>6.0f}"
              f" {r['rating_calibration']:>7.0f} {r['source_quality']:>7.0f} {r['clinical_relevance']:>7.0f}"
              f" {r['combo_supportive']:>6.0f}")

    if rows:
        avg_q = sum(r['quality_score'] for r in rows) / len(rows)
        avg_b = sum(r['board_score'] for r in rows) / len(rows)
        print(f"\n  Mean quality: {avg_q:.1f}/100 | Mean board: {avg_b:.1f}/100\n")
    return rows


def query_sources(conn: sqlite3.Connection, source_type: str = None):
    """Query all unique sources across cases."""
    sql = """
        SELECT DISTINCT url, title, source_type,
               GROUP_CONCAT(DISTINCT case_id) as cited_in,
               COUNT(DISTINCT case_id) as citation_count
        FROM sources
        WHERE url IS NOT NULL AND url != ''
    """
    params = []
    if source_type:
        sql += " AND source_type LIKE ?"
        params.append(f"%{source_type}%")
    sql += " GROUP BY url ORDER BY citation_count DESC, title"

    rows = conn.execute(sql, params).fetchall()

    print(f"\n{'='*90}")
    print(f"  SOURCES DATABASE")
    print(f"{'='*90}")
    print(f"  {'Cited':>5}  {'Type':<15} {'Title':<50} {'Cases'}")
    print(f"  {'-'*5}  {'-'*15} {'-'*50} {'-'*15}")
    for r in rows:
        print(f"  {r['citation_count']:>5}  {(r['source_type'] or 'unknown')[:14]:<15} {(r['title'] or '')[:49]:<50} {r['cited_in']}")
    print(f"\n  Total unique sources: {len(rows)}\n")
    return rows


def query_combos(conn: sqlite3.Connection):
    """Query all combination strategies."""
    rows = conn.execute("""
        SELECT base_therapy, combination_partner, evidence_level,
               GROUP_CONCAT(DISTINCT case_id) as cases,
               rationale
        FROM combinations
        GROUP BY base_therapy, combination_partner
        ORDER BY evidence_level DESC
    """).fetchall()

    print(f"\n{'='*90}")
    print(f"  COMBINATION STRATEGIES DATABASE")
    print(f"{'='*90}")
    for r in rows:
        print(f"  {r['base_therapy']} + {r['combination_partner']}")
        print(f"    Evidence: {r['evidence_level']} | Cases: {r['cases']}")
        print()
    print(f"  Total unique combos: {len(rows)}\n")
    return rows


def query_supportive(conn: sqlite3.Connection):
    """Query all supportive care approaches."""
    rows = conn.execute("""
        SELECT approach, recommendation_level, evidence, benefit,
               GROUP_CONCAT(DISTINCT case_id) as cases,
               COUNT(DISTINCT case_id) as frequency
        FROM supportive_care
        GROUP BY approach
        ORDER BY frequency DESC
    """).fetchall()

    print(f"\n{'='*90}")
    print(f"  SUPPORTIVE CARE DATABASE")
    print(f"{'='*90}")
    for r in rows:
        print(f"  [{r['recommendation_level']}] {r['approach']} (cited in {r['frequency']} cases)")
        print(f"    Benefit: {(r['benefit'] or '')[:80]}")
        print()
    print(f"  Total unique approaches: {len(rows)}\n")
    return rows


def query_board(conn: sqlite3.Connection):
    """Query tumor board scores across all cases."""
    rows = conn.execute("""
        SELECT doctor_name, philosophy,
               AVG(score) as avg_score,
               MIN(score) as min_score,
               MAX(score) as max_score,
               COUNT(*) as reviews
        FROM board_reviews
        GROUP BY doctor_id
        ORDER BY avg_score DESC
    """).fetchall()

    print(f"\n{'='*70}")
    print(f"  TUMOR BOARD — DOCTOR SCORING SUMMARY")
    print(f"{'='*70}")
    print(f"  {'Doctor':<20} {'Philosophy':<30} {'Avg':>5} {'Min':>5} {'Max':>5} {'N':>3}")
    print(f"  {'-'*20} {'-'*30} {'-'*5} {'-'*5} {'-'*5} {'-'*3}")
    for r in rows:
        print(f"  {r['doctor_name']:<20} {r['philosophy'][:29]:<30} {r['avg_score']:>5.1f} {r['min_score']:>5.0f} {r['max_score']:>5.0f} {r['reviews']:>3}")
    print()
    return rows


def query_dashboard(conn: sqlite3.Connection):
    """Print a comprehensive dashboard of the entire database."""
    print(f"\n{'='*70}")
    print(f"  AUTORESEARCH DATABASE DASHBOARD")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}")

    # Counts
    counts = {}
    for table in ["cases", "reports", "treatments", "clinical_trials",
                  "combinations", "supportive_care", "sources",
                  "evaluations", "board_reviews"]:
        row = conn.execute(f"SELECT COUNT(*) as n FROM {table}").fetchone()
        counts[table] = row["n"]
        print(f"  {table:<20} {row['n']:>6} rows")

    print()

    # Top 5 treatments globally
    top5 = conn.execute("""
        SELECT name, composite_rating, category, case_id
        FROM treatments ORDER BY composite_rating DESC LIMIT 5
    """).fetchall()
    if top5:
        print(f"  Top 5 Treatments Globally:")
        for i, t in enumerate(top5):
            print(f"    {i+1}. [{t['composite_rating']:.1f}] {t['name'][:50]} ({t['case_id']})")
        print()

    # Score summary
    score_row = conn.execute("""
        SELECT AVG(quality_score) as avg_q, MIN(quality_score) as min_q,
               MAX(quality_score) as max_q, COUNT(*) as n
        FROM evaluations
    """).fetchone()
    if score_row and score_row["n"] > 0:
        print(f"  Quality Scores: avg={score_row['avg_q']:.1f} min={score_row['min_q']:.0f} max={score_row['max_q']:.0f} (n={score_row['n']})")

    board_row = conn.execute("""
        SELECT AVG(board_score) as avg_b FROM reports WHERE board_score IS NOT NULL
    """).fetchone()
    if board_row and board_row["avg_b"]:
        print(f"  Board Scores:   avg={board_row['avg_b']:.1f}")

    # Unique treatments
    unique_tx = conn.execute("SELECT COUNT(DISTINCT name) as n FROM treatments").fetchone()
    print(f"  Unique treatment names: {unique_tx['n']}")

    # Unique trials
    unique_tr = conn.execute(
        "SELECT COUNT(DISTINCT trial_id) as n FROM clinical_trials WHERE trial_id != ''"
    ).fetchone()
    print(f"  Unique trial IDs: {unique_tr['n']}")

    # Unique sources
    unique_src = conn.execute(
        "SELECT COUNT(DISTINCT url) as n FROM sources WHERE url != ''"
    ).fetchone()
    print(f"  Unique source URLs: {unique_src['n']}")

    print()


# ══════════════════════════════════════════════════════════════════════════════
# EXPORT
# ══════════════════════════════════════════════════════════════════════════════

def export_treatments_csv(conn: sqlite3.Connection) -> str:
    """Export all treatments as CSV."""
    rows = conn.execute("""
        SELECT t.case_id, t.iteration, t.rank, t.name, t.category,
               t.composite_rating, t.evidence_score, t.survival_score,
               t.accessibility_score, t.safety_score, t.biomarker_score,
               t.study_name, t.journal, t.study_year, t.sample_size,
               t.os_treatment, t.os_control, t.hazard_ratio, t.p_value,
               t.pfs_treatment, t.pfs_control, t.orr_treatment, t.orr_control,
               t.availability, t.mechanism,
               t.biomarker_requirements, t.side_effects, t.source_urls
        FROM treatments t
        ORDER BY t.composite_rating DESC
    """).fetchall()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([desc[0] for desc in conn.execute("""
        SELECT t.case_id, t.iteration, t.rank, t.name, t.category,
               t.composite_rating, t.evidence_score, t.survival_score,
               t.accessibility_score, t.safety_score, t.biomarker_score,
               t.study_name, t.journal, t.study_year, t.sample_size,
               t.os_treatment, t.os_control, t.hazard_ratio, t.p_value,
               t.pfs_treatment, t.pfs_control, t.orr_treatment, t.orr_control,
               t.availability, t.mechanism,
               t.biomarker_requirements, t.side_effects, t.source_urls
        FROM treatments t LIMIT 0
    """).description])
    for r in rows:
        writer.writerow(list(r))

    return output.getvalue()


def export_full_json(conn: sqlite3.Connection) -> dict:
    """Export entire database as a single JSON structure."""
    result = {
        "exported_at": datetime.now().isoformat(),
        "cases": [],
        "reports": [],
        "treatments": [],
        "clinical_trials": [],
        "combinations": [],
        "supportive_care": [],
        "sources": [],
        "evaluations": [],
        "board_reviews": [],
    }

    for table_name in result:
        if table_name in ("exported_at",):
            continue
        rows = conn.execute(f"SELECT * FROM {table_name}").fetchall()
        result[table_name] = [dict(r) for r in rows]

    return result


# ══════════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Unified research database for autoresearch loop")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # ingest
    p_ingest = subparsers.add_parser("ingest", help="Ingest a single report")
    p_ingest.add_argument("report", help="Path to report JSON file")
    p_ingest.add_argument("--case-id", required=True, help="Case ID (e.g. HN-001)")
    p_ingest.add_argument("--iteration", type=int, default=0)
    p_ingest.add_argument("--db", default=DB_PATH)

    # ingest-all
    p_all = subparsers.add_parser("ingest-all", help="Ingest all reports from directory")
    p_all.add_argument("--dir", default="experiment_reports", help="Reports directory")
    p_all.add_argument("--iteration", type=int, default=0)
    p_all.add_argument("--db", default=DB_PATH)

    # ingest-cases
    p_cases = subparsers.add_parser("ingest-cases", help="Ingest benchmark cases")
    p_cases.add_argument("--file", default="benchmark_cases.json")
    p_cases.add_argument("--db", default=DB_PATH)

    # query
    p_query = subparsers.add_parser("query", help="Query the database")
    p_query.add_argument("what", choices=["treatments", "trials", "scores", "sources",
                                           "combos", "supportive", "board", "dashboard"])
    p_query.add_argument("--top", type=int, default=50)
    p_query.add_argument("--category", default=None)
    p_query.add_argument("--type", dest="source_type", default=None)
    p_query.add_argument("--db", default=DB_PATH)

    # export
    p_export = subparsers.add_parser("export", help="Export data")
    p_export.add_argument("what", choices=["treatments", "full"])
    p_export.add_argument("--format", choices=["csv", "json"], default="csv")
    p_export.add_argument("--db", default=DB_PATH)

    # stats
    p_stats = subparsers.add_parser("stats", help="Show database statistics")
    p_stats.add_argument("--db", default=DB_PATH)

    # init
    p_init = subparsers.add_parser("init", help="Initialize database + ingest cases and all reports")
    p_init.add_argument("--db", default=DB_PATH)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    conn = get_db(args.db)

    if args.command == "ingest":
        rid = ingest_report(conn, args.report, args.case_id, args.iteration)
        print(f"Ingested {args.case_id} -> report_id={rid}")

    elif args.command == "ingest-all":
        n = ingest_all_reports(conn, args.dir, args.iteration)
        print(f"Ingested {n} reports from {args.dir}/")

    elif args.command == "ingest-cases":
        n = ingest_cases(conn, args.file)
        print(f"Ingested {n} benchmark cases")

    elif args.command == "query":
        if args.what == "treatments":
            query_treatments(conn, top=args.top, category=args.category)
        elif args.what == "trials":
            query_trials(conn)
        elif args.what == "scores":
            query_scores(conn)
        elif args.what == "sources":
            query_sources(conn, source_type=args.source_type)
        elif args.what == "combos":
            query_combos(conn)
        elif args.what == "supportive":
            query_supportive(conn)
        elif args.what == "board":
            query_board(conn)
        elif args.what == "dashboard":
            query_dashboard(conn)

    elif args.command == "export":
        if args.what == "treatments":
            if args.format == "csv":
                print(export_treatments_csv(conn))
            else:
                rows = conn.execute("SELECT * FROM treatments ORDER BY composite_rating DESC").fetchall()
                print(json.dumps([dict(r) for r in rows], indent=2))
        elif args.what == "full":
            print(json.dumps(export_full_json(conn), indent=2, default=str))

    elif args.command == "stats":
        query_dashboard(conn)

    elif args.command == "init":
        # Full initialization: cases + all reports
        if os.path.exists("benchmark_cases.json"):
            n = ingest_cases(conn)
            print(f"Ingested {n} benchmark cases")
        if os.path.exists("experiment_reports"):
            n = ingest_all_reports(conn, "experiment_reports", 0)
            print(f"Ingested {n} reports")
        query_dashboard(conn)

    conn.close()


if __name__ == "__main__":
    main()
