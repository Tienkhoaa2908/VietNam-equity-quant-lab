from __future__ import annotations

import pandas as pd


def equal_weight_targets(ranked: pd.DataFrame) -> pd.DataFrame:
    """Assign equal portfolio weights within each signal date."""

    out = ranked.copy()
    count = out.groupby("date")["symbol"].transform("count")
    if (count <= 0).any():
        raise ValueError("empty portfolio cross-section")
    out["target_weight"] = 1.0 / count
    return out
