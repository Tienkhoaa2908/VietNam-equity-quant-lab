from __future__ import annotations

from dataclasses import dataclass
from io import StringIO
from urllib.parse import urlparse

import pandas as pd
import requests

from .schema import validate_market_frame


@dataclass(frozen=True)
class HTTPMarketDataSource:
    """Generic public HTTPS CSV adapter with explicit timeout and no credentials."""

    url: str
    timeout_seconds: float = 20.0
    user_agent: str = "vn-equity-quant-lab/0.2"

    def __post_init__(self) -> None:
        parsed = urlparse(self.url)
        if parsed.scheme.lower() != "https" or not parsed.netloc:
            raise ValueError("url must be an absolute HTTPS URL")
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")

    def load(self) -> pd.DataFrame:
        response = requests.get(
            self.url,
            timeout=self.timeout_seconds,
            headers={"User-Agent": self.user_agent},
        )
        response.raise_for_status()
        return validate_market_frame(pd.read_csv(StringIO(response.text)))
