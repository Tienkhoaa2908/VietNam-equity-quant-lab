import pandas as pd
import pytest

from vn_equity_quant.data import validate_market_frame


def _row() -> dict[str, object]:
    return {
        "date": "2026-01-02",
        "symbol": "ABC",
        "open": 10.0,
        "high": 11.0,
        "low": 9.5,
        "close": 10.5,
        "volume": 1000,
    }


def test_schema_rejects_duplicate_symbol_session() -> None:
    row = _row()
    with pytest.raises(ValueError, match="duplicate"):
        validate_market_frame(pd.DataFrame([row, row]))


def test_schema_normalizes_symbol_and_date() -> None:
    row = _row()
    row["symbol"] = " abc "
    out = validate_market_frame(pd.DataFrame([row]))
    assert out.loc[0, "symbol"] == "ABC"
    assert str(out.loc[0, "date"].date()) == "2026-01-02"
