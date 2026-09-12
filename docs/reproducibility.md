# Reproducibility

The demonstration is deterministic for a fixed configuration and Python dependency set.

## Reproduce

```bash
python -m pip install -e ".[dev,report]"
pytest
vnq demo --config configs/research_demo.toml
vnq report --config configs/research_demo.toml --output artifacts/local_report
```

The report records a data fingerprint. Re-running with the same configuration and synthetic seed should reproduce the same dataset fingerprint, portfolio path and metrics up to numerical-library precision.

GitHub Actions runs the test suite on Python 3.11, 3.12 and 3.13. A separate reproducibility workflow executes the full deterministic demonstration and verifies that report artifacts are created.
