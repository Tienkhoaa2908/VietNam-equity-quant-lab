# Limitations

This repository is a technical research demonstration, not a production trading system.

- The committed report uses synthetic data and does not represent Vietnamese-market performance.
- Commercial market data and broker/account data are intentionally excluded.
- The generic schema does not establish a vendor's raw-versus-adjusted price basis.
- The example does not reconstruct corporate actions or point-in-time index membership.
- The execution model uses next-session open prices with explicit costs but does not simulate queue position, partial fills, price limits, halts or market impact.
- The model is a transparent Ridge baseline, not a claim that linear regression is the preferred production estimator.
- Realtime logic is a readiness gate only and contains no order mutation.

A result is only as credible as its data provenance, causal timing, transaction assumptions and independent evaluation period.
