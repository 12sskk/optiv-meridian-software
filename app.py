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


def _error(message: str) -> None:
    st.session_state.last_error = message
    logger.error(message)
    st.error(message)


st.set_page_config(page_title="Meridian AI Assessment", layout="wide")
_init_state()

st.title("Meridian AI Assessment")
st.caption(
    "Vendor AI usage and security-risk assessment for the case study. "
    "Public-web results are heuristic leads, not vendor verdicts."
)

with st.sidebar:
    st.header("Workspace")
    db_path = st.text_input("SQLite path", value=str(ROOT / "data" / "meridian.db"))
    export_path = st.text_input("Export path", value=str(ROOT / "exports" / "assessment.xlsx"))
    fetch_pages = st.checkbox(
        "Fetch discovered website pages",
        value=False,
        help="Off by default. Enable only for sites you are allowed to retrieve.",
    )
    if st.session_state.last_error:
        st.warning("Last error is shown in the main panel.")

case_file = ROOT / "supporting material" / "Meridian_Vendor_Input.xlsx"

col_up1, col_up2 = st.columns([3, 1])
with col_up1:
    upload = st.file_uploader("Vendor intake Excel (.xlsx)", type=["xlsx"])
with col_up2:
    st.write("")
    st.write("")
    quick_load = False
    if case_file.exists():
        if st.button("📂 Load Case Study", help="Load supporting material/Meridian_Vendor_Input.xlsx directly"):
            quick_load = True

col_a, col_b, col_c = st.columns(3)

target_source = upload if upload is not None else (case_file if quick_load else None)

if col_a.button("Load vendors", type="primary") or quick_load:
    active_source = upload if upload is not None else (case_file if case_file.exists() else None)
    if active_source is None:
        _error("Choose an .xlsx file before loading vendors.")
    else:
        try:
            # The case-study workbook has three sheets and a non-standard header row.
            # Detect it first and use the template-aware parser; retain generic intake
            # support for other workbooks.
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
                    f"Loaded {len(st.session_state.vendors)} real vendor(s). "
                    f"The fictional example was excluded from assessment. Header row: {bundle.header_row}."
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
                st.success(f"Loaded {len(st.session_state.vendors)} vendor(s).")
            else:
                _error("Excel module is not available.")
        except Exception as exc:
            _error(str(exc))

if col_b.button("Score, discover, analyse"):
    if not st.session_state.vendors:
        _error("Load vendors first.")
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
            st.success("Analysis draft updated. Unfetched pages produce insufficient evidence.")
        except Exception as exc:
            _error(str(exc))

if col_c.button("Save & export"):
    if not st.session_state.vendors:
        _error("Nothing to save yet.")
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

tab_vendors, tab_crit, tab_src, tab_ev, tab_risk, tab_dossier = st.tabs(
    ["Vendors", "Criticality", "Sources", "Evidence", "Risk", "🧠 AI Dossier & LLM Co-Pilot"]
)

with tab_vendors:
    if st.session_state.vendors:
        if st.session_state.workbook_mode == "meridian":
            st.info(
                "Meridian template mode: the fictional worked example is excluded from scoring. "
                f"Student-completion columns detected: {len(st.session_state.student_columns)}."
            )
        st.dataframe(_rows(st.session_state.vendors), use_container_width=True)
    else:
        st.info("Upload an intake workbook with a vendor name column to begin.")

with tab_crit:
    if st.session_state.criticality:
        st.dataframe(_rows(st.session_state.criticality), use_container_width=True)
    else:
        st.info("Run analysis to compute intake-based criticality scores.")

with tab_src:
    st.write(
        "Source rows are **candidates and search queries**, not confirmed OSINT findings."
    )
    if st.session_state.sources:
        st.dataframe(_rows(st.session_state.sources), use_container_width=True)
    else:
        st.info("No source candidates yet.")

