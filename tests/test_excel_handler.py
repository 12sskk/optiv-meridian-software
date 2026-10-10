"""Tests for the Meridian vendor inventory workbook handler."""

from __future__ import annotations

from pathlib import Path

import pytest
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Protection

from src.excel_handler import (
    ExcelHandlerError,
    export_inventory,
    get_real_vendors_and_student_columns,
    identify_header_row,
    load_meridian_workbook,
    to_vendor_record,
)


def _build_workbook(path: Path, *, include_vendor_id: bool = True) -> Path:
    workbook = Workbook()

    inventory = workbook.active
    inventory.title = "Vendor Inventory"
    inventory["A1"] = "Meridian — Vendor Inventory"
    inventory["A1"].font = Font(name="Georgia", size=16, bold=True, color="FF0000")
    inventory["A1"].fill = PatternFill("solid", fgColor="FFF2CC")
    inventory["A2"] = (
        "Row 4 is the example vendor. It is fictional and must not be assessed."
    )
    inventory.merge_cells("A1:G1")

    headers = (
        ["Vendor ID", "Vendor Name", "Product", "Website", "Data Sensitivity"]
        if include_vendor_id
        else ["Vendor Name", "Product", "Website", "Data Sensitivity"]
    )
    headers += ["Student AI notes", "Student risk rating"]
    header_row = 4
    for col, title in enumerate(headers, start=1):
        cell = inventory.cell(header_row, col, title)
        cell.font = Font(name="Georgia", size=11, bold=True, color="003366")
        cell.fill = PatternFill("solid", fgColor="D9E2F3")

    example = {
        "Vendor ID": "EX-001",
        "Vendor Name": "Example Vendor (fictional)",
        "Product": "Demo platform",
        "Website": "https://example.invalid",
        "Data Sensitivity": "High",
        "Student AI notes": "Worked example only — do not copy as a finding.",
        "Student risk rating": "n/a",
    }
    real_one = {
        "Vendor ID": "V-101",
        "Vendor Name": "Northwind Labs",
        "Product": "Collaboration suite",
        "Website": "https://northwind.invalid",
        "Data Sensitivity": "Medium",
        "Student AI notes": None,
        "Student risk rating": None,
    }
    real_two = {
        "Vendor ID": "V-102",
        "Vendor Name": "Contoso Supplies",
        "Product": "Procurement portal",
        "Website": "https://contoso.invalid",
        "Data Sensitivity": "Low",
        "Student AI notes": None,
        "Student risk rating": None,
    }
    for row_idx, payload in enumerate((example, real_one, real_two), start=5):
        for title in headers:
            inventory.cell(row_idx, headers.index(title) + 1, payload.get(title))
        for col in range(1, len(headers) + 1):
            header_name = headers[col - 1]
            supplied = header_name not in {"Student AI notes", "Student risk rating"}
            inventory.cell(row_idx, col).protection = Protection(locked=supplied)

    guide = workbook.create_sheet("Field Guide")
    guide.append(["Field Name", "Description", "Required", "Completed by"])
    guide.append(["Vendor ID", "Stable identifier. Do not change.", "Yes", "Supplied"])
    guide.append(["Vendor Name", "Legal or trading name.", "Yes", "Supplied"])
    guide.append(["Product", "Product or service in use.", "No", "Supplied"])
    guide.append(["Website", "Public website if known.", "No", "Supplied"])
    guide.append(["Data Sensitivity", "Intake classification.", "No", "Supplied"])
    guide.append(
        [
            "Student AI notes",
            "Student research notes. Leave blank when evidence is insufficient.",
            "No",
            "Student",
        ]
    )
    guide.append(
        [
            "Student risk rating",
            "Draft rating from the assessment workflow, not a vendor verdict.",
            "No",
            "Student",
        ]
    )

    points = workbook.create_sheet("Points to consider")
    points["A1"] = "Points to consider"
    points["A3"] = "Do not treat the example row as a real vendor."
    points["A4"] = "Do not overwrite supplied inventory values."
    points["A5"] = "Public sources are leads, not conclusions."

    workbook.save(path)
    workbook.close()
    return path


def test_header_row_is_detected_below_titles(tmp_path: Path) -> None:
    path = _build_workbook(tmp_path / "inventory.xlsx")
    bundle = load_meridian_workbook(path)
    assert bundle.header_row == 4
    workbook = load_workbook(path)
    detected = identify_header_row(
        workbook["Vendor Inventory"],
        ["Vendor ID", "Vendor Name", "Student AI notes"],
    )
    workbook.close()
    assert detected == 4


def test_example_vendor_is_excluded_and_values_preserved(tmp_path: Path) -> None:
    path = _build_workbook(tmp_path / "inventory.xlsx")
    real, student_columns = get_real_vendors_and_student_columns(path)
    assert [record.vendor_id for record in real] == ["V-101", "V-102"]
    assert all(not record.is_example for record in real)
    assert real[0].values["Vendor Name"] == "Northwind Labs"
    assert real[0].values["Website"] == "https://northwind.invalid"
    assert real[0].values["Data Sensitivity"] == "Medium"
    assert student_columns == ["Student AI notes", "Student risk rating"]
    vendor = to_vendor_record(real[0])
    assert vendor.vendor_id == "V-101"
    assert vendor.name == "Northwind Labs"


def test_missing_required_column_has_useful_error(tmp_path: Path) -> None:
    path = _build_workbook(tmp_path / "inventory.xlsx", include_vendor_id=False)
    with pytest.raises(ExcelHandlerError, match="Vendor ID") as info:
        load_meridian_workbook(path)
    assert "Present columns" in str(info.value)


def test_export_keeps_formatting_and_supplied_cells(tmp_path: Path) -> None:
    source = _build_workbook(tmp_path / "inventory.xlsx")
    bundle = load_meridian_workbook(source)
    dest = tmp_path / "completed.xlsx"
    export_inventory(
        bundle,
        dest,
        updates={
            "V-101": {
                "Student AI notes": "insufficient_evidence",
                "Student risk rating": "not_rated",
                "Vendor Name": "should not apply",
            },
            "EX-001": {"Student AI notes": "must not write example"},
            "V-999": {"Student AI notes": "unknown vendor"},
        },
    )

    original = load_workbook(source)
    exported = load_workbook(dest)
    orig_title = original["Vendor Inventory"]["A1"]
    new_title = exported["Vendor Inventory"]["A1"]
    assert new_title.value == orig_title.value
    assert new_title.font.name == "Georgia"
    assert new_title.font.size == 16
    assert new_title.font.color.rgb == orig_title.font.color.rgb
    assert new_title.fill.fgColor.rgb == orig_title.fill.fgColor.rgb

    orig_inv = original["Vendor Inventory"]
    new_inv = exported["Vendor Inventory"]
    assert orig_inv.max_row == new_inv.max_row
    assert new_inv.cell(6, 2).value == "Northwind Labs"
    assert new_inv.cell(6, 6).value == "insufficient_evidence"
    assert new_inv.cell(6, 7).value == "not_rated"
    assert new_inv.cell(5, 6).value == "Worked example only — do not copy as a finding."
    assert new_inv.cell(7, 2).value == "Contoso Supplies"
    original.close()
    exported.close()


def test_missing_sheet_lists_found_sheets(tmp_path: Path) -> None:
    path = _build_workbook(tmp_path / "inventory.xlsx")
    workbook = load_workbook(path)
    del workbook["Points to consider"]
    workbook.save(path)
    workbook.close()
    with pytest.raises(ExcelHandlerError, match="Points to consider") as info:
        load_meridian_workbook(path)
    assert "Vendor Inventory" in str(info.value)
