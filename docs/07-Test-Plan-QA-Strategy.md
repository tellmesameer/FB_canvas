# Test Plan & QA Strategy

Project: Real-Time Collaborative Football Tactical Canvas
Scope: MVP (Server-authoritative WebSocket, React Konva frontend, FastAPI backend, Redis, SQLite)

---

# 1. Goals & Exit Criteria

**Goals**

* Verify correctness of real-time authoritative behavior (locks, moves, snapshots).
* Validate role permissions, team rules, persistence, reconnect/recovery.
* Meet NFRs: latency <100ms, handle target concurrency, autosave correctness.

**Exit Criteria (for MVP release)**

* All Critical tests pass (automated + manual): 100%.
* High severity defects: 0 open.
* Medium severity defects: ≤2, with mitigation/plan.
* Performance acceptance: sustain target load with <100ms median broadcast latency.
* Test coverage: unit ≥70%, integration ≥50% (measured by CI).

---

# 2. Test Environments

1. **Local Dev** — single dev machine, dev config.
2. **CI Staging** — ephemeral environment spun by CI (single instance FastAPI, Redis, SQLite file).
3. **Load Test Env** — separate instance(s) with similar resources to expected local deployment.
4. **Production (post-MVP)** — only smoke & canary tests.

Environment configs use centralized config files; tests load settings from `.env.test`.

---

# 3. Test Types & Tools

* **Unit Tests** (fast, deterministic) — pytest, pytest-asyncio.
* **Integration Tests** (server+DB+Redis) — pytest with test containers or fixtures.
* **WebSocket Contract Tests** — pytest + websockets client (or FastAPI TestClient for WS).
* **Frontend Unit Tests** — Jest + React Testing Library.
* **Frontend Integration / E2E** — Playwright (multi-tab simulation).
* **Load & Stress Tests** — Locust (user behavior scripts) + k6 for scenarios.
* **Chaos/Resilience Tests** — scripts to kill Redis/processes; verify autosave & recovery.
* **Security & Static Analysis** — Bandit, Snyk, ESLint rules, mypy.
* **Performance Profiling** — APM or logs + custom latency harness.
* **Accessibility (optional)** — axe (for UI elements).

---

# 4. Test Automation Strategy / CI

* All unit & integration tests run on every PR.
* E2E tests run nightly and on release branches.
* Load tests run in dedicated pipeline (not on every PR).
* Test artifacts (logs, traces, snapshots) stored by CI.
* Failure on PR: block merge until addressed (Critical/High).
* Use coverage gates: fail if critical code paths lack tests.

---

# 5. Test Data & Fixtures

* Deterministic UUID provider stub for tests.
* Time provider stub for timer tests.
* Sample room/test accounts:

  * `coach_1` role=coach
  * `player_1` role=player
  * `player_2` role=player
* Preseed DB fixtures for formations, teams, players.
* TearDown: reset SQLite file between tests, flush Redis.

---

# 6. Test Scenarios & Cases (Representative, prioritized)

## Critical Functional Scenarios (must pass) (Ref: BRD-FUNC-005)

1. **Join & Snapshot** (Ref: FRS-ROOM-003, WS-PROTO-003)

   * Start server; client joins with `JOIN_ROOM`; receives `SNAPSHOT`.
   * Acceptance: snapshot format correct; canonical store matches DB after autosave.

2. **Lock Race** (Ref: FRS-LOCK-001)

   * Two clients `REQUEST_LOCK` same player simultaneously.
   * Acceptance: single `LOCK_GRANTED` delivered; other receives `LOCK_DENIED`.

3. **Move While Locked**

   * Client with lock sends `MOVE_UPDATE` throttled; server increments version and broadcasts `STATE_UPDATE`.
   * Acceptance: clients apply versioned delta; positions normalized and within bounds.

4. **Simultaneous Moves Different Players**

   * Multiple clients move different players concurrently.
   * Acceptance: no state corruption; version increments per mutation; final state matches expected.

5. **Drag Reconnect**

   * Client drags, loses connection, reconnects, sends `JOIN_ROOM` with last_known_version.
   * Acceptance: server sends `SNAPSHOT` or `STATE_UPDATE` to reconcile; locks released as per timeout.

6. **Autosave** (Ref: FRS-DATA-001)

   * Server autosaves at interval.
   * Acceptance: formation snapshot created in DB with correct version metadata.

7. **Start Match Locking**

   * Coach starts match; try rename team after start.
   * Acceptance: server rejects renaming; returns `ERROR` 403.

8. **Capacity Enforcement** (Ref: FRS-TEAM-001)

   * Try to add 16 players to team (limit=15).
   * Acceptance: server rejects with `ERROR` 409.

9. **Boundary Handling** (Ref: FRS-MOVE-002)

   * Drag player outside field; final position rejected and red indicator state broadcast.
   * Acceptance: server sends `ERROR` or `STATE_UPDATE` correcting position.

10. **Cursor Broadcast**

    * Multiple clients send `CURSOR_UPDATE`; server broadcasts aggregated cursors at 5/sec.
    * Acceptance: UI receives only aggregated updates; throttling effective.

## Important Integration Scenarios

11. **Version Mismatch**

    * Client with stale version sends `MOVE_UPDATE`; server returns `VERSION_MISMATCH` + `SNAPSHOT`.
    * Acceptance: client replaces canonical state.

12. **Autosave & Restore**

    * Server restart simulation: persists last autosave; restart server; clients reconnect; canonical state restored.
    * Acceptance: restored state equals last saved formation.

13. **Rate Limit**

    * Flood `MOVE_UPDATE` above rate limit.
    * Acceptance: server returns `429`; subsequent messages blocked temporarily.

