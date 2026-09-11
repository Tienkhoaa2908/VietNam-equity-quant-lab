from __future__ import annotations

import math

import pandas as pd


def performance_summary(nav: pd.DataFrame) -> dict[str, float]:
    """Compute standard performance statistics from a daily NAV series."""

    if nav.empty:
        raise ValueError("NAV series is empty")
    series = nav.set_index("date")["nav"].astype(float).sort_index()
    returns = series.pct_change().dropna()
    elapsed_days = max((series.index[-1] - series.index[0]).days, 1)
    years = elapsed_days / 365.25
    total_return = series.iloc[-1] / series.iloc[0] - 1.0
    cagr = (series.iloc[-1] / series.iloc[0]) ** (1.0 / years) - 1.0 if years > 0 else 0.0
    rolling_peak = series.cummax()
    drawdown = series / rolling_peak - 1.0
    annualized_volatility = returns.std(ddof=0) * math.sqrt(252.0) if len(returns) else 0.0
    annualized_return = returns.mean() * 252.0 if len(returns) else 0.0
    sharpe = annualized_return / annualized_volatility if annualized_volatility > 1e-12 else 0.0
    return {
        "starting_nav": float(series.iloc[0]),
        "ending_nav": float(series.iloc[-1]),
        "total_return": float(total_return),
        "cagr": float(cagr),
        "annualized_volatility": float(annualized_volatility),
        "max_drawdown": float(drawdown.min()),
        "sharpe_zero_rate": float(sharpe),
    }
