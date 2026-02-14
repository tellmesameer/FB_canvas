# 11. Non-Functional Requirements (NFR)

## 1. Performance & Latency Targets

### 1.1 Real-Time Latency
*   **Broadcast Latency**: < 100ms for state propagation (Drag/Move updates).
*   **Cursor Updates**: < 100ms (Throttled at 10hz).
*   **Input Lag**: < 50ms (Optimistic UI updates required).

### 1.2 Throughput & Capacity
*   **Concurrent Users per Room**: 30 active users (Soft limit), 50 max (Hard limit).
*   **Concurrent Rooms**: MVP target of 5 concurrent active rooms on single instance.
*   **Event Throughput**:
    *   30 users * 10 cursor updates/sec = 300 msgs/sec ingress.
    *   Fan-out: 300 * 30 = 9,000 msgs/sec egress (requires batching/throttling).

## 2. Reliability & Availability

### 2.1 Recovery Time Objective (RTO)
*   **Server Restart**: < 5 seconds to recover last snapshot.
*   **State Recovery**: Room state restored from last Autosave (max 30s data loss).

### 2.2 Availability
*   **Uptime**: 99.5% for MVP.
*   **Circuit Breakers**: Redis and DB connections must fail fast to protect core loop.

## 3. Scalability Constraints

### 3.1 Resource Limits
*   **Max Players per Room**: 22 active on field + 10 subs = 32 max entities.
*   **Max JSON Snapshot Size**: 1 MB.
*   **Max WebSocket Message Size**: 16 KB.

### 3.2 Backpressure
*   **Outbound Queue**: Max 100 pending messages per client.
*   **Slow Consumers**: Disconnect client if queue exceeds limit > 5 seconds.

## 4. Data Retention & Compliance

### 4.1 Persistence
*   **Autosave Interval**: 30 seconds default.
*   **Room TTL**: 90 minutes + 30 minutes grace period.
*   **Data Cleanup**: Expired rooms deleted/archived after 24 hours.

## 5. Security NFRs

*   **Rate Limiting**:
    *   **IP Limit**: Default 20 connections per IP (Configurable via `MAX_CONNECTIONS_PER_IP`).
    *   **User Limit**: 1 active connection per `user_id`.
    *   **Room Limit**: Max 30 users per room.
*   **Input Validation**: Strict type checking on all JSON payloads.

*   **DOS Protection**: Max drag event rate 20/sec per user.

---

# 6. Cross-References

*   **Monitoring**: [12-Deployment-Plan.md](12-Deployment-Plan.md).
*   **Risk Context**: [13-Risk-Register.md](13-Risk-Register.md).
*   **Design Constraints**: [01-BRD.md](01-BRD.md).

