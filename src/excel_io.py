"""Load and validate vendor intake Excel files."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import BinaryIO

import pandas as pd

from src.models import VendorRecord

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = ("vendor_name",)

COLUMN_ALIASES: dict[str, tuple[str, ...]] = {
    "vendor_name": ("vendor_name", "vendor", "name", "supplier", "company"),
    "product": ("product", "product_name", "service", "application"),
    "website": ("website", "url", "home_page", "homepage"),
    "business_function": ("business_function", "function", "use_case"),
    "data_sensitivity": ("data_sensitivity", "sensitivity", "data_class"),
    "user_impact": ("user_impact", "users", "user_count", "scale"),
    "internet_facing": ("internet_facing", "external", "public_facing"),
    "regulated_data": ("regulated_data", "regulatory", "compliance_data"),
}


class ExcelLoadError(ValueError):
    """Raised when an intake spreadsheet cannot be used."""


def _normalize_columns(columns: list[str]) -> dict[str, str]:
    """Map canonical field names to actual spreadsheet column names."""
    lowered = {str(col).strip().lower(): str(col) for col in columns}
    mapping: dict[str, str] = {}
    for canonical, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in lowered:
                mapping[canonical] = lowered[alias]
                break
    return mapping


def load_vendor_workbook(source: str | Path | BinaryIO) -> pd.DataFrame:
    """Read the first worksheet of an .xlsx file into a DataFrame.

    Args:
        source: Filesystem path or file-like object opened in binary mode.

    Returns:
        DataFrame with original columns preserved.

    Raises:
        ExcelLoadError: If the file is missing, unreadable, or empty.
    """
    try:
        frame = pd.read_excel(source, engine="openpyxl")
    except FileNotFoundError as exc:
        raise ExcelLoadError(f"Excel file not found: {source}") from exc
    except ValueError as exc:
        raise ExcelLoadError(f"Unable to read Excel file: {exc}") from exc
    except Exception as exc:  # pandas/openpyxl wrap many format errors
        raise ExcelLoadError(
            f"Failed to open workbook. Use a valid .xlsx file. Details: {exc}"
        ) from exc

    if frame.empty:
        raise ExcelLoadError("The spreadsheet has no data rows.")
    logger.info("Loaded workbook with %s rows and %s columns", len(frame), len(frame.columns))
    return frame


def parse_vendors(frame: pd.DataFrame) -> list[VendorRecord]:
    """Convert a DataFrame into vendor records using flexible column names.

    Raises:
        ExcelLoadError: If a vendor name column cannot be identified.
    """
    mapping = _normalize_columns([str(c) for c in frame.columns])
    if "vendor_name" not in mapping:
        raise ExcelLoadError(
            "A vendor name column is required. Accepted headers: "
            + ", ".join(COLUMN_ALIASES["vendor_name"])
        )

    records: list[VendorRecord] = []
    name_col = mapping["vendor_name"]
    for idx, row in frame.iterrows():
        raw_name = row.get(name_col)
        if pd.isna(raw_name) or not str(raw_name).strip():
            logger.warning("Skipping row %s: missing vendor name", idx)
            continue
        attributes: dict[str, object] = {}
        for canonical, actual in mapping.items():
            if canonical in {"vendor_name", "product", "website"}:
                continue
            value = row.get(actual)
            attributes[canonical] = None if pd.isna(value) else value

        product = row.get(mapping["product"]) if "product" in mapping else None
        website = row.get(mapping["website"]) if "website" in mapping else None
        records.append(
            VendorRecord(
                name=str(raw_name).strip(),
                product=None if product is None or pd.isna(product) else str(product).strip(),
                website=None if website is None or pd.isna(website) else str(website).strip(),
                attributes=attributes,
                row_index=int(idx) if isinstance(idx, (int, float)) else None,
            )
        )

    if not records:
        raise ExcelLoadError("No usable vendor rows were found after validation.")
    logger.info("Parsed %s vendor records", len(records))
    return records
