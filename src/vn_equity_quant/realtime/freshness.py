from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionGateInput:
    market_window_open: bool
    transport_connected: bool
    authenticated: bool
    subscriptions_active: bool
    heartbeat_healthy: bool
    trade_age_seconds: float | None
    bbo_age_seconds: float | None
    broker_age_seconds: float | None
    best_ask: float | None


@dataclass(frozen=True)
class ExecutionGateResult:
    ready: bool
    state: str
    reasons: tuple[str, ...]


def evaluate_manual_entry_gate(
    state: ExecutionGateInput,
    *,
    max_quote_age_seconds: float = 30.0,
    max_broker_age_seconds: float = 300.0,
) -> ExecutionGateResult:
    """Evaluate a fail-closed manual entry-reference gate.

    Trade and BBO clocks are deliberately separate. A fresh last trade cannot
    make an old order book fresh.
    """

    reasons: list[str] = []
    if not state.market_window_open:
        reasons.append("MARKET_WINDOW_CLOSED")
    if not state.transport_connected:
        reasons.append("TRANSPORT_DISCONNECTED")
    if not state.authenticated:
        reasons.append("PUBLIC_FEED_NOT_AUTHENTICATED")
    if not state.subscriptions_active:
        reasons.append("SUBSCRIPTIONS_INACTIVE")
    if not state.heartbeat_healthy:
        reasons.append("HEARTBEAT_STALE")
    if state.bbo_age_seconds is None or state.bbo_age_seconds > max_quote_age_seconds:
        reasons.append("BBO_STALE_OR_MISSING")
    if state.best_ask is None or state.best_ask <= 0:
        reasons.append("BEST_ASK_MISSING")
    if state.broker_age_seconds is None or state.broker_age_seconds > max_broker_age_seconds:
        reasons.append("BROKER_SNAPSHOT_STALE_OR_MISSING")

    if reasons:
        return ExecutionGateResult(False, "WAIT_FOR_FRESH_DATA", tuple(reasons))
    return ExecutionGateResult(True, "MANUAL_ENTRY_REFERENCE_READY", ())
