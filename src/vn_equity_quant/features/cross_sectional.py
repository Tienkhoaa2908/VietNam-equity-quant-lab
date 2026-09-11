from __future__ import annotations

import numpy as np
import pandas as pd

RAW_FEATURES = (
    "momentum_20",
    "momentum_60",
    "volatility_20",
    "distance_252_high",
    "volume_ratio_20",
)
MODEL_FEATURES = tuple(f"z_{name}" for name in RAW_FEATURES)


def _zscore(series: pd.Series) -> pd.Series:
    std = series.std(ddof=0)
    if not np.isfinite(std) or std <= 1e-12:
        return pd.Series(0.0, index=series.index)
    return (series - series.mean()) / std


def cross_sectional_standardize(features: pd.DataFrame) -> pd.DataFrame:
    """Standardize each feature across the investable cross-section by date."""

    frame = features.copy()
    for raw, output in zip(RAW_FEATURES, MODEL_FEATURES, strict=True):
        frame[output] = frame.groupby("date")[raw].transform(_zscore)
    return frame
