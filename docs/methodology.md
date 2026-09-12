# Research methodology

## Information timing

Every feature is backward-looking. A feature row timestamped `t` may depend on observations at or before `t` only.

## Labels

The model target is a fixed-horizon close-to-close forward return. Each target carries `label_available_date`, the session on which the terminal price required to calculate that target becomes observable. During a fit at date `t`, only rows satisfying `label_available_date <= t` are eligible.

## Validation

Model fitting uses an expanding chronological history. There is no random train/test split. Predictions are generated only on scheduled signal dates after the minimum training-history requirement is reached.

## Portfolio construction

On each signal date, stocks are ranked by predicted forward return. The top `k` valid names receive equal target weights. Equal weighting is transparent and keeps the public example focused on research timing rather than optimizer complexity.

## Execution

A target computed from closing information on date `t` executes no earlier than the next available session open. The simulator applies transaction costs to traded notional, rounds target positions to configured lots, preserves residual cash, and marks the portfolio at each session close.

## Diagnostics

The report includes portfolio metrics and cross-sectional Spearman rank information coefficient. Rank IC is an evaluation diagnostic. It is not fed back into the same historical sample to search for thresholds.
