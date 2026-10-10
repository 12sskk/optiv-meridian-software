"""Source discovery must return candidates, not fabricated findings."""

import pytest

from src.models import VendorRecord
from src.osint import SourceDiscoveryError, discover_sources


def test_search_query_is_not_a_finding() -> None:
    sources = discover_sources(VendorRecord(name="Contoso"))
    assert sources
    assert all(item.source_type == "search_query" for item in sources)
    assert all("Not a finding" in item.reason for item in sources)


def test_website_adds_path_candidates_without_claiming_they_exist() -> None:
    sources = discover_sources(
        VendorRecord(name="Contoso", website="contoso.invalid")
    )
    urls = {item.url for item in sources}
    assert "https://contoso.invalid/privacy" in urls
    assert all("finding" not in item.reason.lower() or "Not a finding" in item.reason for item in sources)


def test_blank_name_rejected() -> None:
    with pytest.raises(SourceDiscoveryError):
        discover_sources(VendorRecord(name="  "))
