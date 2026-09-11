from __future__ import annotations

import json
from pathlib import Path

from vn_equity_quant.config import ResearchConfig
from vn_equity_quant.research import ResearchResult

from .charts import coefficient_chart, drawdown_chart, equity_chart, rank_ic_chart


def _pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def write_research_report(
    result: ResearchResult,
    config: ResearchConfig,
    output_dir: str | Path,
) -> Path:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    equity_chart(result.backtest.nav, output / "equity_curve.svg")
    drawdown_chart(result.backtest.nav, output / "drawdown.svg")
    rank_ic_chart(result.rank_ic, output / "rank_ic.svg")
    coefficient_chart(result.walk_forward.coefficients, output / "model_coefficients.svg")
    (output / "metrics.json").write_text(
        json.dumps(result.metrics, indent=2, sort_keys=True, allow_nan=True) + "\n",
        encoding="utf-8",
    )
    (output / "data_manifest.json").write_text(result.manifest.to_json() + "\n", encoding="utf-8")

    metrics = result.metrics
    report = f"""# Example Research Report

## Scope

This report is generated from deterministic synthetic OHLCV data.
It validates the software pipeline and research timing contract.
It is not evidence of expected returns in the Vietnamese equity market.

## Research configuration

| Parameter | Value |
| --- | ---: |
| Symbols | {config.symbol_count} |
| Sessions | {config.sessions} |
| Forward-return horizon | {config.prediction_horizon} sessions |
| Portfolio size | {config.top_k} names |
| Minimum training history | {config.min_training_sessions} sessions |
| Ridge alpha | {config.ridge_alpha:g} |
| Initial cash | {config.initial_cash:,.0f} |
| Transaction cost | {config.transaction_cost_bps:.1f} bps per traded notional |
| Round lot | {config.lot_size} shares |

## Results

| Metric | Value |
| --- | ---: |
| Total return | {_pct(float(metrics["total_return"]))} |
| CAGR | {_pct(float(metrics["cagr"]))} |
| Maximum drawdown | {_pct(float(metrics["max_drawdown"]))} |
| Annualized volatility | {_pct(float(metrics["annualized_volatility"]))} |
| Sharpe, zero rate | {float(metrics["sharpe_zero_rate"]):.2f} |
| Mean rank IC | {float(metrics["mean_rank_ic"]):.3f} |
| Signals | {int(metrics["signal_count"])} |
| Trades | {int(metrics["trade_count"])} |
| Transaction cost | {float(metrics["transaction_cost"]):,.0f} |
| Annualized turnover | {float(metrics["annualized_turnover"]):.2f}x |

## Diagnostics

![Equity curve](equity_curve.svg)

![Drawdown](drawdown.svg)

![Rank IC](rank_ic.svg)

![Model coefficients](model_coefficients.svg)

## Timing and leakage controls

- Features at date `t` use data at or before `t`.
- A forward label enters training only when `label_available_date <= signal_date`.
- Portfolio targets formed on a signal date execute at the next available session open.
- Transaction costs and round-lot constraints are applied during execution.

## Data lineage

The generated dataset contains {result.manifest.rows:,} rows across
{result.manifest.symbols} symbols from {result.manifest.first_date} to
{result.manifest.last_date}. Its deterministic fingerprint is
`{result.manifest.sha256}`.

## Interpretation

The synthetic generator intentionally contains persistent cross-sectional structure
so that the complete research stack can be tested. Performance values therefore
describe this deterministic software fixture only. They must not be presented as
historical Vietnamese-market performance.
"""
    report_path = output / "research_report.md"
    report_path.write_text(report, encoding="utf-8")
    return report_path
