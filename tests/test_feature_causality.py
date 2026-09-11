import pandas as pd

from vn_equity_quant.data import SyntheticMarketDataSource
from vn_equity_quant.features import build_time_series_features


def test_future_price_change_does_not_change_past_features() -> None:
    market = SyntheticMarketDataSource(symbol_count=2, sessions=180, seed=8).load()
    original = build_time_series_features(market)
    cutoff = pd.Timestamp(market["date"].sort_values().unique()[150])
    changed = market.copy()
    changed.loc[changed["date"] > cutoff, "close"] *= 3.0
    recomputed = build_time_series_features(changed)
    columns = ["momentum_21", "momentum_63", "momentum_126", "volatility_21"]
    left = original[original["date"] <= cutoff].reset_index(drop=True)[columns]
    right = recomputed[recomputed["date"] <= cutoff].reset_index(drop=True)[columns]
    pd.testing.assert_frame_equal(left, right)
