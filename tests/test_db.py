"""SQLite helpers."""

from src.db import connect, list_assessments, save_assessment, upsert_vendor
from src.models import EvidenceItem, RiskResult, VendorRecord


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


def test_evidence_metadata_persists(tmp_path) -> None:
    connection = connect(tmp_path / "evidence.db")
    vendor_id = upsert_vendor(connection, VendorRecord(name="Evidence Vendor"))
    from src.db import save_evidence
    save_evidence(connection, vendor_id, [EvidenceItem(
        category="ai_subprocessor_disclosure", snippet="Powered by OpenAI.",
        heuristic_score=0.65, rationale="Review lead", source_url="https://example.com/trust",
        source_title="Trust Center", retrieved_at="2026-10-11T12:00:00+00:00",
        matched_terms=["OpenAI", "powered by"],
    )])
    row = connection.execute("SELECT * FROM evidence").fetchone()
    connection.close()
    assert row["source_title"] == "Trust Center"
    assert row["retrieved_at"] == "2026-10-11T12:00:00+00:00"
    assert '"OpenAI"' in row["matched_terms_json"]
