# Realtime readiness

Realtime state is evaluated independently from historical model research.

A manual execution reference is ready only when all required conditions are true:

- the expected market window is open;
- transport is connected;
- the public feed is authenticated;
- subscriptions are active;
- heartbeat is healthy;
- the order book is fresh;
- the broker snapshot is fresh;
- a valid best ask exists.

Trade freshness and order-book freshness are separate concepts. A recent trade does not make an old best bid or offer current.

When any requirement fails, the gate returns `BLOCKED_FAIL_CLOSED` and an explicit reason list. The module does not submit, cancel or replace broker orders.
