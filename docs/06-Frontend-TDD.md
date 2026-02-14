# Frontend Technical Design Document (F-TDD)

## Project: Real-Time Collaborative Football Tactical Canvas

## Stack: React + TypeScript + React Konva

## Architecture Style: Modular Feature-Based + Centralized State

## Backend Contract: Server Authoritative (WebSocket)

---

# 1. Architectural Principles

1. Server is single source of truth.
2. Canonical state is immutable on client.
3. Local UI state is isolated from canonical state.
4. No business logic inside components.
5. WebSocket communication centralized.
6. Deterministic reconciliation on every update.
7. Performance-first rendering model.

---

# 2. Technology Stack

* React (Function Components)
* TypeScript (strict mode)
* React Konva (canvas rendering)
* Zustand (lightweight global state)
* Native WebSocket API
* React Query (optional for REST)
* ESLint + Prettier + TypeScript strict
* Vite (build tool)

---

# 3. Frontend Architecture Overview

```
UI Components
   ↓
Feature Layer
   ↓
State Store (Zustand)
   ↓
WebSocket Service
   ↓
Server
```

Clear separation:

* UI layer = pure rendering
* Feature layer = interaction logic
* Store = state container
* WebSocket service = communication adapter

---

# 4. Project Structure

```
src/
 ├── app/
 │    ├── App.tsx
 │    └── routes.tsx
 ├── features/
 │    ├── room/
 │    ├── canvas/
 │    ├── players/
 │    ├── teams/
 │    ├── cursors/
 │    ├── locks/
 │    └── formations/
 ├── services/
 │    ├── websocket.ts
 │    └── api.ts
 ├── store/
 │    ├── canonicalStore.ts
 │    ├── uiStore.ts
 │    └── selectors.ts
 ├── hooks/
 ├── types/
 ├── utils/
 └── config/
```

Feature-first organization. No cross-feature direct imports.

---

# 5. State Architecture

## 5.1 State Separation Model (Ref: FRS-DATA-003)

Two isolated stores:

### 1. Canonical Store (Server Controlled)

Contains:

```
{
  version: number
  matchStatus: "setup" | "live" | "expired"
  teams: Team[]
  players: Player[]
  locks: Lock[]
  cursors: Cursor[]
  formations: FormationMeta[]
}
```

Rules:

* Only WebSocket service updates this store.
* UI never mutates directly.
* Snapshot replaces entire store.
* State update applies minimal diff.

---

### 2. UI Store (Local Only)

Contains:

```
{
  zoomLevel
  panOffset
  isDragging
  selectedPlayerId
  connectionStatus
  localCursorPosition
  notifications
}
```

Rules:

* Never sent to server.
* Never affects canonical version.
* Fully isolated.

---

# 6. WebSocket Service Layer

File: `services/websocket.ts`

Responsibilities:

* Open/close connection
* Reconnect with exponential backoff
* Queue outgoing messages
* Throttle MOVE_UPDATE
* Throttle CURSOR_UPDATE
* Dispatch incoming messages to store
* Handle version mismatch

No UI code inside service.

---

## 6.1 Message Flow (Ref: FRS-NET-001)

Incoming:

```
onMessage(event):
   parse
   switch(type):
      SNAPSHOT -> replace canonical store
      STATE_UPDATE -> apply mutations
      LOCK_GRANTED -> update locks
      LOCK_DENIED -> notify UI
      CURSOR_BROADCAST -> update cursors
      ERROR -> dispatch notification
```

Outgoing:

* REQUEST_LOCK
* MOVE_UPDATE
* RELEASE_LOCK
* CURSOR_UPDATE
* ADD_PLAYER
* SWITCH_FORMATION

---

# 7. Reconciliation Strategy

## 7.1 Version Handling

* If received version > local version:

  * Apply update.
* If version mismatch:

  * Await SNAPSHOT.
* SNAPSHOT always overrides local canonical state.

No merge logic.

---

## 7.2 Drag Behavior (Ref: FRS-LOCK-001)

During drag:

1. REQUEST_LOCK sent.
2. On LOCK_GRANTED:

   * Set isDragging true.
