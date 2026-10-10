"""Heuristic classification of extracted text. Does not invent evidence."""

from __future__ import annotations

import logging
import re

from src.models import EvidenceItem, ExtractedDocument

logger = logging.getLogger(__name__)

# Keyword groups are indicators in the provided text only. Matching a keyword
# is not proof of product behaviour, residual risk, or a control gap.
CATEGORY_PATTERNS: dict[str, tuple[str, ...]] = {
    "ai_capability_claim": (
        r"\bgenerative ai\b",
        r"\bmachine learning\b",
        r"\blarge language model\b",
        r"\bllm\b",
        r"\bartificial intelligence\b",
    ),
    "data_processing": (
        r"\bpersonal data\b",
        r"\bcustomer data\b",
        r"\bdata processing\b",
        r"\bretain(s|ed|ing)?\b",
    ),
    "model_training": (
        r"\btrain(s|ed|ing)? (our |the )?(models?|ai)\b",
        r"\bused to (improve|train)\b",
    ),
    "security_control": (
        r"\bencryption\b",
        r"\bsso\b",
        r"\bsoc 2\b",
        r"\biso 27001\b",
        r"\baccess control\b",
    ),
    "privacy_commitment": (
        r"\bprivacy policy\b",
        r"\bgdpr\b",
        r"\bccpa\b",
        r"\bdata subject\b",
    ),
    "third_party_sharing": (
        r"\bthird[- ]party\b",
        r"\bsubprocessor\b",
        r"\bshare(s|d)? (your |customer )?data\b",
    ),
}


def _snippets_for(pattern: str, text: str, *, window: int = 140) -> list[str]:
    found: list[str] = []
    for match in re.finditer(pattern, text, flags=re.IGNORECASE):
        start = max(0, match.start() - window)
        end = min(len(text), match.end() + window)
        snippet = text[start:end].strip()
        if snippet and snippet not in found:
            found.append(snippet)
        if len(found) >= 3:
            break
    return found


def classify_text(text: str, *, source_url: str = "") -> list[EvidenceItem]:
    """Label snippets in analyst-supplied text.

    Returns an empty list when nothing matches. Silence is not treated as a
    negative finding about a vendor.
    """
    if not text or not text.strip():
        return []

    items: list[EvidenceItem] = []
    for category, patterns in CATEGORY_PATTERNS.items():
        hits = 0
        snippets: list[str] = []
        for pattern in patterns:
            matches = _snippets_for(pattern, text)
            hits += len(matches)
            for snippet in matches:
                if snippet not in snippets:
                    snippets.append(snippet)
        if not snippets:
            continue
        score = min(1.0, 0.35 + 0.15 * hits)
        items.append(
            EvidenceItem(
                category=category,
                snippet=snippets[0],
                heuristic_score=round(score, 2),
                rationale=(
                    f"Keyword pattern(s) for {category} matched {hits} time(s) "
                    "in the extracted text. This is a lead for review, not a conclusion."
                ),
                source_url=source_url,
            )
        )
    logger.info("Classified %s evidence items from %s", len(items), source_url or "text")
    return items


def classify_documents(documents: list[ExtractedDocument]) -> list[EvidenceItem]:
    """Classify successfully extracted documents only."""
    evidence: list[EvidenceItem] = []
    for document in documents:
        if document.status != "ok" or not document.text:
            continue
        evidence.extend(classify_text(document.text, source_url=document.url))
    return evidence
