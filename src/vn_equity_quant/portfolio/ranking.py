from __future__ import annotations

import pandas as pd


def rank_cross_section(frame: pd.DataFrame, score_column: str, top_k: int) -> pd.DataFrame:
    """Return the highest-scoring securities for each signal date."""

    if top_k <= 0:
        raise ValueError("top_k must be positive")
    ranked = frame.dropna(subset=[score_column]).copy()
    ranked["rank"] = ranked.groupby("date")[score_column].rank(
        method="first", ascending=False
    )
    return ranked[ranked["rank"] <= top_k].sort_values(["date", "rank"])
