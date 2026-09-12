from pathlib import Path

from vn_equity_quant.data import SyntheticMarketDataSource

output = Path("data/sample/mini_ohlcv.csv")
output.parent.mkdir(parents=True, exist_ok=True)
frame = SyntheticMarketDataSource(symbol_count=4, sessions=12, seed=7).load()
frame.to_csv(output, index=False)
print(output)
