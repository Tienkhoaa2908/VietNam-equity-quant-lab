import pandas as pd

from vn_equity_quant.data import SyntheticMarketDataSource
from vn_equity_quant.models import attach_forward_labels


def test_label_availability_is_horizon_date() -> None:
    market = SyntheticMarketDataSource(symbol_count=1, sessions=20, seed=1).load()
    labeled = attach_forward_labels(market, horizon=5)
    assert labeled.loc[0, "label_available_date"] == labeled.loc[5, "date"]
    expected = labeled.loc[5, "close"] / labeled.loc[0, "close"] - 1.0
    assert abs(labeled.loc[0, "target_forward_return"] - expected) < 1e-12
    assert pd.isna(labeled.iloc[-1]["target_forward_return"])
