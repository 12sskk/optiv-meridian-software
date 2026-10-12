# Meridian AI Analytics Tool: Enhancements & Cognitive TPRM Extension
**Author / Team:** Optiv Consulting Cyber Strategy Team (`sskk`)  
**Date:** October 2026  
**Context:** Case Study 01 — Third-Party AI Due Diligence for Meridian Financial  

---

## 1. Summary of Changes Over Original Repository

This repository extends the baseline heuristic evaluation tool with a **Hybrid Cognitive TPRM Architecture** to evaluate third-party vendor AI footprints, eliminate marketing false positives, align with regulatory standards (**NIST AI RMF 1.0**, **ISO 42001**), and produce audit-ready deliverables.

---

## 2. Code Modifications & New Modules

### A. Modified Files
- **[`app.py`](app.py)**:
  - **Quick-Load Case Study**: Added direct one-click ingestion of `supporting material/Meridian_Vendor_Input.xlsx`.
  - **Manual Evidence Screening**: Added an interactive expander allowing analysts to paste and classify arbitrary text snippets (SEC 10-K, whitepapers, press releases) on the fly.
  - **Benchmark Case Evidence**: Added one-click pre-loading of verified OSINT research for Fiserv, BNY, and AutomWorx.
  - **Executive KPI Cards**: Added risk distribution metric cards (Critical, High, Medium, Unrated).
  - **Dedicated AI TPRM Dossier Tab**: Added a 6th interactive tab integrating LLM semantic reasoning and questionnaire generation.

### B. New Core Modules
- **[`src/llm_analysis.py`](src/llm_analysis.py)**:
  - **Semantic Intent Classifier**: Differentiates runtime embedded AI in delivered products vs. internal employee tools vs. marketing thought leadership.
  - **NIST AI RMF 1.0 Alignment**: Maps vendor AI risk to the 4 core functions (*Govern, Map, Measure, Manage*).
  - **Automated Custom Questionnaires**: Auto-generates 5 tailored technical questions per vendor for TPRM audits.
  - **Dual Operation Mode**: Connects to live Google Gemini or OpenAI APIs with an offline cognitive synthesis fallback so assessments work without an API key.

### C. Helper & Generator Scripts
- **[`create_input_workbook.py`](create_input_workbook.py)**: Recreates the original case study Excel template (`supporting material/Meridian_Vendor_Input.xlsx`), resolving missing file dependencies and bringing the test suite to **100% passing (30 of 30 tests)**.
- **[`populate_completed_workbook.py`](populate_completed_workbook.py)**: Automates the populating of student columns L through P for all 6 Meridian vendors (`V-001` through `V-006`) while preserving formatting and the `V-000 Larkspur` example.
- **[`generate_presentation_deck.py`](generate_presentation_deck.py)**: Generates a 10-slide widescreen Optiv-branded PowerPoint presentation (`.pptx`) covering the 5 case study deliverables.

---

## 3. Case Study Deliverable Artifacts

1. **[`exports/Meridian_Vendor_Input_Completed.xlsx`](exports/Meridian_Vendor_Input_Completed.xlsx)**:
   - The completed offline student workbook.
   - Preserves all 3 sheets (`Vendor Inventory`, `Field Guide`, `Points to consider`) and original formatting.
   - Contains consulting-grade findings, depth rationale, exact quotes, and TPRM action plans for all 6 active vendors.

2. **[`exports/Meridian_AI_Assessment_Case_Study_1.pptx`](exports/Meridian_AI_Assessment_Case_Study_1.pptx)**:
   - Optiv-branded 16:9 widescreen presentation deck.
   - Covers: Functional Design Diagram, Technical System Architecture, 4-Tier OSINT Source Strategy, Criticality Scoring Rubric, Portfolio Matrix, Fiserv/BNY Deep Dives, Governance Safeguards, and Demo Summary.

3. **[`DELIVERABLE_CASE_1_GUIDE.md`](DELIVERABLE_CASE_1_GUIDE.md)**:
   - Slide-by-slide 10–15 minute walkthrough speaking script.
   - Stakeholder Q&A defense guide for anticipated questions from partners and CISOs.
   - 4 Model AI Master Services Agreement (MSA) Contract Clauses.

---

## 4. Test Suite Execution

All pipeline tests pass:
```bash
python -m pytest -q
# Output: 30 passed in 1.23s (100%)
```
