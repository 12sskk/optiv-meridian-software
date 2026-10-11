"""Fetch public HTML and extract visible text."""

from __future__ import annotations

import logging
import re
from datetime import datetime, timezone
from typing import Iterable

import requests
from bs4 import BeautifulSoup

from src.models import ExtractedDocument, SourceCandidate

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 15
MAX_BYTES = 1_000_000
USER_AGENT = "MeridianAIAssessment/0.1 (case-study research; +https://localhost)"
SKIP_SOURCE_TYPES = {"search_query"}


class ExtractionError(ValueError):
    """Raised when a page cannot be fetched or parsed."""


def _visible_text(html: str) -> tuple[str | None, str]:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    title = soup.title.get_text(strip=True) if soup.title else None
    text = soup.get_text(separator=" ", strip=True)
    text = re.sub(r"\s+", " ", text).strip()
    return title, text


def extract_url(url: str, *, timeout: int = DEFAULT_TIMEOUT) -> ExtractedDocument:
    """GET a URL and return extracted visible text.

    Search-engine result pages and JavaScript-only apps are out of scope.
    """
    if url.startswith("https://duckduckgo.com/"):
        return ExtractedDocument(
            url=url,
            status="skipped",
            error="Search query URLs are not fetched automatically.",
        )

    try:
        response = requests.get(
            url,
            timeout=timeout,
            headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"},
            allow_redirects=True,
        )
    except requests.RequestException as exc:
        logger.warning("Fetch failed for %s: %s", url, exc)
        return ExtractedDocument(url=url, status="failed", error=f"Request failed: {exc}")

    if response.status_code >= 400:
        message = f"HTTP {response.status_code} from {url}"
        logger.warning(message)
        return ExtractedDocument(url=url, status="failed", error=message)

    content_type = response.headers.get("Content-Type", "")
    if content_type and "html" not in content_type.lower() and "text" not in content_type.lower():
        return ExtractedDocument(
            url=url,
            status="skipped",
            error=f"Unsupported content type: {content_type}",
        )

    content = response.content[: MAX_BYTES + 1]
    if len(content) > MAX_BYTES:
        return ExtractedDocument(
            url=url,
            status="failed",
            error=f"Response exceeded {MAX_BYTES} bytes.",
        )

    try:
        html = content.decode(response.encoding or "utf-8", errors="replace")
        title, text = _visible_text(html)
    except Exception as exc:
        return ExtractedDocument(url=url, status="failed", error=f"Parse failed: {exc}")

    if not text:
        return ExtractedDocument(
            url=url,
            status="empty",
            title=title,
            error="No visible text was extracted.",
        )

    retrieved_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    logger.info("Extracted %s characters from %s", len(text), url)
    return ExtractedDocument(
        url=url, status="ok", title=title, text=text, retrieved_at=retrieved_at
    )


def extract_candidates(
    candidates: Iterable[SourceCandidate],
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> list[ExtractedDocument]:
    """Extract text from candidate pages, skipping search-query placeholders."""
    documents: list[ExtractedDocument] = []
    for candidate in candidates:
        if candidate.source_type in SKIP_SOURCE_TYPES:
            documents.append(
                ExtractedDocument(
                    url=candidate.url,
                    status="skipped",
                    error="Source type is a search query, not a page to fetch.",
                )
            )
            continue
        documents.append(extract_url(candidate.url, timeout=timeout))
    return documents
