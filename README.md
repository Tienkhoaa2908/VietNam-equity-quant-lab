# Vietnam Equity Quant Lab

[![CI](https://github.com/Tienkhoaa2908/VietNam-equity-quant-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/Tienkhoaa2908/VietNam-equity-quant-lab/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-3776AB.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A causal, execution-aware quantitative research framework for Vietnamese equities.

This repository presents the core technical methods of a larger private research system. It covers market-data validation, feature engineering, chronological model training, cross-sectional ranking, portfolio construction, transaction-aware backtesting, and realtime freshness controls. Broker credentials, account data, proprietary datasets, and production trading state are not included.

![Research pipeline](docs/assets/system_pipeline.svg)

## Core capabilities

- strict OHLCV schema validation and source abstraction;
- backward-looking momentum, volatility, price-state, and volume features;
- cross-sectional feature normalization;
- forward-return labels with explicit label-availability dates;
- expanding chronological validation utilities;
- transparent Ridge cross-sectional return model;
- top-k ranking and equal-weight portfolio construction;
- next-session-open execution to prevent same-close look-ahead;
- transaction costs, round-lot sizing, residual cash, and daily NAV accounting;
- fail-closed realtime market and broker freshness checks;
- deterministic synthetic data for reproducible tests and examples.

## Research contract

The implementation follows four rules.

1. Features use information available at or before their timestamp.
2. Training labels are used only after the complete forward horizon is observable.
3. Signals formed at session close execute no earlier than the next market-session open.
4. Strategy evaluation includes transaction costs and explicit portfolio accounting.

The timing contract is documented in [Research methodology](docs/methodology.md).

## Repository structure

```text
.
├── src/vn_equity_quant/
│   ├── data/          # source interfaces, schema validation, synthetic data
│   ├── features/      # backward-looking features and cross-sectional transforms
│   ├── models/        # labels, model fitting, chronological validation
│   ├── portfolio/     # ranking and target construction
│   ├── backtest/      # next-session execution and NAV accounting
│   ├── realtime/      # market and broker freshness gates
│   └── research/      # end-to-end research orchestration
├── examples/          # executable research and realtime examples
├── tests/             # causal, accounting, and data-quality tests
├── docs/              # methodology, architecture, data contract, limitations
└── .github/workflows/ # continuous integration
```

The layout follows the same separation of library code, tests, examples, documentation, and automated quality checks used by established scientific Python and quantitative-research projects.

## Quick start

```bash
git clone https://github.com/Tienkhoaa2908/VietNam-equity-quant-lab.git
cd VietNam-equity-quant-lab
python -m venv .venv
```

Activate the environment, then install the package.

```bash
python -m pip install -e ".[dev]"
pytest
python examples/run_research_pipeline.py
```

The example generates deterministic synthetic OHLCV data, builds features, fits the model using causally available labels, creates monthly rankings, and runs the execution-aware backtest.

The same pipeline is available as a console command.

```bash
veql-demo
```

## Pipeline

```python
from vn_equity_quant.config import ResearchConfig
from vn_equity_quant.data import SyntheticMarketDataSource
from vn_equity_quant.research import run_research_pipeline

source = SyntheticMarketDataSource(symbol_count=30, sessions=900, seed=42)
result = run_research_pipeline(source, ResearchConfig())

print(result.metrics)
```

For external market data, implement the `MarketDataSource` protocol or use the CSV adapter described in [Market data contract](docs/data_contract.md).

## Causal execution

![Causal timeline](docs/assets/causal_timeline.svg)

The backtester separates signal formation from execution. A ranking computed after the close at `T` is executed at the next available session open. Tests enforce this behavior.

## Realtime controls

The realtime component is an execution-reference safety layer rather than a trading strategy. It independently checks market-window state, transport, authentication, subscriptions, heartbeat, bid-offer freshness, and broker snapshot freshness.

```python
from vn_equity_quant.realtime import ExecutionGateInput, evaluate_manual_entry_gate

result = evaluate_manual_entry_gate(
    ExecutionGateInput(
        market_window_open=True,
        transport_connected=True,
        authenticated=True,
        subscriptions_active=True,
        heartbeat_healthy=True,
        trade_age_seconds=0.8,
        bbo_age_seconds=1.2,
        broker_age_seconds=35.0,
        best_ask=26_400.0,
    )
)
```

A fresh trade cannot override a stale order book. The gate fails closed when required evidence is missing or stale.

## Documentation

- [Architecture](docs/architecture.md)
- [Research methodology](docs/methodology.md)
- [Market data contract](docs/data_contract.md)
- [Realtime controls](docs/realtime.md)
- [Scope and limitations](docs/limitations.md)

## Quality controls

Continuous integration runs on Python 3.11, 3.12, and 3.13. The test suite covers data validation, no-future feature construction, causal label availability, next-session execution, realtime freshness separation, and the end-to-end pipeline.

```bash
make lint
make test
make demo
```

## License

MIT. See [LICENSE](LICENSE).
