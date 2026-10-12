# Meridian AI Assessment

Local Streamlit tool for reviewing vendor AI usage signals and related security risks. It supports the supplied Meridian case-study workbook as well as generic vendor intake spreadsheets.

## Important assessment limits

- Source discovery creates **source candidates**, not findings.
- Keyword matches are **heuristic leads**, not proof of AI use, a security control, a breach, or a compliance failure. Evidence rows retain the exact matched sentence, source URL/title, retrieval timestamp when fetched, and matched terms.
- If no AI-related evidence is found, the tool does not infer that the vendor does not use AI.
- Criticality scoring for the Meridian workbook is a proposed transparent heuristic, not an official Optiv scoring formula. Its rationale and missing-input notes should be reviewed.
- AI-specific risk is left unrated unless an AI capability signal is present in the extracted evidence; unrelated privacy/security keywords or a provider-name lead alone do not trigger an AI risk score. Any score remains a draft requiring human review.
- Named AI-provider/subprocessor screening requires a provider name and an explicit relationship/processing cue in the same sentence. This is still a review lead, not proof that the provider processes Meridian data.
- Meridian export updates only student-completion cells in a copy of the original workbook. The supplied vendor rows and other sheets are preserved.

## Setup

Python 3.11+ is recommended.

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS/Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the app

From the project root:

```bash
streamlit run app.py
```

Upload `supporting material/Meridian_Vendor_Input.xlsx` to use template-aware mode. The app detects the non-standard header row, excludes the fictional worked example from assessment, maps the supplied inventory fields into criticality scoring, and exports back into a copy of the original template.

Other spreadsheets can still be loaded using the generic intake mode.

Page fetching is off by default. Enable it only when appropriate for the source sites. A guessed URL or search query is not evidence that a page exists or that a vendor uses AI.

## Tests

```bash
pytest -q
```

The test suite covers the pipeline modules, the Meridian workbook parser, criticality mapping, and template-preserving export.

## Layout

- `app.py` — Streamlit workflow
- `src/excel_handler.py` — Meridian workbook parsing and protected-cell export
- `src/excel_io.py` — generic workbook intake
- `src/scoring.py` — criticality scoring
- `src/osint.py` — source candidate generation
- `src/extract.py` — public webpage fetching and text extraction
- `src/classify.py` — keyword-based evidence leads
- `src/risk.py` — conservative risk draft
- `src/meridian_export.py` — map findings into Meridian student fields
- `src/db.py` — SQLite persistence
- `src/export.py` — generic multi-sheet export
- `tests/` — unit and integration tests


## Important: the fictional example row

The supplied `Meridian_Vendor_Input.xlsx` intentionally contains a completed fictional worked example
(`V-000`, Larkspur Servicing Group Ltd) in the `Vendor Inventory` sheet. Those cells are part of the
original template and must remain exactly as supplied. Do not clear them or treat them as a real vendor.
The loader excludes this row from scoring, and the template-aware exporter writes assessment updates only
for the six real vendor IDs (`V-001` through `V-006`). The export test compares the example row against
the original workbook to ensure it remains unchanged.

## Evidence interpretation

Generated URLs are source candidates, not findings. Fetched-page keyword matches are leads for human review,
not proof that the specific Meridian service uses AI or that a named provider processes Meridian data.
Generic privacy, security, and third-party-sharing terms provide context only; they do not independently
establish AI usage. Keep AI usage unknown and AI-specific risk not rated when relevant evidence is insufficient.
