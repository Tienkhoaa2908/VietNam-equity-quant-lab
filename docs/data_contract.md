# Data contract

The canonical input is one row per symbol and trading session.

| Column | Type | Rule |
| --- | --- | --- |
| `date` | date | normalized trading-session date |
| `symbol` | string | non-empty, upper case after validation |
| `open` | float | positive |
| `high` | float | not below open, close or low |
| `low` | float | not above open, close or high |
| `close` | float | positive |
| `volume` | integer | non-negative |

The validator rejects duplicate date-symbol pairs, missing columns, non-finite values and impossible OHLC relationships.

## Price basis

The public validator does not guess whether vendor prices are raw or adjusted. A production research system should establish one coherent price basis, apply corporate actions causally, and preserve source lineage before using long-horizon historical results as execution evidence.

## Lineage

`build_manifest` records row count, symbol count, first and last dates, and a deterministic SHA-256 fingerprint of the canonical frame. A changed fingerprint means the research input changed and results should be regenerated.
