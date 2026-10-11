"""Classification operates only on supplied text."""

from src.classify import classify_text
from src.extract import _visible_text
from src.models import ExtractedDocument
from src.classify import classify_documents


def test_empty_text_yields_no_evidence() -> None:
    assert classify_text("") == []
    assert classify_text("   ") == []


def test_keywords_label_snippets_without_vendor_verdict() -> None:
    text = "We use generative AI and encryption for customer data."
    items = classify_text(text, source_url="https://example.invalid/security")
    categories = {item.category for item in items}
    assert "ai_capability_claim" in categories
    assert "security_control" in categories
    assert all("not a conclusion" in item.rationale.lower() for item in items)


def test_failed_documents_are_ignored() -> None:
    docs = [
        ExtractedDocument(url="https://x.invalid", status="failed", error="timeout"),
        ExtractedDocument(url="https://y.invalid", status="ok", text="ISO 27001 controls"),
    ]
    items = classify_documents(docs)
    assert len(items) == 1
    assert items[0].category == "security_control"


def test_visible_text_strips_scripts() -> None:
    title, text = _visible_text(
        "<html><head><title>Trust</title></head>"
        "<body><script>secret()</script><p>Privacy policy</p></body></html>"
    )
    assert title == "Trust"
    assert "secret" not in text
    assert "Privacy policy" in text


def test_evidence_keeps_exact_sentence_and_source_metadata() -> None:
    sentence = "Our AI assistant is powered by OpenAI via API."
    items = classify_text(
        "A general introduction. " + sentence + " More unrelated text.",
        source_url="https://example.invalid/trust",
        source_title="Trust Center",
        retrieved_at="2026-10-11T12:00:00+00:00",
    )
    ai_item = next(item for item in items if item.category == "ai_capability_claim")
    assert ai_item.snippet == sentence
    assert ai_item.source_title == "Trust Center"
    assert ai_item.retrieved_at == "2026-10-11T12:00:00+00:00"
    provider_item = next(item for item in items if item.category == "ai_subprocessor_disclosure")
    assert "OpenAI" in provider_item.matched_terms
    assert provider_item.source_url == "https://example.invalid/trust"


def test_provider_name_alone_does_not_trigger_subprocessor_category() -> None:
    items = classify_text("Our staff attended an OpenAI conference.")
    assert all(item.category != "ai_subprocessor_disclosure" for item in items)
