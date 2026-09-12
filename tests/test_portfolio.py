import pandas as pd

from vn_equity_quant.portfolio import build_equal_weight_targets


def test_top_k_equal_weight_targets() -> None:
    date = pd.Timestamp("2026-01-30")
    predictions = pd.DataFrame(
        {"date": [date] * 4, "symbol": ["A", "B", "C", "D"], "score": [1.0, 4.0, 3.0, 2.0]}
    )
    targets = build_equal_weight_targets(predictions, 2)
    assert targets["symbol"].tolist() == ["B", "C"]
    assert targets["target_weight"].tolist() == [0.5, 0.5]
