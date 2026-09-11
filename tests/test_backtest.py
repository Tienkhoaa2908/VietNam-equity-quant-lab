import pandas as pd

from vn_equity_quant.backtest import ExecutionAwareBacktester
from vn_equity_quant.data import SyntheticMarketDataSource


def test_signal_executes_on_next_market_session() -> None:
    market = SyntheticMarketDataSource(symbol_count=2, sessions=40, seed=9).load()
    dates = pd.DatetimeIndex(market["date"].drop_duplicates()).sort_values()
    signal_date = dates[10]
    targets = pd.DataFrame(
        [
            {"date": signal_date, "symbol": "VN01", "target_weight": 0.5},
            {"date": signal_date, "symbol": "VN02", "target_weight": 0.5},
        ]
    )
    result = ExecutionAwareBacktester(
        initial_nav=100_000_000,
        transaction_cost_bps=10,
        lot_size=100,
    ).run(market, targets)

    buys = result.trades[result.trades["side"] == "BUY"]
    assert not buys.empty
    assert pd.Timestamp(buys["date"].min()) == dates[11]
    assert pd.Timestamp(buys["date"].min()) > signal_date
