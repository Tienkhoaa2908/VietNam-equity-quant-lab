from __future__ import annotations

from dataclasses import dataclass
from io import StringIO

import pandas as pd
import requests

from .schema import validate_market_frame


@dataclass(frozen=True)
class HTTPMarketDataSource:
    """Generic public CSV adapter with explicit timeout and no credential handling."""

    url: str
    timeout_seconds: float = 20.0
    user_agent: str = "vn-equity-quant-lab/0.2"

    def load(self) -> pd.DataFrame:
        response = requests.get(
            self.url,
            timeout=self.timeout_seconds,
            headers={"User-Agent": self.user_agent},
        )
        response.raise_for_status()
        return validate_market_frame(pd.read_csv(StringIO(response.text)))
