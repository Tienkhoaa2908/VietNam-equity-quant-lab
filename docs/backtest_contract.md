# Backtest contract

The simulator is designed to make information and execution timing explicit.

1. Model features and ranking are formed at a session close.
2. The target cannot trade at that same close.
3. The earliest execution is the next available session open.
4. Existing positions are sold before new purchases are funded.
5. Purchases are rounded down to the configured lot size.
6. Transaction costs apply to each traded notional.
7. Unused capital remains as cash.
8. End-of-day NAV equals cash plus marked holdings.

The engine is deliberately compact and auditable. It is not a market microstructure simulator. It does not model queue priority, partial fills, price limits, halts or intraday market impact.
