# Data-source integration

The public package provides three source patterns.

## Local CSV

`CSVMarketDataSource` is the simplest reproducible adapter. It reads a file and immediately applies the canonical schema validator.

## HTTP CSV

`HTTPMarketDataSource` retrieves a public CSV through HTTPS with an explicit timeout and user agent, then validates the response. It contains no credential handling and is intentionally vendor-neutral.

For a reproducible download outside the research process:

```bash
python scripts/fetch_public_csv.py https://example.org/market.csv data/raw/market.csv
```

The script prints the SHA-256 checksum so an external dataset can be pinned in a research manifest without committing the dataset itself.

## Private or licensed providers

Implement the `MarketDataSource` protocol and return the canonical columns. Provider credentials and proprietary raw data should stay outside Git. Data licensing, corporate-action semantics, historical revision behavior and timestamp provenance remain the responsibility of the provider adapter.
