"""SQLite persistence for assessment artefacts."""

from __future__ import annotations

import json
import logging
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from src.models import (
    CriticalityResult,
    EvidenceItem,
    RiskResult,
    SourceCandidate,
    VendorRecord,
)

logger = logging.getLogger(__name__)

SCHEMA = """
CREATE TABLE IF NOT EXISTS vendors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    product TEXT,
    website TEXT,
    attributes_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS assessments (
    id INTEGER PRIMARY KEY,
    vendor_id INTEGER NOT NULL,
    criticality_score REAL,
    criticality_level TEXT,
    risk_score REAL,
    risk_level TEXT,
    status TEXT NOT NULL,
    drivers_json TEXT NOT NULL DEFAULT '[]',
    caveats_json TEXT NOT NULL DEFAULT '[]',
    created_at TEXT NOT NULL,
    FOREIGN KEY (vendor_id) REFERENCES vendors(id)
);

CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY,
    vendor_id INTEGER NOT NULL,
    url TEXT NOT NULL,
    source_type TEXT NOT NULL,
    reason TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (vendor_id) REFERENCES vendors(id)
);

CREATE TABLE IF NOT EXISTS evidence (
    id INTEGER PRIMARY KEY,
    vendor_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    snippet TEXT NOT NULL,
    heuristic_score REAL NOT NULL,
    rationale TEXT NOT NULL,
    source_url TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (vendor_id) REFERENCES vendors(id)
);
"""


class DatabaseError(RuntimeError):
    """Raised when a database operation fails."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def connect(path: str | Path) -> sqlite3.Connection:
    """Open (and create) the SQLite database, applying schema as needed."""
    db_path = Path(path)
    try:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(SCHEMA)
        connection.commit()
    except sqlite3.Error as exc:
        raise DatabaseError(f"Could not open database at {db_path}: {exc}") from exc
    logger.info("Opened database %s", db_path)
    return connection


def upsert_vendor(connection: sqlite3.Connection, vendor: VendorRecord) -> int:
    """Insert a vendor row and return its id."""
    try:
        cursor = connection.execute(
            """
            INSERT INTO vendors (name, product, website, attributes_json, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                vendor.name,
                vendor.product,
                vendor.website,
                json.dumps(vendor.attributes, default=str),
                _now(),
            ),
        )
        connection.commit()
    except sqlite3.Error as exc:
        raise DatabaseError(f"Failed to store vendor {vendor.name}: {exc}") from exc
    return int(cursor.lastrowid)


def save_assessment(
    connection: sqlite3.Connection,
    *,
    vendor_id: int,
    criticality: CriticalityResult | None,
    risk: RiskResult,
) -> int:
    """Persist a risk assessment snapshot."""
    try:
        cursor = connection.execute(
            """
            INSERT INTO assessments (
                vendor_id, criticality_score, criticality_level, risk_score,
                risk_level, status, drivers_json, caveats_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                vendor_id,
                None if criticality is None else criticality.score,
                None if criticality is None else criticality.level,
                risk.risk_score,
                risk.risk_level,
                risk.status,
                json.dumps(risk.drivers),
                json.dumps(risk.caveats),
                _now(),
            ),
        )
        connection.commit()
    except sqlite3.Error as exc:
        raise DatabaseError(f"Failed to store assessment: {exc}") from exc
    return int(cursor.lastrowid)


def save_sources(
    connection: sqlite3.Connection,
    vendor_id: int,
    sources: list[SourceCandidate],
) -> None:
    """Store discovered source candidates."""
    try:
        connection.executemany(
            """
            INSERT INTO sources (vendor_id, url, source_type, reason, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (vendor_id, item.url, item.source_type, item.reason, _now())
                for item in sources
            ],
        )
        connection.commit()
    except sqlite3.Error as exc:
        raise DatabaseError(f"Failed to store sources: {exc}") from exc


def save_evidence(
    connection: sqlite3.Connection,
    vendor_id: int,
    evidence: list[EvidenceItem],
) -> None:
    """Store classified evidence snippets."""
    try:
        connection.executemany(
            """
            INSERT INTO evidence (
                vendor_id, category, snippet, heuristic_score, rationale, source_url, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    vendor_id,
                    item.category,
                    item.snippet,
                    item.heuristic_score,
                    item.rationale,
                    item.source_url,
                    _now(),
                )
                for item in evidence
            ],
        )
        connection.commit()
    except sqlite3.Error as exc:
        raise DatabaseError(f"Failed to store evidence: {exc}") from exc


def list_assessments(connection: sqlite3.Connection) -> list[sqlite3.Row]:
    """Return stored assessments joined with vendor names."""
    try:
        cursor = connection.execute(
            """
            SELECT a.id, v.name AS vendor_name, a.criticality_score, a.criticality_level,
                   a.risk_score, a.risk_level, a.status, a.created_at
            FROM assessments a
            JOIN vendors v ON v.id = a.vendor_id
            ORDER BY a.id DESC
            """
        )
        return list(cursor.fetchall())
    except sqlite3.Error as exc:
        raise DatabaseError(f"Failed to list assessments: {exc}") from exc