3. MOVE_UPDATE sent throttled (10–20/sec).
4. Server broadcasts STATE_UPDATE.
5. Canonical state replaces local position.
6. On RELEASE_LOCK:

   * isDragging false.

Optimistic rendering allowed but must reconcile to server coordinates.

---

# 8. Canvas Architecture (React Konva)

Layers:

1. FieldLayer
2. BenchLayer
3. PlayersLayer
4. LockOverlayLayer
5. CursorLayer

Each layer isolated.

---

## 8.1 Player Component

Props:

```
{
  id
  x
  y
  teamColor
  label
  role
  isLocked
  isMine
}
```

Behavior:

* If locked and not mine → greyed
* If locked and mine → highlighted
* Drag enabled only if:

  * lock granted
  * editing allowed
  * match not expired

---

# 9. Lock UI Behavior (Ref: SM-LOCK-01)

When LOCK_DENIED:

* Show toast notification
* Player briefly flashes grey

When LOCK_GRANTED:

* Player border glows
* Cursor changes to grabbing

Lock expiration:

* UI automatically updates from canonical lock removal

---

# 10. Cursor Rendering

Each cursor:

```
{
  client_id
  display
  x
  y
}
```

Rendered as small marker with name label.

Updates throttled 10/sec.

Cursor layer independent from players.

---

# 11. Zoom & Pan (Local Only)

* Implemented using React Konva Stage scale + position.
* Stored in UI store.
* Does not affect canonical coordinates.
* Movement coordinates normalized before sending.

Coordinate transformation:

```
canvasX = normalizedX * stageWidth
canvasY = normalizedY * stageHeight
```

---

# 12. Performance Optimization Strategy

* Memoize Player components.
* Use shallow compare selectors.
* Avoid re-render entire store.
* Batch Zustand updates.
* Limit cursor render frequency.
* Avoid heavy computations in render loop.

Expected load:

* 22 players
* 30 cursors
* Smooth 60fps drag

---

# 13. Error Handling Strategy

WebSocket states (Ref: SM-CONN-01):

* CONNECTING
* CONNECTED
* RECONNECTING
* DISCONNECTED

UI reactions:

* Disable editing if disconnected.
* Display connection banner.
* Auto-reconnect with exponential backoff.
* After reconnect:

  * JOIN_ROOM with last_known_version.

---

# 14. Role Enforcement (Client Side) (Ref: FRS-USER-002)

Client hides UI controls based on role:

Coach:

* Rename team
* Change color
* Start match
* Change autosave interval
* Switch formation

Player:

* Move players
* View formations

Server still enforces all rules.

---

# 15. Formation Switching

When SWITCH_FORMATION:

* Server returns SNAPSHOT.
* Canonical store replaced.
* UI re-renders entire canvas.

---

# 16. Type Safety

Define shared message types:

```
type ServerEvent =
  | SnapshotEvent
  | StateUpdateEvent
  | LockGrantedEvent
  | LockDeniedEvent
  | ErrorEvent
```

All events strictly typed.

No `any`.

---

# 17. Testing Strategy

Unit tests:

* Reconciliation reducer
* Lock logic
* WebSocket event dispatcher
* Version mismatch handling

Integration tests:

* Simulated SNAPSHOT
* Simulated LOCK_DENIED
* Simulated reconnection

Manual test:

* Two tabs drag race
* Disconnect mid-drag
* Server restart

---

# 18. Future-Proofing

Designed for:

* Multi-instance backend
* Larger rooms
* Tactical overlays
* Undo/redo
* CRDT alternative (if ever needed)

---

# Frontend System Properties

* Deterministic
* Lock-safe
* Version-consistent
* Performance-optimized
* Server-authoritative compliant
* Fully isolated local UI state
* Strictly typed
* Scalable architecture

---

Frontend architecture now formally aligned with:

* [BRD](01-BRD.md)
* [FRS](02-FRS.md)
* [WebSocket Protocol](03-WebSocket-Protocol-Spec.md)
* [Backend TDD](05-Backend-TDD.md)
