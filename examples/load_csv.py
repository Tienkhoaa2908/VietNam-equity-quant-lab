from vn_equity_quant.data import CSVMarketDataSource, build_manifest

frame = CSVMarketDataSource("data/sample/mini_ohlcv.csv").load()
print(build_manifest(frame).to_json())
