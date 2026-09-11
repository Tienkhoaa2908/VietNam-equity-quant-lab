from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json

import pandas as pd


@dataclass(frozen=True)
class DataManifest:
    rows: int
    symbols: int
    first_date: str
    last_date: str
    sha256: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)


def frame_fingerprint(frame: pd.DataFrame) -> str:
    canonical = frame.sort_values(["date", "symbol"], kind="mergesort").copy()
    canonical["date"] = pd.to_datetime(canonical["date"]).dt.strftime("%Y-%m-%d")
    payload = canonical.to_csv(index=False, lineterminator="\n", float_format="%.10g")
    return sha256(payload.encode("utf-8")).hexdigest()


def build_manifest(frame: pd.DataFrame) -> DataManifest:
    dates = pd.to_datetime(frame["date"])
    return DataManifest(
        rows=len(frame),
        symbols=int(frame["symbol"].nunique()),
        first_date=dates.min().date().isoformat(),
        last_date=dates.max().date().isoformat(),
        sha256=frame_fingerprint(frame),
    )