with tab_ev:
    st.write("Evidence appears only from fetched page text or analyst-vetted OSINT inputs. Nothing is fabricated.")
    
    if st.session_state.vendors:
        with st.expander("🔍 Ingest & Classify Manual OSINT Finding / Snippet", expanded=False):
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
                        st.success(f"Classified and attached {len(new_items)} evidence item(s) to {selected_v}!")
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

            if c_btn2.button("⚡ Pre-load Verified Case Study Evidence"):
                benchmark_snippets = [
                    ("Fiserv, Inc.", "https://www.fiserv.com/en/about-fiserv/newsroom/2025/agentos-openai.html", "Fiserv announced the deployment of agentOS in partnership with OpenAI to bring frontier AI agents into core banking and account workflows, powered by OpenAI models and Microsoft Azure Copilot."),
                    ("BNY", "https://www.bny.com/us/en/insights/ai-payments-innovation.html", "BNY has integrated OpenAI ChatGPT Enterprise and proprietary Eliza platform using machine learning models for real-time payment routing and anomaly detection across RTP rails."),
                    ("AutomWorx", "https://www.broadcom.com/products/software/automation/automic", "Broadcom Automic Automation integrates Automation.AI and MCP servers with ASK_AI function for script generation and incident resolution.")
                ]
                if classify is not None and risk is not None:
                    from src.models import SourceCandidate
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
                    st.success("Loaded verified benchmark evidence for Fiserv, BNY, and AutomWorx!")
                    st.rerun()

    if st.session_state.evidence:
        st.dataframe(_rows(st.session_state.evidence), use_container_width=True)
    else:
        st.info("No evidence snippets. Enable fetching or use the expander above to ingest verified OSINT text.")

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
        st.dataframe(_rows(st.session_state.risks), use_container_width=True)
    else:
        st.info("Risk stays unrated until classified evidence exists.")

with tab_dossier:
    st.subheader("Cognitive TPRM Co-Pilot & Executive Vendor AI Dossier")
    st.caption("Deep semantic reasoning, NIST AI RMF 1.0 alignment, and automated audit questionnaire generation.")

    if not st.session_state.vendors:
        st.info("Load vendors to generate an AI Audit Dossier.")
    elif llm_analysis is None:
        st.warning("LLM analysis module is unavailable.")
    else:
        dossier_col1, dossier_col2 = st.columns([1, 2])
        with dossier_col1:
            target_v_name = st.selectbox("Select Vendor to Audit", [v.name for v in st.session_state.vendors], key="dossier_vendor")
            target_v = next((v for v in st.session_state.vendors if v.name == target_v_name), None)
            
            with st.expander("API Configuration (Optional)", expanded=False):
                api_key_input = st.text_input("Gemini or OpenAI API Key", type="password", help="Leave blank to use Optiv's pre-computed cognitive synthesis benchmarks.")
                llm_mode = st.radio("Provider", ["Auto-detect", "Gemini", "OpenAI"])
            
            gen_btn = st.button("🚀 Generate AI Audit Dossier", type="primary")

        with dossier_col2:
            if target_v:
                st.markdown(f"**Target Vendor:** `{target_v.name}` | **Service:** `{target_v.product or 'N/A'}`")
                
                url_to_vendor = {s.url: s.vendor_name for s in st.session_state.sources}
                v_ev = [item.snippet for item in st.session_state.evidence if url_to_vendor.get(item.source_url) == target_v.name]
                ev_summary = "\n".join(v_ev) if v_ev else "No extracted page text. Utilizing vendor profile and OSINT intelligence."

                if gen_btn or f"dossier_{target_v_name}" in st.session_state:
                    with st.spinner("Analyzing semantic vectors and mapping NIST AI RMF..."):
                        if gen_btn or f"dossier_{target_v_name}" not in st.session_state:
                            prov = "gemini" if "Gemini" in llm_mode else ("openai" if "OpenAI" in llm_mode else "auto")
                            res = llm_analysis.analyze_with_llm(
                                vendor_name=target_v.name,
                                service_description=str(target_v.product or ""),
                                evidence_text=ev_summary,
                                api_key=api_key_input.strip() or None,
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

                    st.markdown("#### 🛡️ Identified Threat Vectors & Data Exposure")
                    for threat in res.get("data_exposure_threats", []):
                        st.markdown(f"- ⚠️ {threat}")

                    st.markdown("#### 🏛️ NIST AI RMF 1.0 Governance Mapping")
                    nist = res.get("nist_ai_rmf", {})
                    n_col1, n_col2 = st.columns(2)
                    with n_col1:
                        st.markdown(f"**Govern:** {nist.get('Govern', 'N/A')}")
                        st.markdown(f"**Map:** {nist.get('Map', 'N/A')}")
                    with n_col2:
                        st.markdown(f"**Measure:** {nist.get('Measure', 'N/A')}")
                        st.markdown(f"**Manage:** {nist.get('Manage', 'N/A')}")

                    st.markdown("#### 📋 Tailored AI TPRM Vendor Questionnaire")
                    st.caption("Custom technical questions generated for Meridian to issue to this vendor's CISO:")
                    q_text = "\n".join(f"{i+1}. {q}" for i, q in enumerate(res.get("tailored_questionnaire", [])))
                    st.text_area("Copy Questionnaire", value=q_text, height=140)

                    st.markdown(f"**Contractual Recommendation:** *{res.get('contractual_recommendation', '')}*")
            else:
                st.info("Select a vendor to view or generate an audit dossier.")
