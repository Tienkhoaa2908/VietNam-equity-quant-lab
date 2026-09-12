from __future__ import annotations

import json

from vn_equity_quant.config import ResearchConfig
from vn_equity_quant.data import SyntheticMarketDataSource
from vn_equity_quant.research import run_research_pipeline

config = ResearchConfig()
source = SyntheticMarketDataSource(
    symbol_count=config.symbol_count,
    sessions=config.sessions,
    seed=config.seed,
)
result = run_research_pipeline(source, config)
print(json.dumps(result.metrics, indent=2, sort_keys=True))
