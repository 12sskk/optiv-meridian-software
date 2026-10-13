"""Unit tests verifying that Cognitive TPRM Synthesis resolves the 'All Unrated' trap."""

from pathlib import Path
from src.excel_handler import load_meridian_workbook, get_real_vendors_and_student_columns, to_vendor_record
from src.scoring import score_vendors
from src.risk import evaluate_vendor_portfolio, analyse_risk
from src.meridian_export import build_meridian_updates

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "supporting material" / "Meridian_Vendor_Input.xlsx"


def test_cognitive_synthesis_resolves_all_unrated_trap() -> None:
    bundle = load_meridian_workbook(SOURCE)
    records, student_cols = get_real_vendors_and_student_columns(bundle)
    vendors = [to_vendor_record(r) for r in records]
    criticality = score_vendors(vendors)

    # Empty raw web evidence (which normally causes all vendors to be unrated)
    evidence_by_vendor = {v.name: [] for v in vendors}

    # Evaluate using cognitive synthesis
    risks = evaluate_vendor_portfolio(
        vendors=vendors,
        criticality=criticality,
        evidence_by_vendor=evidence_by_vendor,
        enable_cognitive=True,
    )

    assert len(risks) == 6
    risk_by_name = {r.vendor_name: r for r in risks}

    # Verify no vendor is left as 'not_rated' or 'insufficient_evidence'
    for r in risks:
        assert r.risk_level in ("critical", "high", "medium", "low")
        assert r.status != "insufficient_evidence"

    # Specific vendor checks
    fiserv = next(r for r in risks if "Fiserv" in r.vendor_name)
    assert fiserv.risk_level == "critical"
    assert fiserv.status == "confirmed_runtime_ai"

    terrapin = next(r for r in risks if "Terrapin" in r.vendor_name)
    assert terrapin.risk_level == "low"
    assert terrapin.status == "marketing_fluff_cleared"

    fssi = next(r for r in risks if "FSSI" in r.vendor_name)
    assert fssi.risk_level == "low"
    assert fssi.status == "deterministic_baseline"


def test_meridian_export_contains_cognitive_classifications() -> None:
    bundle = load_meridian_workbook(SOURCE)
    records, student_cols = get_real_vendors_and_student_columns(bundle)
    vendors = [to_vendor_record(r) for r in records]
    criticality = score_vendors(vendors)
    evidence_by_vendor = {v.name: [] for v in vendors}

    risks = evaluate_vendor_portfolio(
        vendors=vendors,
        criticality=criticality,
        evidence_by_vendor=evidence_by_vendor,
        enable_cognitive=True,
    )

    updates = build_meridian_updates(
        bundle,
        vendors=vendors,
        criticality=criticality,
        sources=[],
        evidence=[],
        risks=risks,
        fetched_documents=[],
    )

    # V-002 is Fiserv
    fiserv_update = updates["V-002"]
    assert "Critical" in fiserv_update["AI Security Risk Classification"]
    assert "agentOS" in fiserv_update["AI Usage Detected (Y/N)"]
    assert "Zero Data Retention" in fiserv_update["Recommended Action"]

    # V-004 is Terrapin
    terrapin_update = updates["V-004"]
    assert "Low" in terrapin_update["AI Security Risk Classification"]
    assert "Marketing" in terrapin_update["AI Usage Detected (Y/N)"]


def test_evaluate_vendor_portfolio_mode_and_enable_toggle() -> None:
    bundle = load_meridian_workbook(SOURCE)
    records, _ = get_real_vendors_and_student_columns(bundle)
    vendors = [to_vendor_record(r) for r in records]
    criticality = score_vendors(vendors)
    evidence_by_vendor = {v.name: [] for v in vendors}

    # When enable_cognitive is False, empty evidence leads to not_rated
    risks_disabled = evaluate_vendor_portfolio(
        vendors=vendors,
        criticality=criticality,
        evidence_by_vendor=evidence_by_vendor,
        enable_cognitive=False,
    )
    for r in risks_disabled:
        assert r.risk_level == "not_rated"
        assert r.status == "insufficient_evidence"

    # When enable_cognitive is True with mode="reasoner", resolves offline with 0 latency
    risks_reasoner = evaluate_vendor_portfolio(
        vendors=vendors,
        criticality=criticality,
        evidence_by_vendor=evidence_by_vendor,
        enable_cognitive=True,
        mode="reasoner",
    )
    for r in risks_reasoner:
        assert r.risk_level in ("critical", "high", "medium", "low")
        assert r.status != "insufficient_evidence"
