# Architecture

The repository separates data acquisition, feature computation, model fitting, portfolio construction, execution simulation, diagnostics, and reporting. Each layer has a narrow contract and can be tested independently.

```text
Data source
   │
   ▼
Schema validation ──► lineage fingerprint
   │
   ▼
Backward-looking features
   │
   ▼
Cross-sectional normalization
   │
   ▼
Forward labels + availability timestamps
   │
   ▼
Chronological model fit
   │
   ▼
Cross-sectional scores
   │
   ▼
Top-k portfolio targets
   │
   ▼
Next-session-open simulator
   │
   ├── transaction costs
   ├── round lots
   └── residual cash
   │
   ▼
NAV, drawdown, turnover, rank IC, report
```

Realtime readiness is deliberately separate from historical research. It evaluates market-session state, public-feed health, order-book freshness, broker freshness, and the presence of an execution reference. It does not rerank the historical model or submit orders.

The package follows a `src/` layout so imports in tests and examples resolve the installed package rather than the repository working directory.
