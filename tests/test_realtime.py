from vn_equity_quant.realtime import ExecutionGateInput, evaluate_manual_entry_gate


def test_fresh_trade_does_not_make_stale_bbo_ready() -> None:
    result = evaluate_manual_entry_gate(
        ExecutionGateInput(
            market_window_open=True,
            transport_connected=True,
            authenticated=True,
            subscriptions_active=True,
            heartbeat_healthy=True,
            trade_age_seconds=0.5,
            bbo_age_seconds=90.0,
            broker_age_seconds=20.0,
            best_ask=30_000.0,
        )
    )
    assert not result.ready
    assert "BBO_STALE_OR_MISSING" in result.reasons


def test_gate_opens_only_when_all_required_inputs_are_fresh() -> None:
    result = evaluate_manual_entry_gate(
        ExecutionGateInput(
            market_window_open=True,
            transport_connected=True,
            authenticated=True,
            subscriptions_active=True,
            heartbeat_healthy=True,
            trade_age_seconds=2.0,
            bbo_age_seconds=2.0,
            broker_age_seconds=30.0,
            best_ask=30_000.0,
        )
    )
    assert result.ready
    assert result.state == "MANUAL_ENTRY_REFERENCE_READY"
