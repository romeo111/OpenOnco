#!/usr/bin/env python3
"""
server.py — Orchestrator Server for Cancer AutoResearch Distributed Platform

Implements the distributed Karpathy autoresearch loop:
  - Workers pull jobs (cancer_type + benchmark_case + strategy_hash)
  - Workers submit scored results
  - Orchestrator promotes strategy variants that improve mean_score by ≥2.5
    across ≥3 independent worker validations

Zero external dependencies — uses only Python stdlib.

Usage:
    python server.py
    python server.py --port 8080 --host 0.0.0.0
    python server.py --db-path /data/orchestrator.db --strategy strategy.md
    python server.py --port 8080 --host 0.0.0.0 --db-path orchestrator.db
"""

import argparse
import hashlib
import http.server
import json
import logging
import os
import signal
import sqlite3
import sys
import threading
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import parse_qs, urlparse


# ── Constants ─────────────────────────────────────────────────────────────────

VERSION = "1.0.0"
PROMOTION_MIN_VALIDATIONS = 3
PROMOTION_MIN_SCORE_DELTA = 2.5
JOB_TIMEOUT_SECONDS = 3600        # 1 hour — re-queue if not submitted
SIMPLE_CASE_COMPLEXITY_MAX = 4    # cases with complexity ≤ 4 assigned to local workers


# ── NDJSON Logging ────────────────────────────────────────────────────────────

class NDJSONHandler(logging.StreamHandler):
    """Emit log records as newline-delimited JSON."""
    def emit(self, record: logging.LogRecord) -> None:
        log_entry = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "msg": record.getMessage(),
        }
        if record.exc_info:
            log_entry["exc"] = self.formatException(record.exc_info)
        try:
            self.stream.write(json.dumps(log_entry) + "\n")
            self.flush()
        except Exception:
            self.handleError(record)


def setup_logging(log_file: Optional[str] = None) -> logging.Logger:
    logger = logging.getLogger("orchestrator")
    logger.setLevel(logging.INFO)
    handler = NDJSONHandler(sys.stdout)
    logger.addHandler(handler)
    if log_file:
        fh = NDJSONHandler(open(log_file, "a", encoding="utf-8"))
        logger.addHandler(fh)
    return logger


log = setup_logging()


# ── Database Layer ────────────────────────────────────────────────────────────

