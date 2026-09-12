# Vietnam Equity Quant Lab

[![CI](https://github.com/Tienkhoaa2908/VietNam-equity-quant-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/Tienkhoaa2908/VietNam-equity-quant-lab/actions/workflows/ci.yml)
[![Reproducibility](https://github.com/Tienkhoaa2908/VietNam-equity-quant-lab/actions/workflows/reproducibility.yml/badge.svg)](https://github.com/Tienkhoaa2908/VietNam-equity-quant-lab/actions/workflows/reproducibility.yml)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Quantitative equity research framework built around causal features, chronological model fitting, cross-sectional ranking, and execution-aware backtesting.

> The committed example report uses deterministic synthetic OHLCV data. It is included to verify the research pipeline, not to represent live or historical Vietnamese-market performance.

![Research pipeline](docs/assets/system_pipeline.svg)

## Design

- validated OHLCV ingestion with source lineage and dataset fingerprints;
- backward-looking price, volatility, position, and liquidity features;
- cross-sectional winsorization and normalization;
- forward-return labels with explicit availability dates;
- expanding chronological model fitting with Ridge regression;
- rank-IC diagnostics and top-k portfolio construction;
- next-session-open execution with round lots, transaction costs, residual cash, and continuous NAV;
- fail-closed handling of missing prices and stale realtime inputs;
- deterministic CLI reports and automated reproducibility checks.

## Research timing

A signal formed from session `t` may use information available by the close of `t`. Execution occurs no earlier than the next market-session open. A forward label is used for training only after its full horizon is observable.

![Causal timeline](docs/assets/causal_timeline.svg)

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev,report]"
pytest
```

Run the deterministic research example:

```bash
vnq demo --config configs/research_demo.toml
```

Generate the report:

```bash
vnq report --config configs/research_demo.toml --output artifacts/local_report
```

Validate an OHLCV CSV:

```bash
vnq validate --csv data/sample/mini_ohlcv.csv
```

## Example output

![Synthetic equity curve](artifacts/example_report/equity_curve.svg)

| Artifact | Path |
| --- | --- |
| Research report | [`artifacts/example_report/research_report.md`](artifacts/example_report/research_report.md) |
| Metrics | [`artifacts/example_report/metrics.json`](artifacts/example_report/metrics.json) |
| Drawdown | [`artifacts/example_report/drawdown.svg`](artifacts/example_report/drawdown.svg) |
| Rank IC | [`artifacts/example_report/rank_ic.svg`](artifacts/example_report/rank_ic.svg) |
| Model coefficients | [`artifacts/example_report/model_coefficients.svg`](artifacts/example_report/model_coefficients.svg) |

## Project structure

```text
configs/                  reproducible research settings
data/sample/              small schema example
docs/                     methodology and technical contracts
examples/                 executable examples
artifacts/example_report/ deterministic generated report
scripts/                  data and report utilities
src/vn_equity_quant/      research library
tests/                    causal, accounting and integration tests
```

The implementation is split into data, features, models, portfolio construction, backtesting, realtime readiness, reporting, and end-to-end research orchestration.

## Verification

CI runs linting, formatting checks, dependency checks, package installation, and tests on Python 3.11, 3.12, and 3.13. A separate workflow reruns the deterministic pipeline and verifies the generated artifacts.

Local checks:

```bash
make lint
make test
make report
```

## Documentation

- [Architecture](docs/architecture.md)
- [Methodology](docs/methodology.md)
- [Data contract](docs/data_contract.md)
- [Data sources](docs/data_sources.md)
- [Model card](docs/model_card.md)
- [Backtest contract](docs/backtest_contract.md)
- [Realtime readiness](docs/realtime.md)
- [Reproducibility](docs/reproducibility.md)
- [Limitations](docs/limitations.md)

## Scope

The repository contains research and simulation code only. It does not include broker credentials, account data, proprietary datasets, production state, or order-submission logic. Commercial Vietnamese market data is not redistributed.

## License

MIT. See [LICENSE](LICENSE).
