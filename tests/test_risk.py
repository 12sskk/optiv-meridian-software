"""Risk analysis stays unrated without evidence."""

from src.models import CriticalityResult, EvidenceItem
from src.risk import analyse_risk


def test_no_evidence_is_insufficient() -> None:
    result = analyse_risk(
        vendor_name="Vendor A",
        criticality=CriticalityResult(
            vendor_name="Vendor A",
            score=90,
            level="high",
            factors={},
        ),
        evidence=[],
    )
    assert result.status == "insufficient_evidence"
    assert result.risk_score is None
    assert result.risk_level == "not_rated"


def test_evidence_produces_draft_not_audit_opinion() -> None:
    evidence = [
        EvidenceItem(
            category="ai_capability_claim",
            snippet="generative AI",
            heuristic_score=0.5,
            rationale="test",
        )
    ]
    result = analyse_risk(vendor_name="Vendor B", criticality=None, evidence=evidence)
    assert result.status == "heuristic_draft"
    assert result.risk_score is not None
    assert any("not an audit opinion" in caveat.lower() for caveat in result.caveats)
