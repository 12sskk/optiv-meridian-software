"""Map the current assessment draft into the supplied Meridian template fields."""

from __future__ import annotations

from datetime import date
import re
from typing import Any

from src.excel_handler import MeridianWorkbook
from src.models import CriticalityResult, EvidenceItem, RiskResult, SourceCandidate, VendorRecord


def _normalise(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def _clip(value: str, limit: int = 30000) -> str:
    """Stay safely below Excel's 32,767-character cell limit."""
    if len(value) <= limit:
        return value
    return value[: limit - 32].rstrip() + "\n[Truncated for Excel cell limit.]"


def _depth_text(level: str, fetched_count: int) -> str:
    level = level.lower()
    target_depth = {
        "critical": "Target depth: comprehensive public-source sweep and human review.",
        "high": "Target depth: deep public-source review and human review.",
        "medium": "Target depth: standard public-source review.",
        "low": "Target depth: baseline public-source review.",
    }.get(level, "Target depth: manual review required.")
    if fetched_count:
        performed = f"Performed so far: {fetched_count} public page(s) fetched and keyword-screened; findings remain heuristic and need human verification."
    else:
        performed = "Performed so far: source candidates generated only; page fetching was not performed, so this is not a completed OSINT assessment."
    return f"{target_depth} {performed}"


def build_meridian_updates(
    bundle: MeridianWorkbook,
    *,
    vendors: list[VendorRecord],
    criticality: list[CriticalityResult],
    sources: list[SourceCandidate],
    evidence: list[EvidenceItem],
    risks: list[RiskResult],
    fetched_documents: list[Any] | None = None,
) -> dict[str, dict[str, Any]]:
    """Create student-cell updates keyed by original Vendor ID.

    This function intentionally avoids converting weak keyword matches into
    confirmed AI-use or security-risk conclusions.
    """
    real_records = {str(record.vendor_id).strip(): record for record in bundle.records if not record.is_example}
    vendors_by_id = {str(v.vendor_id).strip(): v for v in vendors if v.vendor_id is not None}
    criticality_by_name = {item.vendor_name: item for item in criticality}
    risks_by_name = {item.vendor_name: item for item in risks}
    sources_by_name: dict[str, list[SourceCandidate]] = {}
    evidence_by_url: dict[str, list[EvidenceItem]] = {}
    for item in sources:
        sources_by_name.setdefault(item.vendor_name, []).append(item)
    for item in evidence:
        evidence_by_url.setdefault(item.source_url, []).append(item)
    fetched_documents = fetched_documents or []
    fetched_urls = {getattr(doc, "url", "") for doc in fetched_documents if getattr(doc, "status", "") == "ok"}

    # Resolve the actual workbook header spellings, including any spelling quirks.
    actual_columns = { _normalise(col.name): col.name for col in bundle.columns }

    def field_name(*needles: str) -> str | None:
        for needle in needles:
            exact = _normalise(needle)
            if exact in actual_columns:
                return actual_columns[exact]
        for actual_norm, actual_name in actual_columns.items():
            if all(_normalise(needle) in actual_norm for needle in needles):
                return actual_name
        return None

    fields = {
        "tier": field_name("Criticality Tier"),
        "criticality_rationale": field_name("Criticality Rationale"),
        "depth": field_name("Assessment Depth Applied"),
        "ai_usage": field_name("AI Usage Detected (Y/N)"),
        "evidence_description": field_name("Evidence Description along with OSINT Source(s) / Evidence Link"),
        "usage_description": field_name("How Vendor May Be Using AI"),
        "providers": field_name("Named AI Sub-processors / Model Providers"),
        "risk_classification": field_name("AI Security Risk Classification"),
        "risk_rationale": field_name("Risk Rationale"),
        "action": field_name("Recommended Action"),
        "assessed_by": field_name("Assessed By / Date", "Assessedd By / Date"),
    }

    updates: dict[str, dict[str, Any]] = {}
    for vendor_id, record in real_records.items():
        vendor = vendors_by_id.get(vendor_id)
        if vendor is None:
            continue
        crit = criticality_by_name.get(vendor.name)
        risk = risks_by_name.get(vendor.name)
        vendor_sources = sources_by_name.get(vendor.name, [])
        source_urls = {item.url for item in vendor_sources}
        vendor_evidence = [item for url in source_urls for item in evidence_by_url.get(url, [])]
        ai_evidence = [item for item in vendor_evidence if item.category == "ai_capability_claim"]
        fetched_count = len({url for url in fetched_urls if url in source_urls})

        output: dict[str, Any] = {}
        def put(key: str, value: Any) -> None:
            name = fields.get(key)
            if name is not None:
                output[name] = _clip(str(value)) if value is not None else ""

        if crit is not None:
            put("tier", crit.level.title())
            factor_text = "; ".join(f"{name.replace('_', ' ').title()}: {value:.0f}/100" for name, value in crit.factors.items())
            rationale = f"Proposed heuristic score: {crit.score:.1f}/100. Factors: {factor_text or 'none scored'}. " + " ".join(crit.notes)
            put("criticality_rationale", rationale)
            put("depth", _depth_text(crit.level, fetched_count))
        else:
            put("tier", "Requires manual review")
            put("criticality_rationale", "No criticality result was available for this vendor.")
            put("depth", "Manual review required; criticality has not been scored.")

        if ai_evidence:
            put("ai_usage", "Potential AI signal — analyst verification required; not confirmed by keyword matching alone.")
            usage_lines = [f"Potential signal: {item.snippet} [Source: {item.source_url}]" for item in ai_evidence[:5]]
            put("usage_description", "\n".join(usage_lines))
        elif fetched_count:
            put("ai_usage", "No AI keyword signal found in fetched pages; this does not prove AI is not used.")
            put("usage_description", "AI usage was not established by the currently fetched and keyword-screened pages.")
        else:
            put("ai_usage", "Unknown — source candidates have not been fetched; AI usage is not established.")
            put("usage_description", "Not established from current evidence. Public source candidates have not been fetched and reviewed.")

        if vendor_evidence:
            lines = []
            for item in vendor_evidence[:10]:
                lines.append(f"[{item.category}] {item.snippet}\nSource: {item.source_url}\nScreening note: {item.rationale}")
            put("evidence_description", "Heuristic excerpts from fetched public pages; review source context before relying on them:\n\n" + "\n\n".join(lines))
        else:
            candidate_urls = "\n".join(item.url for item in vendor_sources[:8])
            prefix = "No retrieved excerpts are available. The following are source candidates, not verified evidence:"
            put("evidence_description", prefix + ("\n" + candidate_urls if candidate_urls else " No source candidates were generated."))

        # No provider-name extraction is implemented yet; do not infer names.
        put("providers", "No AI sub-processor/model provider has been verified from the current extracted evidence. This is not evidence that none are used.")

        if not ai_evidence:
            put("risk_classification", "Not rated — AI usage has not been established by current evidence.")
            put("risk_rationale", "The current keyword screening did not establish AI usage in the relevant vendor service. Do not infer low risk or absence of AI. " + ("Other public-page keywords may be present but are not sufficient to assign an AI-specific risk rating."))
            put("action", "Fetch and review product/service documentation, privacy and trust pages, and sub-processor disclosures. Verify whether the documented AI capability applies to the service Meridian uses before assigning an AI security risk rating.")
        elif risk is None or risk.risk_score is None:
            put("risk_classification", "Not rated — insufficient risk evidence.")
            put("risk_rationale", "Potential AI-related keyword signal found, but there is not enough evidence to assign an AI-specific risk rating.")
            put("action", "Manually verify the AI-use claim and investigate data flows, retention/training terms, provider identity, and human oversight.")
        else:
            put("risk_classification", f"{risk.risk_level.title()} — heuristic draft; human review required.")
            put("risk_rationale", "Potential AI-related signal is present, but keyword matches do not prove production behaviour or harm. Drivers: " + "; ".join(risk.drivers) + " Caveats: " + " ".join(risk.caveats))
            put("action", "Verify the AI feature and its relevance to Meridian's service. Review data sent to the model, retention/training terms, named providers/sub-processors, contractual disclosures, access controls, and human oversight. Escalate unresolved high-impact unknowns.")

        put("assessed_by", f"Project team — draft generated {date.today().isoformat()}; human review required.")
        updates[vendor_id] = output

    return updates
