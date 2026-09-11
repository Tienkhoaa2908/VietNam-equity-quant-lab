from vn_equity_quant.realtime import ExecutionGateInput, evaluate_manual_entry_gate

state = ExecutionGateInput(
    market_window_open=True,
    transport_connected=True,
    authenticated=True,
    subscriptions_active=True,
    heartbeat_healthy=True,
    trade_age_seconds=0.8,
    bbo_age_seconds=1.2,
    broker_age_seconds=35.0,
    best_ask=26_400.0,
)

print(evaluate_manual_entry_gate(state))
