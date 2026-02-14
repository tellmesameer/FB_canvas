# 13. Risk Register

| ID | Risk | Impact | Probability | Mitigation Strategy | status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **R-01** | **WebSocket Event Flooding** | High (Server Crash) | Medium | Implement strict rate limiting (10/sec) and leaky bucket algorithm. | planned |
| **R-02** | **Lock Leakage** | Medium (Unmovable players) | Low | Server-side TTL (2s) on all locks + disconnect cleanup handler. | in-progress |
| **R-03** | **Redis Failure** | High (State Loss) | Low | Circuit breaker pattern + Fallback to DB state reload. | planned |
| **R-04** | **Autosave Corruption** | High (Data Loss) | Very Low | Transactional writes (Atomic) + Schema validation before save. | planned |
| **R-05** | **SQLite Locking (Dev)** | Medium (Latency) | High (if scaled) | Migrate to PostgreSQL for production/concurrency. | mitigation-ready |
| **R-06** | **Clock Skew** | Low (Visual Jitter) | Medium | Enforce Server Authoritative time; ignore client timestamps. | active |
| **R-07** | **Memory Leak (Rooms)** | Medium (OOM) | Medium | Strict room expiry (TTL) and cleanup cron jobs. | planned |
