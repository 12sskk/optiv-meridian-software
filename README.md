# Optiv TPRM | Meridian Financial AI Due Diligence Platform

**Practice Area:** Optiv Cyber Strategy & Third-Party Risk Management (TPRM)  
**Client Engagement:** Meridian Financial — Third-Party Artificial Intelligence Risk Assessment  
**Repository:** [12sskk/optiv-meridian-software](https://github.com/12sskk/optiv-meridian-software)  
**Target Environment:** Python 3.10+ | Streamlit | Local LLM / Offline Semantic Reasoner | openpyxl  

---

## Executive Summary

The **Optiv Meridian TPRM Platform** is an enterprise-grade assessment workbench developed to uncover, evaluate, and mitigate shadow artificial intelligence and machine learning models embedded in third-party banking software.

Banking institutions like Meridian Financial face a critical challenge: commercial vendors (core ledger, payment switches, batch schedulers) are rapidly embedding foundation models, autonomous agent frameworks, and third-party APIs (OpenAI, Microsoft Azure OpenAI) into delivered services without adequate transparency. Traditional keyword-based web scrapers fail in this environment—either deadlocking with 100% of vendors left "Unrated" due to corporate firewalls, or generating false positives by confusing marketing whitepapers with active runtime AI.

This platform bridges automated Open-Source Intelligence (OSINT) screening with a **pluggable, zero-cloud Local Cognitive Reasoning Engine** and an **Enterprise AI Governance Suite** to produce defensible audit determinations, tailored technical questionnaires, and contract-ready legal remedies.

---

## Architecture & Operational Workflow

The application executes an end-to-end 4-stage assessment pipeline:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   Meridian_Vendor_Input.xlsx Ingestion                 │
│  - Parses non-standard Row 4 headers                                   │
│  - Preserves Row 5 (V-000 Larkspur) fictional example untouched        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│             Stage 1: Business Criticality Intake Scoring               │
│  - Data Sensitivity (35%)       - Operational Dependency (30%)         │
│  - Regulatory Exposure (20%)    - Transaction Volume (15%)             │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│             Stage 2: Heuristic Screening & OSINT Discovery             │
│  - Candidate path discovery (/privacy, /security, /trust, /ai)         │
│  - Safe HTML text extraction and sentence parsing                      │
│  - Regex screening (AI claims, sub-processors, security controls)      │
│  - Conservative baseline: absence of scraped proof = "Not Rated"       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│            Stage 3: Cognitive TPRM Scanning (Local AI Engine)          │
│  - Pluggable inference: Local Ollama daemon OR 100% Offline Reasoner   │
│  - Resolves unrated deadlock via domain ontology & semantic cues       │
│  - Differentiates active Runtime AI from marketing thought leadership  │
│  - Assigns defensible risk scores (Critical: 92, High: 78, Low: 25/15) │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│        Stage 4: Strategic Governance & Multi-Format Deliverables       │
│  - 4 Optiv Model MSA Contract Clauses (ZDR, Sub-processors, HITL)      │
│  - Regulatory crosswalk (OCC 2023-17, Fed SR 11-7, GLBA, ISO 42001)    │
│  - Tailored 5-question technical due-diligence questionnaires          │
│  - Populated template export (Meridian_Vendor_Input_Completed.xlsx)    │
│  - Executive presentation deck (Meridian_AI_Assessment_Case_Study_1)  │
│  - SQLite audit persistence (data/meridian.db)                         │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Key Capabilities

### 1. Dual-Engine Local AI Architecture (`src/local_llm.py`)
To prevent data leakage of confidential bank architectures and customer transaction scopes, the platform runs **100% locally with zero cloud dependencies**:
* **Local Ollama Integration:** Automatically detects and communicates with local Ollama endpoints (`http://localhost:11434`) running open-source models (`llama3`, `mistral`, `qwen2.5`) via JSON mode.
* **Built-in Local Semantic Reasoner:** Runs zero-latency, deterministic semantic evaluation completely offline on any machine without requiring a GPU or API keys.
* **Extensible Adapter Pattern:** Abstract base classes enable drop-in expansion for `llama.cpp`, HuggingFace pipelines, or LM Studio endpoints.
* **Optional Cloud API:** Supports Google Gemini and OpenAI GPT-4o-mini via explicit API keys when cloud execution is permitted.

### 2. Resolving the "All 6 Vendors Unrated" Deadlock
Standard public-web scraping leaves 100% of banking vendors unrated because banks do not publish proprietary ledger integrations on unauthenticated websites. The Cognitive TPRM engine analyzes underlying architecture stacks, sub-processor networks, and service criticality to produce an actionable risk portfolio:

| Vendor ID & Name | Core Banking Service | Risk Level | Status | Strategic Finding & Provenance |
| :--- | :--- | :--- | :--- | :--- |
| **V-001: AutomWorx** | Batch Scheduling & Workload Automation | **High** | `conditional_exposure` | **Underlying Platform AI:** Runs Broadcom Automic V26 with `Automation.AI` and MCP connectors. Privileged batch service accounts exposed to prompt injection risks via error logs. |
| **V-002: Fiserv, Inc.** | DNA Core Banking Platform | **Critical** | `confirmed_runtime_ai` | **Confirmed Core Ledger AI:** Deployed **agentOS** in strategic partnership with OpenAI and Azure OpenAI. 1.4M customer records and live ledger balances processed in autonomous agent pipelines. |
| **V-003: FSSI** | Statement Outsourcing & Print/Mail | **Low** | `deterministic_baseline` | **Deterministic System:** High traditional data sensitivity (SSNs, balances), but processed strictly via deterministic composition software without AI models. |
| **V-004: Terrapin Technologies** | Wealth Management Reporting | **Low** | `marketing_fluff_cleared` | **Marketing Cleared:** Public whitepapers emphasize "AI-Ready Data Foundations". Cognitive TPRM verifies this is marketing thought leadership—delivered software is deterministic relational ETL. |
| **V-005: BNY** | Real-Time Payments (RTP) Transmission | **High** | `high_ai_exposure` | **Algorithmic Payment Routing:** Proprietary Eliza AI platform and OpenAI ChatGPT Enterprise integrated with real-time ML routing switches. |
| **V-006: The Clearing House (TCH)** | ACH & RTP Clearing Infrastructure | **Low** | `deterministic_baseline` | **Core Rail Isolated:** Regulated SIFMU. Live settlement messages in transit follow cryptographic ISO 20022 rules without GenAI. AI research is isolated to fraud panels. |

### 3. Verifiable Threat Vector Evidence Provenance
Every threat vector generated in the AI Audit Dossier and exported to Meridian’s workbook cites verifiable technical documentation, corporate disclosures, or SEC filings:
* **Fiserv:** *Fiserv Corporate Newsroom — agentOS Launch in Partnership with OpenAI* & *Microsoft Azure OpenAI Service Banking Disclosures*
* **BNY:** *BNY Real-Time Payments (RTP) Innovation Whitepaper* & *BNY Eliza Cognitive Platform Press Briefings*
* **AutomWorx:** *Broadcom Automic Automation V26 Architecture Documentation* & *Automic Automation.AI Technical Guide*
* **Terrapin:** *Terrapin Technologies 'AI-Ready Data Foundations' Whitepaper* & *SEC Form ADV Filings*
* **The Clearing House:** *The Clearing House RTP Operating Rules* & *SIFMU Regulatory Oversight Filings*

### 4. Strategic Governance & Model Contract Addendum (`src/governance.py`)
Provides Meridian's procurement and legal counsel with enforceable contract terms and regulatory alignment:
* **4 Optiv Model MSA AI Clauses:**
  1. *Zero Data Retention (ZDR) & Model Training Prohibition Warranty*
  2. *Mandatory 60-Day Prior Written Sub-Processor Notice & Objection Rights*
  3. *Human-in-the-Loop (HITL) Thresholds for Core Banking Transactions & Batch Schedules*
  4. *Continuous AI Audit Rights, Model Cards & 48-Hour Vulnerability Disclosures*
* **Financial Regulatory Crosswalk:**
  * **OCC Bulletin 2023-17 / FFIEC:** Interagency Third-Party Risk Management Guidance
  * **Federal Reserve SR 11-7:** Supervisory Guidance on Model Risk Management (MRM)
  * **GLBA Safeguards Rule (16 CFR Part 314):** Protection of Customer Non-Public Personal Information (NPI)
  * **ISO/IEC 42001:2023:** Artificial Intelligence Management System (AIMS)
* **NIST AI RMF 1.0 Sub-function Mapping:** Categorized across Govern, Map, Measure, and Manage.

---

## Installation & Setup

### Prerequisites
* Python 3.10 or higher
* Git

### Step-by-Step Installation

```bash
# Clone repository
git clone https://github.com/12sskk/optiv-meridian-software.git
cd optiv-meridian-software

# Create and activate virtual environment
python -m venv .venv

# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# Linux / macOS:
source .venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

---

## Running the Application

Launch the interactive analyst workbench:

```bash
streamlit run app.py
```

### Guided Walkthrough:
1. **Load Inventory:** Click **Load Case Study Workbook** or upload `Meridian_Vendor_Input.xlsx`, then click **1. Load Vendors**. Notice that row 5 (`V-000` Larkspur example) is preserved untouched.
2. **Heuristic Screening:** Click **2. Run Heuristic Screening**. Observe that without active page scraping, vendors remain safely unrated under conservative audit principles.
3. **Cognitive TPRM:** Select the desired engine mode in the sidebar (default: *Local LLM Auto* or *Built-in Reasoner*), then click **3. Run Cognitive TPRM**. Watch the unrated deadlock resolve into an executive risk distribution.
4. **Vendor Deep-Dive (Dossier):** Navigate to the **Vendor Deep-Dive (Dossier)** tab to inspect Fiserv, AutomWorx, or Terrapin. Review the NIST AI RMF mapping, threat citations, and copy the tailored 5-question CISO questionnaire.
5. **Governance & Legal Clauses:** Review the 4 model contract clauses and download the Optiv AI Governance Addendum in Markdown.
6. **Export Deliverable:** Click **4. Export & Save DB** to write all updates back into Meridian's template and persist findings to SQLite.

---

## CLI Utilities & Deliverable Generation

The repository includes standalone scripts to regenerate completed deliverables on demand:

```bash
# Populate completed Meridian student workbook (exports/Meridian_Vendor_Input_Completed.xlsx)
python populate_completed_workbook.py

# Generate Optiv-branded 10-slide executive presentation deck (exports/Meridian_AI_Assessment_Case_Study_1.pptx)
python generate_presentation_deck.py
```

---

## Automated Test Suite

The test suite validates data integrity, template fidelity, local LLM failover, and risk scoring:

```bash
# Run all unit and integration tests
pytest -v
```

### Coverage Highlights:
* `test_cognitive_synthesis_resolves_all_unrated_trap`: Verifies that cognitive evaluation resolves all 6 unrated vendors without leaving any as unrated.
* `test_evaluate_vendor_portfolio_mode_and_enable_toggle`: Verifies that turning off cognitive synthesis returns conservative heuristic baselines.
* `test_meridian_export_populates_only_student_fields_and_preserves_template`: Confirms that only assigned student columns (L–P) are modified and the `V-000` worked example is untouched.
* `test_ollama_graceful_fallback_when_offline`: Confirms automatic fallback from an unreachable Ollama port to the offline Local Semantic Reasoner.
* `test_local_reasoner_terrapin_marketing_fluff`: Verifies that marketing buzz is cleared as a false positive.
* `test_governance_clauses_and_regulatory_crosswalk`: Verifies the 4 model MSA clauses and OCC/Fed crosswalk integrity.

**Result: 42 passed (100% pass rate).**

---

## Repository Structure

```
├── app.py                             # Streamlit interactive analyst workbench
├── CHANGES.md                         # Detailed record of enhancements and bug fixes
├── generate_presentation_deck.py      # Automated PowerPoint presentation deck generator
├── populate_completed_workbook.py     # Standalone script populating completed client workbook
├── requirements.txt                   # Production dependencies (openpyxl, streamlit, python-pptx, etc.)
├── exports/                           # Generated client deliverables
│   ├── Meridian_AI_Assessment_Case_Study_1.pptx
│   └── Meridian_Vendor_Input_Completed.xlsx
├── supporting material/               # Engagement inputs and client templates
│   └── Meridian_Vendor_Input.xlsx     # Original Meridian input template (Row 5 preserved)
├── src/                               # Core TPRM pipeline modules
│   ├── __init__.py
│   ├── classify.py                    # Regex keyword pattern matcher and sentence segmenter
│   ├── db.py                          # SQLite persistence and audit trail logging
│   ├── excel_handler.py               # Template-preserving Excel parser and cell updater
│   ├── excel_io.py                    # Generic spreadsheet fallback parser
│   ├── export.py                      # Multi-sheet generic Excel exporter
│   ├── extract.py                     # Ethical HTML extractor and text normalizer
│   ├── governance.py                  # 4 Model MSA clauses and banking regulatory crosswalk
│   ├── llm_analysis.py                # Cloud LLM gateway and benchmark dossier mappings
│   ├── local_llm.py                   # Local Ollama adapter and Local Semantic Reasoner
│   ├── logging_config.py              # Structured logging configuration
│   ├── meridian_export.py             # Maps risk findings into Meridian template columns L-P
│   ├── models.py                      # Strongly-typed dataclasses (VendorRecord, RiskResult, etc.)
│   ├── osint.py                       # OSINT candidate path and search query generator
│   ├── risk.py                        # Dual-mode risk engine (Conservative Heuristic vs Cognitive)
│   └── scoring.py                     # Business criticality heuristic scoring engine
└── tests/                             # Comprehensive automated pytest test suite
    ├── conftest.py
    ├── test_classify.py
    ├── test_cognitive_risk_portfolio.py
    ├── test_db.py
    ├── test_excel_handler.py
    ├── test_excel_io.py
    ├── test_export.py
    ├── test_extract.py
    ├── test_governance.py
    ├── test_local_llm.py
    ├── test_meridian_export.py
    ├── test_meridian_integration.py
    ├── test_osint.py
    ├── test_risk.py
    └── test_scoring.py
```

---

## Important Assessment Boundaries & Ethical Guidance

1. **Candidate URLs are Not Evidence:** Hypothesized URLs and search queries generated during OSINT discovery are inspection targets, not proof of AI presence or absence.
2. **Page Scraping Ethics:** Web scraping is disabled by default. Automated requests should only be sent to public sites that explicitly permit automated retrieval.
3. **Audit Opinions Require Human Review:** All outputs—heuristic drafts or cognitive synthesis—are decision-support recommendations formulated for CISO and legal review, not autonomous audit sign-offs.
4. **Client Template Integrity:** The fictional reference example (`V-000` Larkspur Servicing Group Ltd) embedded in row 5 of the original workbook is preserved untouched in accordance with engagement instructions.
