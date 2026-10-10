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

upload = st.file_uploader("Vendor intake Excel (.xlsx)", type=["xlsx"])
col_a, col_b, col_c = st.columns(3)

if col_a.button("Load vendors", type="primary"):
    if upload is None:
        _error("Choose an .xlsx file before loading vendors.")
    else:
        try:
            # The case-study workbook has three sheets and a non-standard header row.
            # Detect it first and use the template-aware parser; retain generic intake
            # support for other workbooks.
            if excel_handler is not None and excel_handler.is_meridian_workbook(upload):
                bundle = excel_handler.load_meridian_workbook(upload)
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
                frame = excel_io.load_vendor_workbook(upload)
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

tab_vendors, tab_crit, tab_src, tab_ev, tab_risk = st.tabs(
    ["Vendors", "Criticality", "Sources", "Evidence", "Risk"]
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
    st.write("Evidence appears only from fetched page text. Nothing is fabricated.")
    if st.session_state.evidence:
        st.dataframe(_rows(st.session_state.evidence), use_container_width=True)
    else:
        st.info("No evidence snippets. Enable fetching or classify pasted text in later work.")

with tab_risk:
    if st.session_state.risks:
        st.dataframe(_rows(st.session_state.risks), use_container_width=True)
    else:
        st.info("Risk stays unrated until classified evidence exists.")
