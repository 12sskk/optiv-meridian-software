"""Integration checks for the supplied Meridian case-study workbook."""

from pathlib import Path

from src.excel_handler import (
    get_real_vendors_and_student_columns,
    load_meridian_workbook,
    to_vendor_record,
)
from src.scoring import score_vendors


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = PROJECT_ROOT / "supporting material" / "Meridian_Vendor_Input.xlsx"


def test_real_meridian_workbook_loads_six_vendors_and_excludes_example() -> None:
    bundle = load_meridian_workbook(WORKBOOK)
    real_records, student_columns = get_real_vendors_and_student_columns(bundle)

    assert bundle.header_row == 4
    assert len(real_records) == 6
    assert all(not record.is_example for record in real_records)
    assert all("EXAMPLE VENDOR" not in str(record.vendor_name).upper() for record in real_records)
    assert len(student_columns) == 11
    assert {str(record.vendor_id) for record in real_records} == {
        "V-001", "V-002", "V-003", "V-004", "V-005", "V-006"
    }


def test_meridian_fields_map_into_scoring_without_blanket_defaults() -> None:
    bundle = load_meridian_workbook(WORKBOOK)
    real_records, _ = get_real_vendors_and_student_columns(bundle)
    vendors = [to_vendor_record(record) for record in real_records]

    assert vendors[0].name == "AutomWorx"
    assert vendors[0].website == "www.automworx.com"
    assert vendors[0].attributes["Operational Dependency"] == "High"
    assert "Data Classification Accessed" in vendors[0].attributes

    results = score_vendors(vendors)
    by_name = {result.vendor_name: result for result in results}

    assert by_name["Fiserv, Inc."].level == "critical"
    assert by_name["The Clearing House Payments Company L.L.C."].level == "critical"
    assert by_name["Fiserv, Inc."].factors["operational_dependency"] == 100.0
    assert by_name["Fiserv, Inc."].factors["data_volume"] == 90.0
    assert all("Meridian-specific scoring" in " ".join(result.notes) for result in results)
    # Different inventory records should not all collapse to the same default score.
    assert len({result.score for result in results}) > 1
