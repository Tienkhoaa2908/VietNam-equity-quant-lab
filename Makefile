.PHONY: install lint test coverage demo report all

install:
	python -m pip install -e ".[dev,report]"

lint:
	ruff check src tests examples scripts
	ruff format --check src tests examples scripts

test:
	pytest

coverage:
	pytest --cov=vn_equity_quant --cov-report=term-missing

demo:
	vnq demo --config configs/research_demo.toml

report:
	vnq report --config configs/research_demo.toml --output artifacts/local_report

all: lint test demo
