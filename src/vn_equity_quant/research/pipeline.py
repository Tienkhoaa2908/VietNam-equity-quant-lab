from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from vn_equity_quant.backtest import BacktestResult, performance_metrics, run_next_open_backtest
from vn_equity_quant.config import ResearchConfig
from vn_equity_quant.data import MarketDataSource, build_manifest
from vn_equity_quant.data.lineage import DataManifest
from vn_equity_quant.features import build_time_series_features, normalize_cross_section
from vn_equity_quant.models import (
    WalkForwardResult,
    attach_forward_labels,
    information_coefficient_series,
    walk_forward_predictions,
)
from vn_equity_quant.portfolio import build_equal_weight_targets


@dataclass(frozen=True)
class ResearchResult:
    manifest: DataManifest
    features: pd.DataFrame
    walk_forward: WalkForwardResult
    targets: pd.DataFrame
    backtest: BacktestResult
    rank_ic: pd.DataFrame
    metrics: dict[str, float | int]

    @property
    def latest_coefficients(self) -> dict[str, float]:
        if self.walk_forward.coefficients.empty:
            return {}
        row = self.walk_forward.coefficients.iloc[-1]
        return {
            column: float(row[column])
            for column in self.walk_forward.coefficients.columns
            if column != "date"
        }


def run_research_pipeline(source: MarketDataSource, config: ResearchConfig) -> ResearchResult:
    config.validate()
    market = source.load()
    manifest = build_manifest(market)
    features = build_time_series_features(market)
    features = normalize_cross_section(features)
    labeled = attach_forward_labels(features, config.prediction_horizon)
    walk_forward = walk_forward_predictions(
        labeled,
        alpha=config.ridge_alpha,
        min_training_sessions=config.min_training_sessions,
    )
    targets = build_equal_weight_targets(walk_forward.predictions, config.top_k)
    backtest = run_next_open_backtest(
        market,
        targets,
        initial_cash=config.initial_cash,
        transaction_cost_bps=config.transaction_cost_bps,
        lot_size=config.lot_size,
    )
    rank_ic = information_coefficient_series(walk_forward.predictions)
    metrics = performance_metrics(backtest.nav, backtest.trades)
    valid_ic = rank_ic["rank_ic"].dropna()
    metrics["mean_rank_ic"] = float(valid_ic.mean()) if not valid_ic.empty else float("nan")
    metrics["median_rank_ic"] = float(valid_ic.median()) if not valid_ic.empty else float("nan")
    metrics["signal_count"] = int(targets["date"].nunique()) if not targets.empty else 0
    return ResearchResult(
        manifest=manifest,
        features=labeled,
        walk_forward=walk_forward,
        targets=targets,
        backtest=backtest,
        rank_ic=rank_ic,
        metrics=metrics,
    )
