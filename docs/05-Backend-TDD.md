# 1. Add Explicit Domain Layer (DDD-lite)

Current structure is service-heavy. Introduce clear domain separation.

Add:

```
app/domain/
 ├── entities/
 │    ├── room.py
 │    ├── player.py
 │    ├── team.py
 │    └── lock.py
 ├── value_objects/
 │    ├── position.py
 │    └── match_timer.py
 └── policies/
      ├── movement_policy.py
      └── team_policy.py
```

Benefits:

* Isolates business invariants.
* Makes mutation rules explicit.
* Prevents logic leakage into services.

Room engine becomes orchestrator, not rule container.

---

# 2. Add Explicit Mutation Pipeline

> **Reference:** [SM-LOCK-01](09-State-Machines.md) (Lock SM), [SM-ROOM-01](09-State-Machines.md) (Room SM). (Ref: FRS-DATA-003)

Define deterministic mutation stages:


Define deterministic mutation stages:

1. Validate intent
2. Authorize
3. Acquire lock
4. Apply mutation
5. Increment version
6. Emit domain event
7. Broadcast
8. Persist (if required)

Document this as a state machine.

Add:

```
app/core/mutation_pipeline.py
```

Prevents inconsistent mutation handling.

---

# 3. Introduce Event System (Internal Domain Events)

Add internal event bus:

```
class DomainEvent:
    pass
```

Examples:

* PlayerMoved
* PlayerLocked
* MatchStarted
* FormationSaved

Room engine emits events.
Subscribers handle:

* Logging
* Autosave triggers
* Metrics increment
* Redis publish

Prevents cross-coupling.

---

# 4. Define State Snapshot Strategy Clearly

Add snapshot compression strategy.

Options:

* Full snapshot JSON
* Snapshot + delta chain
* Snapshot every N mutations

Document:

* Max diff size threshold before forced snapshot
* Snapshot memory footprint limits
* Max room state size

Prevents unbounded memory growth.

---

# 5. Add Backpressure Strategy (Ref: WS-PROTO-008)

WebSocket flood protection:

* Drop non-critical events under load (cursor updates first).
* Queue size limit per connection.
* Reject writes when event loop lag > threshold.

Add:

* Max outbound queue length
* Slow consumer detection

Prevents server collapse under burst.

---

# 6. Explicit Resource Limits

> **Moved:** See [11-Non-Functional-Requirements.md](11-Non-Functional-Requirements.md).


Add configurable hard limits:

* Max players per room
* Max formations stored
* Max JSON snapshot size
* Max WebSocket message size
* Max autosave retention versions

Protects from abuse.

---

# 7. Introduce Circuit Breaker for Redis & DB

Retry alone is insufficient.

Add:

* Circuit breaker state:

  * CLOSED
  * OPEN
  * HALF_OPEN

If Redis repeatedly fails:

* Stop attempting temporarily.
* Degrade gracefully.

Prevents cascading failure.

---

# 8. Add Observability Layer

Formalize structured observability:

## Correlation ID

Each connection receives:

```
connection_id
```

Each mutation includes:

```
trace_id
```

Log correlation across:

* WebSocket event
* Mutation
* DB write
* Redis publish

---

## Metrics Instrumentation Plan

Add counters:

* mutation_count
* lock_conflict_count
* version_mismatch_count
* autosave_latency
* redis_publish_latency
* websocket_active_connections

Even if not implemented now, define metric names.

---

# 9. Add Consistency Guarantees Section

Define clearly:

* Linearizability per room (yes).
* Global ordering across rooms (no).
* Lock fairness (first processed wins).
* Idempotency guarantee for formation save.

Formalizing consistency avoids hidden assumptions.

---

# 10. Add Formal State Diagram (Ref: FRS-ROOM-004)

> **Moved:** See [09-State-Machines.md](09-State-Machines.md) [SM-ROOM-01].


Document room lifecycle:

States:

* setup
* live
* expired
* archived

Transitions:

* create_room
* start_match
* timer_expire
* manual_archive

Prevents ambiguous behavior.

---

# 11. Add Formal Lock State Machine (Ref: FRS-LOCK-001)

> **Moved:** See [09-State-Machines.md](09-State-Machines.md) [SM-LOCK-01].


States:

* unlocked
* locked
* expired
* released

Transitions:

* request_lock
* timeout
* release_lock
* disconnect

Prevents lock leakage bugs.

---

# 12. Add Load Modeling Section

Document expected per-room throughput:

* MOVE_UPDATE ~ 20/sec per active drag
* CURSOR_UPDATE ~ 10/sec per user
* STATE_UPDATE broadcast fan-out cost

Calculate theoretical worst case:
30 users × 10 cursor updates/sec = 300 msgs/sec
Add headroom multiplier.

This exposes performance risks early.

---

# 13. Add Time Synchronization Model

Define authoritative time source:

* Server time only.
* Client timestamps ignored for ordering.
* All ordering determined server-side.

Prevents clock skew issues.

---

# 14. Add Migration Strategy

> **Moved:** See [10-Database-Schema-Spec.md](10-Database-Schema-Spec.md) Section 4.


Even with SQLite, define:

* Alembic or migration tool.
* Migration versioning policy.
* Forward-only migration rule.

Prevents schema chaos later.

---

# 15. Add Testability Section

Design for test injection:

* Redis client abstraction interface.
* DB session interface.
* Time provider abstraction.
* UUID provider abstraction.

Enables deterministic unit tests.

---

# 16. Add Memory Management Policy

Define:

* Room cleanup after expiration.
* Formation retention limit.
* Cursor cleanup.
* In-memory state size guard.

Prevents memory leaks.

---

# 17. Add Security Hardening Section

Include:

* WebSocket connection rate limiting per IP.
* Input length validation for display names.
* JSON depth limits.
* Protection against oversized formation snapshots.

---

# 18. Add Upgrade Path to True Distributed Mode

Explicitly document future path:

Phase 1:

* Single instance

Phase 2:

* Redis state externalization

Phase 3:

* Stateless WebSocket nodes
* Dedicated state service

This avoids architectural dead-end.

---

# 19. Add Code Ownership & Module Boundaries

Document:

* Which module can import which.
* Forbid circular dependencies.
* Enforce domain layer independence.

Prevents architectural decay.

---

# 20. Add Explicit Non-Goals

State clearly what system will NOT guarantee:

* No CRDT
* No offline merge resolution
* No eventual consistency across rooms
* No replay event sourcing (for MVP)

Clarity prevents scope creep.

---

# Highest Impact Additions (Priority Order)

1. Mutation pipeline formalization
2. Domain event system
3. Lock state machine documentation
4. Backpressure strategy
5. Consistency guarantees section
6. Circuit breaker implementation
7. Memory management policy

These convert the TDD from functional to robust.

---

If system is expected to evolve beyond MVP, implement the first 7 immediately.

---

# 21. Cross-References

*   **Related Specs**: [03-WebSocket-Protocol-Spec.md](03-WebSocket-Protocol-Spec.md), [04-REST-API-Spec.md](04-REST-API-Spec.md).
*   **Logic Definitions**: [09-State-Machines.md](09-State-Machines.md).
*   **Persistence**: [10-Database-Schema-Spec.md](10-Database-Schema-Spec.md).

