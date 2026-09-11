import pandas as pd

from vn_equity_quant.data import SyntheticMarketDataSource
from vn_equity_quant.features import build_time_series_features, normalize_cross_section
from vn_equity_quant.models import RidgeCrossSectionalModel, attach_forward_labels


def test_model_ignores_labels_not_available_by_fit_date() -> None:
    market = SyntheticMarketDataSource(symbol_count=8, sessions=320, seed=3).load()
    frame = attach_forward_labels(normalize_cross_section(build_time_series_features(market)), 20)
    fit_date = pd.Timestamp(sorted(frame["date"].unique())[280])
    baseline = RidgeCrossSectionalModel(alpha=5).fit(frame, fit_date).coefficients
    changed = frame.copy()
    mask = changed["label_available_date"] > fit_date
    changed.loc[mask, "target_forward_return"] = 9999.0
    altered = RidgeCrossSectionalModel(alpha=5).fit(changed, fit_date).coefficients
    assert baseline == altered
