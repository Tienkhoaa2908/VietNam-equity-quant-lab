# Market data contract

The core package expects long-form OHLCV data with one row per symbol and market session.

| Column | Type | Constraint |
| --- | --- | --- |
| `date` | datetime | market-session date |
| `symbol` | string | non-empty, normalized to uppercase |
| `open` | float | positive |
| `high` | float | not below open, close, or low |
| `low` | float | not above open, close, or high |
| `close` | float | positive |
| `volume` | numeric | non-negative |

Duplicate symbol-session rows are rejected.

The repository does not include proprietary Vietnamese market history, broker account data, or provider credentials. Source adapters are deliberately separated from the research engine. A deterministic synthetic generator is included so the complete pipeline can be executed without external data access.

For real research, a provider adapter should preserve acquisition timestamps, price-adjustment semantics, corporate-action handling, and source revision lineage.
