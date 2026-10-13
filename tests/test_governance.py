"""Unit tests for Governance, NIST AI RMF 1.0, and Model Contract Clauses."""

from src.governance import (
    get_model_contract_clauses,
    get_regulatory_crosswalk,
    get_nist_pillars,
    format_clauses_as_markdown,
)


def test_model_contract_clauses_completeness() -> None:
    clauses = get_model_contract_clauses()
    assert len(clauses) == 4
    clause_ids = [c["id"] for c in clauses]
    assert clause_ids == ["CLAUSE-01", "CLAUSE-02", "CLAUSE-03", "CLAUSE-04"]

    # Verify key protections are present
    assert any("Zero Data Retention" in c["title"] for c in clauses)
    assert any("60-Day" in c["title"] for c in clauses)
    assert any("Human-in-the-Loop" in c["title"] for c in clauses)
    assert any("Audit Rights" in c["title"] for c in clauses)


def test_regulatory_crosswalk_coverage() -> None:
    regs = get_regulatory_crosswalk()
    assert "OCC Bulletin 2023-17 / FFIEC TPRM Guidance" in regs
    assert "Federal Reserve SR 11-7" in regs
    assert "GLBA Safeguards Rule (16 CFR Part 314)" in regs
    assert "ISO/IEC 42001:2023" in regs


def test_nist_pillars_structure() -> None:
    pillars = get_nist_pillars()
    assert set(pillars.keys()) == {"Govern", "Map", "Measure", "Manage"}
    for name, p in pillars.items():
        assert len(p["core_subfunctions"]) >= 3


def test_format_clauses_markdown() -> None:
    md = format_clauses_as_markdown()
    assert "Optiv Consulting" in md
    assert "CLAUSE-01" in md
    assert "CLAUSE-04" in md
    assert "Zero Data Retention" in md
