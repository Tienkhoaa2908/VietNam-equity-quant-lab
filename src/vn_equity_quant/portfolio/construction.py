from __future__ import annotations

import pandas as pd


def build_equal_weight_targets(predictions: pd.DataFrame, top_k: int) -> pd.DataFrame:
    if top_k < 1:
        raise ValueError("top_k must be positive")
    rows: list[dict[str, object]] = []
    for date, group in predictions.groupby("date", sort=True):
        ranked = group.dropna(subset=["score"]).sort_values(
            ["score", "symbol"], ascending=[False, True]
        )
        selected = ranked.head(top_k)
        if selected.empty:
            continue
        weight = 1.0 / len(selected)
        for rank, (_, row) in enumerate(selected.iterrows(), start=1):
            rows.append(
                {
                    "date": pd.Timestamp(date),
                    "symbol": str(row["symbol"]),
                    "rank": rank,
                    "score": float(row["score"]),
                    "target_weight": weight,
                }
            )
    return pd.DataFrame(rows)
