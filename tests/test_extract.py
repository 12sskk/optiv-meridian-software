"""Extraction skips search queries and does not require the network."""

from src.extract import extract_candidates, extract_url
from src.models import SourceCandidate


def test_duckduckgo_is_not_fetched() -> None:
    document = extract_url("https://duckduckgo.com/?q=test")
    assert document.status == "skipped"
    assert document.text == ""


def test_search_candidates_are_skipped() -> None:
    docs = extract_candidates(
        [
            SourceCandidate(
                url="https://duckduckgo.com/?q=acme",
                source_type="search_query",
                reason="Not a finding.",
                vendor_name="Acme",
            )
        ]
    )
    assert docs[0].status == "skipped"
