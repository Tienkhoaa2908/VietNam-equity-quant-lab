import pandas as pd

from vn_equity_quant.data import SyntheticMarketDataSource
from vn_equity_quant.features import build_technical_features


def test_past_features_do_not_change_when_future_rows_are_appended() -> None:
    source = SyntheticMarketDataSource(symbol_count=3, sessions=320, seed=4)
    full = source.load()
    cutoff = pd.Timestamp(full["date"].drop_duplicates().sort_values().iloc[260])
    prefix = full[full["date"] <= cutoff].copy()

    prefix_features = build_technical_features(prefix)
    full_features = build_technical_features(full)
    full_prefix = full_features[full_features["date"] <= cutoff]

    columns = ["date", "symbol", "momentum_20", "momentum_60", "volatility_20"]
    pd.testing.assert_frame_equal(
        prefix_features[columns].reset_index(drop=True),
        full_prefix[columns].reset_index(drop=True),
        check_dtype=False,
    )
