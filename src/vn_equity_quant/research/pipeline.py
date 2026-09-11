from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from vn_equity_quant.backtest import BacktestResult, ExecutionAwareBacktester, performance_summary
from vn_equity_quant.config import ResearchConfig
from vn_equity_quant.data import MarketDataSource, validate_market_frame
from vn_equity_quant.features import build_technical_features, cross_sectional_standardize
from vn_equity_quant.models import RidgeCrossSectionalModel, add_forward_return_labels
from vn_equity_quant.portfolio import equal_weight_targets, rank_cross_section


@dataclass(frozen=True)
class ResearchRun:
    signals: pd.DataFrame
    targets: pd.DataFrame
    backtest: BacktestResult
    metrics: dict[str, float]
    latest_coefficients: dict[str, float]


def _month_end_signal_dates(dates: pd.Series, minimum_index: int) -> pd.DatetimeIndex:
    unique = pd.DatetimeIndex(pd.to_datetime(dates.unique())).sort_values()
    if len(unique) <= minimum_index:
        return pd.DatetimeIndex([])
    eligible = pd.Series(unique[minimum_index:])
    return pd.DatetimeIndex(eligible.groupby(eligible.dt.to_period("M")).max().tolist())


def run_research_pipeline(
    source: MarketDataSource,
    config: ResearchConfig | None = None,
) -> ResearchRun:
    """Run a deterministic causal research pipeline from data to backtest."""

    cfg = config or ResearchConfig()
    market = validate_market_frame(source.load())
    features = cross_sectional_standardize(build_technical_features(market))
    labeled = add_forward_return_labels(features, horizon=cfg.prediction_horizon)
    signal_dates = _month_end_signal_dates(
        labeled["date"], minimum_index=cfg.min_training_sessions
    )
    if len(signal_dates) < 2:
        raise ValueError("not enough history for monthly walk-forward signals")

    signal_rows: list[pd.DataFrame] = []
    latest_coefficients: dict[str, float] = {}
    for signal_date in signal_dates:
        model = RidgeCrossSectionalModel(alpha=cfg.ridge_alpha)
        model.fit(labeled, as_of=signal_date)
        cross_section = labeled[labeled["date"] == signal_date].copy()
        cross_section["score"] = model.predict(cross_section)
        cross_section = cross_section.dropna(subset=["score"])
        signal_rows.append(cross_section[["date", "symbol", "score"]])
        latest_coefficients = model.coefficients

    signals = pd.concat(signal_rows, ignore_index=True)
    ranked = rank_cross_section(signals, "score", cfg.top_k)
    targets = equal_weight_targets(ranked)
    backtester = ExecutionAwareBacktester(
        initial_nav=cfg.initial_nav,
        transaction_cost_bps=cfg.transaction_cost_bps,
        lot_size=cfg.lot_size,
    )
    result = backtester.run(market, targets)
    metrics = performance_summary(result.nav)
    return ResearchRun(
        signals=signals,
        targets=targets,
        backtest=result,
        metrics=metrics,
        latest_coefficients=latest_coefficients,
    )
