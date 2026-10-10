"""Tests for intake-only criticality scoring."""

from src.models import VendorRecord
from src.scoring import score_vendor


def test_high_sensitivity_raises_score() -> None:
    vendor = VendorRecord(
        name="Example Co",
        attributes={
            "data_sensitivity": "high",
            "user_impact": "high",
            "internet_facing": "yes",
            "regulated_data": "yes",
        },
    )
    result = score_vendor(vendor)
    assert result.score >= 75
    assert result.level == "high"
    assert result.vendor_name == "Example Co"


def test_missing_attributes_are_noted_not_invented() -> None:
    result = score_vendor(VendorRecord(name="Unknown Vendor"))
    assert result.score == 50.0
    assert result.level == "medium"
    assert any("Missing data_sensitivity" in note for note in result.notes)
