from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .schema import validate_market_frame


@dataclass(frozen=True)
class SyntheticMarketDataSource:
    """Deterministic panel used for tests and demonstrations.

    The process contains a shared market component, persistent symbol quality,
    medium-horizon trend and idiosyncratic noise. It is not calibrated to the
    empirical distribution of Vietnamese equities.
    """

    symbol_count: int = 30
    sessions: int = 900
    start: str = "2020-01-02"
    seed: int = 42

    def load(self) -> pd.DataFrame:
        rng = np.random.default_rng(self.seed)
        dates = pd.bdate_range(self.start, periods=self.sessions)
        market = rng.normal(0.00015, 0.008, self.sessions)
        market_trend = pd.Series(market).rolling(20, min_periods=1).mean().to_numpy()
        rows: list[dict[str, object]] = []

        for index in range(self.symbol_count):
            symbol = f"VN{index + 1:02d}"
            quality = rng.normal(0.0, 0.00022)
            beta = rng.uniform(0.7, 1.3)
            idio = rng.normal(0.0, 0.011, self.sessions)
            returns = beta * market + 0.18 * market_trend + quality + idio
            close = rng.uniform(18_000, 70_000) * np.exp(np.cumsum(returns))
            previous_close = np.r_[close[0] / np.exp(returns[0]), close[:-1]]
            overnight = rng.normal(0.0, 0.003, self.sessions)
            open_price = previous_close * np.exp(overnight)
            spread = np.abs(rng.normal(0.006, 0.0025, self.sessions))
            high = np.maximum(open_price, close) * (1.0 + spread)
            low = np.minimum(open_price, close) * np.maximum(0.75, 1.0 - spread)
            volume = rng.lognormal(13.0 + index / 80.0, 0.55, self.sessions).astype(int)

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
