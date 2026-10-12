import openpyxl
from pathlib import Path

out_dir = Path("supporting material")
out_dir.mkdir(exist_ok=True)
wb_path = out_dir / "Meridian_Vendor_Input.xlsx"

wb = openpyxl.Workbook()

# Sheet 1: Vendor Inventory
ws1 = wb.active
ws1.title = "Vendor Inventory"

ws1["B2"] = "Meridian — Third-Party Vendor Inventory (Case Study Input)"
ws1["B3"] = "Columns A–K are provided.  Columns L-P (highlighted) are to be completed by the student using OSINT-based analysis of each vendor's public footprint."

headers = [
    "Vendor ID", "Vendor Name", "Vendor Description", "Service / Product Provided", "Category",
    "Public Website", "Business Process Supported", "Operational Dependency",
    "Data Classification Accessed", "Data Volume (annual)", "Criticality Tier",
    "Criticality Rationale", "Assessment Depth Applied", "AI Usage Detected (Y/N)",
    "Evidence Description along with OSINT Source(s) / Evidence Link",
    "How Vendor May Be Using AI", "Named AI Sub-processors / Model Providers",
    "AI Security Risk Classification", "Risk Rationale", "Recommended Action",
    "Assessedd By / Date"
]

for col_idx, h in enumerate(headers, start=2):  # start at col B
    ws1.cell(row=4, column=col_idx, value=h)

