from vn_equity_quant.data import SyntheticMarketDataSource, build_manifest


def test_data_fingerprint_is_deterministic_and_sensitive() -> None:
    frame = SyntheticMarketDataSource(symbol_count=3, sessions=30, seed=4).load()
    first = build_manifest(frame)
    second = build_manifest(frame.copy())
    assert first.sha256 == second.sha256
    changed = frame.copy()
    changed.loc[0, "close"] *= 1.01
    assert build_manifest(changed).sha256 != first.sha256
