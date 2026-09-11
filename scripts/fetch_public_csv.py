from __future__ import annotations

import argparse
from hashlib import sha256
from pathlib import Path

import requests

parser = argparse.ArgumentParser(description="Download a public CSV with a reproducible checksum")
parser.add_argument("url")
parser.add_argument("output")
args = parser.parse_args()
response = requests.get(args.url, timeout=30, headers={"User-Agent": "vn-equity-quant-lab/0.2"})
response.raise_for_status()
path = Path(args.output)
path.parent.mkdir(parents=True, exist_ok=True)
path.write_bytes(response.content)
print(f"sha256={sha256(response.content).hexdigest()} path={path}")
