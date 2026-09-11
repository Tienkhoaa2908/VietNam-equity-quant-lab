from __future__ import annotations

import numpy as np
import pandas as pd

RAW_FEATURES = (
    "momentum_21",
    "momentum_63",
    "momentum_126",
    "reversal_5",
    "volatility_21",
    "price_to_high_126",
    "volume_ratio_20",
)
MODEL_FEATURES = tuple(f"z_{name}" for name in RAW_FEATURES)


def _zscore(series: pd.Series) -> pd.Series:
    values = series.astype(float)
    valid = values.dropna()
    if len(valid) < 3:
        return pd.Series(np.nan, index=series.index, dtype=float)
    low, high = valid.quantile([0.025, 0.975])
    clipped = values.clip(lower=low, upper=high)
    std = clipped.std(ddof=0)
    if not np.isfinite(std) or std <= 1e-12:
        return pd.Series(0.0, index=series.index, dtype=float).where(values.notna())
    return (clipped - clipped.mean()) / std


def normalize_cross_section(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    for raw, target in zip(RAW_FEATURES, MODEL_FEATURES, strict=True):
        out[target] = out.groupby("date", sort=False)[raw].transform(_zscore)
    return out
