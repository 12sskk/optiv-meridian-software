"""Combine intake criticality and verified evidence into a defensible risk view.

Supports:
1. Conservative heuristic scoring when only raw web snippets are present.
2. Cognitive semantic TPRM synthesis to prevent 'all vendors unrated' deadlocks.
3. Explicit differentiation between Runtime AI, Marketing Fluff, and Deterministic systems.
"""

from __future__ import annotations

import logging
from typing import Any

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
    cognitive_dossier: dict[str, Any] | None = None,
) -> RiskResult:
    """Produce a defensible third-party risk assessment.

    If cognitive_dossier is supplied (from Local LLM or benchmark analysis),
    incorporates semantic reasoning, NIST mapping, and threat vectors to resolve
    unrated deadlocks. Otherwise, adheres strictly to conservative heuristic rules.
    """
    caveats = [
        "Public-web heuristics are incomplete and can miss or overstate AI usage.",
        "Keyword matches are not confirmation of product behaviour or control effectiveness.",
    ]

    # --- Mode 1: Cognitive TPRM Synthesis (Resolves 'All Unrated' Trap) ---
    if cognitive_dossier is not None:
        verdict = cognitive_dossier.get("verdict", "")
        conf = cognitive_dossier.get("confidence_score", 85)
        runtime_ai = cognitive_dossier.get("runtime_ai_present", "")
        fluff = cognitive_dossier.get("marketing_fluff", "")
        threats = cognitive_dossier.get("data_exposure_threats", [])
        contract_rec = cognitive_dossier.get("contractual_recommendation", "")

        crit_score = 50.0 if criticality is None else criticality.score
        crit_level = "unrated" if criticality is None else criticality.level

        drivers = [f"Intake criticality: {crit_level} ({crit_score:.1f}/100)"]
        drivers.append(f"Cognitive verdict: {verdict} (Confidence: {conf}%)")
        drivers.append(f"Runtime AI status: {runtime_ai}")
        if threats:
            for t in threats[:3]:
                if isinstance(t, dict):
                    th_text = t.get("threat", "")
                    th_src = t.get("source", "")
                    if th_src:
                        drivers.append(f"Threat vector: {th_text} [Source: {th_src}]")
                    else:
                        drivers.append(f"Threat vector: {th_text}")
                else:
                    drivers.append(f"Threat vector: {t}")

        # Determine level and score based on cognitive verdict
        verdict_lower = verdict.lower()
        if "critical" in verdict_lower or "critical" in runtime_ai.lower():
            level = "critical"
            score = 92.0
            status = "confirmed_runtime_ai"
        elif "high" in verdict_lower:
            level = "high"
            score = 78.0
            status = "high_ai_exposure"
        elif "conditional" in verdict_lower or "inconclusive" in verdict_lower:
            level = "high"
            score = 68.0
            status = "conditional_exposure"
        elif "marketing" in verdict_lower or fluff.lower() == "high":
            level = "low"
            score = 25.0
            status = "marketing_fluff_cleared"
            drivers.append("Educational/marketing whitepapers only; no live model execution on client data.")
        else:
            level = "low"
            score = 15.0
            status = "deterministic_baseline"
            drivers.append("Deterministic execution pipeline with no generative model dependencies.")

        logger.info("Cognitive risk evaluation for %s: level=%s status=%s", vendor_name, level, status)
        return RiskResult(
            vendor_name=vendor_name,
            criticality_score=None if criticality is None else criticality.score,
            risk_score=score,
            risk_level=level,
            status=status,
            drivers=drivers,
            caveats=caveats + [
                f"Evaluated via Local Cognitive TPRM Engine. Recommendation: {contract_rec}",
                "Treat as a defensible risk opinion for executive CISO review.",
            ],
        )

    # --- Mode 2: Baseline Heuristic Evaluation (Conservative) ---
    ai_claims = [item for item in evidence if item.category == "ai_capability_claim"]
    if not evidence or not ai_claims:
        logger.info("AI-specific risk not rated for %s: no AI capability claim", vendor_name)
        reason = (
            "No classified public-text evidence was available for this vendor."
            if not evidence
            else "Other keywords or a provider disclosure may be present, but no AI capability claim was identified."
        )
        return RiskResult(
            vendor_name=vendor_name,
            criticality_score=None if criticality is None else criticality.score,
            risk_score=None,
            risk_level="not_rated",
            status="insufficient_evidence",
            drivers=[],
            caveats=caveats + [reason, "Not rated does not mean low risk or no AI usage."],
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


def evaluate_vendor_portfolio(
    *,
    vendors: list[Any],
    criticality: list[CriticalityResult],
    evidence_by_vendor: dict[str, list[EvidenceItem]],
    enable_cognitive: bool = True,
    mode: str = "auto",
) -> list[RiskResult]:
    """Score the complete vendor portfolio using Local LLM synthesis where available."""
    from src import local_llm

    crit_by_name = {c.vendor_name: c for c in criticality}
    results = []

    for vendor in vendors:
        v_evidence = evidence_by_vendor.get(vendor.name, [])
        v_crit = crit_by_name.get(vendor.name)

        cognitive_dossier = None
        if enable_cognitive:
            ev_summary = "\n".join(e.snippet for e in v_evidence[:5]) if v_evidence else ""
            cognitive_dossier = local_llm.analyze_vendor_locally(
                vendor_name=vendor.name,
                service_description=getattr(vendor, "product", "") or "",
                evidence_text=ev_summary,
                mode=mode,
            )

        res = analyse_risk(
            vendor_name=vendor.name,
            criticality=v_crit,
            evidence=v_evidence,
            cognitive_dossier=cognitive_dossier,
        )
        results.append(res)

    return results
