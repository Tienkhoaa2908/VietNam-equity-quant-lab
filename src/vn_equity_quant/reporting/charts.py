from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def _save(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, format="svg", bbox_inches="tight")
    plt.close(fig)


def equity_chart(nav: pd.DataFrame, path: Path) -> None:
    series = nav.set_index("date")["nav"]
    normalized = series / series.iloc[0]
    fig, ax = plt.subplots(figsize=(9, 4.6))
    ax.plot(normalized.index, normalized.values, linewidth=1.7)
    ax.set_title("Normalized portfolio value")
    ax.set_ylabel("NAV / initial NAV")
    ax.set_xlabel("Date")
    ax.grid(alpha=0.25)
    _save(fig, path)


def drawdown_chart(nav: pd.DataFrame, path: Path) -> None:
    series = nav.set_index("date")["nav"]
    drawdown = series / series.cummax() - 1.0
    fig, ax = plt.subplots(figsize=(9, 4.2))
    ax.fill_between(drawdown.index, drawdown.values, 0.0, alpha=0.35)
    ax.set_title("Portfolio drawdown")
    ax.set_ylabel("Drawdown")
    ax.set_xlabel("Date")
    ax.grid(alpha=0.25)
    _save(fig, path)


def rank_ic_chart(rank_ic: pd.DataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 4.2))
    ax.axhline(0.0, linewidth=1.0)
    ax.plot(rank_ic["date"], rank_ic["rank_ic"], marker="o", markersize=3, linewidth=1.0)
    ax.set_title("Cross-sectional rank information coefficient")
    ax.set_ylabel("Spearman rank IC")
    ax.set_xlabel("Signal date")
    ax.grid(alpha=0.25)
    _save(fig, path)


def coefficient_chart(coefficients: pd.DataFrame, path: Path) -> None:
    latest = coefficients.iloc[-1].drop(labels=["date"])
    fig, ax = plt.subplots(figsize=(9, 4.5))
    latest.sort_values().plot.barh(ax=ax)
    ax.set_title("Latest Ridge coefficients")
    ax.set_xlabel("Coefficient")
    ax.grid(axis="x", alpha=0.25)
    _save(fig, path)
