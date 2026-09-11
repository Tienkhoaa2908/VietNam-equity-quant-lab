from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ResearchConfig:
    """Configuration shared by the public research pipeline."""

    prediction_horizon: int = 20
    top_k: int = 10
    min_training_sessions: int = 252
    initial_nav: float = 1_000_000_000.0
    transaction_cost_bps: float = 10.0
    lot_size: int = 100
    ridge_alpha: float = 1.0
    random_state: int = 42
