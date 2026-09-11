from __future__ import annotations

from typing import Protocol

import pandas as pd


class MarketDataSource(Protocol):
    """Minimal source interface required by the research pipeline."""

    def load(self) -> pd.DataFrame:
        """Return a validated long-form OHLCV frame."""
        ...
