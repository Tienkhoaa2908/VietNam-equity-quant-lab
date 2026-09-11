from __future__ import annotations

import pandas as pd


def attach_forward_labels(frame: pd.DataFrame, horizon: int) -> pd.DataFrame:
    """Attach close-to-close forward returns and the date they become observable."""
    if horizon < 1:
        raise ValueError("horizon must be positive")
    parts: list[pd.DataFrame] = []
    for _, symbol_frame in frame.groupby("symbol", sort=False):
        part = symbol_frame.sort_values("date").copy()
        part["target_forward_return"] = part["close"].shift(-horizon) / part["close"] - 1.0
        part["label_available_date"] = part["date"].shift(-horizon)
        parts.append(part)
    return (
        pd.concat(parts, ignore_index=True)
        .sort_values(["date", "symbol"])
        .reset_index(drop=True)
    )
