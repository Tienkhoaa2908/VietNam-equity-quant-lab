from __future__ import annotations

import numpy as np
import pandas as pd

REQUIRED_COLUMNS = ("date", "symbol", "open", "high", "low", "close", "volume")


def validate_market_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Validate and canonicalize long-form OHLCV data.

    Prices are expressed in one consistent currency unit. The validator deliberately
    does not guess price scaling or corporate-action adjustments.
    """
    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"missing required columns: {missing}")

    out = frame.loc[:, REQUIRED_COLUMNS].copy()
    out["date"] = pd.to_datetime(out["date"], errors="raise").dt.normalize()
    out["symbol"] = out["symbol"].astype(str).str.strip().str.upper()
    if (out["symbol"] == "").any():
        raise ValueError("symbol cannot be empty")

    for column in ("open", "high", "low", "close", "volume"):
        out[column] = pd.to_numeric(out[column], errors="raise")
        if not np.isfinite(out[column].to_numpy(dtype=float)).all():
            raise ValueError(f"{column} contains non-finite values")

    if (out[["open", "high", "low", "close"]] <= 0).any().any():
        raise ValueError("prices must be strictly positive")
    if (out["volume"] < 0).any():
        raise ValueError("volume cannot be negative")
    if (out["high"] < out[["open", "close", "low"]].max(axis=1)).any():
        raise ValueError("high is below another price field")
    if (out["low"] > out[["open", "close", "high"]].min(axis=1)).any():
        raise ValueError("low is above another price field")
    if out.duplicated(["date", "symbol"]).any():
        raise ValueError("duplicate date-symbol rows")

    out["volume"] = out["volume"].round().astype("int64")
    return out.sort_values(["date", "symbol"], kind="mergesort").reset_index(drop=True)
