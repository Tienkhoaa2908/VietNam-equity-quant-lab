from vn_equity_quant.realtime import ExecutionGateInput, evaluate_manual_entry_gate


def _state(**changes):
    payload = dict(
        market_window_open=True,
        transport_connected=True,
        authenticated=True,
        subscriptions_active=True,
        heartbeat_healthy=True,
        trade_age_seconds=1.0,
        bbo_age_seconds=1.0,
        broker_age_seconds=10.0,
        best_ask=25_000.0,
    )
    payload.update(changes)
    return ExecutionGateInput(**payload)


def test_gate_ready_when_all_inputs_are_fresh() -> None:
    result = evaluate_manual_entry_gate(_state())
    assert result.ready
    assert result.buy_reference == 25_000.0


def test_fresh_trade_does_not_rescue_stale_bbo() -> None:
    result = evaluate_manual_entry_gate(_state(trade_age_seconds=0.1, bbo_age_seconds=90.0))
    assert not result.ready
    assert "BBO_STALE_OR_MISSING" in result.reasons


def test_closed_market_fails_closed() -> None:
    result = evaluate_manual_entry_gate(_state(market_window_open=False))
    assert not result.ready
    assert "MARKET_WINDOW_CLOSED" in result.reasons
