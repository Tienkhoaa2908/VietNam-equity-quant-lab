from __future__ import annotations

import math

import numpy as np
import pandas as pd


def performance_metrics(nav: pd.DataFrame, trades: pd.DataFrame) -> dict[str, float | int]:
    if nav.empty:
        raise ValueError("NAV series is empty")
    series = nav.set_index("date")["nav"].astype(float)
    returns = series.pct_change().dropna()
    total_return = series.iloc[-1] / series.iloc[0] - 1.0
    years = max(len(series) / 252.0, 1.0 / 252.0)
    cagr = (series.iloc[-1] / series.iloc[0]) ** (1.0 / years) - 1.0
    running_max = series.cummax()
    drawdown = series / running_max - 1.0
    annual_vol = returns.std(ddof=0) * math.sqrt(252.0) if not returns.empty else 0.0
    sharpe = (
        returns.mean() / returns.std(ddof=0) * math.sqrt(252.0)
        if len(returns) > 1 and returns.std(ddof=0) > 0
        else 0.0
    )
    traded_notional = float(trades["notional"].sum()) if not trades.empty else 0.0
    transaction_cost = float(trades["cost"].sum()) if not trades.empty else 0.0
    average_nav = float(series.mean())
    annualized_turnover = traded_notional / average_nav / years if average_nav > 0 else np.nan
    return {
        "start_nav": float(series.iloc[0]),
        "end_nav": float(series.iloc[-1]),
        "total_return": float(total_return),
        "cagr": float(cagr),
        "annualized_volatility": float(annual_vol),
        "sharpe_zero_rate": float(sharpe),
        "max_drawdown": float(drawdown.min()),
        "trade_count": int(len(trades)),
        "traded_notional": traded_notional,
        "transaction_cost": transaction_cost,
        "annualized_turnover": float(annualized_turnover),
    }
