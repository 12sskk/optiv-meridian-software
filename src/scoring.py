"""Transparent vendor criticality scoring from supplied intake attributes.

The Meridian workbook has descriptive fields rather than the canonical numeric
fields used by generic intake spreadsheets. Those descriptive fields are mapped
explicitly below; inferred factors are called out in the result notes.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from src.models import CriticalityResult, VendorRecord

logger = logging.getLogger(__name__)

# Backward-compatible weights for generic intake spreadsheets.
WEIGHTS = {
    "data_sensitivity": 0.40,
    "user_impact": 0.25,
    "internet_facing": 0.20,
    "regulated_data": 0.15,
}

LEVELS = (
    (75.0, "high"),
    (45.0, "medium"),
    (0.0, "low"),
)

MERIDIAN_WEIGHTS = {
    "data_sensitivity": 0.35,
    "operational_dependency": 0.30,
    "payment_regulatory_exposure": 0.20,
    "data_volume": 0.15,
}


def _normalise_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")


def _to_scale(value: Any, *, default: float = 50.0) -> float:
    """Map common qualitative or numeric inputs onto 0-100."""
    if value is None:
        return default
    if isinstance(value, bool):
        return 100.0 if value else 0.0
    if isinstance(value, (int, float)):
        number = float(value)
        if 0 <= number <= 5:
            return number / 5.0 * 100.0
        return max(0.0, min(100.0, number))

    text = str(value).strip().lower()
    qualitative = {
        "critical": 100.0,
        "high": 85.0,
        "medium": 50.0,
        "moderate": 50.0,
        "low": 20.0,
        "none": 0.0,
        "yes": 100.0,
        "y": 100.0,
        "true": 100.0,
        "no": 0.0,
        "n": 0.0,
        "false": 0.0,
        "unknown": default,
        "n/a": default,
        "not applicable": default,
        "": default,
    }
    if text in qualitative:
        return qualitative[text]
    try:
        return _to_scale(float(text), default=default)
    except ValueError:
        logger.warning("Unrecognised scale value %r; using default %.0f", value, default)
        return default


def _attribute_lookup(attributes: dict[str, Any]) -> dict[str, Any]:
    return {_normalise_key(str(key)): value for key, value in attributes.items()}


def _first_value(attrs: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = attrs.get(_normalise_key(key))
        if value is not None and str(value).strip():
            return value
    return None


def _dependency_score(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip().lower()
    if "critical" in text:
        return 100.0
    if "high" in text:
        return 85.0
    if "moderate" in text or "medium" in text:
        return 55.0
    if "low" in text:
        return 25.0
    return None


def _sensitivity_score(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip().lower()
    if not text or text in {"unknown", "n/a", "not applicable"}:
        return None
    if any(term in text for term in ("health", "vulnerab", "tax identifier", "tax document", "full customer master")):
        return 100.0
    if "no direct customer data" in text or "payment messages in transit only" in text:
        if any(term in text for term in ("credential", "privileged access", "production job", "system configuration")):
            return 80.0
        return 45.0
    if any(term in text for term in ("customer", "account number", "account identifier", "balance", "transaction", "payment instruction", "portfolio", "compensation", "personal data", "borrower", "financial data")):
        return 85.0
    if any(term in text for term in ("credential", "privileged access", "production job", "system configuration", "call audio")):
        return 80.0
    return 50.0


def _volume_score(value: Any, *, context: str = "") -> float | None:
    if value is None:
        return None
    text = str(value).strip().lower()
    if not text or text in {"unknown", "n/a"}:
        return None
    if "not applicable" in text or text in {"none", "zero", "0"}:
        return 0.0
    combined = f"{text} {context}".lower()
    # Treat explicit counts as rough bands, not exact risk measurements.
    if re.search(r"\b(?:billion|billions)\b", combined):
        return 100.0
    if re.search(r"\b(?:million|millions)\b", combined):
        return 90.0
    if re.search(r"\b(?:thousand|thousands)\b", combined):
        return 70.0
    if re.search(r"\b\d[\d,]{3,}\b", combined):
        return 65.0
    # Some inventory entries describe cycles/messages without a numeric scale.
    if any(term in combined for term in ("message", "transaction", "document", "customer", "client", "account")):
        return 50.0
    return None


def _regulatory_payment_score(*values: Any) -> float | None:
    text = " ".join(str(value) for value in values if value is not None).lower()
    if not text.strip():
        return None
    high_terms = (
        "payment", "payments", "banking", "tax", "regulatory", "regulated",
        "clearing", "settlement", "financial institution", "core account",
        "transaction processing", "compliance", "irs",
    )
    if any(term in text for term in high_terms):
        return 85.0
    moderate_terms = ("financial", "wealth management", "customer statements", "account", "reporting")
    if any(term in text for term in moderate_terms):
        return 60.0
    return 40.0


def _score_meridian_vendor(vendor: VendorRecord) -> CriticalityResult:
    attrs = _attribute_lookup(vendor.attributes)
    sensitivity_raw = _first_value(attrs, "Data Classification Accessed", "data_sensitivity")
    dependency_raw = _first_value(attrs, "Operational Dependency", "operational_dependency", "user_impact")
    volume_raw = _first_value(attrs, "Data Volume (annual)", "data_volume", "customer_data_volume")
    category = _first_value(attrs, "Category", "Vendor Description", "vendor_description")
    business_process = _first_value(attrs, "Business Process Supported", "business_process")
    service = vendor.product
    description = _first_value(attrs, "Vendor Description", "vendor_description")

    raw_scores: dict[str, float | None] = {
        "data_sensitivity": _sensitivity_score(sensitivity_raw),
        "operational_dependency": _dependency_score(dependency_raw),
        "payment_regulatory_exposure": _regulatory_payment_score(category, business_process, service, description),
        "data_volume": _volume_score(volume_raw, context=str(sensitivity_raw or "")),
    }
    notes: list[str] = [
        "Meridian-specific scoring uses the supplied descriptive inventory fields and a proposed heuristic rubric; it is not an official Optiv formula.",
        "Payment/regulatory exposure is inferred from supplied category, service and business-process descriptions; verify it during review.",
    ]
    factors: dict[str, float] = {}
    available_weight = 0.0
    weighted_total = 0.0
    for name, weight in MERIDIAN_WEIGHTS.items():
        value = raw_scores[name]
        if value is None:
            notes.append(f"Missing or uninterpretable input for {name}; excluded from the weighted average.")
            continue
        factors[name] = round(value, 2)
        available_weight += weight
        weighted_total += value * weight

    if available_weight == 0:
        score = 50.0
        notes.append("No criticality factors could be scored; 50 is a placeholder only and requires manual review.")
    else:
        score = round(weighted_total / available_weight, 2)
        if available_weight < 0.999:
            notes.append(f"Score uses {available_weight:.0%} of the configured factor weight because some inputs were unavailable.")

    # The explicit operational dependency value is a strong tier signal.
    dependency_text = str(dependency_raw or "").strip().lower()
    if "critical" in dependency_text:
        level = "critical"
        notes.append("Criticality tier set to Critical because the supplied Operational Dependency field explicitly says Critical; treat this as an override for review.")
    elif score >= 75:
        level = "high"
    elif score >= 45:
        level = "medium"
    else:
        level = "low"

    logger.info("Meridian criticality for %s: score=%s level=%s", vendor.name, score, level)
    return CriticalityResult(
        vendor_name=vendor.name,
        score=score,
        level=level,
        factors=factors,
        notes=notes,
    )


def score_vendor(vendor: VendorRecord) -> CriticalityResult:
    """Score business criticality from supplied intake attributes only.

    Meridian inventory records are handled using explicit source-column mapping
    and text-aware scoring. Generic workbooks retain the original canonical
    scoring behavior for backward compatibility.
    """
    normalised = _attribute_lookup(vendor.attributes)
    if "data_classification_accessed" in normalised or "operational_dependency" in normalised:
        return _score_meridian_vendor(vendor)

    notes: list[str] = []
    factors: dict[str, float] = {}
    weighted = 0.0
    for name, weight in WEIGHTS.items():
        raw = vendor.attributes.get(name)
        if raw is None:
            notes.append(f"Missing {name}; defaulted to 50.")
        scaled = _to_scale(raw)
        factors[name] = round(scaled, 2)
        weighted += scaled * weight

    score = round(weighted, 2)
    level = "low"
    for threshold, label in LEVELS:
        if score >= threshold:
            level = label
            break

    logger.info("Criticality for %s: score=%s level=%s", vendor.name, score, level)
    return CriticalityResult(
        vendor_name=vendor.name,
        score=score,
        level=level,
        factors=factors,
        notes=notes,
    )


def score_vendors(vendors: list[VendorRecord]) -> list[CriticalityResult]:
    """Score each vendor independently."""
    return [score_vendor(vendor) for vendor in vendors]