class OrchestratorDB:
    """All database operations for the orchestrator."""

    SCHEMA = """
    CREATE TABLE IF NOT EXISTS workers (
        worker_id       TEXT PRIMARY KEY,
        mode            TEXT NOT NULL CHECK (mode IN ('local', 'claude')),
        gpu_model       TEXT,
        registered_at   TEXT NOT NULL,
        last_seen       TEXT NOT NULL,
        jobs_completed  INTEGER DEFAULT 0,
        jobs_submitted  INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS strategy_variants (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        hash            TEXT UNIQUE NOT NULL,
        parent_hash     TEXT,
        content         TEXT NOT NULL,
        mutation_desc   TEXT,
        is_canonical    INTEGER DEFAULT 0,
        mean_score      REAL DEFAULT 0.0,
        validation_count INTEGER DEFAULT 0,
        promoted_at     TEXT,
        created_at      TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS jobs (
        job_id          TEXT PRIMARY KEY,
        cancer_type     TEXT NOT NULL,
        category        TEXT NOT NULL,
        case_id         TEXT NOT NULL,
        case_data       TEXT NOT NULL,
        complexity      INTEGER DEFAULT 0,
        strategy_hash   TEXT NOT NULL,
        status          TEXT NOT NULL DEFAULT 'pending'
                        CHECK (status IN ('pending','assigned','completed','stale')),
        assigned_to     TEXT,
        assigned_at     TEXT,
        completed_at    TEXT,
        score           REAL,
        quality_dims    TEXT,
        report_path     TEXT,
        preferred_mode  TEXT DEFAULT 'any'
    );

    CREATE TABLE IF NOT EXISTS reports (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id         TEXT NOT NULL,
        cancer_type     TEXT NOT NULL,
        category        TEXT NOT NULL,
        strategy_hash   TEXT NOT NULL,
        worker_id       TEXT NOT NULL,
        score           REAL NOT NULL,
        quality_dims    TEXT,
        report_path     TEXT,
        created_at      TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS mutations (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        base_hash       TEXT NOT NULL,
        variant_content TEXT NOT NULL,
        variant_hash    TEXT NOT NULL,
        mutation_desc   TEXT,
        proposed_by     TEXT NOT NULL,
        proposed_at     TEXT NOT NULL,
        status          TEXT NOT NULL DEFAULT 'proposed'
                        CHECK (status IN ('proposed','validating','promoted','rejected')),
        validation_count INTEGER DEFAULT 0,
        mean_score      REAL DEFAULT 0.0,
        promoted_at     TEXT
    );

    CREATE TABLE IF NOT EXISTS mutation_validations (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        mutation_id     INTEGER NOT NULL REFERENCES mutations(id),
        worker_id       TEXT NOT NULL,
        case_id         TEXT NOT NULL,
        score           REAL NOT NULL,
        quality_dims    TEXT,
        validated_at    TEXT NOT NULL
    );

    CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
    CREATE INDEX IF NOT EXISTS idx_jobs_strategy ON jobs(strategy_hash);
    CREATE INDEX IF NOT EXISTS idx_reports_cancer ON reports(cancer_type);
    CREATE INDEX IF NOT EXISTS idx_mutations_status ON mutations(status);
    """

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._local = threading.local()
        self._init_db()

    def _conn(self) -> sqlite3.Connection:
        """Thread-local SQLite connection."""
        if not hasattr(self._local, "conn") or self._local.conn is None:
            self._local.conn = sqlite3.connect(self.db_path)
            self._local.conn.row_factory = sqlite3.Row
            self._local.conn.execute("PRAGMA journal_mode=WAL")
            self._local.conn.execute("PRAGMA foreign_keys=ON")
        return self._local.conn

    def _init_db(self) -> None:
        conn = self._conn()
        conn.executescript(self.SCHEMA)
        conn.commit()

    # ── Workers ───────────────────────────────────────────────────────────────

    def register_worker(self, worker_id: str, mode: str,
                        gpu_model: Optional[str] = None) -> Dict[str, Any]:
        now = datetime.utcnow().isoformat()
        conn = self._conn()
        conn.execute("""
            INSERT INTO workers (worker_id, mode, gpu_model, registered_at, last_seen)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(worker_id) DO UPDATE SET
                mode=excluded.mode,
                gpu_model=excluded.gpu_model,
                last_seen=excluded.last_seen
        """, (worker_id, mode, gpu_model, now, now))
        conn.commit()
        return {"worker_id": worker_id, "mode": mode, "registered_at": now}

    def update_worker_seen(self, worker_id: str) -> None:
        now = datetime.utcnow().isoformat()
        self._conn().execute(
            "UPDATE workers SET last_seen=? WHERE worker_id=?", (now, worker_id)
        )
        self._conn().commit()

    def get_worker_count(self) -> int:
        row = self._conn().execute("SELECT COUNT(*) FROM workers").fetchone()
        return row[0] if row else 0

    def get_active_worker_count(self, minutes: int = 10) -> int:
        cutoff = datetime.utcfromtimestamp(time.time() - minutes * 60).isoformat()
        row = self._conn().execute(
            "SELECT COUNT(*) FROM workers WHERE last_seen > ?", (cutoff,)
        ).fetchone()
        return row[0] if row else 0

    # ── Strategy ──────────────────────────────────────────────────────────────

    def get_canonical_strategy(self) -> Optional[sqlite3.Row]:
        return self._conn().execute(
            "SELECT * FROM strategy_variants WHERE is_canonical=1"
        ).fetchone()

    def set_canonical_strategy(self, content: str, mutation_desc: str = "seed",
                                parent_hash: Optional[str] = None) -> str:
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        now = datetime.utcnow().isoformat()
        conn = self._conn()
        # Demote all existing canonical
        conn.execute("UPDATE strategy_variants SET is_canonical=0")
        conn.execute("""
            INSERT INTO strategy_variants
                (hash, parent_hash, content, mutation_desc, is_canonical,
                 mean_score, promoted_at, created_at)
            VALUES (?, ?, ?, ?, 1, 0.0, ?, ?)
            ON CONFLICT(hash) DO UPDATE SET
                is_canonical=1,
                mutation_desc=excluded.mutation_desc,
                promoted_at=excluded.promoted_at
        """, (content_hash, parent_hash, content, mutation_desc, now, now))
        conn.commit()
        return content_hash

    def get_strategy_history(self, limit: int = 50) -> List[sqlite3.Row]:
        return self._conn().execute("""
            SELECT id, hash, parent_hash, mutation_desc, is_canonical,
                   mean_score, validation_count, promoted_at, created_at
            FROM strategy_variants
            ORDER BY id DESC LIMIT ?
        """, (limit,)).fetchall()

    def update_strategy_mean_score(self, strategy_hash: str, mean_score: float) -> None:
        conn = self._conn()
        conn.execute(
            "UPDATE strategy_variants SET mean_score=? WHERE hash=?",
            (mean_score, strategy_hash)
        )
        conn.commit()

    # ── Jobs ──────────────────────────────────────────────────────────────────

    def add_job(self, job_id: str, cancer_type: str, category: str,
                case_id: str, case_data: dict, complexity: int,
                strategy_hash: str, preferred_mode: str = "any") -> None:
        conn = self._conn()
        conn.execute("""
            INSERT OR IGNORE INTO jobs
                (job_id, cancer_type, category, case_id, case_data, complexity,
                 strategy_hash, status, preferred_mode)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', ?)
        """, (job_id, cancer_type, category, case_id,
              json.dumps(case_data), complexity, strategy_hash, preferred_mode))
        conn.commit()

    def get_next_job(self, worker_id: str, worker_mode: str) -> Optional[sqlite3.Row]:
        """
        Assign next pending job to worker.
        Local workers prefer simple cases (complexity ≤ 4).
        Claude workers prefer complex cases (complexity > 4).
        """
        conn = self._conn()
        now = datetime.utcnow().isoformat()

        # Re-queue timed-out jobs
        timeout_cutoff = datetime.utcfromtimestamp(
            time.time() - JOB_TIMEOUT_SECONDS
        ).isoformat()
        conn.execute("""
            UPDATE jobs SET status='pending', assigned_to=NULL, assigned_at=NULL
            WHERE status='assigned' AND assigned_at < ?
        """, (timeout_cutoff,))
        conn.commit()

        # Select job based on worker mode preference
        if worker_mode == "local":
            row = conn.execute("""
                SELECT * FROM jobs
                WHERE status='pending'
                  AND (preferred_mode='local' OR preferred_mode='any')
                  AND complexity <= ?
                ORDER BY complexity ASC, job_id ASC LIMIT 1
            """, (SIMPLE_CASE_COMPLEXITY_MAX,)).fetchone()
            if not row:
                # Fall back to any pending job
                row = conn.execute("""
                    SELECT * FROM jobs
                    WHERE status='pending'
                      AND (preferred_mode='local' OR preferred_mode='any')
                    ORDER BY job_id ASC LIMIT 1
                """).fetchone()
        else:
            # Claude mode: prefer complex cases
            row = conn.execute("""
                SELECT * FROM jobs
                WHERE status='pending'
                  AND (preferred_mode='claude' OR preferred_mode='any')
                  AND complexity > ?
                ORDER BY complexity DESC, job_id ASC LIMIT 1
            """, (SIMPLE_CASE_COMPLEXITY_MAX,)).fetchone()
            if not row:
                row = conn.execute("""
                    SELECT * FROM jobs
                    WHERE status='pending'
                      AND (preferred_mode='claude' OR preferred_mode='any')
                    ORDER BY complexity DESC, job_id ASC LIMIT 1
                """).fetchone()

        if not row:
            return None

        conn.execute("""
            UPDATE jobs SET status='assigned', assigned_to=?, assigned_at=?
            WHERE job_id=?
        """, (worker_id, now, row["job_id"]))
        conn.commit()
        return row

    def submit_job_result(self, job_id: str, worker_id: str, score: float,
                          quality_dims: dict, report_path: str,
                          report_json: Optional[dict] = None) -> bool:
        conn = self._conn()
        row = conn.execute(
            "SELECT * FROM jobs WHERE job_id=? AND assigned_to=?",
            (job_id, worker_id)
        ).fetchone()
        if not row:
            return False

        now = datetime.utcnow().isoformat()
        conn.execute("""
            UPDATE jobs SET status='completed', completed_at=?, score=?,
                           quality_dims=?, report_path=?
            WHERE job_id=?
        """, (now, score, json.dumps(quality_dims), report_path, job_id))

        conn.execute("""
            INSERT INTO reports
                (case_id, cancer_type, category, strategy_hash, worker_id,
                 score, quality_dims, report_path, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (row["case_id"], row["cancer_type"], row["category"],
              row["strategy_hash"], worker_id, score,
              json.dumps(quality_dims), report_path, now))

        conn.execute(
            "UPDATE workers SET jobs_completed=jobs_completed+1, last_seen=? WHERE worker_id=?",
            (now, worker_id)
        )
        conn.commit()

        # Write report to research_db if provided
        if report_json and report_path:
            os.makedirs(os.path.dirname(report_path), exist_ok=True)
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(report_json, f, indent=2)

        return True

    def get_job_stats(self) -> Dict[str, int]:
        conn = self._conn()
        row = conn.execute("""
            SELECT
                SUM(CASE WHEN status='pending'   THEN 1 ELSE 0 END) AS pending,
                SUM(CASE WHEN status='assigned'  THEN 1 ELSE 0 END) AS assigned,
                SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END) AS completed,
                SUM(CASE WHEN status='stale'     THEN 1 ELSE 0 END) AS stale
            FROM jobs
        """).fetchone()
        return dict(row) if row else {}

    # ── Mutations ─────────────────────────────────────────────────────────────

    def propose_mutation(self, base_hash: str, variant_content: str,
                         mutation_desc: str, proposed_by: str) -> int:
        variant_hash = hashlib.sha256(variant_content.encode()).hexdigest()[:16]
        now = datetime.utcnow().isoformat()
        conn = self._conn()
        cursor = conn.execute("""
            INSERT OR IGNORE INTO mutations
                (base_hash, variant_content, variant_hash, mutation_desc,
                 proposed_by, proposed_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (base_hash, variant_content, variant_hash, mutation_desc,
              proposed_by, now))
        conn.commit()
        # Return the id (new or existing)
        row = conn.execute(
            "SELECT id FROM mutations WHERE variant_hash=?", (variant_hash,)
        ).fetchone()
        return row["id"] if row else cursor.lastrowid

    def add_mutation_validation(self, mutation_id: int, worker_id: str,
                                case_id: str, score: float,
                                quality_dims: dict) -> None:
        now = datetime.utcnow().isoformat()
        conn = self._conn()
        # Prevent the same worker validating the same mutation twice
        existing = conn.execute("""
            SELECT id FROM mutation_validations
            WHERE mutation_id=? AND worker_id=?
        """, (mutation_id, worker_id)).fetchone()
        if existing:
            return

        conn.execute("""
            INSERT INTO mutation_validations
                (mutation_id, worker_id, case_id, score, quality_dims, validated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (mutation_id, worker_id, case_id, score, json.dumps(quality_dims), now))

        # Update aggregate stats on the mutation
        agg = conn.execute("""
            SELECT COUNT(*) AS cnt, AVG(score) AS avg_score
            FROM mutation_validations WHERE mutation_id=?
        """, (mutation_id,)).fetchone()
        conn.execute("""
            UPDATE mutations SET validation_count=?, mean_score=?, status='validating'
            WHERE id=?
        """, (agg["cnt"], agg["avg_score"] or 0.0, mutation_id))
        conn.commit()

    def check_promotion_eligibility(self, mutation_id: int,
                                    current_best_score: float) -> bool:
        """Return True if this mutation should be promoted to canonical."""
        conn = self._conn()
        mut = conn.execute(
            "SELECT * FROM mutations WHERE id=?", (mutation_id,)
        ).fetchone()
        if not mut:
            return False
        return (
            mut["validation_count"] >= PROMOTION_MIN_VALIDATIONS and
            mut["mean_score"] >= current_best_score + PROMOTION_MIN_SCORE_DELTA
        )

    def promote_mutation(self, mutation_id: int) -> Optional[str]:
        """Promote mutation to canonical strategy. Returns new strategy hash."""
        conn = self._conn()
        mut = conn.execute(
            "SELECT * FROM mutations WHERE id=?", (mutation_id,)
        ).fetchone()
        if not mut:
            return None

        now = datetime.utcnow().isoformat()
        new_hash = hashlib.sha256(mut["variant_content"].encode()).hexdigest()[:16]

        # Demote existing canonical
        conn.execute("UPDATE strategy_variants SET is_canonical=0")

        # Insert or update new canonical
        conn.execute("""
            INSERT INTO strategy_variants
                (hash, parent_hash, content, mutation_desc, is_canonical,
                 mean_score, validation_count, promoted_at, created_at)
            VALUES (?, ?, ?, ?, 1, ?, ?, ?, ?)
            ON CONFLICT(hash) DO UPDATE SET
                is_canonical=1,
                mean_score=excluded.mean_score,
                validation_count=excluded.validation_count,
                promoted_at=excluded.promoted_at
        """, (new_hash, mut["base_hash"], mut["variant_content"],
              mut["mutation_desc"], mut["mean_score"],
              mut["validation_count"], now, now))

        # Mark mutation as promoted
        conn.execute(
            "UPDATE mutations SET status='promoted', promoted_at=? WHERE id=?",
            (now, mutation_id)
        )

        # Mark all pending/assigned jobs with the old hash as stale
        conn.execute("""
            UPDATE jobs SET status='stale'
            WHERE status IN ('pending','assigned')
              AND strategy_hash=?
        """, (mut["base_hash"],))

        conn.commit()
        log.info(
            f"Mutation {mutation_id} promoted: {mut['base_hash']} -> {new_hash} "
            f"(mean_score={mut['mean_score']:.1f})"
        )
        return new_hash

    def get_next_mutation_to_validate(self, worker_id: str) -> Optional[sqlite3.Row]:
        """Get a proposed/validating mutation this worker hasn't validated yet."""
        conn = self._conn()
        # Find mutations not yet validated by this worker
        row = conn.execute("""
            SELECT m.* FROM mutations m
            WHERE m.status IN ('proposed','validating')
              AND m.proposed_by != ?
              AND m.id NOT IN (
                  SELECT mv.mutation_id FROM mutation_validations mv
                  WHERE mv.worker_id=?
              )
            ORDER BY m.validation_count ASC, m.proposed_at ASC
            LIMIT 1
        """, (worker_id, worker_id)).fetchone()
        return row

    # ── Reports / Database Search ─────────────────────────────────────────────

    def search_reports(self, cancer_type: Optional[str] = None,
                       category: Optional[str] = None,
                       min_score: float = 0.0,
                       limit: int = 20) -> List[sqlite3.Row]:
        query = """
            SELECT r.*, sv.mutation_desc as strategy_mutation
            FROM reports r
            LEFT JOIN strategy_variants sv ON r.strategy_hash = sv.hash
            WHERE r.score >= ?
        """
        params: List[Any] = [min_score]
        if cancer_type:
            query += " AND LOWER(r.cancer_type) LIKE ?"
            params.append(f"%{cancer_type.lower()}%")
        if category:
            query += " AND LOWER(r.category) = ?"
            params.append(category.lower())
        query += " ORDER BY r.score DESC LIMIT ?"
        params.append(limit)
        return self._conn().execute(query, params).fetchall()

    def get_best_report_for_cancer(self, cancer_type: str) -> Optional[sqlite3.Row]:
        return self._conn().execute("""
            SELECT * FROM reports
            WHERE LOWER(cancer_type) LIKE ?
            ORDER BY score DESC LIMIT 1
        """, (f"%{cancer_type.lower()}%",)).fetchone()

    def get_leaderboard(self, limit: int = 10) -> List[sqlite3.Row]:
        return self._conn().execute("""
            SELECT sv.hash, sv.mutation_desc, sv.mean_score,
                   sv.validation_count, sv.is_canonical, sv.promoted_at,
                   COUNT(r.id) as report_count,
                   AVG(r.score) as actual_mean_score
            FROM strategy_variants sv
            LEFT JOIN reports r ON r.strategy_hash = sv.hash
            GROUP BY sv.id
            ORDER BY COALESCE(actual_mean_score, sv.mean_score) DESC
            LIMIT ?
        """, (limit,)).fetchall()

    def get_database_stats(self) -> Dict[str, Any]:
        conn = self._conn()
        total_reports = conn.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
        mean_score_row = conn.execute("SELECT AVG(score) FROM reports").fetchone()
        mean_score = round(mean_score_row[0] or 0.0, 1)
        cancer_types = conn.execute(
            "SELECT COUNT(DISTINCT cancer_type) FROM reports"
        ).fetchone()[0]
        categories = conn.execute(
            "SELECT COUNT(DISTINCT category) FROM reports"
        ).fetchone()[0]
        top_score_row = conn.execute("SELECT MAX(score) FROM reports").fetchone()
        top_score = top_score_row[0] or 0.0
        return {
            "total_reports": total_reports,
            "mean_score": mean_score,
            "top_score": top_score,
            "cancer_types_covered": cancer_types,
            "categories_covered": categories,
        }


# ── HTTP Handler ──────────────────────────────────────────────────────────────

class OrchestratorHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler for the orchestrator server."""

    db: OrchestratorDB  # set by factory
    strategy_file: str   # set by factory
    server_start: float  # set by factory

    def log_message(self, fmt: str, *args: Any) -> None:
        """Suppress default Apache-style logs; we use NDJSON."""
        log.info(f"{self.command} {self.path} {args[1] if len(args) > 1 else ''}")

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _parse_body(self) -> Optional[dict]:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            return None

    def _send_json(self, data: Any, status: int = 200) -> None:
        body = json.dumps(data, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_error(self, message: str, status: int = 400) -> None:
        self._send_json({"error": message}, status)

    def _get_canonical_strategy_content(self) -> str:
        row = self.db.get_canonical_strategy()
        if row:
            return row["content"]
        # Fall back to reading from disk
        if os.path.exists(self.strategy_file):
            with open(self.strategy_file, "r", encoding="utf-8") as f:
                return f.read()
        return ""

    def _get_canonical_hash(self) -> str:
        row = self.db.get_canonical_strategy()
        if row:
            return row["hash"]
        content = self._get_canonical_strategy_content()
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _qs(self) -> Dict[str, List[str]]:
        parsed = urlparse(self.path)
        return parse_qs(parsed.query)

    def _qs_str(self, key: str, default: str = "") -> str:
        qs = self._qs()
        vals = qs.get(key, [default])
        return vals[0] if vals else default

    def _qs_float(self, key: str, default: float = 0.0) -> float:
        try:
            return float(self._qs_str(key, str(default)))
        except ValueError:
            return default

    def _qs_int(self, key: str, default: int = 20) -> int:
        try:
            return int(self._qs_str(key, str(default)))
        except ValueError:
            return default

    # ── Route Dispatch ────────────────────────────────────────────────────────

    def do_GET(self) -> None:
        path = urlparse(self.path).path.rstrip("/")
        try:
            if path == "/status":
                self._handle_status()
            elif path == "/strategy":
                self._handle_get_strategy()
            elif path == "/jobs/next":
                self._handle_get_next_job()
            elif path == "/leaderboard":
                self._handle_leaderboard()
            elif path == "/database/search":
                self._handle_db_search()
            elif path == "/mutations/next":
                self._handle_get_next_mutation()
            else:
                self._send_error("Not found", 404)
        except Exception as e:
            log.error(f"GET {path} error: {e}")
            self._send_error(f"Internal server error: {e}", 500)

    def do_POST(self) -> None:
        path = urlparse(self.path).path.rstrip("/")
        try:
            body = self._parse_body()
            if body is None:
                self._send_error("Invalid JSON body")
                return

            if path == "/register":
                self._handle_register(body)
            elif path == "/mutations/propose":
                self._handle_propose_mutation(body)
            elif path.startswith("/jobs/") and path.endswith("/result"):
                job_id = path.split("/")[2]
                self._handle_submit_result(job_id, body)
            elif path.startswith("/mutations/") and path.endswith("/validate"):
                parts = path.split("/")
                if len(parts) >= 3:
                    try:
                        mutation_id = int(parts[2])
                        self._handle_validate_mutation(mutation_id, body)
                    except ValueError:
                        self._send_error("Invalid mutation id")
                else:
                    self._send_error("Not found", 404)
            else:
                self._send_error("Not found", 404)
        except Exception as e:
            log.error(f"POST {path} error: {e}")
            self._send_error(f"Internal server error: {e}", 500)

    # ── Handlers ──────────────────────────────────────────────────────────────

    def _handle_status(self) -> None:
        job_stats = self.db.get_job_stats()
        canonical = self.db.get_canonical_strategy()
        db_stats = self.db.get_database_stats()
        self._send_json({
            "status": "ok",
            "version": VERSION,
            "uptime_seconds": round(time.time() - self.server_start),
            "canonical_strategy_hash": canonical["hash"] if canonical else None,
            "canonical_strategy_score": canonical["mean_score"] if canonical else 0.0,
            "workers_total": self.db.get_worker_count(),
            "workers_active_10min": self.db.get_active_worker_count(10),
            "jobs": job_stats,
            "database": db_stats,
            "promotion_threshold": PROMOTION_MIN_SCORE_DELTA,
            "promotion_min_validations": PROMOTION_MIN_VALIDATIONS,
        })

    def _handle_get_strategy(self) -> None:
        content = self._get_canonical_strategy_content()
        strategy_hash = self._get_canonical_hash()
        if not content:
            self._send_error("No strategy loaded", 404)
            return
        self._send_json({
            "strategy_hash": strategy_hash,
            "content": content,
            "retrieved_at": datetime.utcnow().isoformat() + "Z",
        })

    def _handle_register(self, body: dict) -> None:
        worker_id = body.get("worker_id", "")
        mode = body.get("mode", "")
        gpu_model = body.get("gpu_model")

        if not worker_id:
            self._send_error("worker_id required")
            return
        if mode not in ("local", "claude"):
            self._send_error("mode must be 'local' or 'claude'")
            return

        result = self.db.register_worker(worker_id, mode, gpu_model)
        canonical = self.db.get_canonical_strategy()
        result["canonical_strategy_hash"] = canonical["hash"] if canonical else None
        result["promotion_threshold"] = PROMOTION_MIN_SCORE_DELTA
        result["promotion_min_validations"] = PROMOTION_MIN_VALIDATIONS
        log.info(f"Worker registered: {worker_id} mode={mode} gpu={gpu_model}")
        self._send_json(result)

    def _handle_get_next_job(self) -> None:
        worker_id = self._qs_str("worker_id")
        worker_mode = self._qs_str("mode", "local")

        if not worker_id:
            self._send_error("worker_id query param required")
            return

        self.db.update_worker_seen(worker_id)
        job = self.db.get_next_job(worker_id, worker_mode)
        if not job:
            self._send_json({"status": "no_jobs", "message": "No pending jobs available"})
            return

        # Get current canonical strategy for this job
        canonical = self.db.get_canonical_strategy()
        strategy_content = canonical["content"] if canonical else ""

        self._send_json({
            "job_id": job["job_id"],
            "case_id": job["case_id"],
            "cancer_type": job["cancer_type"],
            "category": job["category"],
            "complexity": job["complexity"],
            "case_data": json.loads(job["case_data"]),
            "strategy_hash": job["strategy_hash"],
            "strategy_content": strategy_content,
        })

    def _handle_submit_result(self, job_id: str, body: dict) -> None:
        worker_id = body.get("worker_id", "")
        score = body.get("score")
        quality_dims = body.get("quality_dimensions", {})
        report_json = body.get("report_json")

        if not worker_id:
            self._send_error("worker_id required")
            return
        if score is None:
            self._send_error("score required")
            return

        try:
            score = float(score)
        except (TypeError, ValueError):
            self._send_error("score must be a number")
            return

        # Determine report path from job info
        job_row = self.db._conn().execute(
            "SELECT * FROM jobs WHERE job_id=?", (job_id,)
        ).fetchone()
        if not job_row:
            self._send_error(f"Job {job_id} not found", 404)
            return

        report_path = os.path.join(
            "research_db", job_row["category"], job_row["cancer_type"].lower().replace(" ", "_"),
            "reports", f"{job_row['case_id']}_report.json"
        )

        success = self.db.submit_job_result(
            job_id, worker_id, score, quality_dims, report_path, report_json
        )

        if not success:
            self._send_error(f"Job {job_id} not found or not assigned to {worker_id}", 404)
            return

        # Check if canonical strategy score should be updated
        canonical = self.db.get_canonical_strategy()
        if canonical:
            completed_scores = self.db._conn().execute("""
                SELECT AVG(score) FROM jobs
                WHERE strategy_hash=? AND status='completed'
            """, (canonical["hash"],)).fetchone()
            if completed_scores and completed_scores[0]:
                self.db.update_strategy_mean_score(canonical["hash"], completed_scores[0])

        log.info(f"Job {job_id} completed by {worker_id}: score={score:.1f}")
        self._send_json({"status": "accepted", "job_id": job_id, "score": score})

    def _handle_leaderboard(self) -> None:
        limit = self._qs_int("limit", 10)
        rows = self.db.get_leaderboard(limit)
        entries = []
        for r in rows:
            entries.append({
                "hash": r["hash"],
                "mutation_desc": r["mutation_desc"],
                "is_canonical": bool(r["is_canonical"]),
                "mean_score": round(r["actual_mean_score"] or r["mean_score"] or 0.0, 1),
                "validation_count": r["validation_count"],
                "report_count": r["report_count"],
                "promoted_at": r["promoted_at"],
            })
        self._send_json({"leaderboard": entries, "count": len(entries)})

    def _handle_db_search(self) -> None:
        cancer_type = self._qs_str("cancer_type") or None
        category = self._qs_str("category") or None
        min_score = self._qs_float("min_score", 0.0)
        limit = self._qs_int("limit", 20)

        rows = self.db.search_reports(cancer_type, category, min_score, limit)
        results = []
        for r in rows:
            results.append({
                "case_id": r["case_id"],
                "cancer_type": r["cancer_type"],
                "category": r["category"],
                "score": r["score"],
                "strategy_hash": r["strategy_hash"],
                "report_path": r["report_path"],
                "created_at": r["created_at"],
            })
        self._send_json({"results": results, "count": len(results)})

    def _handle_propose_mutation(self, body: dict) -> None:
        base_hash = body.get("base_hash", "")
        variant_content = body.get("variant_content", "")
        mutation_desc = body.get("mutation_desc", "")
        proposed_by = body.get("worker_id", "")

        if not base_hash or not variant_content or not proposed_by:
            self._send_error("base_hash, variant_content, worker_id required")
            return

        mutation_id = self.db.propose_mutation(
            base_hash, variant_content, mutation_desc, proposed_by
        )
        log.info(f"Mutation proposed: id={mutation_id} by={proposed_by} desc={mutation_desc}")
        self._send_json({
            "mutation_id": mutation_id,
            "status": "proposed",
            "message": f"Mutation {mutation_id} queued for validation",
        })

    def _handle_validate_mutation(self, mutation_id: int, body: dict) -> None:
        worker_id = body.get("worker_id", "")
        case_id = body.get("case_id", "")
        score = body.get("score")
        quality_dims = body.get("quality_dimensions", {})

        if not worker_id or score is None:
            self._send_error("worker_id and score required")
            return

        try:
            score = float(score)
        except (TypeError, ValueError):
            self._send_error("score must be a number")
            return

        self.db.add_mutation_validation(mutation_id, worker_id, case_id, score, quality_dims)

        # Check for promotion
        canonical = self.db.get_canonical_strategy()
        current_best = canonical["mean_score"] if canonical else 0.0
        eligible = self.db.check_promotion_eligibility(mutation_id, current_best)

        promoted = False
        new_hash = None
        if eligible:
            new_hash = self.db.promote_mutation(mutation_id)
            promoted = bool(new_hash)

        mut = self.db._conn().execute(
            "SELECT * FROM mutations WHERE id=?", (mutation_id,)
        ).fetchone()

        response: Dict[str, Any] = {
            "mutation_id": mutation_id,
            "validation_accepted": True,
            "validations_so_far": mut["validation_count"] if mut else 0,
            "mean_score": round(mut["mean_score"] if mut else 0.0, 1),
            "promoted": promoted,
        }
        if promoted:
            response["new_canonical_hash"] = new_hash
            response["message"] = f"Mutation promoted to canonical strategy (hash={new_hash})"
        self._send_json(response)

    def _handle_get_next_mutation(self) -> None:
        worker_id = self._qs_str("worker_id")
        if not worker_id:
            self._send_error("worker_id query param required")
            return
        mut = self.db.get_next_mutation_to_validate(worker_id)
        if not mut:
            self._send_json({"status": "none", "message": "No mutations pending validation"})
            return
        # Include a canonical case for the worker to run the variant against
        canonical = self.db.get_canonical_strategy()
        self._send_json({
            "mutation_id": mut["id"],
            "base_hash": mut["base_hash"],
            "variant_content": mut["variant_content"],
            "variant_hash": mut["variant_hash"],
            "mutation_desc": mut["mutation_desc"],
            "validation_count": mut["validation_count"],
            "mean_score": mut["mean_score"],
            "current_canonical_hash": canonical["hash"] if canonical else None,
            "current_canonical_score": canonical["mean_score"] if canonical else 0.0,
        })


# ── Server Factory ────────────────────────────────────────────────────────────

def make_handler(db: OrchestratorDB, strategy_file: str,
                 server_start: float) -> type:
    """Create a handler class with bound db/strategy references."""

    class BoundHandler(OrchestratorHandler):
        pass

    BoundHandler.db = db
    BoundHandler.strategy_file = strategy_file
    BoundHandler.server_start = server_start
    return BoundHandler


# ── Job Seeding ───────────────────────────────────────────────────────────────

def seed_jobs_from_benchmark(db: OrchestratorDB, cases_file: str,
                              strategy_hash: str) -> int:
    """
    Populate the job queue from a benchmark cases JSON file.
    Returns the number of jobs added.
    """
    if not os.path.exists(cases_file):
        log.info(f"Benchmark file not found: {cases_file}")
        return 0
    try:
        with open(cases_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        cases = data.get("cases", [])
        cancer_type_key = data.get("cancer_type", "unknown")
        category = data.get("category", "carcinomas")
        added = 0
        for case in cases:
            case_id = case.get("id", "")
            if not case_id:
                continue
            cancer_type = case.get("cancer_type", cancer_type_key)
            complexity = _estimate_complexity(case)
            preferred = "claude" if complexity > SIMPLE_CASE_COMPLEXITY_MAX else "any"
            job_id = f"{case_id}_{strategy_hash[:8]}"
            db.add_job(job_id, cancer_type, category, case_id,
                       case, complexity, strategy_hash, preferred)
            added += 1
        return added
    except Exception as e:
        log.error(f"Failed to seed jobs from {cases_file}: {e}")
        return 0


def _estimate_complexity(case: dict) -> int:
    """Quick complexity estimate for job routing (mirrors run_experiment.py logic)."""
    score = 0
    cancer_type = case.get("cancer_type", "").lower()
    ctx = case.get("patient_context", {})
    markers = [m.lower() for m in case.get("molecular_markers", [])]
    ps = (ctx.get("performance_status", "") or "").lower()
    stage = (case.get("stage", "") or "").lower()
    risk = " ".join(ctx.get("risk_factors", [])).lower()

    rare_terms = [
        "adenoid cystic", "mucoepidermoid", "sarcoma", "lymphoma", "melanoma",
        "chordoma", "esthesioneuroblastoma", "snuc", "plasmacytoma", "ewing",
    ]
    if any(t in cancer_type for t in rare_terms):
        score += 3
    if len(markers) >= 3:
        score += 2
    fusion_terms = ["fusion", "ntrk", "alk", "ros1", "ret", "braf v600e"]
    if any(t in " ".join(markers) for t in fusion_terms):
        score += 2
    if any(f"ecog {n}" in ps for n in ["2", "3", "4"]):
        score += 3
    if any(t in stage for t in ["m1", "ivb", "ivc", "unresectable"]):
        score += 2
    if any(t in risk for t in ["prior radiation", "prior surgery", "recurrent"]):
        score += 1
    return score


# ── Graceful Shutdown ─────────────────────────────────────────────────────────

_shutdown_event = threading.Event()


def _signal_handler(signum: int, frame: Any) -> None:
    log.info(f"Received signal {signum}, initiating graceful shutdown...")
    _shutdown_event.set()


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cancer AutoResearch Orchestrator Server"
    )
    parser.add_argument("--port", type=int, default=8765,
                        help="Port to listen on (default: 8765)")
    parser.add_argument("--host", default="127.0.0.1",
                        help="Host to bind to (default: 127.0.0.1)")
    parser.add_argument("--db-path", default="orchestrator.db",
                        help="SQLite database path (default: orchestrator.db)")
    parser.add_argument("--strategy", default="strategy.md",
                        help="Path to canonical strategy.md (default: strategy.md)")
    parser.add_argument("--seed-cases", default=None,
                        help="Benchmark cases JSON to seed job queue on startup")
    parser.add_argument("--log-file", default=None,
                        help="NDJSON log file path (default: stdout only)")
    args = parser.parse_args()

    global log
    if args.log_file:
        log = setup_logging(args.log_file)

    # Initialize database
    db = OrchestratorDB(args.db_path)
    log.info(f"Database initialized: {args.db_path}")

    # Load or create canonical strategy
    canonical = db.get_canonical_strategy()
    if not canonical:
        if os.path.exists(args.strategy):
            with open(args.strategy, "r", encoding="utf-8") as f:
                content = f.read()
            strategy_hash = db.set_canonical_strategy(content, "seed")
            log.info(f"Loaded canonical strategy from {args.strategy} (hash={strategy_hash})")
        else:
            log.info(f"No strategy file found at {args.strategy}; waiting for first proposal")
            strategy_hash = "none"
    else:
        strategy_hash = canonical["hash"]
        log.info(f"Using existing canonical strategy (hash={strategy_hash}, "
                 f"score={canonical['mean_score']:.1f})")

    # Seed jobs if requested
    if args.seed_cases:
        n = seed_jobs_from_benchmark(db, args.seed_cases, strategy_hash)
        log.info(f"Seeded {n} jobs from {args.seed_cases}")

    server_start = time.time()
    handler_class = make_handler(db, args.strategy, server_start)

    # Register signal handlers
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    # Start HTTP server
    server = http.server.ThreadingHTTPServer((args.host, args.port), handler_class)
    log.info(f"Orchestrator listening on http://{args.host}:{args.port}")
    log.info(f"Endpoints: GET /status /strategy /jobs/next /leaderboard /database/search")
    log.info(f"           POST /register /jobs/{{id}}/result /mutations/propose /mutations/{{id}}/validate")

    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    # Wait for shutdown signal
    _shutdown_event.wait()
    log.info("Shutting down server...")
    server.shutdown()
    server_thread.join(timeout=5)
    log.info("Server stopped.")


if __name__ == "__main__":
    main()
