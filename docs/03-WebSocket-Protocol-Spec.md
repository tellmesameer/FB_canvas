# Real-Time WebSocket Protocol Specification

Server-authoritative, JSON over WebSocket. Path: `/ws/room/{room_id}`. All messages are UTF-8 JSON objects. Timestamp values are ISO 8601 UTC strings. All numeric coordinates are normalized `0.0–1.0`. Every client message MUST include `client_id` (UUID) and `display` (display name or jersey number). Server enforces role permissions.

---

## Envelope (WS-PROTO-001)

```json
{
  "type": "STRING_EVENT_NAME",
  "req_id": "optional-client-request-id",
  "client_id": "uuid-v4",
  "display": "string",
  "payload": { ... }
}
```

---

## Connection & Handshake (WS-PROTO-002)

> **Ref:** [FRS-NET-001](02-FRS.md) (Reconnect), [FRS-ROOM-003](02-FRS.md) (Join), [SM-CONN-01](09-State-Machines.md)

1. Client opens `wss://<host>/ws/room/{room_id}?role={role}` with role `coach` or `player`.
2. Immediately send `JOIN_ROOM` message with `last_known_version` (nullable).
3. Server replies with either `SNAPSHOT` (full canonical state) or `STATE_UPDATE` if incremental.
4. Server sends `ROOM_META` broadcast on meta changes.

### JOIN_ROOM (client → server)

```json
{
  "type":"JOIN_ROOM",
  "client_id":"...",
  "display":"Sam #9",
  "payload": {
    "role":"player",
    "last_known_version": 32
  }
}
```

### SNAPSHOT (WS-PROTO-003)

> **Ref:** [FRS-DATA-003](02-FRS.md) (State Model)

Large canonical state used to fully reconcile client.

```json
{
  "type":"SNAPSHOT",
  "version": 33,
  "payload": {
    "room_id":"...",
    "match_status":"setup",
    "teams":[ { "team_id":"home", "name":"Home", "color":"#0055ff" }, ... ],
    "players":[ { "player_id":"...", "team_id":"home","x":0.1,"y":0.2,"label":"9","role":"FWD" }, ... ],
    "locks": [ { "player_id":"...", "client_id":"...", "since":"2026-02-14T12:00:00Z" } ],
    "cursor_states": [ { "client_id":"...", "x":0.12, "y":0.34 } ],
    "formations":[ { "id":"v1","timestamp":"...","author":"..." } ]
  }
}
```

---

## Message Types — Client → Server (intents)

* `JOIN_ROOM` — join with role and last_known_version.
* `LEAVE_ROOM` — graceful disconnect intent.
* `REQUEST_LOCK` — request exclusive lock on `player_id` (sent automatically on drag start).
* `RELEASE_LOCK` — release lock (drag end, cancel).
* `MOVE_UPDATE` — throttled position update while holding lock.
* `ADD_PLAYER` — coach/player intent to add a player (server validates capacity/team).
* `REMOVE_PLAYER` — remove a player (coach only for match settings; coach configurable).
* `ADD_FORMATION` — save current canonical state as a named formation (coach).
* `SWITCH_FORMATION` — request active formation switch by formation id (coach).
* `CURSOR_UPDATE` — local cursor position broadcast for visibility (throttled).
* `PING` — keepalive (server replies `PONG`).

### REQUEST_LOCK (WS-PROTO-004)

> **Ref:** [FRS-LOCK-001](02-FRS.md) (Drag Concurrency), [SM-LOCK-01](09-State-Machines.md)

```json
{
  "type":"REQUEST_LOCK",
  "client_id":"...",
  "payload": { "player_id": "player-uuid" }
}
```

### MOVE_UPDATE (WS-PROTO-005)

> **Ref:** [FRS-MOVE-001](02-FRS.md) (Movement Scope)

```json
{
  "type":"MOVE_UPDATE",
  "client_id":"...",
  "payload": {
    "player_id":"player-uuid",
    "x":0.412,
    "y":0.733,
    "timestamp":"..."
  }
}
```

---

## Message Types — Server → Clients (canonical broadcasts / responses)

* `LOCK_GRANTED` — lock assigned to a client.
* `LOCK_DENIED` — lock request denied (includes `current_owner`).
* `STATE_UPDATE` — incremental canonical mutation (preferred small diffs).
* `ERROR` — error with code and message.
* `ROOM_META` — meta changes (team rename, color changed, match started).
    * Note: `match_started` event implies **all locks released**. (Ref: [SM-MATCH-01](09-State-Machines.md))
* `CURSOR_BROADCAST` — cursor positions (aggregated).
* `PONG` — ping response.
* `VERSION_MISMATCH` — server instructs client to `SNAPSHOT`.

### LOCK_GRANTED (WS-PROTO-006)

```json
{
  "type":"LOCK_GRANTED",
  "payload": { "player_id":"...", "client_id":"...", "expires_at":"2026-02-14T12:00:02Z" }
}
```

### LOCK_DENIED

```json
{
  "type":"LOCK_DENIED",
  "payload": { "player_id":"...", "current_owner":"other-client-id", "reason":"locked" }
}
```

### STATE_UPDATE (WS-PROTO-007)

> **Ref:** [FRS-DATA-003](02-FRS.md) (State Model)

Minimal canonical change; server increments `version`.

```json
{
  "type":"STATE_UPDATE",
  "version": 34,
  "payload": {
    "mutations":[
      { "op":"move", "player_id":"...", "x":0.412, "y":0.733 },
      { "op":"add", "player": { "player_id":"...", "team_id":"away", "x":0.1, "y":0.2, "label":"12" } }
    ]
  }
}
```

