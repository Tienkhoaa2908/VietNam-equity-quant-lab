from __future__ import annotations

import numpy as np
import pandas as pd


def build_time_series_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Create strictly backward-looking features within each symbol."""
    parts: list[pd.DataFrame] = []
    for _, symbol_frame in frame.groupby("symbol", sort=False):
        part = symbol_frame.sort_values("date").copy()
        close = part["close"].astype(float)
        log_return = np.log(close).diff()
        part["momentum_21"] = close.pct_change(21)
        part["momentum_63"] = close.pct_change(63)
        part["momentum_126"] = close.pct_change(126)
        part["reversal_5"] = -close.pct_change(5)
        part["volatility_21"] = log_return.rolling(21, min_periods=21).std(ddof=0)
        rolling_high = close.rolling(126, min_periods=126).max()
        part["price_to_high_126"] = close / rolling_high - 1.0
        rolling_volume = part["volume"].rolling(20, min_periods=20).mean()
        part["volume_ratio_20"] = part["volume"] / rolling_volume - 1.0
        parts.append(part)
    return (
        pd.concat(parts, ignore_index=True).sort_values(["date", "symbol"]).reset_index(drop=True)
    )
