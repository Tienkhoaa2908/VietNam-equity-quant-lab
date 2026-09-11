from __future__ import annotations

import json

from vn_equity_quant.config import ResearchConfig
from vn_equity_quant.data import SyntheticMarketDataSource
from vn_equity_quant.research import run_research_pipeline


source = SyntheticMarketDataSource(symbol_count=30, sessions=900, seed=42)
config = ResearchConfig(
    prediction_horizon=20,
    top_k=10,
    min_training_sessions=252,
    transaction_cost_bps=10.0,
    lot_size=100,
)
result = run_research_pipeline(source, config)

print(
    json.dumps(
        {
            "data": "synthetic",
            "signals": int(result.targets["date"].nunique()),
            "trades": int(len(result.backtest.trades)),
            "metrics": result.metrics,
            "latest_coefficients": result.latest_coefficients,
        },
        indent=2,
        sort_keys=True,
    )
)
