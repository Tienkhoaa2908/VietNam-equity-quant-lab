# Contributing

Changes should preserve the repository's causal research contract and reproducibility.

## Development workflow

1. Create a branch from `main`.
2. Install `.[dev,report]`.
3. Add or update tests for behavioral changes.
4. Run `make lint` and `make test`.
5. Keep datasets, credentials, account identifiers, broker payloads, and proprietary data out of the repository.

## Research changes

A research change should state the information timestamp, label timestamp, execution timestamp, cost assumptions, and evaluation period. Do not introduce random train/test splits for time-series evaluation or same-close execution for close-derived signals.
