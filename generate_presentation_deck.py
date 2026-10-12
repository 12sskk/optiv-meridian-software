"""Generates a professional, Optiv-branded 10-slide PowerPoint presentation
for Case Study 1: Vendor AI Usage Analysis.
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path="exports/Meridian_AI_Assessment_Case_Study_1.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9 widescreen
    prs.slide_height = Inches(7.5)

    # Optiv Brand Colors
    NAVY_DARK = RGBColor(10, 25, 47)      # #0A192F (Dark Navy)
    NAVY_LIGHT = RGBColor(17, 34, 64)     # #112240 (Card Navy)
    ORANGE_OPTIV = RGBColor(255, 94, 20)  # #FF5E14 (Optiv Accent Orange)
    WHITE = RGBColor(255, 255, 255)       # #FFFFFF
    GREY_TEXT = RGBColor(204, 214, 246)   # #CCD6F6
    MUTED_GREY = RGBColor(136, 146, 176)  # #8892B0
    BORDER_GREY = RGBColor(35, 53, 84)

    def set_bg(slide, color=NAVY_DARK):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, title_text, category_text="CASE STUDY 01 • ENGAGEMENT WITH OPTIV"):
        # Category Tracker
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ORANGE_OPTIV
        p_cat.font.name = "Arial"

        # Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE
        p_title.font.name = "Arial"

    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1, NAVY_DARK)

    # Optiv Logo indicator
    logo_box = s1.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(6.0), Inches(0.5))
    tf_l = logo_box.text_frame
    p_l = tf_l.paragraphs[0]
    p_l.text = "Optiv Consulting  |  Cyber Strategy"
    p_l.font.size = Pt(14)
    p_l.font.bold = True
    p_l.font.color.rgb = ORANGE_OPTIV

    # Title box
    tbox = s1.shapes.add_textbox(Inches(0.8), Inches(2.2), Inches(11.5), Inches(2.5))
    tf = tbox.text_frame
    p1 = tf.paragraphs[0]
    p1.text = "Case Study-1: Vendor AI Usage Analysis"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.font.name = "Arial"

    p2 = tf.add_paragraph()
    p2.text = "Evidentiary OSINT Framework & AI Third-Party Risk Management for Meridian Financial"
    p2.font.size = Pt(18)
    p2.font.color.rgb = GREY_TEXT
    p2.space_before = Pt(14)

    # Footer Metadata
    ft_box = s1.shapes.add_textbox(Inches(0.8), Inches(5.8), Inches(11.5), Inches(0.8))
    tf_ft = ft_box.text_frame
    p_ft = tf_ft.paragraphs[0]
    p_ft.text = "Confidential  •  10–15 Minute Executive Walkthrough  •  October 2026"
    p_ft.font.size = Pt(11)
    p_ft.font.color.rgb = MUTED_GREY

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT & CONTEXT
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2, NAVY_DARK)
    add_header(s2, "Executive Context: The Shadow AI Challenge in TPRM")

    # Card 1: Meridian Context
    card1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    card1.fill.solid()
    card1.fill.fore_color.rgb = NAVY_LIGHT
    card1.line.color.rgb = BORDER_GREY
    tf_c1 = card1.text_frame
    tf_c1.word_wrap = True
    tf_c1.margin_left = tf_c1.margin_right = tf_c1.margin_top = Inches(0.4)
    p = tf_c1.paragraphs[0]
    p.text = "Background: Meridian Financial"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ORANGE_OPTIV

    bullets1 = [
        "Global financial institution relying on an extensive vendor ecosystem across core banking, RTP payments, and batch scheduling.",
        "Rapid, unannounced embedding of GenAI & LLMs by commercial software vendors without contractual disclosures.",
        "TPRM teams lack systematic methods to verify whether AI is genuinely active in production services vs. marketing commentary.",
        "Goal: Establish an evidence-driven, repeatable, auditable OSINT assessment methodology."
    ]
    for b in bullets1:
        p = tf_c1.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(13)
        p.font.color.rgb = GREY_TEXT
        p.space_before = Pt(12)

    # Card 2: Core Risks Surfaced
    card2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    card2.fill.solid()
    card2.fill.fore_color.rgb = NAVY_LIGHT
    card2.line.color.rgb = BORDER_GREY
    tf_c2 = card2.text_frame
    tf_c2.word_wrap = True
    tf_c2.margin_left = tf_c2.margin_right = tf_c2.margin_top = Inches(0.4)
    p = tf_c2.paragraphs[0]
    p.text = "Target Third-Party AI Risks"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = WHITE

    bullets2 = [
        "Sensitive Data Ingestion: Exposure of Meridian customer PII, account master records, and transaction logs to LLMs.",
        "Undisclosed AI Sub-processors: Data leakage to unvetted third parties (e.g. OpenAI, Azure OpenAI, Anthropic, Bedrock).",
        "Model Training on Enterprise Data: Retention of financial prompt data for foundation model training without consent.",
        "Uncontrolled Agentic Operations: Automated workflows making consequential financial actions without human-in-the-loop oversight."
    ]
    for b in bullets2:
        p = tf_c2.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(13)
        p.font.color.rgb = GREY_TEXT
        p.space_before = Pt(12)

    # =========================================================================
    # SLIDE 3: FUNCTIONAL DESIGN DIAGRAM (Deliverable 01)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3, NAVY_DARK)
    add_header(s3, "01. Functional Design: End-to-End Intelligence Pipeline")

    # 4 Sequential Process Cards
    steps = [
        ("1. Ingestion & Criticality", "• Parse Meridian non-standard Excel\n• Isolate V-000 worked example\n• Weighted formula (35/30/20/15)\n• Critical dependency overrides", ORANGE_OPTIV),
        ("2. OSINT Candidate Discovery", "• Proportional depth assignment\n• Domain path heuristics (/trust, /ai)\n• Targeted Dork search queries\n• SEC 10-K & Job posting targets", WHITE),
        ("3. Dual-Gate Classification", "• Strip scripts & extract text\n• Sentence-level regex matcher\n• Dual-condition sub-processor rule (Provider + Relationship cue)\n• Strict audit traceability log", WHITE),
        ("4. Risk Synthesis & Export", "• Guardrail: No AI claim = Not Rated\n• Elevating vs Mitigating factors\n• Student-cell template updates\n• Non-destructive Excel export", ORANGE_OPTIV)
    ]

    for i, (stitle, sbody, scolor) in enumerate(steps):
        c = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i * 2.95), Inches(1.8), Inches(2.8), Inches(4.8))
        c.fill.solid()
        c.fill.fore_color.rgb = NAVY_LIGHT
        c.line.color.rgb = BORDER_GREY
        tf_s = c.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = Inches(0.3)
        p = tf_s.paragraphs[0]
        p.text = stitle
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = scolor

        for line in sbody.split("\n"):
            p = tf_s.add_paragraph()
            p.text = line
            p.font.size = Pt(12)
            p.font.color.rgb = GREY_TEXT
            p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 4: SYSTEM ARCHITECTURE DIAGRAM (Deliverable 02)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4, NAVY_DARK)
    add_header(s4, "02. Technical System Architecture")

    arch_layers = [
        ("Presentation Layer (Streamlit)", "app.py\nInteractive UI with 6 Tabs (Vendors, Criticality, Sources, Evidence, Risk, AI Dossier & LLM Co-Pilot), live file uploader, parameter toggles, and instant Excel export.", Inches(0.8), Inches(1.7), Inches(11.7), Inches(1.05)),
        ("Pipeline Core (src/)", "excel_handler.py: Template-aware openpyxl parser & format preserver\nscoring.py: Meridian-specific weighted business impact rubric\nosint.py: Discovery heuristics & search candidate engine\nclassify.py: Regex pattern extraction & dual-gate subprocessor detector\nrisk.py: Conservative residual risk synthesizer with insufficient evidence guardrails", Inches(0.8), Inches(2.85), Inches(11.7), Inches(1.6)),
        ("Cognitive TPRM Layer (src/llm_analysis.py)", "Semantic LLM Verification (Gemini / OpenAI / Offline Cognitive Engine): Separates runtime embedded AI from marketing fluff.\nNIST AI RMF 1.0 Alignment (Govern, Map, Measure, Manage) & automated tailor-made 5-question vendor audit questionnaire.", Inches(0.8), Inches(4.55), Inches(11.7), Inches(1.15)),
        ("Extraction & Persistence", "extract.py: BeautifulSoup visible text parser & HTML sanitizer\ndb.py: Relational SQLite audit trail (vendors, candidate URLs, classified evidence, assessments)\nmeridian_export.py: Precision cell writer updating cream-colored cells (Cols L-P)", Inches(0.8), Inches(5.8), Inches(11.7), Inches(1.05))
    ]

    for title, desc, l, t, w, h in arch_layers:
        box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h)
        box.fill.solid()
        box.fill.fore_color.rgb = NAVY_LIGHT
        box.line.color.rgb = BORDER_GREY
        tf_a = box.text_frame
        tf_a.word_wrap = True
        tf_a.margin_left = tf_a.margin_right = tf_a.margin_top = Inches(0.25)
        p = tf_a.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = ORANGE_OPTIV
        for line in desc.split("\n"):
            p = tf_a.add_paragraph()
            p.text = line
            p.font.size = Pt(11)
            p.font.color.rgb = GREY_TEXT
            p.space_before = Pt(4)

    # =========================================================================
    # SLIDE 5: SOURCE STRATEGY & EVIDENTIARY WEIGHT (Deliverable 03)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5, NAVY_DARK)
    add_header(s5, "03. OSINT Source Strategy & Evidentiary Hierarchy")

    # Table of Source Tiers
    table_shape = s5.shapes.add_table(5, 4, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8))
    table = table_shape.table
    table.columns[0].width = Inches(1.8)
    table.columns[1].width = Inches(3.2)
    table.columns[2].width = Inches(4.2)
    table.columns[3].width = Inches(2.5)

    headers_t = ["Tier & Authority", "Source Types", "Significance in Assessment", "Evidentiary Weight"]
    for col_idx, h_text in enumerate(headers_t):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_LIGHT
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = ORANGE_OPTIV

    tiers_data = [
        ("Tier 1: Contractual & Authoritative", "Trust Centers, Sub-processor Lists, SEC 10-K, SOC 2 / ISO Bridges, DPA Terms", "Confirms legal and operational realities; named model providers here establish factual findings.", "High (0.85 – 1.0)"),
        ("Tier 2: Technical & Architectural", "Developer Documentation, API Endpoints, Architecture Whitepapers, GitHub", "Reveals real functional model execution, data payloads, inference APIs, and automated agent loops.", "High-Med (0.70 – 0.85)"),
        ("Tier 3: Organizational & Talent", "Technical Job Postings (Prompt Eng, LLMOps), Patent Filings, Engineering Blogs", "Proves active R&D and internal AI building; indicates direction, but not production live data flow.", "Medium (0.45 – 0.65)"),
        ("Tier 4: Commercial & Commentary", "Press Releases, Website Marketing Copy, Keynotes, Executive LinkedIn Posts", "Treat as hypotheses only. Never base risk scores solely on marketing buzzwords.", "Low (0.20 – 0.40)")
    ]

    for row_idx, r in enumerate(tiers_data, start=1):
        for col_idx, val in enumerate(r):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY_LIGHT if row_idx % 2 == 1 else RGBColor(14, 30, 56)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(11)
            p.font.color.rgb = WHITE if col_idx == 0 else GREY_TEXT

    # =========================================================================
    # SLIDE 6: VENDOR CRITICALITY RATINGS & RUBRIC (Deliverable 04)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6, NAVY_DARK)
    add_header(s6, "04. Defensible Vendor Criticality Scoring Rubric")

    # Left: Rubric details
    c_rubric = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    c_rubric.fill.solid()
    c_rubric.fill.fore_color.rgb = NAVY_LIGHT
    c_rubric.line.color.rgb = BORDER_GREY
    tf_rub = c_rubric.text_frame
    tf_rub.word_wrap = True
    tf_rub.margin_left = tf_rub.margin_right = tf_rub.margin_top = Inches(0.3)
    p = tf_rub.paragraphs[0]
    p.text = "Mathematical Criticality Model"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ORANGE_OPTIV

    r_items = [
        "Data Sensitivity (35% Weight): Direct PII, account master records, tax IDs, and credentials score 80–100; transit metadata scores 45–60.",
        "Operational Dependency (30% Weight): Total = 100, High = 85, Moderate = 55, Low = 25.",
        "Regulatory & Payment Exposure (20% Weight): Core platforms, funds transfer, tax notices score 85; reporting scores 60.",
        "Annual Volume (15% Weight): Millions/billions score 90–100; thousands score 65–70.",
        "Critical Override: Explicit 'Critical' Operational Dependency forces Critical Tier regardless of volume."
    ]
    for item in r_items:
        p = tf_rub.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(11.5)
        p.font.color.rgb = GREY_TEXT
        p.space_before = Pt(10)

    # Right: Resulting Tiers
    c_tiers = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    c_tiers.fill.solid()
    c_tiers.fill.fore_color.rgb = NAVY_LIGHT
    c_tiers.line.color.rgb = BORDER_GREY
    tf_t = c_tiers.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = Inches(0.3)
    p = tf_t.paragraphs[0]
    p.text = "Assigned Meridian Vendor Tiers"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = WHITE

    assigned = [
        ("V-002: Fiserv, Inc.", "Critical (Score: 92.5) — Core banking ledger (1.4M customers)."),
        ("V-006: The Clearing House", "Critical (Score: 88.0) — Systemic payments clearing utility."),
        ("V-005: BNY", "High (Score: 79.0) — Inbound RTP payments rail & counterparty data."),
        ("V-001: AutomWorx", "High (Score: 74.5) — Privileged production batch schedule access."),
        ("V-003: FSSI", "High (Score: 73.0) — High data exposure: 19M tax & statement docs."),
        ("V-004: Terrapin Technologies", "Medium (Score: 56.0) — Monthly wealth compensation reporting.")
    ]
    for vname, vdesc in assigned:
        p = tf_t.add_paragraph()
        p.text = vname + "\n" + vdesc
        p.font.size = Pt(11.5)
        p.font.color.rgb = GREY_TEXT
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 7: CONSOLIDATED FINDINGS MATRIX (The 6 Vendors)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7, NAVY_DARK)
    add_header(s7, "05. Vendor Portfolio AI Assessment Matrix")

    table_v = s7.shapes.add_table(7, 6, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8)).table
    table_v.columns[0].width = Inches(1.0)
    table_v.columns[1].width = Inches(2.4)
    table_v.columns[2].width = Inches(1.5)
    table_v.columns[3].width = Inches(1.4)
    table_v.columns[4].width = Inches(2.6)
    table_v.columns[5].width = Inches(2.8)

    cols_v = ["ID", "Vendor Name", "Criticality", "AI Found?", "Named AI Sub-processors", "AI Security Risk"]
    for c_i, c_name in enumerate(cols_v):
        cell = table_v.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_LIGHT
        p = cell.text_frame.paragraphs[0]
        p.text = c_name
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = ORANGE_OPTIV

    v_rows = [
        ("V-001", "AutomWorx", "High", "Inconclusive", "None named (Automic)", "High (Conditional)"),
        ("V-002", "Fiserv, Inc.", "Critical", "Yes", "OpenAI, Azure, UiPath", "Critical (Confirmed)"),
        ("V-003", "FSSI", "High", "No", "None identified", "Low (Deterministic)"),
        ("V-004", "Terrapin Tech", "Medium", "No", "None identified", "None identified"),
        ("V-005", "BNY", "High", "Yes", "OpenAI (Eliza)", "High (Confirmed)"),
        ("V-006", "The Clearing House", "Critical", "No", "None identified", "Low (Rail isolated)")
    ]

    for r_i, r_data in enumerate(v_rows, start=1):
        for c_i, val in enumerate(r_data):
            cell = table_v.cell(r_i, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY_LIGHT if r_i % 2 == 1 else RGBColor(14, 30, 56)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(11)
            p.font.color.rgb = ORANGE_OPTIV if c_i == 5 and "Critical" in val else (WHITE if c_i < 2 else GREY_TEXT)

    # =========================================================================
    # SLIDE 8: DEEP DIVE: CRITICAL & HIGH RISK VENDORS
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8, NAVY_DARK)
    add_header(s8, "Deep Dive: High Exposure Case Studies (Fiserv & BNY)")

    # Box 1: Fiserv DNA
    b_fiserv = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    b_fiserv.fill.solid()
    b_fiserv.fill.fore_color.rgb = NAVY_LIGHT
    b_fiserv.line.color.rgb = BORDER_GREY
    tf_f = b_fiserv.text_frame
    tf_f.word_wrap = True
    tf_f.margin_left = tf_f.margin_right = tf_f.margin_top = Inches(0.3)
    p = tf_f.paragraphs[0]
    p.text = "Fiserv, Inc. — DNA Core Banking"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ORANGE_OPTIV

    f_points = [
        "Signal: Fiserv announced 'agentOS' with OpenAI and Azure OpenAI Foundry integration for agentic banking operations.",
        "Data at Risk: Full customer master, transactions, and balances for 1.4 million Meridian accounts.",
        "Key Vulnerability: Uncontrolled autonomous agent handoffs, prompt injection through customer inputs, and external model retention.",
        "Required Action: Formal Optiv AI TPRM questionnaire; contractually demand Zero Data Retention (ZDR) and Zero Training guarantees on Meridian core accounts."
    ]
    for pt in f_points:
        p = tf_f.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(11.5)
        p.font.color.rgb = GREY_TEXT
        p.space_before = Pt(8)

    # Box 2: BNY RTP
    b_bny = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    b_bny.fill.solid()
    b_bny.fill.fore_color.rgb = NAVY_LIGHT
    b_bny.line.color.rgb = BORDER_GREY
    tf_b = b_bny.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = Inches(0.3)
    p = tf_b.paragraphs[0]
    p.text = "BNY — Real-Time Payments"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = WHITE

    bny_points = [
        "Signal: Proprietary 'Eliza' enterprise platform deployed with ChatGPT Enterprise and OpenAI API integrations; ML routing in payments.",
        "Data at Risk: 2.1M inbound payment instructions, counterparty identifiers, and liquidity accounts.",
        "Key Vulnerability: Potential exposure of payment metadata to generative API endpoints; opaque anomaly detection decisioning.",
        "Required Action: Secure written attestation verifying that RTP payment messages bypass generative LLM pipelines; review BNY Model Risk Management (MRM) audit."
    ]
    for pt in bny_points:
        p = tf_b.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(11.5)
        p.font.color.rgb = GREY_TEXT
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 9: GOVERNANCE & CONTRACTUAL SAFEGUARDS
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9, NAVY_DARK)
    add_header(s9, "Governance Framework: TPRM AI Contract Addendum")

    gov_cards = [
        ("1. Zero Model Training Warranty", "Mandate that no customer, transaction, or privileged configuration data is retained or used to train, fine-tune, or align foundational or proprietary AI models."),
        ("2. AI Sub-processor Notification", "Impose a 60-day prior written notice requirement before introducing new AI/LLM providers (e.g. OpenAI, Anthropic), granting Meridian termination rights."),
        ("3. Human-in-the-Loop Thresholds", "Require explicit human checkpoints on any agentic automated action involving borrower records, payment releases, or batch schedule updates."),
        ("4. Continuous Verification & Audit", "Demand annual SOC 2 Type II with AI Trust Services Criteria, ISO 42001 attestations, and independent red-teaming reports for AI-enabled modules.")
    ]

    for idx, (title_g, desc_g) in enumerate(gov_cards):
        col_pos = idx % 2
        row_pos = idx // 2
        card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + col_pos * 5.9), Inches(1.8 + row_pos * 2.45), Inches(5.6), Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = NAVY_LIGHT
        card.line.color.rgb = BORDER_GREY
        tf_g = card.text_frame
        tf_g.word_wrap = True
        tf_g.margin_left = tf_g.margin_right = tf_g.margin_top = Inches(0.25)
        p = tf_g.paragraphs[0]
        p.text = title_g
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = ORANGE_OPTIV
        p = tf_g.add_paragraph()
        p.text = desc_g
        p.font.size = Pt(11.5)
        p.font.color.rgb = GREY_TEXT
        p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 10: WORKING DEMONSTRATION & NEXT STEPS
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10, NAVY_DARK)
    add_header(s10, "Working Demonstration & Immediate Next Steps")

    c_demo = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8))
    c_demo.fill.solid()
    c_demo.fill.fore_color.rgb = NAVY_LIGHT
    c_demo.line.color.rgb = BORDER_GREY
    tf_d = c_demo.text_frame
    tf_d.word_wrap = True
    tf_d.margin_left = tf_d.margin_right = tf_d.margin_top = Inches(0.35)

    p = tf_d.paragraphs[0]
    p.text = "Operational Tooling: Streamlit Interactive Workbench"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ORANGE_OPTIV

    d_items = [
        "Live Demonstration: Streamlit application running on Python 3.10 with openpyxl, pandas, and SQLite.",
        "Template Fidelity: Seamlessly ingests 'Meridian_Vendor_Input.xlsx', detects non-standard Row 4 headers, and preserves the V-000 worked example untouched.",
        "Full Traceability: Generates audit logs with exact matched terms, sentence snippets, retrieval timestamps, and conservative risk tags.",
        "Immediate Next Steps for Meridian TPRM Leadership:",
        "  1. Issue Targeted AI Questionnaires to Fiserv (DNA) and BNY (RTP) within 15 business days.",
        "  2. Embed Optiv's 4 Model AI Contract Clauses in upcoming Q4 2026 vendor contract reviews.",
        "  3. Operationalize the automated Streamlit tool across Meridian's wider 200+ vendor ecosystem."
    ]
    for it in d_items:
        p = tf_d.add_paragraph()
        p.text = it
        p.font.size = Pt(12)
        p.font.color.rgb = GREY_TEXT
        p.space_before = Pt(8)

    prs.save(output_path)
    print(f"Successfully generated presentation deck at: {output_path}")

if __name__ == "__main__":
    create_deck()
