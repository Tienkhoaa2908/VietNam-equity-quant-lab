# Research methodology

## Timing contract

Features are computed from observations available at or before each row timestamp. Model labels use future returns only during training and include an explicit `label_available_date`. A training row is eligible only when the full label horizon is observable by the model fit date.

![Causal timeline](assets/causal_timeline.svg)

Signals are formed after the close of the signal session. Backtest execution begins at the next available market-session open.

## Validation

Model development uses chronological windows. Random train-test splitting is not used for strategy validation because it breaks the information ordering of financial time series.

## Portfolio evaluation

The public backtester includes:

- next-session-open execution;
- explicit transaction costs;
- round-lot sizing;
- residual cash accounting;
- daily close mark-to-market NAV;
- turnover through recorded trades;
- total return, CAGR, volatility, maximum drawdown, and zero-rate Sharpe ratio.

## Model scope

The included Ridge model is a transparent reference model. It is not presented as a production alpha model. The purpose of the implementation is to demonstrate the research contract from data ingestion through causal evaluation.
