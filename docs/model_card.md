# Model card

## Objective

Rank a cross-section of equities by a fixed-horizon forward-return estimate using information available at the signal date.

## Inputs

The demonstration uses backward-looking price and volume features:

- 21, 63 and 126-session momentum;
- five-session reversal;
- 21-session realized volatility;
- distance from the 126-session high;
- 20-session volume ratio.

Features are winsorized and standardized cross-sectionally on each date.

## Estimator

The public model is Ridge linear regression. It is intentionally transparent: fitted coefficients can be inspected at every signal date, training is deterministic, and the estimator is sufficient to demonstrate chronology, leakage controls and portfolio integration without presenting model complexity as evidence of skill.

## Training policy

Training expands through time. A row is eligible only when its complete forward-return label is observable by the fit date. No random split is used.

## Outputs

The model emits one score per valid symbol on each scheduled signal date. Scores are used for ranking only; they are not interpreted as calibrated return forecasts.

## Known limitations

The committed report uses synthetic data. The model does not include fundamentals, survivorship controls, corporate-action reconstruction, borrow constraints, exchange-specific auction behavior, or a production liquidity model. These omissions are documented rather than hidden behind simulated precision.
