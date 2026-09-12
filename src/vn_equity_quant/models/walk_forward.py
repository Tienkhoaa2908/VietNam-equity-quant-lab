from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from vn_equity_quant.features.cross_sectional import MODEL_FEATURES

from .linear import RidgeCrossSectionalModel


@dataclass(frozen=True)
class WalkForwardResult:
    predictions: pd.DataFrame
    coefficients: pd.DataFrame
    signal_dates: tuple[pd.Timestamp, ...]


def _month_end_dates(frame: pd.DataFrame) -> list[pd.Timestamp]:
    unique = pd.Series(pd.to_datetime(frame["date"].unique())).sort_values()
    table = pd.DataFrame({"date": unique})
    table["period"] = table["date"].dt.to_period("M")
    return table.groupby("period", sort=True)["date"].max().tolist()


def walk_forward_predictions(
    frame: pd.DataFrame,
    *,
    alpha: float,
    min_training_sessions: int,
) -> WalkForwardResult:
    dates = sorted(pd.to_datetime(frame["date"].unique()))
    if len(dates) <= min_training_sessions:
        raise ValueError("not enough sessions for chronological fitting")
    earliest = dates[min_training_sessions - 1]
    signal_dates = [date for date in _month_end_dates(frame) if date >= earliest]
    prediction_parts: list[pd.DataFrame] = []
    coefficient_rows: list[dict[str, object]] = []

    for signal_date in signal_dates:
        signal_rows = frame[frame["date"] == signal_date].copy()
        if signal_rows.dropna(subset=list(MODEL_FEATURES)).empty:
            continue
        model = RidgeCrossSectionalModel(alpha=alpha).fit(frame, signal_date)
        signal_rows["score"] = model.predict(signal_rows)
        prediction_parts.append(signal_rows)
        coefficient_rows.append({"date": signal_date, **model.coefficients})

    if not prediction_parts:
        raise ValueError("no valid walk-forward prediction dates")
    predictions = pd.concat(prediction_parts, ignore_index=True)
    coefficients = pd.DataFrame(coefficient_rows)
    return WalkForwardResult(
        predictions=predictions,
        coefficients=coefficients,
        signal_dates=tuple(pd.to_datetime(predictions["date"].unique())),
    )
