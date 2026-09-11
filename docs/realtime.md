# Realtime execution-reference controls

The realtime module demonstrates a fail-closed manual execution gate. It does not place orders.

The gate tracks market and broker state independently. A manual entry reference is available only when the required conditions are current:

- market window is open;
- transport is connected;
- public feed authentication is valid;
- subscriptions are active;
- heartbeat is current;
- best bid or offer data is fresh;
- broker snapshot is fresh.

Trade freshness and order-book freshness use separate clocks. A recent trade does not make an old bid-offer quote current.

This design keeps realtime execution references separate from historical model selection.
