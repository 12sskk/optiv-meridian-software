"""Combine criticality and evidence into a conservative risk view."""

from __future__ import annotations

import logging

from src.models import CriticalityResult, EvidenceItem, RiskResult

logger = logging.getLogger(__name__)

# Evidence categories that can raise residual risk when present in text.
ELEVATING = {"ai_capability_claim", "model_training", "third_party_sharing", "data_processing"}
MITIGATING = {"security_control", "privacy_commitment"}


def analyse_risk(
    *,
    vendor_name: str,
    criticality: CriticalityResult | None,
    evidence: list[EvidenceItem],
) -> RiskResult:
    """Produce a risk result that refuses to conclude without evidence.

    Hardcoded vendor reputations are not used. Missing public text yields
    ``insufficient_evidence`` rather than a Low/Medium/High rating.
    """
    caveats = [
        "Public-web heuristics are incomplete and can miss or overstate AI usage.",
        "Keyword matches are not confirmation of product behaviour or control effectiveness.",
    ]
    if not evidence:
        logger.info("Insufficient evidence for %s", vendor_name)
        return RiskResult(
            vendor_name=vendor_name,
            criticality_score=None if criticality is None else criticality.score,
            risk_score=None,
            risk_level="not_rated",
            status="insufficient_evidence",
            drivers=[],
            caveats=caveats
            + ["No classified public-text evidence was available for this vendor."],
        )

    criticality_score = 50.0 if criticality is None else criticality.score
    elevating = [item for item in evidence if item.category in ELEVATING]
    mitigating = [item for item in evidence if item.category in MITIGATING]

    elevation = min(25.0, 8.0 * len(elevating))
    mitigation = min(15.0, 5.0 * len(mitigating))
    score = round(max(0.0, min(100.0, criticality_score * 0.7 + elevation - mitigation)), 2)

    if score >= 70:
        level = "high"
    elif score >= 40:
        level = "medium"
    else:
        level = "low"

    drivers = [
        f"{item.category} (heuristic {item.heuristic_score})"
        for item in evidence[:8]
    ]
    if criticality is not None:
        drivers.insert(0, f"intake criticality {criticality.level} ({criticality.score})")

    logger.info("Risk for %s: score=%s level=%s", vendor_name, score, level)
    return RiskResult(
        vendor_name=vendor_name,
        criticality_score=None if criticality is None else criticality.score,
        risk_score=score,
        risk_level=level,
        status="heuristic_draft",
        drivers=drivers,
        caveats=caveats + ["Treat this as a draft for analyst review, not an audit opinion."],
    )
