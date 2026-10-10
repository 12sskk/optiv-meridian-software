"""Tests for Excel intake loading."""

from io import BytesIO

import pandas as pd
import pytest

from src.excel_io import ExcelLoadError, load_vendor_workbook, parse_vendors


def _xlsx(frame: pd.DataFrame) -> BytesIO:
    buffer = BytesIO()
    frame.to_excel(buffer, index=False, engine="openpyxl")
    buffer.seek(0)
    return buffer


def test_parse_accepts_alias_columns() -> None:
    frame = pd.DataFrame(
        {
            "Vendor": ["Acme"],
            "Website": ["https://example.invalid"],
            "data_sensitivity": ["medium"],
        }
    )
    records = parse_vendors(frame)
    assert len(records) == 1
    assert records[0].name == "Acme"
    assert records[0].website == "https://example.invalid"


def test_missing_name_column_raises() -> None:
    with pytest.raises(ExcelLoadError, match="vendor name"):
        parse_vendors(pd.DataFrame({"product": ["x"]}))


def test_load_round_trip() -> None:
    buffer = _xlsx(pd.DataFrame({"vendor_name": ["Northwind"]}))
    frame = load_vendor_workbook(buffer)
    records = parse_vendors(frame)
    assert records[0].name == "Northwind"
