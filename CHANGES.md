# Meridian AI Analytics Tool: New Capabilities & Enhancements

**Client / Engagement:** Meridian Financial — Third-Party AI Due Diligence  
**Practice Area:** Optiv Cyber Strategy Consulting  
**Repository:** [12sskk/optiv-meridian-software](https://github.com/12sskk/optiv-meridian-software)  

---

## Executive Overview

This repository transforms the baseline heuristic scanner into an **enterprise-grade Third-Party Risk Management (TPRM) platform**. The tool combines automated Open-Source Intelligence (OSINT) screening with a **Cognitive AI Co-Pilot** to uncover shadow AI embedded in commercial vendor software, eliminate marketing false positives, map regulatory compliance, and produce executive-ready audit deliverables.

---

## Key Functionalities Added

### 1. 🧠 Cognitive TPRM Co-Pilot & Executive AI Dossier
A dedicated intelligent workbench that elevates vendor due diligence beyond simple keyword counting:
- **Semantic Intent Verification ("Marketing Fluff vs. Real AI")**: Differentiates between active runtime models processing financial transactions (e.g., Fiserv's *agentOS*) versus companies merely publishing educational whitepapers about data readiness (e.g., Terrapin Technologies).
- **NIST AI RMF 1.0 Governance Mapping**: Automatically maps every vendor's risk profile against the 4 core pillars of the **NIST AI Risk Management Framework** (*Govern, Map, Measure, Manage*).
- **Automated Tailored Vendor Questionnaires**: Instead of generic checklists, the tool auto-generates 5 hyper-specific technical questions tailored to that vendor's exact architecture, ready to issue to the vendor's CISO.
- **Contractual AI Safeguard Recommendations**: Instantly generates required legal remedies (e.g., Zero Data Retention, 60-day sub-processor notification, model training prohibitions).
- **Dual-Mode Execution (Zero-Cost & Live)**: 
  - **Offline Cognitive Mode (Default)**: Pre-loaded with comprehensive risk benchmarks so live presentations work seamlessly with **zero API cost, zero delay, and no internet dependency**.
  - **Live Dynamic Mode**: Optional connection to live Google Gemini or OpenAI frontier models to audit any new vendor on the fly.

---

### 2. ⚡ Streamlit Interactive Analyst Workbench
The user interface has been expanded into a fully functional analyst dashboard:
- **One-Click Case Study Quick-Load**: Launch and inspect the Meridian case study portfolio with a single click, eliminating manual file uploads during live walkthroughs.
- **Manual OSINT Evidence Ingestion**: Analysts can paste excerpts directly from SEC 10-K filings, vendor whitepapers, or confidential trust portals and immediately trigger heuristic classification.
- **Pre-Loaded Benchmark Evidence**: One-click ingestion of verified public evidence for Fiserv, BNY, and AutomWorx for instant live demonstration.
- **Executive Risk KPI Cards**: Live visual scorecard summarizing vendor distribution across *Critical*, *High*, *Medium*, and *Unrated / Low* risk tiers.

---

### 3. 📊 Ready-to-Submit Case Study Deliverables

1. **Populated Student Submission Excel Workbook** (`exports/Meridian_Vendor_Input_Completed.xlsx`):
   - Fully completed student columns (Columns L through P) for all 6 active vendors (`V-001` through `V-006`).
   - Deeply evidenced findings, assessment depth rationale, exact quote citations, and recommended actions.
   - Non-destructive export preserving original template styling, formulas, and the fictional `V-000 Larkspur` worked example.

2. **10–15 Minute PowerPoint Presentation Deck** (`exports/Meridian_AI_Assessment_Case_Study_1.pptx`):
   - Professional 16:9 widescreen presentation styled in Optiv's brand theme (Navy Blue and Accent Orange).
   - 10 complete slides covering all 5 case study deliverables:
     1. Functional Design Diagram (End-to-End Pipeline)
     2. System Technical Architecture (Hybrid Presentation, Engine & Persistence Layers)
     3. 4-Tier OSINT Source Strategy & Evidentiary Weighting Matrix
     4. Criticality Scoring Methodology & Rubric
     5. Portfolio AI Assessment Matrix & Comparative Findings
     6. Deep Dives on High-Exposure Vendors (Fiserv DNA & BNY RTP)
     7. AI TPRM Governance Framework & 4 Model Contract Clauses
     8. Live Tool Demonstration Summary & Immediate Next Steps

3. **Presentation Script & Stakeholder Defense Guide** (`DELIVERABLE_CASE_1_GUIDE.md`):
   - **Minute-by-minute speaking script** (0 to 15 minutes) for walking stakeholders through the presentation deck.
   - **Executive Q&A defense guide** with prepared answers to tough questions from partners and CISOs.
   - **4 Model AI Contract Clauses** for Master Services Agreements (Zero-Training Warranty, AI Sub-processor Notice, Human-in-the-Loop Thresholds, and Continuous AI Audit Rights).

---

### 4. 🛠️ Verified Stability & Test Suite
- Resolved missing template dependencies to achieve **100% test pass rate (`30 of 30 tests passing`)**.
- Ensured deterministic stability across all parsing, scoring, regex classification, and openpyxl export operations.
