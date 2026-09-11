from __future__ import annotations

import argparse
import json
from pathlib import Path

from vn_equity_quant.config import load_research_config
from vn_equity_quant.data import CSVMarketDataSource, SyntheticMarketDataSource, build_manifest
from vn_equity_quant.research import run_research_pipeline


def _run(config_path: str):
    config = load_research_config(config_path)
    source = SyntheticMarketDataSource(
        symbol_count=config.symbol_count,
        sessions=config.sessions,
        seed=config.seed,
    )
    return config, run_research_pipeline(source, config)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="vnq", description="Vietnam Equity Quant Lab")
    subparsers = parser.add_subparsers(dest="command", required=True)

    demo = subparsers.add_parser("demo", help="run deterministic research pipeline")
    demo.add_argument("--config", default="configs/research_demo.toml")
    demo.add_argument("--json", dest="json_path")

    report = subparsers.add_parser("report", help="generate deterministic research report")
    report.add_argument("--config", default="configs/research_demo.toml")
    report.add_argument("--output", required=True)

    validate = subparsers.add_parser("validate", help="validate an OHLCV CSV")
    validate.add_argument("--csv", required=True)
    return parser


def main() -> None:
    args = _parser().parse_args()
    if args.command == "validate":
        frame = CSVMarketDataSource(args.csv).load()
        print(build_manifest(frame).to_json())
        return

    config, result = _run(args.config)
    if args.command == "report":
        from vn_equity_quant.reporting import write_research_report

        path = write_research_report(result, config, args.output)
        print(path)
        return

    payload = {
        "data_manifest": result.manifest.to_dict(),
        "metrics": result.metrics,
        "latest_coefficients": result.latest_coefficients,
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True, allow_nan=True)
    print(rendered)
    if args.json_path:
        path = Path(args.json_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
