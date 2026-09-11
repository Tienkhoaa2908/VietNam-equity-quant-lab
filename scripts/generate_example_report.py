from vn_equity_quant.config import load_research_config
from vn_equity_quant.data import SyntheticMarketDataSource
from vn_equity_quant.reporting import write_research_report
from vn_equity_quant.research import run_research_pipeline

config = load_research_config("configs/research_demo.toml")
source = SyntheticMarketDataSource(config.symbol_count, config.sessions, seed=config.seed)
result = run_research_pipeline(source, config)
print(write_research_report(result, config, "artifacts/example_report"))
