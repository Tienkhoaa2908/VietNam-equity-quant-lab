from __future__ import annotations

from dataclasses import dataclass
import math

import pandas as pd


@dataclass(frozen=True)
class BacktestResult:
    nav: pd.DataFrame
    trades: pd.DataFrame
    holdings: pd.DataFrame


def _next_session_map(dates: list[pd.Timestamp]) -> dict[pd.Timestamp, pd.Timestamp]:
    return {dates[index]: dates[index + 1] for index in range(len(dates) - 1)}


def _round_lot_shares(value: float, price: float, lot_size: int) -> int:
    if value <= 0 or price <= 0:
        return 0
    return int(math.floor(value / price / lot_size) * lot_size)


def run_next_open_backtest(
    market: pd.DataFrame,
    targets: pd.DataFrame,
    *,
    initial_cash: float,
    transaction_cost_bps: float,
    lot_size: int,
) -> BacktestResult:
    """Simulate target rebalances at the next session open after each signal date."""
    dates = sorted(pd.to_datetime(market["date"].unique()))
    next_session = _next_session_map(dates)
    price = market.set_index(["date", "symbol"])[["open", "close"]].sort_index()
    targets_by_execution: dict[pd.Timestamp, pd.DataFrame] = {}
    for signal_date, group in targets.groupby("date", sort=True):
        execution = next_session.get(pd.Timestamp(signal_date))
        if execution is not None:
            targets_by_execution[execution] = group.copy()

    cash = float(initial_cash)
    shares: dict[str, int] = {}
    trade_rows: list[dict[str, object]] = []
    nav_rows: list[dict[str, object]] = []
    holding_rows: list[dict[str, object]] = []
    cost_rate = transaction_cost_bps / 10_000.0

    for date in dates:
        day_prices = price.loc[date]
        if date in targets_by_execution:
            target_frame = targets_by_execution[date]
            target_weights = dict(
                zip(target_frame["symbol"], target_frame["target_weight"], strict=True)
            )
            equity_open = cash
            for symbol, quantity in shares.items():
                if symbol in day_prices.index:
                    equity_open += quantity * float(day_prices.loc[symbol, "open"])

            desired: dict[str, int] = {}
            for symbol, weight in target_weights.items():
                if symbol not in day_prices.index:
                    continue
                open_price = float(day_prices.loc[symbol, "open"])
                desired[symbol] = _round_lot_shares(
                    equity_open * float(weight), open_price, lot_size
                )
            for symbol in list(shares):
                desired.setdefault(symbol, 0)

            deltas = {symbol: desired[symbol] - shares.get(symbol, 0) for symbol in desired}
            for symbol, delta in sorted(deltas.items()):
                if delta >= 0 or symbol not in day_prices.index:
                    continue
                open_price = float(day_prices.loc[symbol, "open"])
                quantity = -delta
                notional = quantity * open_price
                cost = notional * cost_rate
                cash += notional - cost
                shares[symbol] = shares.get(symbol, 0) - quantity
                trade_rows.append(
                    {
                        "date": date,
                        "symbol": symbol,
                        "side": "SELL",
                        "quantity": quantity,
                        "price": open_price,
                        "notional": notional,
                        "cost": cost,
                    }
                )

            for symbol, delta in sorted(deltas.items()):
                if delta <= 0 or symbol not in day_prices.index:
                    continue
                open_price = float(day_prices.loc[symbol, "open"])
                affordable_lots = int(cash // (open_price * lot_size * (1.0 + cost_rate)))
                requested_lots = delta // lot_size
                buy_lots = max(0, min(requested_lots, affordable_lots))
                quantity = buy_lots * lot_size
                if quantity <= 0:
                    continue
                notional = quantity * open_price
                cost = notional * cost_rate
                cash -= notional + cost
                shares[symbol] = shares.get(symbol, 0) + quantity
                trade_rows.append(
                    {
                        "date": date,
                        "symbol": symbol,
                        "side": "BUY",
                        "quantity": quantity,
                        "price": open_price,
                        "notional": notional,
                        "cost": cost,
                    }
                )
            shares = {symbol: quantity for symbol, quantity in shares.items() if quantity > 0}

        market_value = 0.0
        for symbol, quantity in sorted(shares.items()):
            if symbol not in day_prices.index:
                continue
            close_price = float(day_prices.loc[symbol, "close"])
            value = quantity * close_price
            market_value += value
            holding_rows.append(
                {
                    "date": date,
                    "symbol": symbol,
                    "quantity": quantity,
                    "close": close_price,
                    "market_value": value,
                }
            )
        nav_rows.append(
            {
                "date": date,
                "cash": cash,
                "market_value": market_value,
                "nav": cash + market_value,
            }
        )

    return BacktestResult(
        nav=pd.DataFrame(nav_rows),
        trades=pd.DataFrame(trade_rows),
        holdings=pd.DataFrame(holding_rows),
    )
