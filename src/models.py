"""Shared data structures for the assessment pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class VendorRecord:
    """One vendor row loaded from the intake spreadsheet."""

    name: str
    product: str | None = None
    website: str | None = None
    vendor_id: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    row_index: int | None = None


@dataclass
class CriticalityResult:
    """Transparent criticality score derived from intake attributes only."""

    vendor_name: str
    score: float
    level: str
    factors: dict[str, float]
    notes: list[str] = field(default_factory=list)


@dataclass
class SourceCandidate:
    """A public URL or search query to review. Not an OSINT finding."""

    url: str
    source_type: str
    reason: str
    vendor_name: str


@dataclass
class ExtractedDocument:
    """Plain text extracted from a fetched page."""

    url: str
    status: str
    title: str | None = None
    text: str = ""
    error: str | None = None
    retrieved_at: str | None = None


@dataclass
class EvidenceItem:
    """A labeled snippet taken from extracted text. Heuristic, not a verdict."""

    category: str
    snippet: str
    heuristic_score: float
    rationale: str
    source_url: str = ""
    source_title: str = ""
    retrieved_at: str | None = None
    matched_terms: list[str] = field(default_factory=list)


@dataclass
class RiskResult:
    """Risk output that stays conservative when evidence is missing."""

    vendor_name: str
    criticality_score: float | None
    risk_score: float | None
    risk_level: str
    status: str
    drivers: list[str] = field(default_factory=list)
    caveats: list[str] = field(default_factory=list)
