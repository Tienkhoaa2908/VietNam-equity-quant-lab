from __future__ import annotations

import pandas as pd

REQUIRED_COLUMNS = ("date", "symbol", "open", "high", "low", "close", "volume")


def validate_market_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Validate and normalize long-form OHLCV market data.

    The returned frame is sorted by symbol and date and contains one row per
    symbol-session. Validation is intentionally strict because downstream
    research assumes a stable point-in-time price table.
    """

    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    out = frame.loc[:, REQUIRED_COLUMNS].copy()
    out["date"] = pd.to_datetime(out["date"], utc=False).dt.normalize()
    out["symbol"] = out["symbol"].astype(str).str.upper().str.strip()

    numeric_columns = ["open", "high", "low", "close", "volume"]
    for column in numeric_columns:
        out[column] = pd.to_numeric(out[column], errors="raise")

    if out[["date", "symbol"]].isna().any().any():
        raise ValueError("date and symbol must be non-null")
    if (out["symbol"] == "").any():
        raise ValueError("symbol must be non-empty")
    if out.duplicated(["date", "symbol"]).any():
        raise ValueError("duplicate symbol-session rows are not allowed")
    if (out[["open", "high", "low", "close"]] <= 0).any().any():
        raise ValueError("OHLC prices must be positive")
    if (out["volume"] < 0).any():
        raise ValueError("volume must be non-negative")

    invalid_high = out["high"] < out[["open", "close", "low"]].max(axis=1)
    invalid_low = out["low"] > out[["open", "close", "high"]].min(axis=1)
    if invalid_high.any() or invalid_low.any():
        raise ValueError("OHLC ordering is inconsistent")

    return out.sort_values(["symbol", "date"], kind="stable").reset_index(drop=True)
