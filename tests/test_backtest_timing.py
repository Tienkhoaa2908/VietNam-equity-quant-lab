import pandas as pd

from vn_equity_quant.backtest import run_next_open_backtest


def test_signal_executes_next_session_open() -> None:
    market = pd.DataFrame(
        [
            {"date": "2026-01-02", "symbol": "AAA", "open": 10.0, "close": 10.0},
            {"date": "2026-01-05", "symbol": "AAA", "open": 20.0, "close": 21.0},
            {"date": "2026-01-06", "symbol": "AAA", "open": 22.0, "close": 23.0},
        ]
    )
    market["date"] = pd.to_datetime(market["date"])
    targets = pd.DataFrame(
        [{"date": pd.Timestamp("2026-01-02"), "symbol": "AAA", "target_weight": 1.0}]
    )
    result = run_next_open_backtest(
        market,
        targets,
        initial_cash=1_000.0,
        transaction_cost_bps=0.0,
        lot_size=1,
    )
    assert result.trades.iloc[0]["date"] == pd.Timestamp("2026-01-05")
    assert result.trades.iloc[0]["price"] == 20.0
