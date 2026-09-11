from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class WalkForwardSplit:
    train_end: pd.Timestamp
    test_start: pd.Timestamp
    test_end: pd.Timestamp


def expanding_walk_forward_splits(
    dates: pd.Series | pd.Index,
    *,
    minimum_train_sessions: int = 252,
    test_sessions: int = 63,
) -> list[WalkForwardSplit]:
    """Create expanding chronological train/test windows."""

    unique_dates = pd.DatetimeIndex(pd.to_datetime(pd.Index(dates).unique())).sort_values()
    if minimum_train_sessions <= 0 or test_sessions <= 0:
        raise ValueError("window lengths must be positive")

    splits: list[WalkForwardSplit] = []
    train_end_index = minimum_train_sessions - 1
    while train_end_index + 1 < len(unique_dates):
        test_start_index = train_end_index + 1
        test_end_index = min(test_start_index + test_sessions - 1, len(unique_dates) - 1)
        splits.append(
            WalkForwardSplit(
                train_end=unique_dates[train_end_index],
                test_start=unique_dates[test_start_index],
                test_end=unique_dates[test_end_index],
            )
        )
        train_end_index = test_end_index
    return splits
