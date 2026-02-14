# Functional Requirements Specification (FRS)

## Project: Real-Time Collaborative Football Tactical Canvas

## Architecture Model: Server Authoritative

## Deployment Target: MVP

---

# 1. User Model

## 1.1 Access Policy (FRS-USER-001)

* Anonymous access not allowed.
* Each user must enter:

  * Display name OR
  * Jersey number
* One active session per browser instance.
* Duplicate sessions blocked.

---

## 1.2 Roles (FRS-USER-002)

### Coach

* Creates room.
* Sets match duration (default 90 minutes).
* Controls permissions:

  * Team ownership rules
  * Editing restrictions
* Can start match (locks renaming and color changes).
* Can modify autosave interval.
* Can create formations.

### Player

* Joins via shared link.
* Can move players (default).
* Cannot create room.
* Cannot modify match duration.

---

# 2. Room Model

## 2.1 Room Creation (FRS-ROOM-001)

* Only Coach can create room.
* Room ID:

  * Default: auto-generated UUID.
  * Optional: custom slug.

---

## 2.2 Room Capacity (FRS-ROOM-002)

* Maximum total participants: 12

  * 11 players
  * 1 coach
* System supports up to 30 connected observers technically, but match mode limited to 12 active participants.

---

## 2.3 Join Policy (FRS-ROOM-003)

* Anyone with link may join if capacity not exceeded.
* No password/token protection.

---

## 2.4 Room Lifecycle (FRS-ROOM-004)

* Default match duration: 90 minutes.
* Coach may set custom duration.
* After time expiry:

  * Room becomes read-only.
* Inactivity behavior:

  * Room persists until match timer ends.
* If server restarts:

  * Restore room using last autosaved snapshot.

---

# 3. Editing Permissions

## 3.1 Default Rule (FRS-PERM-001)

* All users can move all players.

---

## 3.2 Optional Restrictions (Coach Controlled) (FRS-PERM-002)

* Restrict editing by team ownership.
* Lock team editing per user.

---

## 3.3 Drag Concurrency Rule (FRS-LOCK-001)

* If a player is being dragged:

  * Server locks that player.
  * Other users see player greyed out.
  * Second drag attempts rejected.
* Lock released on:

  * Drag end
  * Disconnect
  * Timeout (2 seconds no update)

---

# 4. Team Rules

## 4.1 Structure (FRS-TEAM-001)

* Exactly 2 teams.
* Each team:

  * Up to 15 total registered players.
  * Maximum 11 active on field.
  * Minimum 7 required to start match.
  * 1 goalkeeper required.

---

## 4.2 Team Configuration (FRS-TEAM-002)

Before match start:

* Rename team allowed.
* Edit team color allowed.

After match start:

* Renaming disabled.
* Color editing disabled.

---

## 4.3 Bench Logic (FRS-TEAM-003)

* Bench area available outside pitch canvas.
* Players can be positioned on bench.
* Only 11 per team allowed inside pitch boundary.

---

# 5. Movement Rules

## 5.1 Movement Scope (FRS-MOVE-001)

* Players can move:

  * Inside pitch area.
  * Inside bench area.
* Movement outside defined zones prohibited.

---

## 5.2 Boundary Handling (FRS-MOVE-002)

* If player dragged outside legal zone:

  * Red boundary indicator displayed.
  * Server rejects final position.

---

## 5.3 Snap-to-Grid Explanation (FRS-MOVE-003)

Snap-to-grid means:

* Player position auto-aligns to invisible grid intersections.
* Improves formation symmetry.
* Reduces jitter in collaborative mode.

Current Decision:

* Not enabled for MVP.

---

## 5.4 Collision Detection (FRS-MOVE-004)

* No collision enforcement.
* Players may overlap.

---

## 6. Real-Time Cursor Visibility (Required) (FRS-UI-001)

* Each connected user has visible cursor indicator.
* Cursor shows:

  * Display name or jersey number.
* Cursor movement broadcast via WebSocket.
* Cursor does not affect canonical state.
* Cursor updates throttled (10/sec).

---

## 7. Zoom and Pan (FRS-UI-002)

* Zoom/pan is per-user local view.
* Does not affect other users.
* Does not alter canonical state.

---

# 8. Persistence Model

## 8.1 Autosave (FRS-DATA-001)

* Default interval: 30 seconds.
* Coach may modify interval.
* Autosave persists:

  * Teams
  * Players
  * Roles
  * Positions
  * Version

---

## 8.2 Version History (FRS-DATA-002)

* Every autosave creates new immutable version.
* Overwrite not allowed.
* Version metadata:

  * Timestamp
  * Author
  * Match time

---

## 8.3 Multiple Formations (FRS-DATA-004)

* Room may store multiple formations.
* Formation switch resets active state to selected version.

---

# 9. Reconnect Logic (FRS-NET-001)

## 9.1 User Disconnect

* User marked "Offline".
* Player lock released.
* Reconnect restores:

  * Role
  * Team
  * Cursor state

---

## 9.2 Server Restart (FRS-NET-002)

* System restores:

  * Last autosaved state.
  * Teams
  * Players
  * Version
* Unsaved state lost.

---

# 10. Performance Requirements (MVP) (FRS-NFR-001)

> **Note:** See [11-Non-Functional-Requirements.md](11-Non-Functional-Requirements.md) for full details.

* Max 30 users connected per room.
* Max 5 rooms concurrently.
* Drag broadcast latency < 100ms.
* Cursor update latency < 100ms.
* State broadcast size optimized.

---

# 11. Role Tagging (FRS-ROLE-001)

Each player may have role tag:

* GK
* DEF
* MID
* FWD

Tags:

* Optional.
* Editable before match start.
* Locked after match start.

---

# 12. Match Start Behavior (FRS-MATCH-001)

When Coach starts match:

* Team rename disabled.
* Team color editing disabled.
* Role editing disabled.
* Formation still movable unless Coach locks editing.

---

# 13. State Model (Canonical Room Structure) (FRS-DATA-003)

> **Note:** See [10-Database-Schema-Spec.md](10-Database-Schema-Spec.md) for full schema.

```
Room {
  room_id
  version
  match_status (setup | live | expired)
  match_timer
  teams[2]
  players[]
  locks[]
  cursors[]
  formations[]
}
```

---

# 14. Acceptance Criteria (MVP)

* 22 players active without desync.
* Simultaneous drag conflict handled deterministically.
* Real-time cursor visible for all users.
* Autosave every 30 seconds.
* Room restored correctly after server restart.
* Team rules enforced before match start.
* Bench and field separation enforced.

---

# 15. Cross-References

*   **Related Upstream Requirements**: [01-BRD.md](01-BRD.md).
*   **Related Downstream Specifications**: [03-WebSocket-Protocol-Spec.md](03-WebSocket-Protocol-Spec.md), [04-REST-API-Spec.md](04-REST-API-Spec.md).
*   **Traceability**: [08-Requirements-Traceability-Matrix.md](08-Requirements-Traceability-Matrix.md).
*   **Validation**: [07-Test-Plan-QA-Strategy.md](07-Test-Plan-QA-Strategy.md).


