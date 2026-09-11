import pandas as pd

from vn_equity_quant.data import SyntheticMarketDataSource
from vn_equity_quant.features import build_technical_features, cross_sectional_standardize
from vn_equity_quant.models import RidgeCrossSectionalModel, add_forward_return_labels


def test_model_uses_only_labels_available_by_as_of_date() -> None:
    market = SyntheticMarketDataSource(symbol_count=8, sessions=360, seed=11).load()
    frame = add_forward_return_labels(
        cross_sectional_standardize(build_technical_features(market)), horizon=20
    )
    dates = pd.DatetimeIndex(frame["date"].drop_duplicates()).sort_values()
    as_of = dates[300]
    model = RidgeCrossSectionalModel(alpha=1.0).fit(frame, as_of=as_of)
    assert model.coefficients

    eligible = frame[
        frame["label_available_date"].notna() & (frame["label_available_date"] <= as_of)
    ]
    assert not eligible.empty
    assert eligible["label_available_date"].max() <= as_of
