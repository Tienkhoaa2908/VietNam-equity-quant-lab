from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib


@dataclass(frozen=True)
class ResearchConfig:
    seed: int = 42
    symbol_count: int = 30
    sessions: int = 900
    prediction_horizon: int = 20
    rebalance_frequency: str = "M"
    top_k: int = 10
    min_training_sessions: int = 252
    ridge_alpha: float = 10.0
    initial_cash: float = 1_000_000_000.0
    transaction_cost_bps: float = 10.0
    lot_size: int = 100

    def validate(self) -> None:
        if self.symbol_count < self.top_k:
            raise ValueError("symbol_count must be at least top_k")
        if self.sessions <= self.min_training_sessions + self.prediction_horizon:
            raise ValueError("sessions are insufficient for training and labels")
        if self.prediction_horizon < 1:
            raise ValueError("prediction_horizon must be positive")
        if self.top_k < 1:
            raise ValueError("top_k must be positive")
        if self.initial_cash <= 0:
            raise ValueError("initial_cash must be positive")
        if self.transaction_cost_bps < 0:
            raise ValueError("transaction_cost_bps cannot be negative")
        if self.lot_size < 1:
            raise ValueError("lot_size must be positive")


def load_research_config(path: str | Path) -> ResearchConfig:
    payload = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    config = ResearchConfig(**payload.get("research", {}))
    config.validate()
    return config