rows_data = [
    [
        "V-000",
        "EXAMPLE VENDOR — Larkspur Servicing Group Ltd (fictional, do not edit)",
        "Fictional worked example showing the expected level of detail. Each cell is written so a reviewer who has not seen the underlying research can follow how the conclusion was reached.",
        "Outsourced loan servicing and arrears management. Larkspur operates the borrower contact centre, handles payment arrangements and hardship cases, issues arrears correspondence, and maintains the servicing record that synchronises nightly with Meridian's core lending platform. Staff work within Meridian's servicing system under delegated authority.",
        "Lending Servicing & Collections (onshore, staff-augmented)",
        "www.larkspurservicing.example",
        "Retail lending servicing, arrears management and collections.",
        "High",
        "Borrower names, addresses, dates of birth, loan account numbers, repayment schedules, arrears status, income and expenditure statements, hardship and vulnerability notes (including health-related disclosures), and recorded call audio.",
        "Approximately 240,000 active loan accounts under servicing and around 660,000 borrower interactions per year, of which an estimated 180,000 are recorded voice calls.",
        "Critical",
        "Direct access to customer financial data at full population scale, and an outage removes the primary retail channel.",
        "Full review — tier-driven. A Critical tier calls for the deepest level of work: OSINT sweep across corporate and executive channels, trust-centre and sub-processor review, validation of held attestations, contract and schedule review, and a direct vendor questionnaire. Depth followed from the assigned tier rather than from the volume of material the vendor had published.",
        "Yes",
        "Primary source — LinkedIn post published by the vendor's Chief Executive on 04-02-2026, linkedin.com/posts/larkspur-ceo-ai-assist (retrieved 09-03-2026; screenshot retained, as executive posts may later be amended or withdrawn). The post announces an internally developed application, \"Larkspur Assist\", built by the vendor's own engineering team to support servicing staff. It reports an AI upskilling programme described as reaching more than 400 servicing agents, with staff encouraged to apply the tooling in daily casework. Most materially, it describes automation of service delivery through agents that \"draft borrower correspondence, summarise call history and progress routine arrangements without human handoff\", framed as a reduction in average handling time. Supporting source — vendor careers listing, \"Applied AI Engineer — Servicing Automation\", www.larkspurservicing.example/careers (retrieved 09-03-2026), referencing agent orchestration against live account data and call transcription pipelines. Negative finding — no trust centre, sub-processor register or AI policy page is published on the vendor domain; searches of the domain and of the UK companies register returned nothing further. Entries are recorded in the Evidence Log sheet with retrieval dates and screenshots.",
        "Three usages are indicated. First, an in-house application that summarises borrower records and call content for servicing staff, implying transcription of recorded calls. Second, generative drafting of borrower-facing correspondence. Third, agentic progression of routine payment arrangements described as running without human handoff. The extent of human review over borrower-facing output is undetermined from public material and is carried forward to the vendor questionnaire.",
        "None named — Inconclusive. The post refers to \"leading foundation models\" without identifying a provider. The absence of a published sub-processor register leaves the question unresolved from public sources. Model provider identity, hosting region and retention terms are raised directly with the vendor.",
        "Critical",
        "Sensitive borrower data, including vulnerability disclosures and call audio, appears to be processed by an application that progresses servicing actions with limited human checkpoints. No model provider is identified, leaving onward data flows, retention and training use untraceable, and the contract in force carries no AI clauses. Evidence is drawn from the vendor's own Chief Executive and is treated as reliable on the fact of use, while the data flows remain inferred. Sole-source dependency limits the scope for tolerating the position pending clarification.",
        "Issue a targeted questionnaire within 15 business days covering model provider identity, hosting region, retention, training use of borrower data, call-audio handling, and human review over agent-generated correspondence. Register the vendor on the AI sub-processor inventory with an unresolved-provider flag. Raise AI clauses at the Q4 2026 contract review, addressing training restrictions, sub-processor change notification, human oversight thresholds, and rights to review attestations. Escalate to the Third-Party Risk Committee where confirmation is not received.",
        "Team Kestrel / 09-03-2026"
    ],
    [
        "V-001",
        "AutomWorx",
        "An independent consulting firm specializing in workload automation solutions, including AppWorx, UC4 and Automic software implementation and related consulting services.",
        "Implementation, migration, managed support and modernization of the enterprise workload automation and batch scheduling estate.",
        "Professional Services",
        "www.automworx.com",
        "Batch scheduling across core systems",
        "High",
        "No direct customer data. Privileged access to production job schedules, system configuration and service credentials.",
        "Not applicable",
        None, None, None, None, None, None, None, None, None, None, None
    ],
    [
        "V-002",
        "Fiserv, Inc.",
        "A global financial technology and payments provider delivering banking, merchant acquiring, payment processing, billing and point-of-sale solutions to financial institutions.",
        "The DNA core banking platform, a real-time account processing system supporting customer account management, transaction processing and core banking operations.",
        "Core Platform",
        "www.fiserv.com",
        "Core account processing and servicing",
        "Critical",
        "Full customer master, balances and transactions for 1.4 million customers.",
        "240 million transactions",
        None, None, None, None, None, None, None, None, None, None, None
    ],
    [
        "V-003",
        "Financial Statement Services, Inc. (FSSI)",
        "A document outsourcing and customer communications provider delivering secure print, mail, electronic presentment and digital document delivery for transactional documents.",
        "Produces and distributes printed account statements and IRS tax documents, produces regulatory notices, and hosts the electronic notice platform.",
        "Document and Communications",
        "www.fssi-ca.com",
        "Customer statements and regulatory notices",
        "Moderate",
        "Names, addresses, account numbers, balances and tax identifiers for the entire customer base.",
        "19 million documents",
        None, None, None, None, None, None, None, None, None, None, None
    ],
    [
        "V-004",
        "Terrapin Technologies, Inc.",
        "A financial technology company providing data management, reporting, analytics, compensation administration and compliance solutions for wealth management firms.",
        "A wealth management data solution that consolidates data from multiple sources and supports commission calculations, accounting activities and business volume tracking.",
        "Data and Reporting",
        "www.terrapintech.com",
        "Wealth management reporting and advisor compensation",
        "Moderate",
        "Portfolio holdings, revenue and advisor compensation data for 38,000 wealth clients.",
        "12 monthly cycles",
        None, None, None, None, None, None, None, None, None, None, None
    ],
    [
        "V-005",
        "BNY",
        "A global financial services institution providing transaction banking, payment processing, cash management, treasury and trade finance through its Global Payments & Trade division.",
        "Real Time Payments (RTP) transmission services, including facilitating the transmission of RTP payment files from other financial institutions to Meridian.",
        "Payments",
        "www.bny.com",
        "Inbound real-time payments",
        "High",
        "Payment instructions, counterparty names and account identifiers.",
        "2.1 million messages",
        None, None, None, None, None, None, None, None, None, None, None
    ],
    [
        "V-006",
        "The Clearing House Payments Company L.L.C.",
        "A US-based payments infrastructure provider operating critical financial networks, including EPN, CHIPS, the Image Exchange Network and the RTP network.",
        "Payment network infrastructure services, including the transmission and processing of ACH transactions and Real-Time Payments.",
        "Payments Infrastructure",
        "www.theclearinghouse.org",
        "ACH and RTP clearing and settlement",
        "Critical",
        "Payment messages in transit only.",
        "14 million messages",
        None, None, None, None, None, None, None, None, None, None, None
    ]
]

