# Architecture

The repository uses a `src` package layout and separates market data, features, models, portfolio construction, execution simulation, and realtime freshness checks.

![System pipeline](assets/system_pipeline.svg)

## Package boundaries

| Package | Responsibility |
| --- | --- |
| `data` | Source interfaces, schema validation, deterministic synthetic data |
| `features` | Backward-looking technical features and cross-sectional normalization |
| `models` | Forward labels, causal training, walk-forward split utilities |
| `portfolio` | Cross-sectional ranking and target weights |
| `backtest` | Next-session execution, costs, lot sizing, daily NAV accounting |
| `realtime` | Independent freshness checks for market data and broker state |
| `research` | End-to-end orchestration |

Provider-specific code is kept outside the research core. This prevents source authentication, broker state, and vendor-specific data formats from becoming implicit assumptions in model code.
