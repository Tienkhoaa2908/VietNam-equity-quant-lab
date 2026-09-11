from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge

from vn_equity_quant.features.cross_sectional import MODEL_FEATURES


@dataclass
class RidgeCrossSectionalModel:
    alpha: float = 10.0
    feature_names: tuple[str, ...] = MODEL_FEATURES
    _model: Ridge = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._model = Ridge(alpha=self.alpha, fit_intercept=True)

    def fit(self, frame: pd.DataFrame, as_of: pd.Timestamp) -> RidgeCrossSectionalModel:
        cutoff = pd.Timestamp(as_of).normalize()
        eligible = frame[
            frame["label_available_date"].notna()
            & (frame["label_available_date"] <= cutoff)
            & frame["target_forward_return"].notna()
        ].dropna(subset=list(self.feature_names))
        if len(eligible) < 100:
            raise ValueError("insufficient causally available training rows")
        self._model.fit(
            eligible.loc[:, self.feature_names].to_numpy(dtype=float),
            eligible["target_forward_return"].to_numpy(dtype=float),
        )
        return self

    def predict(self, frame: pd.DataFrame) -> pd.Series:
        output = pd.Series(np.nan, index=frame.index, dtype=float)
        valid = frame.dropna(subset=list(self.feature_names))
        if not valid.empty:
            output.loc[valid.index] = self._model.predict(
                valid.loc[:, self.feature_names].to_numpy(dtype=float)
            )
        return output

    @property
    def coefficients(self) -> dict[str, float]:
        return dict(zip(self.feature_names, self._model.coef_, strict=True))
