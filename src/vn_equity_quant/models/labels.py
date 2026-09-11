from __future__ import annotations

import pandas as pd


def add_forward_return_labels(frame: pd.DataFrame, horizon: int = 20) -> pd.DataFrame:
    """Attach forward return labels and the date on which each label is known."""

    if horizon <= 0:
        raise ValueError("horizon must be positive")

    out = frame.sort_values(["symbol", "date"], kind="stable").copy()
    grouped = out.groupby("symbol", group_keys=False)
    future_close = grouped["close"].shift(-horizon)
    future_date = grouped["date"].shift(-horizon)
    out["target_forward_return"] = future_close / out["close"] - 1.0
    out["label_available_date"] = future_date
    return out
