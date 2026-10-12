# Meridian Financial: Third-Party AI Risk Assessment
## Optiv Cyber Strategy Consulting — Case Study 01 Comprehensive Deliverable Guide

---

## 1. Executive Deliverables Checklist

This repository contains everything required to complete and present **Case Study 1: Vendor AI Usage Analysis** to Optiv and Meridian stakeholders:

| Requirement (PDF Slide 5) | Deliverable Artifact | Status & Location |
| :--- | :--- | :--- |
| **01. Functional Design Diagram** | End-to-end data flow from intake & OSINT to risk classification | Slide 3 of [.pptx](file:///c:/Users/sskkt/Documents/Optiv/exports/Meridian_AI_Assessment_Case_Study_1.pptx) & Architecture Guide |
| **02. Technical Architecture Diagram** | Detailed subsystem architecture (UI, Engines, Parsers, SQLite) | Slide 4 of [.pptx](file:///c:/Users/sskkt/Documents/Optiv/exports/Meridian_AI_Assessment_Case_Study_1.pptx) |
| **03. Source Strategy & Weighting** | 4-tier evidentiary weight hierarchy & depth matrix | Slide 5 of [.pptx](file:///c:/Users/sskkt/Documents/Optiv/exports/Meridian_AI_Assessment_Case_Study_1.pptx) |
| **04. Criticality Ratings & Rubric** | Mathematical scoring formula (35/30/20/15) + vendor tiers | Slide 6 of [.pptx](file:///c:/Users/sskkt/Documents/Optiv/exports/Meridian_AI_Assessment_Case_Study_1.pptx) |
| **05. Completed Vendor Inventory** | Offline Excel file with Columns L–P completed for V-001 to V-006 | [Meridian_Vendor_Input_Completed.xlsx](file:///c:/Users/sskkt/Documents/Optiv/exports/Meridian_Vendor_Input_Completed.xlsx) |
| **06. Working Demonstration** | Interactive Streamlit Workbench with template preservation | Run `streamlit run app.py` |
| **07. PowerPoint Deck (.pptx)** | 10-slide Optiv-branded 16:9 presentation deck | [Meridian_AI_Assessment_Case_Study_1.pptx](file:///c:/Users/sskkt/Documents/Optiv/exports/Meridian_AI_Assessment_Case_Study_1.pptx) |

---

## 2. 10–15 Minute Stakeholder Walkthrough Speaking Script

### Minute 0–2: Introduction & Executive Problem Statement (Slides 1–2)
> *"Good morning, everyone. Today we are presenting our methodology and findings for Case Study 1: Third-Party AI Usage Analysis for Meridian Financial.*
>
> *Meridian operates in a highly regulated banking environment, relying on external software across core platforms, payment clearing, and batch automation. The fundamental challenge we are tackling is **Shadow AI in the supply chain**: commercial software vendors are embedding large language models and autonomous agents into their platforms without formally notifying enterprise risk teams.*
>
> *Our mandate was to design an evidence-driven, repeatable Open-Source Intelligence (OSINT) framework that separates genuine AI execution from marketing fluff, quantifies residual security risks, and produces defensible audit findings."*

### Minute 3–5: Functional Design & System Architecture (Slides 3–4)
> *"To ensure repeatability, we engineered a dedicated 4-stage pipeline:*
> 1. *First, **Template-Aware Ingestion**: Our engine recognizes non-standard spreadsheet headers, extracts vendor attributes, isolates the fictional Larkspur worked example, and derives a defensible criticality score.*
> 2. *Second, **Proportional OSINT Discovery**: We generate targeted URL paths and Dork queries based on criticality, searching trust centers, SEC filings, and technical documentation.*
> 3. *Third, **Dual-Gate Heuristic Classification**: We don't rely on simple keyword counts. Our classifier enforces a dual-condition rule: an AI sub-processor is only flagged if an AI model provider AND an explicit processing cue appear within the exact same sentence.*
> 4. *Fourth, **Conservative Risk Synthesis**: If no verified AI claim exists, we refuse to guess; we classify risk as 'Not Rated / Insufficient Evidence' rather than falsely assuming zero risk.*
>
> *The technical architecture is built in Python, backed by a SQLite relational audit store, openpyxl for non-destructive Excel manipulation, and Streamlit for interactive analyst workflows."*

### Minute 6–8: OSINT Source Strategy & Criticality Model (Slides 5–6)
> *"A cornerstone of our methodology is the **Evidentiary Hierarchy Matrix**.*
> *We categorize intelligence across 4 tiers:*
> - *Tier 1: Legal and contractual disclosures (SEC 10-K, Trust Centers, sub-processor registries) carrying high evidentiary weight (0.85–1.0).*
> - *Tier 2: Technical architecture docs and API references (0.70–0.85).*
> - *Tier 3: Engineering job postings and patent filings (0.45–0.65).*
> - *Tier 4: Marketing press releases and social posts (0.20–0.40).*
>
> *Crucially, Tier 4 marketing claims are treated strictly as review leads—never as sole proof of AI risk.*
>
> *Our criticality rubric derives scores mathematically: 35% Data Sensitivity, 30% Operational Dependency, 20% Regulatory Exposure, and 15% Data Volume. This classified Fiserv (DNA) and The Clearing House as Critical; BNY, AutomWorx, and FSSI as High; and Terrapin Technologies as Medium."*

### Minute 9–12: Portfolio Findings & Deep Dive (Slides 7–8)
> *"Looking at the 6 vendors in Meridian's portfolio:*
> - *For **Fiserv DNA (Critical)**: We confirmed active AI adoption. Fiserv recently launched 'agentOS' in partnership with OpenAI, alongside Microsoft Azure OpenAI integration. With 1.4 million customer records and 240 million transactions at stake, this represents a **Critical AI Risk**. We risk confidential financial data leaking into foundation model logs or being used for fine-tuning without explicit consent.*
> - *For **BNY (High)**: We confirmed AI in production. BNY has deployed its enterprise platform 'Eliza' in collaboration with OpenAI, and uses machine learning for real-time payment routing and anomaly detection across RTP rails. This is rated **High AI Risk**; we must verify payment metadata isolation.*
> - *For **AutomWorx (High)**: Findings are **Inconclusive**. While Broadcom Automic V26 features 'Automation.AI' and Model Context Protocol (MCP) servers, AutomWorx has not publicly confirmed if its consultants deploy LLMs in Meridian's batch environment.*
> - *Conversely, for **FSSI, Terrapin, and The Clearing House**, our research revealed **No AI in core services**. For example, Terrapin markets 'AI-ready data', but the actual platform is deterministic ETL. We deliberately rate their AI security risk as Low or None Identified, demonstrating our tool's ability to resist marketing false positives."*

### Minute 13–15: Governance Safeguards & Live Tool Demonstration (Slides 9–10)
> *"To mitigate these risks, we have drafted 4 Model AI Contract Clauses for Meridian:*
> 1. *Zero Model Training warranty,*
> 2. *Mandatory 60-day AI sub-processor notification,*
> 3. *Human-in-the-loop thresholds for financial decisions, and*
> 4. *Annual SOC 2 Type II with AI Trust Services Criteria.*
>
> *I will now conclude by briefly demonstrating the live Streamlit tool, showing how it ingests the template, executes criticality scoring, and exports back to the official Meridian Excel sheet without breaking formatting. Thank you, and I welcome your questions."*

---

## 3. Stakeholder Q&A Defense Guide

### Question 1: *"Why shouldn't Meridian simply implement a blanket ban on vendors using AI?"*
**Answer:**
> *"A blanket ban is practically unenforcable and commercially counterproductive. Major enterprise vendors like Fiserv, Microsoft, and BNY are embedding AI at the platform architecture layer for essential features like real-time fraud detection and anomaly screening. A blanket prohibition would force Meridian onto deprecated legacy platforms. Instead, our framework enables **controlled, auditable adoption**: establishing strict zero-retention agreements, data boundaries, and sub-processor transparency while maintaining operational competitiveness."*

### Question 2: *"How does your tool prevent false positives from vendors who boast about AI in marketing but don't actually use it?"*
**Answer:**
> *"We built two structural safeguards into the code: First, our **Evidentiary Hierarchy** assigns marketing commentary a low weight (0.25) and treats it only as a candidate lead, never a finding. Second, in `classify.py` and `risk.py`, an AI risk score is mathematically blocked unless an explicit AI capability claim is verified in technical or trust documentation. A vendor like Terrapin Technologies who blogs about 'AI-ready data' is flagged by human-in-the-loop screening as a non-user, preventing false alarms."*

### Question 3: *"Why did you score The Clearing House as Critical Criticality but Low AI Security Risk?"*
**Answer:**
> *"This illustrates the critical separation between **Business Criticality** and **AI-Specific Risk**. Business Criticality reflects the catastrophic impact if The Clearing House fails—it is the national clearing backbone for ACH and RTP. However, our OSINT analysis proved that TCH's core settlement engine remains deterministic ISO 20022 message routing. Because they do not route live payments through generative LLMs or unvalidated external model providers, the AI-specific risk to Meridian is Low."*

---

## 4. Model AI Governance Contract Clauses

These 4 clauses can be directly handed to Meridian's Legal and Procurement teams for insertion into Master Services Agreements (MSAs):

### Clause 1: Prohibition on Model Training & Data Retention
> *"Vendor expressly warrants and agrees that neither Customer Data, transaction metadata, nor Customer Confidential Information shall be utilized, retained, processed, or made available for the training, fine-tuning, alignment, or improvement of any machine learning, deep learning, or large language model (LLM), whether owned by Vendor or any third party, without Customer’s prior express written authorization."*

### Clause 2: Disclosure of AI Sub-processors & Foundation Providers
> *"Vendor shall maintain an accurate, up-to-date register of all artificial intelligence infrastructure providers, foundation model hosts, and AI sub-processors (including but not limited to OpenAI, Microsoft Azure, Google Cloud, and Amazon Web Services). Vendor shall provide Customer with no less than sixty (60) days advance written notice prior to engaging any new AI sub-processor that will access, ingest, or process Customer Data, and Customer reserves the absolute right to object or terminate the relevant Service without penalty."*

### Clause 3: Human Oversight & Autonomous Agent Guardrails
> *"Where Vendor delivers capabilities leveraging agentic workflows or automated AI decisioning, Vendor shall ensure that robust human-in-the-loop (HITL) checkpoints are enforced for any action that affects credit decisions, account status modifications, funds disbursement, regulatory reporting, or batch scheduling changes. Vendor warrants that automated model outputs shall not bypass established dual-authorization controls."*

### Clause 4: AI Auditability, Model Risk Management & Red-Teaming
> *"Vendor shall provide Customer annually, upon request, with independent third-party attestations covering its AI estate, including SOC 2 Type II reports addressing AI Trust Services Criteria, ISO/IEC 42001 certification, and summaries of adversarial red-teaming (prompt injection and data exfiltration testing). Vendor shall notify Customer within forty-eight (48) hours of detecting any data leakage, model poisoning, or unauthorized prompt extraction involving Customer Data."*

---

## 5. Verification & Test Suite Summary

All modules have been tested and verified locally:
- **Test suite status**: `30 passed in 1.27s` (`python -m pytest -q`)
- **Excel Template Export**: Verified against openpyxl; preserves template formatting, formulas, and Row 4 header alignments.
- **PowerPoint Presentation**: 10 slides, 16:9 widescreen layout, Optiv navy/orange branding, formatted with native tables and process cards.
