# Project summary for a CV

**Vietnam Equity Quant Lab — Python, pandas, scikit-learn, quantitative research**

Built a reproducible equity-research framework covering market-data validation, feature engineering, chronological model fitting, cross-sectional ranking, portfolio construction, transaction-aware backtesting, data lineage, research reporting and realtime freshness controls.

Implemented explicit anti-leakage contracts: forward labels become trainable only after their full horizon is observable, close-derived signals execute at the next session open, and stale realtime or broker state fails closed.

The public repository is a sanitized technical implementation. Broker credentials, account state, proprietary datasets and production order paths are excluded.
