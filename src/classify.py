"""Heuristic evidence classification with traceable source excerpts.

Matches are review leads only. They do not prove a vendor's deployed product
configuration, use of AI in Meridian's service, or a security/compliance failure.
"""

from __future__ import annotations

import logging
import re
from typing import Iterable

from src.models import EvidenceItem, ExtractedDocument

logger = logging.getLogger(__name__)

CATEGORY_PATTERNS: dict[str, tuple[str, ...]] = {
    "ai_capability_claim": (
        r"\bgenerative ai\b", r"\bmachine learning\b",
        r"\blarge language model(?:s)?\b", r"\bllm(?:s)?\b",
        r"\bartificial intelligence\b", r"\bAI[- ]powered\b",
        r"\bAI assistant\b", r"\bAI feature(?:s)?\b",
    ),
    "data_processing": (
        r"\bpersonal data\b", r"\bcustomer data\b",
        r"\bdata processing\b", r"\bretain(?:s|ed|ing)?\b",
        r"\bconfidential information\b",
    ),
    "model_training": (
        r"\btrain(?:s|ed|ing)? (?:our |the |its )?(?:models?|AI systems?)\b",
        r"\bused to (?:improve|train)\b",
        r"\btraining data\b", r"\bimprove our models\b",
    ),
    "security_control": (
        r"\bencryption\b", r"\bSSO\b", r"\bSOC 2\b",
        r"\bISO 27001\b", r"\baccess control\b",
        r"\bpenetration test(?:ing)?\b", r"\bMFA\b",
    ),
    "privacy_commitment": (
        r"\bprivacy policy\b", r"\bGDPR\b", r"\bCCPA\b",
        r"\bdata subject\b", r"\bdelete your data\b",
    ),
    "third_party_sharing": (
        r"\bthird[- ]party\b", r"\bsubprocessors?\b",
        r"\bshare(?:s|d)? (?:your |customer |personal )?data\b",
        r"\bservice providers?\b",
    ),
}

# These are provider names, not findings by themselves. A disclosure category is
# emitted only when a provider name and an explicit AI/vendor-processing cue occur
# in the same sentence. This intentionally favours precision over recall.
AI_PROVIDER_PATTERNS: tuple[str, ...] = (
    r"\bOpenAI\b", r"\bAnthropic\b", r"\bAzure OpenAI\b",
    r"\bGoogle Vertex AI\b", r"\bAmazon Bedrock\b",
    r"\bAWS Bedrock\b", r"\bCohere\b", r"\bMistral AI\b",
    r"\bGoogle Gemini\b", r"\bMicrosoft Copilot\b",
)
AI_PROCESSING_CUES: tuple[str, ...] = (
    r"\bsubprocessor\b", r"\bthird[- ]party provider\b",
    r"\bAI provider\b", r"\bmodel provider\b",
    r"\bprocess(?:es|ing)? .*data (?:using|with)\b",
    r"\bpowered by\b", r"\bprovided by\b",
    r"\bhosted by\b", r"\bAPI\b",
)


def _sentences(text: str) -> list[str]:
    """Split visible text into short, exact sentence-like excerpts."""
    normalized = re.sub(r"\s+", " ", text).strip()
    if not normalized:
        return []
    # Keep punctuation and avoid treating common web abbreviations as boundaries.
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])", normalized)
    return [part.strip() for part in parts if part.strip()]


def _matching_terms(patterns: Iterable[str], text: str) -> list[str]:
    terms: list[str] = []
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            term = match.group(0)
            if term.lower() not in {item.lower() for item in terms}:
                terms.append(term)
    return terms


def classify_text(
    text: str, *, source_url: str = "", source_title: str = "",
    retrieved_at: str | None = None,
) -> list[EvidenceItem]:
    """Classify text into traceable evidence leads using exact sentence excerpts."""
    if not text or not text.strip():
        return []

    sentences = _sentences(text)
    items: list[EvidenceItem] = []
    for category, patterns in CATEGORY_PATTERNS.items():
        matched: list[tuple[str, list[str]]] = []
        for sentence in sentences:
            terms = _matching_terms(patterns, sentence)
            if terms:
                matched.append((sentence, terms))
            if len(matched) >= 3:
                break
        if not matched:
            continue
        excerpt, terms = matched[0]
        # Score is a reproducible keyword-strength indicator, not probability.
        score = min(0.85, 0.35 + 0.10 * len(terms) + 0.05 * (len(matched) - 1))
        items.append(EvidenceItem(
            category=category, snippet=excerpt[:700],
            heuristic_score=round(score, 2),
            rationale=(
                f"Matched term(s): {', '.join(terms)}. "
                "Heuristic text match only, not a conclusion. Verify the source context and "
                "applicability to the specific service Meridian uses before drawing a conclusion."
            ),
            source_url=source_url, source_title=source_title,
            retrieved_at=retrieved_at, matched_terms=terms,
        ))

    # Separate, stricter signal for named AI/model providers or subprocessors.
    for sentence in sentences:
        providers = _matching_terms(AI_PROVIDER_PATTERNS, sentence)
        cues = _matching_terms(AI_PROCESSING_CUES, sentence)
        if providers and cues:
            items.append(EvidenceItem(
                category="ai_subprocessor_disclosure", snippet=sentence[:700],
                heuristic_score=0.65,
                rationale=(
                    f"Named provider term(s): {', '.join(providers)}; disclosure cue(s): "
                    f"{', '.join(cues)}. This indicates a possible disclosed relationship, "
                    "not confirmation that the provider processes Meridian data."
                ),
                source_url=source_url, source_title=source_title,
                retrieved_at=retrieved_at, matched_terms=providers + cues,
            ))
            break

    logger.info("Classified %s evidence items from %s", len(items), source_url or "text")
    return items


def classify_documents(documents: list[ExtractedDocument]) -> list[EvidenceItem]:
    """Classify successfully extracted documents and retain source metadata."""
    evidence: list[EvidenceItem] = []
    for document in documents:
        if document.status != "ok" or not document.text:
            continue
        evidence.extend(classify_text(
            document.text, source_url=document.url, source_title=document.title or "",
            retrieved_at=document.retrieved_at,
        ))
    return evidence
