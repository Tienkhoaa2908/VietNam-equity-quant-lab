from pathlib import Path

from vn_equity_quant.data import SyntheticMarketDataSource


output = Path("sample_ohlcv.csv")
SyntheticMarketDataSource(symbol_count=8, sessions=320, seed=7).load().to_csv(output, index=False)
print(output.resolve())
