from vn_equity_quant.config import ResearchConfig
from vn_equity_quant.data import SyntheticMarketDataSource
from vn_equity_quant.research import run_research_pipeline


def test_pipeline_runs_end_to_end() -> None:
    source = SyntheticMarketDataSource(symbol_count=12, sessions=420, seed=21)
    result = run_research_pipeline(
        source,
        ResearchConfig(
            prediction_horizon=10,
            top_k=5,
            min_training_sessions=180,
            initial_nav=500_000_000,
            transaction_cost_bps=10,
            lot_size=100,
        ),
    )
    assert not result.targets.empty
    assert not result.backtest.nav.empty
    assert result.metrics["ending_nav"] > 0
    assert len(result.latest_coefficients) == 5
