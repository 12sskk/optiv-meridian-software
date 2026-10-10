"""Discover candidate public sources. Does not assert findings."""

from __future__ import annotations

import logging
from urllib.parse import quote_plus, urljoin, urlparse

from src.models import SourceCandidate, VendorRecord

logger = logging.getLogger(__name__)

PATH_HINTS: tuple[tuple[str, str, str], ...] = (
    ("/", "official", "Vendor website from the intake file."),
    ("/privacy", "privacy", "Common privacy-policy path to review if it exists."),
    ("/privacy-policy", "privacy", "Alternate privacy-policy path."),
    ("/security", "security", "Common security or trust-center path."),
    ("/trust", "security", "Common trust-center path."),
    ("/legal", "legal", "Common legal page path."),
    ("/ai", "ai_docs", "Common product AI documentation path."),
    ("/docs", "docs", "Common documentation root."),
)


class SourceDiscoveryError(ValueError):
    """Raised when source discovery cannot proceed."""


def _normalise_website(website: str) -> str | None:
    text = website.strip()
    if not text:
        return None
    if not urlparse(text).scheme:
        text = "https://" + text
    parsed = urlparse(text)
    if not parsed.netloc:
        return None
    return f"{parsed.scheme}://{parsed.netloc}"


def discover_sources(vendor: VendorRecord) -> list[SourceCandidate]:
    """Return review candidates for a vendor.

    Candidates are hypothesized public locations and search queries. They are
    not evidence that a page exists, that the vendor uses AI, or that a
    control is present or absent.
    """
    if not vendor.name.strip():
        raise SourceDiscoveryError("Vendor name is required to discover sources.")

    candidates: list[SourceCandidate] = []
    seen: set[str] = set()

    def add(url: str, source_type: str, reason: str) -> None:
        key = url.rstrip("/").lower()
        if key in seen:
            return
        seen.add(key)
        candidates.append(
            SourceCandidate(
                url=url,
                source_type=source_type,
                reason=reason,
                vendor_name=vendor.name,
            )
        )

    if vendor.website:
        origin = _normalise_website(vendor.website)
        if origin is None:
            logger.warning("Ignoring invalid website for %s: %s", vendor.name, vendor.website)
        else:
            for path, source_type, reason in PATH_HINTS:
                add(urljoin(origin + "/", path.lstrip("/")), source_type, reason)

    query = quote_plus(f"{vendor.name} AI security privacy")
    add(
        f"https://duckduckgo.com/?q={query}",
        "search_query",
        "Public web search query for the analyst to review. Not a finding.",
    )
    if vendor.product:
        product_query = quote_plus(f"{vendor.name} {vendor.product} documentation")
        add(
            f"https://duckduckgo.com/?q={product_query}",
            "search_query",
            "Product documentation search query. Not a finding.",
        )

    logger.info("Discovered %s source candidates for %s", len(candidates), vendor.name)
    return candidates


def discover_sources_for_vendors(vendors: list[VendorRecord]) -> list[SourceCandidate]:
    """Discover candidates for each vendor without merging conclusions."""
    results: list[SourceCandidate] = []
    for vendor in vendors:
        results.extend(discover_sources(vendor))
    return results
