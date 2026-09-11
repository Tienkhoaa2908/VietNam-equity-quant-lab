.PHONY: install lint test demo

install:
	python -m pip install -e ".[dev]"

lint:
	ruff check src tests examples

format:
	ruff format src tests examples

format-check:
	ruff format --check src tests examples

test:
	pytest

demo:
	python examples/run_research_pipeline.py
