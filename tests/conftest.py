"""Ensure the project root is importable as `src` during tests."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Ensure supporting material workbook exists for integration tests
workbook_path = ROOT / "supporting material" / "Meridian_Vendor_Input.xlsx"
if not workbook_path.exists():
    try:
        from create_input_workbook import generate_input_workbook
        generate_input_workbook(workbook_path)
    except Exception as exc:
        pass
