from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import pandas as pd

from .schema import validate_market_frame


class MarketDataSource(Protocol):
    """Interface for a source that returns long-form OHLCV data."""

    def load(self) -> pd.DataFrame: ...


@dataclass(frozen=True)
class CSVMarketDataSource:
    path: Path

    def load(self) -> pd.DataFrame:
        return validate_market_frame(pd.read_csv(self.path))
