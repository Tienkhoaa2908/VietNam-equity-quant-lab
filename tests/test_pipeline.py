from pathlib import Path

from vn_equity_quant.config import ResearchConfig
from vn_equity_quant.data import SyntheticMarketDataSource
from vn_equity_quant.reporting import write_research_report
from vn_equity_quant.research import run_research_pipeline


def test_end_to_end_pipeline_and_report(tmp_path: Path) -> None:
    config = ResearchConfig(
        symbol_count=12,
        sessions=420,
        prediction_horizon=10,
        top_k=4,
        min_training_sessions=180,
        initial_cash=100_000_000.0,
        lot_size=100,
    )
    result = run_research_pipeline(
        SyntheticMarketDataSource(config.symbol_count, config.sessions, seed=11),
        config,
    )
    assert result.metrics["signal_count"] > 0
    assert result.metrics["trade_count"] > 0
    assert result.backtest.nav["nav"].min() > 0
    path = write_research_report(result, config, tmp_path)
    assert path.exists()
    assert (tmp_path / "equity_curve.svg").exists()
    assert (tmp_path / "metrics.json").exists()
