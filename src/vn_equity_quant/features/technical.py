from __future__ import annotations

import numpy as np
import pandas as pd


def build_technical_features(market: pd.DataFrame) -> pd.DataFrame:
    """Build backward-looking price features without future observations."""

    frame = market.sort_values(["symbol", "date"], kind="stable").copy()
    grouped = frame.groupby("symbol", group_keys=False)

    frame["return_1d"] = grouped["close"].pct_change(fill_method=None)
    frame["momentum_20"] = grouped["close"].pct_change(20, fill_method=None)
    frame["momentum_60"] = grouped["close"].pct_change(60, fill_method=None)
    frame["volatility_20"] = grouped["return_1d"].transform(
        lambda series: series.rolling(20, min_periods=20).std() * np.sqrt(252.0)
    )
    rolling_high = grouped["close"].transform(
        lambda series: series.rolling(252, min_periods=126).max()
    )
    frame["distance_252_high"] = frame["close"] / rolling_high - 1.0
    frame["volume_ratio_20"] = frame["volume"] / grouped["volume"].transform(
        lambda series: series.rolling(20, min_periods=20).mean()
    )
    return frame
