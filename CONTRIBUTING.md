# Contributing

Contributions should preserve the causal research contract of the project.

## Development setup

```bash
python -m pip install -e ".[dev]"
pytest
ruff check src tests examples
```

## Requirements

- Keep signal timestamps and execution timestamps explicit.
- Do not use future observations in feature construction.
- Use chronological validation for model selection.
- Include transaction costs in strategy comparisons.
- Add tests for any change to data validation, execution timing, or portfolio accounting.
- Do not add broker credentials, account data, proprietary raw datasets, or live-order mutation code.

Pull requests should state the research assumption being changed and the evidence used to validate it.
