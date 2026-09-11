import pytest

from vn_equity_quant.data import HTTPMarketDataSource


def test_http_source_requires_https() -> None:
    with pytest.raises(ValueError, match="HTTPS"):
        HTTPMarketDataSource("http://example.com/market.csv")


def test_http_source_requires_positive_timeout() -> None:
    with pytest.raises(ValueError, match="timeout_seconds"):
        HTTPMarketDataSource("https://example.com/market.csv", timeout_seconds=0)
