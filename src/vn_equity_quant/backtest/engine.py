from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class BacktestResult:
    nav: pd.DataFrame
    trades: pd.DataFrame


class ExecutionAwareBacktester:
    """Daily mark-to-market backtester with next-session-open rebalancing.

    Signals are assumed to be finalized after the close on the signal date.
    Portfolio changes are therefore executed no earlier than the next available
    market session open.
    """

    def __init__(
        self,
        *,
        initial_nav: float = 1_000_000_000.0,
        transaction_cost_bps: float = 10.0,
        lot_size: int = 100,
    ) -> None:
        if initial_nav <= 0:
            raise ValueError("initial_nav must be positive")
        if transaction_cost_bps < 0:
            raise ValueError("transaction_cost_bps must be non-negative")
        if lot_size <= 0:
            raise ValueError("lot_size must be positive")
        self.initial_nav = float(initial_nav)
        self.cost_rate = float(transaction_cost_bps) / 10_000.0
        self.lot_size = int(lot_size)

    def run(self, market: pd.DataFrame, targets: pd.DataFrame) -> BacktestResult:
        prices = market.sort_values(["date", "symbol"]).copy()
        dates = pd.DatetimeIndex(prices["date"].drop_duplicates()).sort_values()
        if len(dates) < 2:
            raise ValueError("at least two market sessions are required")

        open_px = prices.pivot(index="date", columns="symbol", values="open").sort_index()
        close_px = prices.pivot(index="date", columns="symbol", values="close").sort_index()

        schedule: dict[pd.Timestamp, pd.DataFrame] = {}
        for signal_date, group in targets.groupby("date"):
            signal_date = pd.Timestamp(signal_date)
            future = dates[dates > signal_date]
            if len(future) == 0:
                continue
            schedule[future[0]] = group.copy()

        cash = self.initial_nav
        holdings: dict[str, int] = {}
        nav_rows: list[dict[str, object]] = []
        trades: list[dict[str, object]] = []

        for date in dates:
            if date in schedule:
                cash, holdings, event_trades = self._rebalance(
                    date=date,
                    target_rows=schedule[date],
                    open_prices=open_px.loc[date],
                    cash=cash,
                    holdings=holdings,
                )
                trades.extend(event_trades)

            marked_value = cash
            for symbol, quantity in holdings.items():
                price = close_px.at[date, symbol] if symbol in close_px.columns else np.nan
                if np.isfinite(price):
                    marked_value += quantity * float(price)
            nav_rows.append({"date": date, "nav": float(marked_value), "cash": float(cash)})

        return BacktestResult(nav=pd.DataFrame(nav_rows), trades=pd.DataFrame(trades))

    def _rebalance(
        self,
        *,
        date: pd.Timestamp,
        target_rows: pd.DataFrame,
        open_prices: pd.Series,
        cash: float,
        holdings: dict[str, int],
    ) -> tuple[float, dict[str, int], list[dict[str, object]]]:
        event_trades: list[dict[str, object]] = []

        for symbol, quantity in list(holdings.items()):
            price = float(open_prices.get(symbol, np.nan))
            if quantity <= 0 or not np.isfinite(price) or price <= 0:
                continue
            gross = quantity * price
            fee = gross * self.cost_rate
            cash += gross - fee
            event_trades.append(
                {
                    "date": date,
                    "symbol": symbol,
                    "side": "SELL",
                    "quantity": quantity,
                    "price": price,
                    "gross_value": gross,
                    "cost": fee,
                }
            )
        holdings = {}

        usable = target_rows.dropna(subset=["target_weight"]).copy()
        usable = usable[usable["symbol"].isin(open_prices.index)]
        if usable.empty:
            return cash, holdings, event_trades

        nav_at_open = cash
        for row in usable.itertuples(index=False):
            symbol = str(row.symbol)
            price = float(open_prices.get(symbol, np.nan))
            weight = float(row.target_weight)
            if not np.isfinite(price) or price <= 0 or weight <= 0:
                continue
            budget = nav_at_open * weight
            all_in_lot_cost = price * self.lot_size * (1.0 + self.cost_rate)
            lots = int(budget // all_in_lot_cost)
            quantity = lots * self.lot_size
            if quantity <= 0:
                continue
            gross = quantity * price
            fee = gross * self.cost_rate
            total = gross + fee
            if total > cash + 1e-9:
                continue
            cash -= total
            holdings[symbol] = quantity
            event_trades.append(
                {
                    "date": date,
                    "symbol": symbol,
                    "side": "BUY",
                    "quantity": quantity,
                    "price": price,
                    "gross_value": gross,
                    "cost": fee,
                }
            )

        return cash, holdings, event_trades
