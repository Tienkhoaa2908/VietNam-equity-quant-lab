from __future__ import annotations

import numpy as np
import pandas as pd


def information_coefficient_series(predictions: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for date, group in predictions.groupby("date", sort=True):
        valid = group[["score", "target_forward_return"]].dropna()
        ic = valid["score"].corr(valid["target_forward_return"], method="spearman")
        rows.append({"date": date, "rank_ic": float(ic) if np.isfinite(ic) else np.nan})
    return pd.DataFrame(rows)