for row_idx, r in enumerate(rows_data, start=5):
    for col_idx, val in enumerate(r, start=2):
        ws1.cell(row=row_idx, column=col_idx, value=val)

# Sheet 2: Field Guide
ws2 = wb.create_sheet("Field Guide")
ws2.append(["Column", "Provided / Student", "Description"])
guide_rows = [
    ["Vendor ID", "Provided", "Unique internal reference for each vendor."],
    ["Vendor Name", "Provided", "Registered or commonly known vendor name."],
    ["Vendor Description", "Provided", "What the company does as a business, independent of Meridian."],
    ["Service / Product Provided", "Provided", "The service or product delivered to Meridian."],
    ["Category", "Provided", "Vendor type (Core Platform, Payments, Data and Reporting, Document and Communications, Professional Services)."],
    ["Public Website", "Provided", "Primary public domain. Your starting point for OSINT."],
    ["Business Process Supported", "Provided", "The Meridian process that stops or degrades if this vendor fails."],
    ["Operational Dependency", "Provided", "How far Meridian depends on the vendor day to day (Total, High, Moderate, Low)."],
    ["Data Classification Accessed", "Provided", "Highest sensitivity of Meridian data the vendor may access."],
    ["Data Volume (annual)", "Provided", "Scale of what passes through the vendor each year."],
    ["Criticality Tier", "Student", "Your business impact ranking (Critical, High, Medium, Low). This is not given to you; deriving it is part of the exercise."],
    ["Criticality Rationale", "Student", "Why that tier, stated so that another analyst working from the same row would reach the same answer."],
    ["Assessment Depth Applied", "Student", "How far you investigated this vendor. It should follow from the tier you assigned, not from how easy the vendor was to research."],
    ["AI Usage Detected (Y/N)", "Student", "Whether public evidence shows the vendor uses AI in its service (Yes, No, Inconclusive)."],
    ["Evidence Description along with OSINT Source(s) / Evidence Link", "Student", "Extract the exact excerpt that evidences the vendor's AI usage. Include only the specific text that supports the finding and avoid adding interpretations or summaries."],
    ["How Vendor May Be Using AI", "Student", "Summary of how AI appears to be used within the service offering."],
    ["Named AI Sub-processors / Model Providers", "Student", "Any third-party model or AI provider the vendor names publicly."],
    ["AI Security Risk Classification", "Student", "Resulting AI security risk to Meridian (Critical, High, Medium, Low, None identified)."],
    ["Risk Rationale", "Student", "Why that rating, tied to the data involved, the dependency, and the strength of your evidence."],
    ["Recommended Action", "Student", "What Meridian should do next with this vendor."],
    ["Assessedd By / Date", "Student", "Team name and the date the assessment was completed."]
]
for r in guide_rows:
    ws2.append(r)

# Sheet 3: Points to consider
ws3 = wb.create_sheet("Points to consider")
ws3.append(["Point", "Guidance"])
ws3.append(["Which cells you edit", "Cream coloured cells are yours. Blue-grey cells are provided by Optiv: do not edit them, and do not add or remove vendors."])
ws3.append(["Criticality drives depth", "Decide how critical each vendor is first, then decide how much investigation that warrants. We assess the reasoning, not only the rating."])
ws3.append(["Evidence Excerpt", "Extract the exact excerpt that evidences the vendor's AI usage. Include only the specific text that supports the finding and avoid adding interpretations or summaries."])
ws3.append(["Confidentiality", "These are real organisations. Keep your findings inside this exercise: no public repository, no published presentation, and no contact with the vendors."])

wb.save(wb_path)
print("Created:", wb_path)
