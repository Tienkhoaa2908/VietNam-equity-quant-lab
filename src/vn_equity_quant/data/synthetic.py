from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .schema import validate_market_frame


@dataclass(frozen=True)
class SyntheticMarketDataSource:
    """Deterministic synthetic OHLCV data for examples and tests.

    The generator creates a shared market component and persistent symbol-level
    drifts. It is not intended to approximate the empirical distribution of the
    Vietnamese equity market.
    """

    symbol_count: int = 30
    sessions: int = 900
    start: str = "2020-01-02"
    seed: int = 42

    def load(self) -> pd.DataFrame:
        rng = np.random.default_rng(self.seed)
        dates = pd.bdate_range(self.start, periods=self.sessions)
        market_shocks = rng.normal(0.0002, 0.009, size=self.sessions)
        rows: list[dict[str, object]] = []

        for index in range(self.symbol_count):
            symbol = f"VN{index + 1:02d}"
            persistent_drift = rng.normal(0.00005, 0.00018)
            idiosyncratic = rng.normal(0.0, 0.012, size=self.sessions)
            returns = market_shocks * rng.uniform(0.7, 1.3) + persistent_drift + idiosyncratic
            close = rng.uniform(18_000, 70_000) * np.exp(np.cumsum(returns))
            overnight = rng.normal(0.0, 0.003, size=self.sessions)
            open_price = close / np.exp(returns) * np.exp(overnight)
            intraday_spread = np.abs(rng.normal(0.006, 0.003, size=self.sessions))
            high = np.maximum(open_price, close) * (1.0 + intraday_spread)
            low = np.minimum(open_price, close) * np.maximum(0.80, 1.0 - intraday_spread)
            volume = rng.lognormal(mean=13.0, sigma=0.55, size=self.sessions).astype(int)

            for day, open_value, high_value, low_value, close_value, volume_value in zip(
                dates, open_price, high, low, close, volume, strict=True
            ):
                rows.append(
                    {
                        "date": day,
                        "symbol": symbol,
                        "open": float(open_value),
                        "high": float(high_value),
                        "low": float(low_value),
                        "close": float(close_value),
                        "volume": int(volume_value),
                    }
                )

        return validate_market_frame(pd.DataFrame(rows))
