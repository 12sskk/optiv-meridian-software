"""Write assessment results to an Excel workbook."""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from src.models import (
    CriticalityResult,
    EvidenceItem,
    RiskResult,
    SourceCandidate,
    VendorRecord,
)

logger = logging.getLogger(__name__)


class ExportError(ValueError):
    """Raised when results cannot be written to Excel."""


def export_workbook(
    path: str | Path,
    *,
    vendors: list[VendorRecord],
    criticality: list[CriticalityResult],
    sources: list[SourceCandidate],
    evidence: list[EvidenceItem],
    risks: list[RiskResult],
) -> Path:
    """Create a multi-sheet .xlsx file for analyst review."""
    destination = Path(path)
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        vendor_rows = [
            {
                "vendor_name": item.name,
                "product": item.product,
                "website": item.website,
                **{k: v for k, v in item.attributes.items()},
            }
            for item in vendors
        ]
        with pd.ExcelWriter(destination, engine="openpyxl") as writer:
            pd.DataFrame(vendor_rows).to_excel(writer, sheet_name="vendors", index=False)
            pd.DataFrame([item.__dict__ for item in criticality]).to_excel(
                writer, sheet_name="criticality", index=False
            )
            pd.DataFrame([item.__dict__ for item in sources]).to_excel(
                writer, sheet_name="sources", index=False
            )
            pd.DataFrame([item.__dict__ for item in evidence]).to_excel(
                writer, sheet_name="evidence", index=False
            )
            pd.DataFrame([item.__dict__ for item in risks]).to_excel(
                writer, sheet_name="risk", index=False
            )
    except OSError as exc:
        raise ExportError(f"Could not write Excel file to {destination}: {exc}") from exc
    except Exception as exc:
        raise ExportError(f"Excel export failed: {exc}") from exc

    logger.info("Wrote export workbook to %s", destination)
    return destination
