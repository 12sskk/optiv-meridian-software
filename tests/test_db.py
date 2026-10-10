"""SQLite helpers."""

from src.db import connect, list_assessments, save_assessment, upsert_vendor
from src.models import RiskResult, VendorRecord


def test_connect_and_store(tmp_path) -> None:
    connection = connect(tmp_path / "test.db")
    vendor_id = upsert_vendor(connection, VendorRecord(name="Stored Vendor"))
    save_assessment(
        connection,
        vendor_id=vendor_id,
        criticality=None,
        risk=RiskResult(
            vendor_name="Stored Vendor",
            criticality_score=None,
            risk_score=None,
            risk_level="not_rated",
            status="insufficient_evidence",
        ),
    )
    rows = list_assessments(connection)
    connection.close()
    assert len(rows) == 1
    assert rows[0]["vendor_name"] == "Stored Vendor"
    assert rows[0]["status"] == "insufficient_evidence"
