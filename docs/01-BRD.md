# UPDATED BUSINESS REQUIREMENTS DOCUMENT (BRD)

## Project: Real-Time Collaborative Football Tactical Canvas

## Architecture Model: Server Authoritative

## Backend: Python (FastAPI)

## Frontend: React + React Konva

## Communication: WebSockets

---

# 1. Executive Summary (BRD-EXEC-001)

Develop a real-time collaborative football tactical board where multiple users can:

* Join the same room
* View identical football field canvas
* Drag and reposition players
* Add and manage two opposing teams
* Observe updates in real time
* Persist formations

System operates under a Server Authoritative model to guarantee deterministic shared state.

---

# 2. Updated Core Feature: Dual-Team Strategy Mode (BRD-CORE-002)

The system must support:

* Two opposing teams on the same field
* Independent team configuration
* Clear visual differentiation
* Strategic positioning across both teams

This enables full formation planning and matchup simulation.

---

# 3. Functional Requirements (Updated)

---

## 3.1 Canvas Rendering (BRD-FUNC-003)

* Full 2D football pitch.
* Scalable and responsive.
* Supports rendering players from two teams simultaneously.

![Image](https://images.openai.com/static-rsc-3/n_jGKzOCJPXvBtMCcCTAiTKHoqjiHup990W5tyCQH8kXN9opl-bbu2LYaePEBPDInjK7Q_1KrMm7GUu5aYInYJKsVDtwnSgF6kGIzr1UWVc?purpose=fullsize\&v=1)

![Image](https://png.pngtree.com/thumb_back/fw800/background/20251127/pngtree-detailed-soccer-team-tactics-diagram-showing-the-red-s-defensive-formation-image_20615247.webp)

![Image](https://images.openai.com/static-rsc-3/QmimNofTG9NdSbGakcoxA3tAFyzcRsmi_b0YPf-nw1vGMW-2FVilSR0XOobBStdWnb5N3Wif2uLKRfS0LPosVyDeEHwOyyw4M6fP4XOUS1M?purpose=fullsize\&v=1)

![Image](https://images.openai.com/static-rsc-3/9xesbwXwIAKMj2sPqco72aUApxh8oCA7azzcZV9j1G38Y8NukM_c9BYhZBvlT7KUFi2M0xlVXb2IDFuzdSUlMixq9jUzd2TQTMOq7Kg5Ddk?purpose=fullsize\&v=1)

---

## 3.2 Team Model (BRD-FUNC-004)

### Team Entity

Each room supports multiple teams (minimum two).

```
Team {
    team_id
    name
    color
    side (home / away)
}
```

### Requirements

* Default two teams: Home and Away.
* Configurable team names.
* Configurable colors.
* Maximum players per team configurable (default 11).

---

## 3.3 Player Model (Updated) (BRD-FUNC-005)

```
Player {
    player_id
    team_id
    x
    y
    label
}
```

Constraints:

* Player must belong to one team.
* Server enforces max player limit per team.
* Players visually styled by team color.

---

## 3.4 Real-Time Events (Updated) (BRD-FUNC-006)

### Client → Server (Intent)

* JOIN_ROOM
* ADD_TEAM (optional, future)
* ADD_PLAYER (must include team_id)
* MOVE_PLAYER
* REMOVE_PLAYER
* RESET_FORMATION
* SWITCH_TEAM_SIDE (optional phase 3)

### Example ADD_PLAYER

```
{
  "type": "ADD_PLAYER",
  "team_id": "home",
  "x": 0.25,
  "y": 0.60
}
```

---

## 3.5 Server Authoritative Enforcement (Updated) (BRD-FUNC-007)

Server validates:

* Team exists
* Player belongs to valid team
* Team player count within limit
* Coordinates within pitch bounds
* No duplicate player IDs

Server broadcasts canonical full state.

---

## 3.6 Visual Requirements (BRD-FUNC-008)

* Team A color distinct from Team B.
* Optional jersey number display.
* Optional goalkeeper marker.
* Clear center line separation.
* Optional half-field locking (Phase 3).

---

# 4. Updated Room State Structure (BRD-DATA-009)

```
Room {
    room_id
    version
    teams: {
        team_id: {
            name,
            color,
            side
        }
    }
    players: {
        player_id: {
            team_id,
            x,
            y,
            label
        }
    }
}
```

---

# 5. Strategic Mode Enhancements (Phase 3+) (BRD-FUTR-010)

Optional future capabilities:

* Lock team half (prevent crossing midfield).
* Tactical zones overlay.
* Heatmap overlay.
* Formation templates per team (4-4-2, 3-5-2, etc).
* Team visibility toggle.

---

# 9. Cross-References

*   **Related Upstream Requirements**: None (Root Document).
*   **Related Downstream Specifications**: [02-FRS.md](02-FRS.md), [11-Non-Functional-Requirements.md](11-Non-Functional-Requirements.md).
*   **Traceability**: [08-Requirements-Traceability-Matrix.md](08-Requirements-Traceability-Matrix.md).
*   **Validation**: [07-Test-Plan-QA-Strategy.md](07-Test-Plan-QA-Strategy.md).


---

# 6. Updated Non-Functional Requirements (BRD-NFR-011)

> **Note:** Detailed NFRs are now maintained in [11-Non-Functional-Requirements.md](11-Non-Functional-Requirements.md). The list below is a summary.

* Maintain performance with 22+ players.
* Broadcast latency < 100ms.
* Support 50 users per room.
* Smooth drag under full team load.

---

# 7. Updated Project Phases

---

## Phase 1 – Protocol & Dual-Team Data Model

Deliverables:

* Team entity definition
* Updated room state structure
* Validation rules for team limits
* React Konva rendering POC with two colors

---

## Phase 2 – Dual-Team MVP

Deliverables:

* Add/remove players per team
* Color-coded rendering
* Real-time movement sync
* Max player enforcement

Acceptance Criteria:

* 22 players rendered
* Both teams synchronized across browsers
* Dragging remains smooth under load

---

## Phase 3 – Strategic Controls

Deliverables:

* Team side switching
* Half-field restriction option
* Lock team editing mode
* Role tagging (GK, DEF, MID, FWD)

---

## Phase 4 – Scaling & Optimization

Deliverables:

* Redis state distribution
* Rate limiting refinement
* Load testing with 50+ users

---

# 8. Success Metrics (Updated)

* 22 players synchronized without desync
* No performance degradation under full-team load
* Deterministic state under simultaneous multi-user edits
* Sub-100ms state propagation

---

# Final Architecture Summary

Frontend:
React + React Konva + WebSocket

Backend:
FastAPI + Server Authoritative Room Engine + PostgreSQL

Scaling:
Redis + Horizontal containers

Strategic Capability:
Full two-team formation planning with deterministic collaborative synchronization.
