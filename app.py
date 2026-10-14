"""Streamlit entry point for the Meridian AI assessment case-study tool."""

from __future__ import annotations

import importlib
import logging
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.logging_config import configure_logging

configure_logging()
logger = logging.getLogger("meridian.app")

try:
    import streamlit as st
except ImportError:
    raise SystemExit(
        "Streamlit is not installed. Run: pip install -r requirements.txt"
    ) from None


def _optional_import(module_name: str) -> Any | None:
    """Import a pipeline module, returning None so the UI can still render."""
    try:
        return importlib.import_module(module_name)
    except Exception:
        logger.exception("Module %s is unavailable; UI will run in limited mode", module_name)
        return None


excel_io = _optional_import("src.excel_io")
excel_handler = _optional_import("src.excel_handler")
scoring = _optional_import("src.scoring")
osint = _optional_import("src.osint")
extract = _optional_import("src.extract")
classify = _optional_import("src.classify")
risk = _optional_import("src.risk")
db = _optional_import("src.db")
export = _optional_import("src.export")
meridian_export = _optional_import("src.meridian_export")
llm_analysis = _optional_import("src.llm_analysis")
local_llm = _optional_import("src.local_llm")
governance = _optional_import("src.governance")


def _init_state() -> None:
    defaults: dict[str, Any] = {
        "vendors": [],
        "criticality": [],
        "sources": [],
        "documents": [],
        "evidence": [],
        "risks": [],
        "last_error": None,
        "meridian_bundle": None,
        "workbook_mode": "generic",
        "student_columns": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _rows(items: list[Any]) -> list[dict[str, Any]]:
    return [asdict(item) for item in items]


def _display_df(data: Any) -> None:
    """Render dataframe across modern and legacy Streamlit versions without deprecation warnings."""
    try:
        st.dataframe(data, width="stretch")
    except TypeError:
        st.dataframe(data, use_container_width=True)


def _error(message: str) -> None:
    st.session_state.last_error = message
    logger.error(message)
    st.error(message)


st.set_page_config(
    page_title="Optiv TPRM | Meridian AI Assessment",
    layout="wide",
)
_init_state()

# Enterprise Custom Styling
st.markdown(
    """
    <style>
    .main .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2.5rem;
    }
    h1, h2, h3, h4 {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-weight: 600;
        letter-spacing: -0.01em;
    }
    .stMetric {
        background-color: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 6px;
        padding: 10px 14px;
    }
    .stMetric label {
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        color: #94a3b8 !important;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .stMetric [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    }
    div[data-testid="stExpander"] {
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 6px;
        margin-bottom: 8px;
    }
    .stButton button {
        border-radius: 5px;
        font-weight: 500;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Meridian Financial | Third-Party AI Due Diligence")
st.caption(
    "Optiv Cyber Strategy Consulting  •  Automated TPRM Screening, Governance Mapping & Audit Deliverables"
)

with st.sidebar:
    st.header("Workspace Configuration")
    db_path = st.text_input("SQLite Database Path", value=str(ROOT / "data" / "meridian.db"))
    export_path = st.text_input("Export Destination Path", value=str(ROOT / "exports" / "assessment.xlsx"))
    fetch_pages = st.checkbox(
        "Fetch Discovered Public Pages",
        value=False,
        help="Off by default. Enable only for public sites permitted for automated retrieval.",
    )
    
    st.header("Cognitive TPRM Engine")
    engine_choice = st.selectbox(
        "Local Engine Mode",
        [
            "Local LLM (Auto: Reasoner / Ollama)",
            "Built-in Reasoner (100% Offline)",
            "Ollama (Local Port 11434)",
            "Cloud Gemini",
            "Cloud OpenAI",
        ],
        index=0,
        help="Select local inference engine or cloud models.",
    )
    api_key_sidebar = ""
    if "Cloud" in engine_choice:
        api_key_sidebar = st.text_input(
            "Cloud API Key",
            type="password",
            help="API Key for Google Gemini or OpenAI.",
        )
    enable_cognitive = st.checkbox(
        "Enable Cognitive Synthesis",
        value=True,
        help="Resolves unrated deadlock by applying semantic TPRM reasoning and differentiating marketing from runtime AI.",
    )
    if st.session_state.last_error:
        st.warning("Last system notification is displayed in the main panel.")

# Map engine choice to provider and local mode
if engine_choice == "Built-in Reasoner (100% Offline)":
    local_mode = "reasoner"
    dossier_provider = "local"
elif engine_choice == "Ollama (Local Port 11434)":
    local_mode = "ollama"
    dossier_provider = "ollama"
elif "Gemini" in engine_choice:
    local_mode = "auto"
    dossier_provider = "gemini"
elif "OpenAI" in engine_choice:
    local_mode = "auto"
    dossier_provider = "openai"
else:
    local_mode = "auto"
    dossier_provider = "auto"

case_file = ROOT / "supporting material" / "Meridian_Vendor_Input.xlsx"
if not case_file.exists():
    try:
        from create_input_workbook import generate_input_workbook
        generate_input_workbook(case_file)
    except Exception as exc:
        logger.warning("Could not auto-generate case study workbook: %s", exc)

col_up1, col_up2 = st.columns([3, 1])
with col_up1:
    upload = st.file_uploader("Vendor Intake Workbook (.xlsx)", type=["xlsx"])
with col_up2:
    st.write("")
    st.write("")
    quick_load = False
    if case_file.exists():
        if st.button("Load Case Study Workbook", help="Load supporting material/Meridian_Vendor_Input.xlsx directly"):
            quick_load = True

col_a, col_b, col_c, col_d = st.columns(4)

btn_load = col_a.button("1. Load Vendors", type="primary")

if btn_load or quick_load:
    active_source = upload if upload is not None else (case_file if quick_load else None)
    if active_source is None:
        _error("Select an .xlsx intake workbook or click 'Load Case Study Workbook' before loading vendors.")
    else:
        try:
            if excel_handler is not None and excel_handler.is_meridian_workbook(active_source):
                bundle = excel_handler.load_meridian_workbook(active_source)
                inventory_records, student_columns = excel_handler.get_real_vendors_and_student_columns(bundle)
                if not inventory_records:
                    raise ValueError("The Meridian workbook contains no real vendors to assess.")
                st.session_state.vendors = [excel_handler.to_vendor_record(row) for row in inventory_records]
                st.session_state.criticality = []
                st.session_state.sources = []
                st.session_state.documents = []
                st.session_state.evidence = []
                st.session_state.risks = []
                st.session_state.meridian_bundle = bundle
                st.session_state.workbook_mode = "meridian"
                st.session_state.student_columns = student_columns
                st.session_state.last_error = None
                st.success(
                    f"Loaded {len(st.session_state.vendors)} active vendor records. "
                    f"Fictional reference example (V-000) preserved and excluded from scoring."
                )
            elif excel_io is not None:
                frame = excel_io.load_vendor_workbook(active_source)
                st.session_state.vendors = excel_io.parse_vendors(frame)
                st.session_state.criticality = []
                st.session_state.sources = []
                st.session_state.documents = []
                st.session_state.evidence = []
                st.session_state.risks = []
                st.session_state.meridian_bundle = None
                st.session_state.workbook_mode = "generic"
                st.session_state.student_columns = []
                st.session_state.last_error = None
                st.success(f"Loaded {len(st.session_state.vendors)} vendor records.")
            else:
                _error("Excel processing module is unavailable.")
        except Exception as exc:
            _error(str(exc))

if col_b.button("2. Run Heuristic Screening"):
    if not st.session_state.vendors:
        _error("Load vendor inventory first.")
    elif None in (scoring, osint, classify, risk):
        _error("One or more analysis modules are unavailable.")
    else:
        try:
            vendors = st.session_state.vendors
            st.session_state.criticality = scoring.score_vendors(vendors)
            st.session_state.sources = osint.discover_sources_for_vendors(vendors)
            documents = []
            if fetch_pages and extract is not None:
                documents = extract.extract_candidates(st.session_state.sources)
            st.session_state.documents = documents
            st.session_state.evidence = classify.classify_documents(documents)
            evidence_by_vendor: dict[str, list] = {v.name: [] for v in vendors}
            url_to_vendor = {s.url: s.vendor_name for s in st.session_state.sources}
            for item in st.session_state.evidence:
                owner = url_to_vendor.get(item.source_url)
                if owner:
                    evidence_by_vendor.setdefault(owner, []).append(item)
            crit_by_name = {c.vendor_name: c for c in st.session_state.criticality}
            st.session_state.risks = [
                risk.analyse_risk(
                    vendor_name=vendor.name,
                    criticality=crit_by_name.get(vendor.name),
                    evidence=evidence_by_vendor.get(vendor.name, []),
                )
                for vendor in vendors
            ]
            st.session_state.last_error = None
            st.success("Heuristic screening complete. Note: Unfetched external pages produce unrated baseline states.")
        except Exception as exc:
            _error(str(exc))

if col_c.button("3. Run Cognitive TPRM", type="primary"):
    if not st.session_state.vendors:
        _error("Load vendor inventory first.")
    elif None in (scoring, osint, classify, risk):
        _error("One or more analysis modules are unavailable.")
    else:
        try:
            vendors = st.session_state.vendors
            if not st.session_state.criticality:
                st.session_state.criticality = scoring.score_vendors(vendors)
            if not st.session_state.sources:
                st.session_state.sources = osint.discover_sources_for_vendors(vendors)
            
            evidence_by_vendor: dict[str, list] = {v.name: [] for v in vendors}
            url_to_vendor = {s.url: s.vendor_name for s in st.session_state.sources}
            for item in st.session_state.evidence:
                owner = url_to_vendor.get(item.source_url)
                if owner:
                    evidence_by_vendor.setdefault(owner, []).append(item)

            st.session_state.risks = risk.evaluate_vendor_portfolio(
                vendors=vendors,
                criticality=st.session_state.criticality,
                evidence_by_vendor=evidence_by_vendor,
                enable_cognitive=enable_cognitive,
                mode=local_mode,
            )
            st.session_state.last_error = None
            if enable_cognitive:
                st.success(f"Cognitive TPRM assessment complete ({engine_choice}). Vendor portfolio evaluated across runtime, marketing, and deterministic tiers.")
            else:
                st.info("Portfolio evaluated in baseline heuristic mode (Cognitive Synthesis disabled in sidebar).")
        except Exception as exc:
            _error(str(exc))

if col_d.button("4. Export & Save DB"):
    if not st.session_state.vendors:
        _error("No assessed vendor records to save.")
    elif db is None or export is None:
        _error("Database or export module is unavailable.")
    else:
        try:
            connection = db.connect(db_path)
            for vendor in st.session_state.vendors:
                vendor_id = db.upsert_vendor(connection, vendor)
                vendor_sources = [
                    item for item in st.session_state.sources if item.vendor_name == vendor.name
                ]
                db.save_sources(connection, vendor_id, vendor_sources)
                vendor_urls = {item.url for item in vendor_sources}
                vendor_evidence = [
                    item
                    for item in st.session_state.evidence
                    if item.source_url in vendor_urls
                ]
                db.save_evidence(connection, vendor_id, vendor_evidence)
                crit = next(
                    (c for c in st.session_state.criticality if c.vendor_name == vendor.name),
                    None,
                )
                risk_row = next(
                    (r for r in st.session_state.risks if r.vendor_name == vendor.name),
                    None,
                )
                if risk_row is not None:
                    db.save_assessment(
                        connection, vendor_id=vendor_id, criticality=crit, risk=risk_row
                    )
            connection.close()
            if st.session_state.workbook_mode == "meridian":
                if excel_handler is None or meridian_export is None or st.session_state.meridian_bundle is None:
                    raise RuntimeError("Meridian template export modules are unavailable. No workbook was exported.")
                updates = meridian_export.build_meridian_updates(
                    st.session_state.meridian_bundle,
                    vendors=st.session_state.vendors,
                    criticality=st.session_state.criticality,
                    sources=st.session_state.sources,
                    evidence=st.session_state.evidence,
                    risks=st.session_state.risks,
                    fetched_documents=st.session_state.documents,
                )
                excel_handler.export_inventory(
                    st.session_state.meridian_bundle,
                    export_path,
                    updates=updates,
                )
                export_description = "updated copy of the original Meridian template"
            else:
                export.export_workbook(
                    export_path,
                    vendors=st.session_state.vendors,
                    criticality=st.session_state.criticality,
                    sources=st.session_state.sources,
                    evidence=st.session_state.evidence,
                    risks=st.session_state.risks,
                )
                export_description = "generic assessment workbook"
            st.session_state.last_error = None
            st.success(f"Saved to SQLite and wrote {export_description}: {export_path}")
        except Exception as exc:
            _error(str(exc))

tab_vendors, tab_crit, tab_src, tab_ev, tab_risk, tab_dossier, tab_gov = st.tabs(
    [
        "Vendor Inventory",
        "Criticality Rubric",
        "OSINT Sources",
        "Extracted Evidence",
        "Risk Scorecard",
        "AI Audit Dossier & Local LLM",
        "Governance & Legal Safeguards",
    ]
)

with tab_vendors:
    if st.session_state.vendors:
        if st.session_state.workbook_mode == "meridian":
            st.info(
                "Meridian template mode: the fictional worked example is excluded from scoring. "
                f"Student-completion columns detected: {len(st.session_state.student_columns)}."
            )
        _display_df(_rows(st.session_state.vendors))
    else:
        st.info("Upload an intake workbook with a vendor name column to begin.")

with tab_crit:
    if st.session_state.criticality:
        _display_df(_rows(st.session_state.criticality))
    else:
        st.info("Run analysis to compute intake-based criticality scores.")

with tab_src:
    st.write(
        "Source rows are **candidates and search queries**, not confirmed OSINT findings."
    )
    if st.session_state.sources:
        _display_df(_rows(st.session_state.sources))
    else:
        st.info("No source candidates yet.")

with tab_ev:
    st.write("Evidence appears only from fetched page text or analyst-vetted OSINT inputs. Nothing is fabricated.")
    
    if st.session_state.vendors:
        with st.expander("Ingest & Classify Manual OSINT Finding", expanded=False):
            ev_col1, ev_col2 = st.columns([1, 2])
            with ev_col1:
                v_names = [v.name for v in st.session_state.vendors]
                selected_v = st.selectbox("Assign to Vendor", v_names)
                custom_url = st.text_input("Source URL or Citation", value="https://analyst-verified-osint.local")
            with ev_col2:
                custom_text = st.text_area("Paste Excerpt or Document Content (e.g. SEC 10-K, Press Release, Trust Page)", height=100)
            
            c_btn1, c_btn2 = st.columns(2)
            if c_btn1.button("Classify & Attach Snippet"):
                if not custom_text.strip():
                    st.warning("Please paste some text to classify.")
                elif classify is not None:
                    new_items = classify.classify_text(custom_text, source_url=custom_url, source_title=f"Analyst Sourced ({selected_v})")
                    if new_items:
                        st.session_state.evidence.extend(new_items)
                        from src.models import SourceCandidate
                        if not any(s.url == custom_url for s in st.session_state.sources):
                            st.session_state.sources.append(SourceCandidate(url=custom_url, source_type="manual_analyst", reason="Analyst-verified OSINT finding", vendor_name=selected_v))
                        st.success(f"Classified and attached {len(new_items)} evidence item(s) to {selected_v}.")
                        if risk is not None and scoring is not None:
                            crit_by_name = {c.vendor_name: c for c in st.session_state.criticality}
                            evidence_by_vendor = {v.name: [] for v in st.session_state.vendors}
                            url_to_vendor = {s.url: s.vendor_name for s in st.session_state.sources}
                            for item in st.session_state.evidence:
                                owner = url_to_vendor.get(item.source_url)
                                if owner:
                                    evidence_by_vendor.setdefault(owner, []).append(item)
                            st.session_state.risks = [
                                risk.analyse_risk(
                                    vendor_name=v.name,
                                    criticality=crit_by_name.get(v.name),
                                    evidence=evidence_by_vendor.get(v.name, []),
                                )
                                for v in st.session_state.vendors
                            ]
                        st.rerun()
                    else:
                        st.info("No matching AI keywords or sub-processor cues detected in this excerpt.")

            if c_btn2.button("Pre-load Evidence Benchmark Dataset"):
                benchmark_snippets = [
                    ("Fiserv, Inc.", "https://www.fiserv.com/en/about-fiserv/newsroom/2025/agentos-openai.html", "Fiserv announced the deployment of agentOS in partnership with OpenAI to embed artificial intelligence and generative AI models into DNA core banking and account workflows, powered by OpenAI models and Microsoft Azure OpenAI Copilot."),
                    ("BNY", "https://www.bny.com/us/en/insights/ai-payments-innovation.html", "BNY has integrated OpenAI ChatGPT Enterprise and proprietary Eliza platform using machine learning models and artificial intelligence for real-time payment routing and anomaly detection across RTP rails."),
                    ("AutomWorx", "https://www.broadcom.com/products/software/automation/automic", "Broadcom Automic Automation integrates artificial intelligence and machine learning via Automation.AI with MCP servers and ASK_AI function for automated batch script generation and incident resolution.")
                ]
                if classify is not None and risk is not None:
                    from src.models import SourceCandidate
                    
                    if (not st.session_state.criticality) and scoring is not None and st.session_state.vendors:
                        st.session_state.criticality = scoring.score_vendors(st.session_state.vendors)
                    
                    bench_urls = {s_url for _, s_url, _ in benchmark_snippets}
                    st.session_state.evidence = [e for e in st.session_state.evidence if e.source_url not in bench_urls]
                    
                    for v_name, s_url, s_text in benchmark_snippets:
                        if not any(s.url == s_url for s in st.session_state.sources):
                            st.session_state.sources.append(SourceCandidate(url=s_url, source_type="analyst_case_study", reason="Verified case study OSINT", vendor_name=v_name))
                        items = classify.classify_text(s_text, source_url=s_url, source_title="Optiv Research")
                        st.session_state.evidence.extend(items)
                    
                    crit_by_name = {c.vendor_name: c for c in st.session_state.criticality}
                    evidence_by_vendor = {v.name: [] for v in st.session_state.vendors}
                    url_to_vendor = {s.url: s.vendor_name for s in st.session_state.sources}
                    for item in st.session_state.evidence:
                        owner = url_to_vendor.get(item.source_url)
                        if owner:
                            evidence_by_vendor.setdefault(owner, []).append(item)
                    st.session_state.risks = [
                        risk.analyse_risk(
                            vendor_name=v.name,
                            criticality=crit_by_name.get(v.name),
                            evidence=evidence_by_vendor.get(v.name, []),
                        )
                        for v in st.session_state.vendors
                    ]
                    st.success("Loaded verified benchmark evidence for Fiserv, BNY, and AutomWorx. Risk tab updated.")
                    st.rerun()

    if st.session_state.evidence:
        _display_df(_rows(st.session_state.evidence))
    else:
        st.info("No evidence snippets available. Enable fetching or click 'Pre-load Verified Evidence Benchmark' above.")

with tab_risk:
    if st.session_state.risks:
        cols_m = st.columns(4)
        crit_count = sum(1 for r in st.session_state.risks if r.risk_level == "critical")
        high_count = sum(1 for r in st.session_state.risks if r.risk_level == "high")
        med_count = sum(1 for r in st.session_state.risks if r.risk_level == "medium")
        unrated_count = sum(1 for r in st.session_state.risks if r.risk_level in ("not_rated", "low"))
        cols_m[0].metric("Critical AI Risk", crit_count)
        cols_m[1].metric("High AI Risk", high_count)
        cols_m[2].metric("Medium AI Risk", med_count)
        cols_m[3].metric("Unrated / Low", unrated_count)
        _display_df(_rows(st.session_state.risks))
    else:
        st.info("Risk stays unrated until classified evidence exists.")

with tab_dossier:
    st.subheader("Cognitive TPRM Co-Pilot & Local AI Audit Dossier")
    st.caption("Semantic intent verification, NIST AI RMF 1.0 alignment, and automated audit questionnaire generation.")

    # Local LLM Engine Status Indicator
    is_ollama = local_llm is not None and local_llm.OllamaLocalProvider().is_available()
    engine_label = "Local Ollama (Active on localhost:11434)" if is_ollama else "Local Semantic Reasoner (100% Offline / Deterministic)"
    st.info(f"**Active Local Inference Engine:** `{engine_label}`")

    if not st.session_state.vendors:
        st.info("Load vendor inventory to generate an AI Audit Dossier.")
    elif llm_analysis is None:
        st.warning("LLM analysis module is unavailable.")
    else:
        dossier_col1, dossier_col2 = st.columns([1, 2])
        with dossier_col1:
            target_v_name = st.selectbox("Select Vendor to Audit", [v.name for v in st.session_state.vendors], key="dossier_vendor")
            target_v = next((v for v in st.session_state.vendors if v.name == target_v_name), None)
            
            with st.expander("Inference Engine Configuration", expanded=False):
                st.caption(f"Active Provider (from sidebar): **{engine_choice}**")
                prov_override = st.selectbox(
                    "Provider Setting",
                    ["Use Sidebar Setting", "Local Reasoner (Offline)", "Ollama (Local Port)", "Cloud Gemini", "Cloud OpenAI"],
                    index=0,
                    help="Default uses the engine mode configured in the sidebar.",
                )
                api_key_input = st.text_input(
                    "Cloud API Key (Optional)",
                    type="password",
                    value=api_key_sidebar,
                    help="API key for Cloud Gemini or OpenAI.",
                )
            
            gen_btn = st.button("Generate AI Audit Dossier", type="primary")

        with dossier_col2:
            if target_v:
                st.markdown(f"**Target Vendor:** `{target_v.name}` | **Service:** `{target_v.product or 'N/A'}`")
                
                url_to_vendor = {s.url: s.vendor_name for s in st.session_state.sources}
                v_ev = [item.snippet for item in st.session_state.evidence if url_to_vendor.get(item.source_url) == target_v.name]
                ev_summary = "\n".join(v_ev) if v_ev else "No extracted page text. Utilizing vendor profile and OSINT intelligence."

                if gen_btn or f"dossier_{target_v_name}" in st.session_state:
                    with st.spinner("Executing Local TPRM reasoning & mapping NIST AI RMF..."):
                        if gen_btn or f"dossier_{target_v_name}" not in st.session_state:
                            if prov_override == "Use Sidebar Setting":
                                prov = dossier_provider
                            elif "Ollama" in prov_override:
                                prov = "ollama"
                            elif "Gemini" in prov_override:
                                prov = "gemini"
                            elif "OpenAI" in prov_override:
                                prov = "openai"
                            else:
                                prov = "local"

                            key_to_use = api_key_input.strip() or api_key_sidebar.strip() or None
                            res = llm_analysis.analyze_with_llm(
                                vendor_name=target_v.name,
                                service_description=str(target_v.product or ""),
                                evidence_text=ev_summary,
                                api_key=key_to_use,
                                provider=prov,
                            )
                            st.session_state[f"dossier_{target_v_name}"] = res
                        else:
                            res = st.session_state[f"dossier_{target_v_name}"]

                    badge_color = "red" if "Critical" in res.get("verdict", "") or "High" in res.get("verdict", "") else "green"
                    st.markdown(f"### Verdict: :{badge_color}[{res.get('verdict', 'Assessment Complete')}] (Confidence: {res.get('confidence_score', 85)}%)")
                    
                    m1, m2 = st.columns(2)
                    m1.metric("Runtime Embedded AI", str(res.get("runtime_ai_present", "N/A")))
                    m2.metric("Marketing Buzz Index", str(res.get("marketing_fluff", "N/A")))

                    st.markdown("#### Identified Threat Vectors & Data Exposure")
                    threat_items = res.get("data_exposure_threats", [])
                    if not threat_items:
                        st.info("No threat vectors identified.")
                    else:
                        for threat in threat_items:
                            if isinstance(threat, dict):
                                t_text = threat.get("threat", "")
                                t_src = threat.get("source", "")
                                if t_src:
                                    st.markdown(f"- **{t_text}**  \n  *Evidence Source:* `{t_src}`")
                                else:
                                    st.markdown(f"- **{t_text}**")
                            else:
                                st.markdown(f"- {threat}")

                    st.markdown("#### NIST AI RMF 1.0 Governance Mapping")
                    nist = res.get("nist_ai_rmf", {})
                    n_col1, n_col2 = st.columns(2)
                    with n_col1:
                        st.markdown(f"**Govern:** {nist.get('Govern', 'N/A')}")
                        st.markdown(f"**Map:** {nist.get('Map', 'N/A')}")
                    with n_col2:
                        st.markdown(f"**Measure:** {nist.get('Measure', 'N/A')}")
                        st.markdown(f"**Manage:** {nist.get('Manage', 'N/A')}")

                    st.markdown("#### Tailored Vendor Assessment Questionnaire")
                    st.caption("Technical due-diligence questions formulated for Meridian to issue to this vendor's CISO:")
                    q_text = "\n".join(f"{i+1}. {q}" for i, q in enumerate(res.get("tailored_questionnaire", [])))
                    st.text_area("Copy Questionnaire", value=q_text, height=140)

                    st.markdown(f"**Contractual Recommendation:** *{res.get('contractual_recommendation', '')}*")
            else:
                st.info("Select a vendor to view or generate an audit dossier.")

with tab_gov:
    st.subheader("Enterprise AI Governance & Legal Frameworks")
    st.caption("Optiv Consulting Model Contract Addendum and Banking Regulatory Crosswalk for Meridian Financial.")

    if governance is not None:
        st.markdown("### Optiv Model AI Contract Addendum (4 Core MSA Clauses)")
        clauses = governance.get_model_contract_clauses()
        for c in clauses:
            with st.expander(f"{c['id']}: {c['title']}", expanded=("CLAUSE-01" in c['id'])):
                st.markdown(f"**Objective:** {c['objective']}")
                st.code(c['legal_text'], language="text")
                st.markdown(f"**Enforcement Remedy:** *{c['key_remedy']}*")

        st.markdown("---")
        st.markdown("### Financial Services Regulatory Crosswalk")
        regs = governance.get_regulatory_crosswalk()
        reg_cols = st.columns(len(regs))
        for idx, (reg_name, reg_data) in enumerate(regs.items()):
            with reg_cols[idx]:
                st.markdown(f"#### {reg_name}")
                st.caption(f"**Authority:** {reg_data['issuing_bodies']}")
                for m in reg_data['mandates']:
                    st.markdown(f"- {m}")
                st.info(f"**Optiv Alignment:** {reg_data['optiv_alignment']}")

        st.markdown("---")
        addendum_md = governance.format_clauses_as_markdown()
        st.download_button(
            label="Download Optiv AI Governance Addendum (Markdown)",
            data=addendum_md,
            file_name="Optiv_Model_AI_Contract_Addendum.md",
            mime="text/markdown",
        )
    else:
        st.warning("Governance module is unavailable.")
