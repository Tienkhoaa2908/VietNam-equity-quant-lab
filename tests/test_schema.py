import pandas as pd
import pytest

from vn_equity_quant.data import SyntheticMarketDataSource, validate_market_frame


def test_synthetic_data_passes_schema() -> None:
    frame = SyntheticMarketDataSource(symbol_count=3, sessions=20).load()
    assert list(frame.columns) == ["date", "symbol", "open", "high", "low", "close", "volume"]
    assert not frame.duplicated(["date", "symbol"]).any()


def test_invalid_ohlc_is_rejected() -> None:
    frame = pd.DataFrame(
        [
            {
                "date": "2026-01-02",
                "symbol": "AAA",
                "open": 10,
                "high": 9,
                "low": 8,
                "close": 10,
                "volume": 1,
            }
        ]
    )
    with pytest.raises(ValueError, match="high"):
        validate_market_frame(frame)
