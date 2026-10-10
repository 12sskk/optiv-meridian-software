"""Excel export writes expected sheets."""

from pathlib import Path

import pandas as pd

from src.export import export_workbook
from src.models import RiskResult, VendorRecord


def test_export_creates_workbook(tmp_path: Path) -> None:
    path = export_workbook(
        tmp_path / "out.xlsx",
        vendors=[VendorRecord(name="Export Vendor")],
        criticality=[],
        sources=[],
        evidence=[],
        risks=[
            RiskResult(
                vendor_name="Export Vendor",
                criticality_score=None,
                risk_score=None,
                risk_level="not_rated",
                status="insufficient_evidence",
            )
        ],
    )
    sheets = pd.ExcelFile(path, engine="openpyxl").sheet_names
    assert sheets == ["vendors", "criticality", "sources", "evidence", "risk"]
    vendors = pd.read_excel(path, sheet_name="vendors")
    assert vendors.iloc[0]["vendor_name"] == "Export Vendor"
