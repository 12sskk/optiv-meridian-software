"""Unit tests for Local LLM and Cognitive Semantic Reasoning Engine."""

import pytest
from src.local_llm import (
    LocalSemanticReasoner,
    OllamaLocalProvider,
    get_local_llm_engine,
    analyze_vendor_locally,
)


def test_local_reasoner_availability() -> None:
    reasoner = LocalSemanticReasoner()
    assert reasoner.is_available() is True


def test_local_reasoner_fiserv_runtime_ai() -> None:
    res = analyze_vendor_locally(
        vendor_name="Fiserv, Inc.",
        service_description="DNA Core Banking Platform",
        evidence_text="agentOS deployment with OpenAI endpoints.",
        mode="reasoner",
    )
    assert "Critical" in res["verdict"]
    assert "Confirmed" in res["runtime_ai_present"]
    assert res["confidence_score"] >= 90
    assert len(res["tailored_questionnaire"]) == 5
    assert "ZDR" in res["contractual_recommendation"] or "Zero Data Retention" in res["contractual_recommendation"]
    assert "Govern" in res["nist_ai_rmf"]
    assert len(res["data_exposure_threats"]) >= 1
    assert "threat" in res["data_exposure_threats"][0]
    assert "source" in res["data_exposure_threats"][0]
    assert "agentos" in res["data_exposure_threats"][0]["source"].lower() or "fiserv" in res["data_exposure_threats"][0]["source"].lower()


def test_local_reasoner_terrapin_marketing_fluff() -> None:
    res = analyze_vendor_locally(
        vendor_name="Terrapin Technologies",
        service_description="Wealth Management Reporting",
        evidence_text="Educational whitepaper on AI-ready data foundations.",
        mode="reasoner",
    )
    assert "Marketing" in res["verdict"]
    assert "High" in res["marketing_fluff"]
    assert res["runtime_ai_present"] == "None Identified"


def test_local_reasoner_dynamic_arbitrary_vendor() -> None:
    reasoner = LocalSemanticReasoner()
    res = reasoner.analyze(
        vendor_name="CloudAudit AI Corp",
        service_description="Automated log scanning",
        evidence_text="Autonomous agent pipeline powered by Anthropic Bedrock model for PII analysis.",
    )
    assert res["vendor_name"] == "CloudAudit AI Corp"
    assert "High AI Risk" in res["verdict"] or "Conditional" in res["verdict"]
    assert len(res["tailored_questionnaire"]) == 5
    assert "Govern" in res["nist_ai_rmf"]
    assert "Map" in res["nist_ai_rmf"]
    assert len(res["data_exposure_threats"]) >= 1
    assert "threat" in res["data_exposure_threats"][0]
    assert "source" in res["data_exposure_threats"][0]


def test_ollama_graceful_fallback_when_offline() -> None:
    # Point to an unreachable port
    provider = OllamaLocalProvider(base_url="http://localhost:59999", timeout=1)
    assert provider.is_available() is False

    # Factory auto mode should fallback gracefully to LocalSemanticReasoner
    engine = get_local_llm_engine(mode="auto")
    assert engine.is_available() is True
    res = engine.analyze(
        vendor_name="FSSI",
        service_description="Document Print",
        evidence_text="",
    )
    assert "Deterministic" in res["verdict"] or "No Runtime AI" in res["verdict"]