14. **Formation Save & Switch**

    * Coach creates formation; switch to that formation in room.
    * Acceptance: `FORMATION_SAVED` created; switch results in `SNAPSHOT` to all.

## Performance & Load Scenarios

15. **Sustained Cursor Load** (Ref: FRS-NFR-001)

    * 30 users × 10 cursor updates/sec (300 msgs/sec).
    * Acceptance: server handles messages without queue growth; aggregated broadcast latency <100ms.

16. **Concurrent Drags**

    * 22 players moved concurrently (simulate 11 per team) with 10 clients dragging.
    * Acceptance: broadcast latencies acceptable; no state corruption.

17. **Autosave Under Load**

    * Trigger autosave while heavy movement; ensure persistence doesn't block event loop.
    * Acceptance: autosave latency acceptable, no lost events.

## Resilience / Chaos

18. **Redis Failure**

    * Kill Redis, continue server.
    * Acceptance: server degrades gracefully; essential functionality (single instance canonical state) continues; logs/metrics show Redis errors; retries attempted.

19. **DB Failure on Save**

    * Simulate SQLite write failure.
    * Acceptance: server logs error; autosave retry executed with backoff; in-memory state persists until DB recovered.

20. **Lock Timeout Handling**

    * Simulate client holds lock but stops sending updates.
    * Acceptance: server auto-releases lock after 2s; other users can request lock.

---

# 7. Test Case Templates (example)

**Test Case:** Lock Race — two clients

* Setup: spawn server, create room, add player.
* Steps:

  1. Client A sends `REQUEST_LOCK(player1)`.
  2. Client B sends same at same time.
* Expected:

  * One `LOCK_GRANTED` (A or B).
  * Other receives `LOCK_DENIED` with current_owner.
  * Lock metadata in canonical state correct.
* Automation: WebSocket test client simulates concurrency.

**Test Case:** Autosave Snapshot Integrity

* Steps:

  1. Move several players.
  2. Wait for autosave interval.
  3. Query DB formation snapshot JSON.
* Expected:

  * Snapshot JSON matches canonical state at save time.
  * Version matches last broadcast version.

---

# 8. QA Roles & Responsibilities

* **QA Lead** — overall test plan, release decisions.
* **Automation Engineer** — implement unit/integration and E2E tests.
* **Performance Engineer** — design/load execution.
* **Dev (owner of feature)** — write unit tests, fix defects.
* **SRE/DevOps** — manage test env, CI pipelines, artifact storage.

---

# 9. Bug Severity & Triage Rules

* **Critical**: data loss, state corruption, security issue, server crash. Fix before release.
* **High**: real-time desync, lock failure, unauthorized access. Fix before release or blocked by mitigation.
* **Medium**: UI glitches, non-blocking feature failures. Fix in next sprint.
* **Low**: cosmetic issues, minor text errors. Track and fix later.

All issues must include repro steps and logs; CI must attach failing artifacts.

---

# 10. Monitoring Tests / Observability Checks

* Verify logging contains correlation IDs and event metadata.
* Verify health endpoints `/health`, `/health/db`, `/health/redis` return expected.
* Check metrics:

  * active_rooms
  * active_users
  * lock_conflict_count
  * autosave_failures
  * ws_message_rate
* Alerts if thresholds exceeded during load tests.

---

# 11. Regression Strategy & Test Retention

* Maintain regression suite: all Critical + High tests automated.
* Run regression before every release candidate.
* Keep test artifacts for 30 days.
* Maintain failing test backlog and assign owners.

---

# 12. Release & Smoke Checklist

Before release to production-like environment:

* All Critical/High defects closed.
* Unit/integration tests green on CI.
* Smoke E2E executed (multi-tab sync, join, lock, move, autosave).
* Load test passed baseline scenarios.
* Monitoring & logging configured.
* Rollback plan validated.

Rollback steps:

1. Disable incoming connections (maintenance page).
2. Revert deployment to previous image.
3. Restore SQLite from last known good autosave (if needed).
4. Notify users.

---

# 13. Test Scheduling & Phases (align to project phases)

* **Phase 1 (Design/POC):** unit tests + basic WS contract tests.
* **Phase 2 (MVP dev):** full unit + integration + basic E2E multi-tab tests.
* **Phase 3 (Persistence & Stability):** autosave tests, DB restore tests, reconnect tests.
* **Phase 4 (Scale & Hardening):** load tests, chaos tests, security scans.

---

# 14. Test Metrics (track in CI dashboard)

* Test pass rate per build.
* Time to fix Critical bug (MTTR).
* Code coverage: unit/integration.
* Average WS message latency under load.
* Autosave success rate.
* Number of flaky tests (goal: 0).

---

# 15. Test Artifacts & Reporting

* On each CI run produce:

  * Test results (JUnit format).
  * Logs: server, Redis, client traces.
  * WebSocket transcripts for failing tests.
  * Screenshots/video for Playwright E2E failures.
* Weekly QA report summarizing failures, trends, and action items.

---

# 16. Test Implementation Notes

* Use dependency injection and stubs for deterministic tests (time, UUID).
* Make WebSocket test clients deterministic and replayable.
* Use fixtures to seed DB and clear Redis.
* Keep tests idempotent and isolated.

---

# 17. Known Risks & Mitigations

* **Flaky network in CI** — isolate unstable tests to nightly or gated pipelines.
* **Time-sensitive tests** — use time mocking.
* **Load test environment variance** — base acceptance on relative thresholds and headroom.
* **Resource limits on CI** — offload heavy load tests to dedicated infra.

---
