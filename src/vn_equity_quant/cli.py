from __future__ import annotations

import json

from vn_equity_quant.config import ResearchConfig
from vn_equity_quant.data import SyntheticMarketDataSource
from vn_equity_quant.research import run_research_pipeline


def main() -> None:
    source = SyntheticMarketDataSource()
    result = run_research_pipeline(source, ResearchConfig())
    payload = {
        "dataset": "deterministic synthetic OHLCV",
        "signal_count": int(result.targets["date"].nunique()),
        "trade_count": int(len(result.backtest.trades)),
        "metrics": result.metrics,
        "latest_model_coefficients": result.latest_coefficients,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
