from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .schema import validate_market_frame


@dataclass(frozen=True)
class CSVMarketDataSource:
    path: str | Path

    def load(self) -> pd.DataFrame:
        return validate_market_frame(pd.read_csv(self.path))