---

## Locking & Drag Flow (Server-Authoritative)

1. Client sends `REQUEST_LOCK(player_id)` (drag start).
2. Server validates and responds:

   * If granted → send `LOCK_GRANTED` to requester and broadcast `LOCK_STATUS` to room.
   * If denied → send `LOCK_DENIED`.
3. While lock held:

   * Client sends `MOVE_UPDATE` events (throttled).
   * Server applies updates to canonical state on each valid `MOVE_UPDATE` or batches them; server increments version on each applied mutation.
4. On drag end:

   * Client sends `RELEASE_LOCK` or server auto-releases after inactivity timeout.
   * Server broadcasts final `STATE_UPDATE` and `LOCK_RELEASED`.

Lock timeout: default 2s without updates — server releases and broadcasts `LOCK_RELEASED`.

Simultaneous request: first valid `REQUEST_LOCK` wins.

---

## Cursor Visibility

* Clients publish `CURSOR_UPDATE` at ≤10/sec.
* Server aggregates and multicasts `CURSOR_BROADCAST` at 5/sec.
* Cursor payload: `{client_id, display, x, y, timestamp}`.
* Cursors never mutate canonical state.

---

## Versioning & Reconciliation

* Server increments integer `version` for every mutation.
* Clients attach `last_known_version` in `JOIN_ROOM`.
* **Decision:** If `last_known_version != current_version` → Server sends full `SNAPSHOT`.
* No replay buffer implemented (simplicity > optimization for MVP).
* Clients must accept server snapshot unconditionally and reconcile UI.

---

## Autosave & Formations

* Server autosaves canonical state at configured interval (default 30s).
* Autosave creates immutable formation version; server broadcasts `FORMATION_SAVED` with formation id & metadata.
* `ADD_FORMATION` (manual save) triggers immediate save.

---

## Error Codes (representative)

* `400` — Bad payload / schema fail.
* `401` — Unauthorized action (role or capacity).
* `403` — Forbidden (editing locked entity).
* `404` — Entity not found.
* `409` — Conflict (version mismatch).
* `429` — Rate limit.
* `500` — Server error.

Server `ERROR` message:

```json
{ "type":"ERROR", "payload": { "code":409, "message":"version mismatch", "expected_version": 34 } }
```

---

## Rate Limiting & Throttling (WS-PROTO-008)

> **Ref:** [FRS-NFR-001](02-FRS.md) (Performance)

* `MOVE_UPDATE` ≤ 20/sec per client (recommended 10/sec burst).
* `CURSOR_UPDATE` ≤ 10/sec per client.
* `REQUEST_LOCK` ≤ 5/min per client for same player.
* Server responds `429` with backoff window and `retry_after` seconds.

### Slow Consumers Policy
1. Queue > 50 msgs: Drop `CURSOR_UPDATE`.
2. Queue > 100 msgs: Drop non-critical (`LOCK`, `STATE_UPDATE` preserved).
3. Queue > 200 msgs: **Disconnect Client**.

---

## Reconnect & Recovery

* On reconnect, client sends `JOIN_ROOM` with `last_known_version`.
* If `last_known_version` < server `version` → server sends `SNAPSHOT`.
* Server retains locks for disconnected clients for `lock_release_timeout` (2s) and marks disconnected users as `offline`.
* If server restarts, it restores last autosaved formation into room canonical state. Unsaved in-memory mutations are lost.

---

## Security & Validation

* Server validates:

  * `client_id` / `display` presence and format.
  * Role permissions (coach only for start/rename/color change/add formation).
  * Team limits and player counts (enforce 11 on-field max; bench allowed).
  * Coordinate bounds `0.0–1.0` and bench/field zones.
* Sanitize all strings; reject oversized payloads.
* Enforce message size limit (e.g., 16 KB).
* Enforce CORS & TLS (wss mandatory).

---

## Testing Scenarios (must pass)

* Two clients race to lock same player → first wins; second receives `LOCK_DENIED`.
* Client drags while network lag → server accepts last valid `MOVE_UPDATE`; client reconciles on `STATE_UPDATE`.
* Lost connection, reconnect with stale version → client receives `SNAPSHOT` and replays UI.
* Autosave creates formation; switching formation broadcasts `SNAPSHOT` to all.
* Cursor updates visible at controlled frequency without affecting canonical state.

---

## Implementation Notes (server side)

* Use JSON Schema / Pydantic models for validation.
* Broadcast minimal `STATE_UPDATE` diffs when possible; fallback to `SNAPSHOT` if diff size grows or on version mismatch.
* Keep lock metadata in authoritative room state (in-memory or Redis).
* Use Redis pub/sub for multi-instance scale (publish `STATE_UPDATE` and lock events).
* Persist autosaves to PostgreSQL with formation metadata.

---

## Example Full Flow (dragging player)

1. Client A: `REQUEST_LOCK(player-1)`
2. Server → `LOCK_GRANTED(player-1, clientA)`
3. Client A: repeated `MOVE_UPDATE` (throttled)
4. Server applies moves, broadcasts `STATE_UPDATE` mutations (version increments)
5. Client B sees player greyed out due to lock via `LOCK_STATUS`/`LOCK_GRANTED`
6. Client A: `RELEASE_LOCK`
7. Server broadcasts final `STATE_UPDATE` + `LOCK_RELEASED`

