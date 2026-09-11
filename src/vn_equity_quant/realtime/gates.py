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
    max_trade_age_seconds: float = 30.0
    max_bbo_age_seconds: float = 10.0
    max_broker_age_seconds: float = 120.0


@dataclass(frozen=True)
class ExecutionGateResult:
    ready: bool
    state: str
    buy_reference: float | None
    reasons: tuple[str, ...]


def _fresh(age: float | None, maximum: float) -> bool:
    return age is not None and 0 <= age <= maximum


def evaluate_manual_entry_gate(state: ExecutionGateInput) -> ExecutionGateResult:
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
        reasons.append("HEARTBEAT_UNHEALTHY")
    if not _fresh(state.bbo_age_seconds, state.max_bbo_age_seconds):
        reasons.append("BBO_STALE_OR_MISSING")
    if not _fresh(state.broker_age_seconds, state.max_broker_age_seconds):
        reasons.append("BROKER_SNAPSHOT_STALE_OR_MISSING")
    if state.best_ask is None or state.best_ask <= 0:
        reasons.append("BEST_ASK_MISSING")

    ready = not reasons
    return ExecutionGateResult(
        ready=ready,
        state="MANUAL_ENTRY_REFERENCE_READY" if ready else "BLOCKED_FAIL_CLOSED",
        buy_reference=float(state.best_ask) if ready and state.best_ask is not None else None,
        reasons=tuple(reasons),
    )
