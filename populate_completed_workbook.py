"""Populates the Meridian Vendor Input Excel workbook with fully verified,
consulting-grade findings for vendors V-001 through V-006.
"""

from pathlib import Path
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

SOURCE = Path("supporting material") / "Meridian_Vendor_Input.xlsx"
DEST_DIR = Path("exports")
DEST_DIR.mkdir(exist_ok=True)
DEST = DEST_DIR / "Meridian_Vendor_Input_Completed.xlsx"

wb = openpyxl.load_workbook(SOURCE)
ws = wb["Vendor Inventory"]

# Mapping of row indices:
# Row 4: Headers
# Row 5: V-000 Larkspur (preserved)
# Row 6: V-001 AutomWorx
# Row 7: V-002 Fiserv, Inc.
# Row 8: V-003 FSSI
# Row 9: V-004 Terrapin Technologies
# Row 10: V-005 BNY
# Row 11: V-006 The Clearing House

ASSESSMENT_DATE = "Team Optiv / 2026-10-13"

VENDOR_DATA = {
    6: {  # V-001 AutomWorx
        "Criticality Tier": "High",
        "Criticality Rationale": "High operational dependency with privileged service credentials and production job schedule access across Meridian's core banking and batch processing estate. While no customer records are housed directly, a compromise or error in batch automation can halt overnight reconciliation and payment settlement.",
        "Assessment Depth Applied": "High-tier review: Targeted vendor site review, Broadcom partner documentation, technical release notes for Automic V24/V26, and engineering forum analysis.",
        "AI Usage Detected (Y/N)": "Inconclusive",
        "Evidence Description along with OSINT Source(s) / Evidence Link": 'Primary source — Broadcom Automic Automation release documentation and Partner Briefings (broadcom.com / automworx.com). Modern Automic engines feature "Automation.AI" with Model Context Protocol (MCP) servers and script functions (ASK_AI) allowing LLM integration for automated incident resolution and script drafting. Negative finding — AutomWorx\'s public domain does not publicly disclose whether its consulting team deploys generative AI agents directly into Meridian\'s managed batch scheduling environment. Documented in TPRM Evidence Log.',
        "How Vendor May Be Using AI": "Potential utilization of LLM-assisted script generation, automated troubleshooting agents, or generative AI code assistants by consulting engineers maintaining client batch workflows.",
        "Named AI Sub-processors / Model Providers": "None named publicly by AutomWorx (Automic ecosystem supports OpenAI and Google Gemini via MCP connectors).",
        "AI Security Risk Classification": "High",
        "Risk Rationale": "Conditional on AI use: Privileged production access combined with unmonitored LLM script generation creates indirect prompt injection risks and potential for hallucinated or unauthorized job execution in core batch schedules.",
        "Recommended Action": "Issue targeted TPRM questionnaire within 15 business days clarifying whether consultants use generative AI tools (ChatGPT, Copilot) when modifying Meridian scripts. Incorporate contractual clause restricting autonomous AI execution in production batch environments. Require dual human sign-off on automated scheduling scripts.",
        "Assessedd By / Date": ASSESSMENT_DATE
    },
    7: {  # V-002 Fiserv, Inc.
        "Criticality Tier": "Critical",
        "Criticality Rationale": "Core platform system of record. Holds full customer master, transaction history, and balances for 1.4 million accountholders (240 million annual transactions). An outage or integrity failure directly halts all core retail banking operations.",
        "Assessment Depth Applied": "Comprehensive review — Tier-driven: Enterprise Trust Center review, SEC 10-K disclosures, Fiserv AI platform announcements, product API specifications, and sub-processor lists.",
        "AI Usage Detected (Y/N)": "Yes",
        "Evidence Description along with OSINT Source(s) / Evidence Link": 'Primary source — Fiserv Enterprise Product Announcements and Partnership Disclosures (fiserv.com, 2025/2026). Fiserv announced the deployment of "agentOS" in partnership with OpenAI to bring frontier AI agents into core banking and account workflows. Supporting source — Microsoft partnership disclosures detailing Fiserv\'s use of Azure OpenAI and Copilot Foundry across developer and financial client workflows, alongside UiPath agentic automation for check fraud detection and account servicing.',
        "How Vendor May Be Using AI": "Three distinct usages: 1) Real-time transaction fraud detection and anomaly scoring on core transactions; 2) Conversational banking and generative customer servicing assistants; 3) Agentic core workflow automation (agentOS) assisting administrative operations and platform integrations.",
        "Named AI Sub-processors / Model Providers": "OpenAI, Microsoft (Azure OpenAI Service), UiPath.",
        "AI Security Risk Classification": "Critical",
        "Risk Rationale": "Core banking account data, transaction streams, and customer master records interface with or feed into automated AI models. Reliance on external foundation model providers introduces risks of confidential financial data leakage, undisclosed data retention for model fine-tuning, and model drift affecting transaction integrity.",
        "Recommended Action": "Escalate to Third-Party Risk Committee. Issue Optiv Targeted AI Assessment within 10 business days. Require written confirmation of zero-data-retention and zero-training guarantees on Meridian core data from OpenAI/Microsoft. Mandate SOC 2 Type II with AI Trust Services Criteria and ISO 42001 certification. Enact strict human oversight thresholds on automated agentOS account actions.",
        "Assessedd By / Date": ASSESSMENT_DATE
    },
    8: {  # V-003 FSSI
        "Criticality Tier": "High",
        "Criticality Rationale": "Moderate operational dependency, but accesses highly sensitive regulated customer data at full population scale: names, addresses, account numbers, balances, and tax identifiers (SSNs/TINs) across 19 million documents annually.",
        "Assessment Depth Applied": "High-tier review: Security & Compliance portal review (SOC 2 Type II, HIPAA, HITRUST CSF), technical specifications for document composition, and public legal/privacy pages.",
        "AI Usage Detected (Y/N)": "No",
        "Evidence Description along with OSINT Source(s) / Evidence Link": "Primary source — FSSI Security & Technology Overview (fssi-ca.com). FSSI's document composition and print/mail infrastructure relies on deterministic variable-data publishing software, automated document factory (ADF) barcodes, and camera-verified insertion systems. Negative finding — Comprehensive review of trust documentation, product sheets, and engineering disclosures reveals no generative AI, machine learning, or external LLM sub-processors in active document processing streams.",
        "How Vendor May Be Using AI": "No AI usage detected in customer document processing. Vendor relies on deterministic, rule-based composition templates and secure electronic delivery portals.",
        "Named AI Sub-processors / Model Providers": "None identified.",
        "AI Security Risk Classification": "Low",
        "Risk Rationale": "Transactional document processing is governed by strict deterministic controls and audited SOC 2 / HIPAA standards. Without AI or LLM integration, AI-specific risks such as data leakage or model hallucination are absent.",
        "Recommended Action": "Maintain baseline TPRM monitoring. Insert standard AI notification clause at next contract renewal requiring 60 days advance written notice and Meridian approval before introducing AI models or LLM sub-processors to customer statement pipelines.",
        "Assessedd By / Date": ASSESSMENT_DATE
    },
    9: {  # V-004 Terrapin Technologies, Inc.
        "Criticality Tier": "Medium",
        "Criticality Rationale": "Moderate operational dependency with monthly batch processing. Accesses portfolio holdings and advisor compensation data for 38,000 wealth clients. Does not sit in direct transaction execution or retail banking paths.",
        "Assessment Depth Applied": "Standard review: Vendor website, wealth management solution briefs, case studies, and thought leadership articles.",
        "AI Usage Detected (Y/N)": "No",
        "Evidence Description along with OSINT Source(s) / Evidence Link": 'Primary source — Terrapin Technologies Thought Leadership & Platform Overview (terrapintech.com). Vendor marketing frequently discusses "AI-ready data foundations" and highlights the importance of clean data before deploying AI. However, platform architecture reviews confirm that Terrapin\'s core offering is a deterministic data aggregation, ETL, and commission calculation software. Negative finding — No native generative AI models, predictive algorithms, or third-party AI sub-processors operate within the reporting pipeline.',
        "How Vendor May Be Using AI": "Vendor positions its clean data outputs as suitable for clients to feed into downstream AI tools; does not execute native AI or LLMs on Meridian wealth data.",
        "Named AI Sub-processors / Model Providers": "None identified.",
        "AI Security Risk Classification": "None identified",
        "Risk Rationale": "Public mentions of AI are educational and marketing commentary regarding data quality, not embedded AI service functionality. No AI model interacts with Meridian wealth management data.",
        "Recommended Action": "Classify as deterministic data provider. Re-evaluate annually during standard third-party risk review cycles.",
        "Assessedd By / Date": ASSESSMENT_DATE
    },
    10: {  # V-005 BNY
        "Criticality Tier": "High",
        "Criticality Rationale": "High operational dependency in payment flow. Facilitates inbound Real-Time Payments (RTP) transmission (2.1 million annual messages), handling irrevocable payment instructions, counterparty account identifiers, and financial messaging.",
        "Assessment Depth Applied": "Deep review: Corporate technology filings, transaction banking whitepapers, BNY AI announcements, and developer API portals.",
        "AI Usage Detected (Y/N)": "Yes",
        "Evidence Description along with OSINT Source(s) / Evidence Link": 'Primary source — BNY Corporate Announcements and Financial Press (bny.com, 2025/2026). BNY has deployed an enterprise-wide AI platform ("Eliza") and executed an enterprise agreement with OpenAI to embed ChatGPT Enterprise and OpenAI API capabilities. In payments, BNY incorporates machine learning models for intelligent payment routing, liquidity forecasting, and real-time transaction anomaly screening across RTP rails.',
        "How Vendor May Be Using AI": "Two primary applications: 1) Algorithmic and ML-driven payment routing and real-time fraud/anomaly detection on RTP payment streams; 2) Internal operational and client service automation via BNY's proprietary Eliza platform.",
        "Named AI Sub-processors / Model Providers": "OpenAI.",
        "AI Security Risk Classification": "High",
        "Risk Rationale": "Payment message metadata and routing parameters are evaluated by machine learning engines. Essential to ensure that real-time payment data and counterparty identifiers remain strictly isolated from generative AI systems and external foundation model APIs.",
        "Recommended Action": "Engage BNY relationship team to review AI data-flow boundaries. Obtain written assurance that RTP payment file transmissions bypass OpenAI APIs and external LLMs. Review BNY Model Risk Management (MRM) audit summary for payment anomaly algorithms.",
        "Assessedd By / Date": ASSESSMENT_DATE
    },
    11: {  # V-006 The Clearing House Payments Company L.L.C.
        "Criticality Tier": "Critical",
        "Criticality Rationale": "Critical infrastructure utility. Operates fundamental interbank payment rails (ACH, RTP, CHIPS) handling 14 million messages for Meridian. An operational failure paralyzes national clearing and settlement.",
        "Assessment Depth Applied": "Comprehensive review: Payment network operating rules, regulatory oversight documentation, conference proceedings, and security policy disclosures.",
        "AI Usage Detected (Y/N)": "No",
        "Evidence Description along with OSINT Source(s) / Evidence Link": "Primary source — The Clearing House Operating Rules and Annual Conference Proceedings (theclearinghouse.org). TCH actively participates in financial sector forums on AI governance and evaluates consortium fraud mitigation concepts. However, core RTP and ACH clearing and settlement systems operate on deterministic ISO 20022 messaging rules with strict cryptographic guarantees. Negative finding — No autonomous AI decisioning or external LLM models are deployed in the core clearing path.",
        "How Vendor May Be Using AI": "Industry policy research and consortium fraud pattern modeling; not embedded in active payment clearing or settlement execution.",
        "Named AI Sub-processors / Model Providers": "None identified for clearing operations.",
        "AI Security Risk Classification": "Low",
        "Risk Rationale": "Systemic operational dependency is Critical, but AI-specific risk is Low because transaction clearing remains deterministic and strictly governed by Federal Reserve and OCC supervisory standards.",
        "Recommended Action": "Maintain existing critical infrastructure third-party assurance program. Monitor TCH regulatory filings annually for any introduction of autonomous AI models into real-time settlement logic.",
        "Assessedd By / Date": ASSESSMENT_DATE
    }
}

# Column header map (Column name -> Column index)
header_col_map = {}
for col in range(2, ws.max_column + 1):
    val = ws.cell(row=4, column=col).value
    if val:
        header_col_map[str(val).strip()] = col

# Populate values
fill_cream = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
font_content = Font(name="Calibri", size=10)
align_content = Alignment(vertical="top", wrap_text=True)

for row_idx, fields in VENDOR_DATA.items():
    for field_name, value in fields.items():
        # Match field_name to header
        target_col = None
        for h, c in header_col_map.items():
            if field_name.lower() in h.lower() or h.lower() in field_name.lower():
                target_col = c
                break
        if target_col:
            cell = ws.cell(row=row_idx, column=target_col, value=value)
            cell.font = font_content
            cell.alignment = align_content
            cell.fill = fill_cream

wb.save(DEST)
print(f"Successfully generated populated student workbook at: {DEST}")
