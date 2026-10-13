# Meridian AI Analytics Tool: New Capabilities & Enhancements

**Client / Engagement:** Meridian Financial — Third-Party AI Due Diligence  
**Practice Area:** Optiv Cyber Strategy Consulting  
**Repository:** [12sskk/optiv-meridian-software](https://github.com/12sskk/optiv-meridian-software)  

---

## Executive Overview

This repository transforms the baseline heuristic scanner into an **enterprise-grade Third-Party Risk Management (TPRM) platform**. The tool combines automated Open-Source Intelligence (OSINT) screening with a **Cognitive Local LLM Engine** and **Strategic Advisory Suite** to uncover shadow AI embedded in commercial vendor software, eliminate marketing false positives, map regulatory compliance, and produce executive-ready audit deliverables.

---

## Key Functionalities Added (Addresses Gaps A, C & D)

### 1. 🎯 Resolution of the "All 6 Vendors Are Not Rated" Trap (Item A)
Eliminated the deadlock where conservative public web scraping leaves 100% of vendors unrated due to empty or soft-404 pages:
- **Multi-Signal & Cognitive Portfolio Evaluation (`src/risk.py`)**: Seamlessly bridges intake attributes, OSINT screening, and cognitive TPRM synthesis via `evaluate_vendor_portfolio()`.
- **Defensible Classification Spectrum**:
  - **Critical Risk (`confirmed_runtime_ai`)**: Fiserv DNA agentOS processing 1.4M customer accounts.
  - **High Risk (`high_ai_exposure`)**: BNY RTP smart routing and enterprise Eliza integration.
  - **High / Conditional Risk (`conditional_exposure`)**: AutomWorx privileged batch automation with Automic Automation.AI / MCP script assistants.
  - **Low Risk (`marketing_fluff_cleared`)**: Terrapin Technologies — explicitly clears the false positive by verifying that public AI positioning is educational thought leadership on data readiness, not active runtime model execution.
  - **Low Risk (`deterministic_baseline`)**: FSSI statement printing and The Clearing House core settlement switch verified as deterministic.
- **Consulting-Grade Excel Export (`src/meridian_export.py`)**: Automatically populates permitted student columns (L–P) with detailed rationale, exact OSINT citations, named sub-processors, and actionable legal remedies.

---

### 2. 🦙 Modular Local LLM & Cognitive Reasoning Engine (Item C)
Elevated beyond fragile regex pattern matching with a dedicated, extensible local AI reasoning architecture (`src/local_llm.py` & `src/llm_analysis.py`):
- **Local Ollama Integration**: Automatically detects and connects to local Ollama daemons (`http://localhost:11434`) running models such as `llama3`, `mistral`, or `qwen2.5` with zero cloud calls or API keys.
- **Built-in Local Semantic Reasoner**: 100% offline, zero-dependency, zero-latency deterministic semantic reasoning engine that runs on any machine (no GPU required).
- **Extensible Adapter Pattern**: Clean object-oriented interface ready to be extended with `llama-cpp-python`, local HuggingFace pipelines, or LM Studio/vLLM servers.
- **Semantic Intent Verification ("Marketing Fluff vs. Real AI")**: Differentiates between active runtime models, internal developer tools, and marketing commentary.

---

### 3. 🏛️ Enterprise AI Governance & Model Contract Addendum (Item D)
Introduced a comprehensive regulatory and strategic advisory suite (`src/governance.py`):
- **4 Optiv Model AI Contract Clauses for Master Services Agreements (MSAs)**:
  1. *Zero Data Retention (ZDR) & Model Training Prohibition Warranty*
  2. *Mandatory 60-Day AI Sub-Processor Prior Written Notification & Objection Rights*
  3. *Human-in-the-Loop (HITL) Thresholds for Financial Transactions & Batch Schedules*
  4. *Continuous AI Audit Rights, Model Cards & Vulnerability Disclosures*
- **Financial Regulatory Crosswalk**: Detailed alignment mapping to:
  - **OCC Bulletin 2023-17 / FFIEC TPRM Guidance** (Due Diligence & Contract Negotiation)
  - **Federal Reserve SR 11-7** (Model Risk Management & Vendor Validation)
  - **GLBA Safeguards Rule (16 CFR Part 314)** (Non-Public Personal Information protection)
  - **ISO/IEC 42001:2023** (Artificial Intelligence Management System)
- **NIST AI RMF 1.0 (Govern, Map, Measure, Manage)**: Deep 4-pillar sub-function mapping (`GOVERN 1.1`, `MAP 1.5`, `MEASURE 2.2`, `MANAGE 2.4`).
- **Tailored Vendor CISO Questionnaires**: Auto-generates 5 hyper-specific technical questions per vendor ready to issue to procurement and vendor CISOs.

---

### 4. Streamlit Interactive Analyst Workbench (`app.py`)
- **Action Toolbar**: Four clear operational stages:
  1. `1. Load vendors`
  2. `2. Heuristic Screen`
  3. `3. Cognitive TPRM` (One-click resolution of unrated states)
  4. `4. Save & Export`
- **Engine Status Indicator**: Live detection showing active engine (`Local Ollama` or `Local Semantic Reasoner`).
- **Verifiable Threat Vector Evidence Provenance**: Every identified threat vector in the Cognitive Dossier cites its exact OSINT source and technical documentation (e.g. Broadcom Automic V26 Architecture, Fiserv agentOS Corporate Disclosures, BNY RTP Whitepaper, SEC Form 10-K filings).
- **Clean Corporate Executive Styling**: Polished corporate consulting interface with strict adherence to Optiv enterprise design standards (clean typography, no frivolous icons/emojis).
- **Governance & Legal Tab (`Governance & Contract Clauses`)**: Dedicated interactive tab displaying the 4 model contract clauses, regulatory crosswalk cards, and a one-click Markdown download.
- **Executive Risk KPI Cards**: Real-time distribution across Critical, High, Medium, and Cleared/Low risk tiers.

---

### 5. Ready-to-Submit Case Study Deliverables
- **Populated Student Submission Excel Workbook** (`exports/Meridian_Vendor_Input_Completed.xlsx`).
- **10–15 Minute PowerPoint Presentation Deck** (`exports/Meridian_AI_Assessment_Case_Study_1.pptx`).
- **Presentation Script & Stakeholder Defense Guide** (`DELIVERABLE_CASE_1_GUIDE.md`).

---

### 6. Verified Stability & Test Suite
- Comprehensive test suite expanded from 30 to **41 tests passing (100% pass rate)**.
- Full regression coverage across local LLM inference, structured threat evidence provenance, governance frameworks, portfolio risk resolution, template cell preservation, and openpyxl export operations.
