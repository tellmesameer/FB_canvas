# 08. Requirements Traceability Matrix (RTM)

| FRS ID | Requirement Name | Owner | Protocol Ref | Test Case Ref | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FRS-USER-001** | Access Policy | Backend | - | TC-USER-001 | Planned |
| **FRS-USER-002** | Roles (Coach/Player) | Backend | WS-PROTO-002 | TC-USER-002 | Planned |
| **FRS-ROOM-001** | Room Creation | Backend | - | TC-ROOM-001 | Planned |
| **FRS-ROOM-002** | Room Capacity | Backend | WS-PROTO-002 | TC-ROOM-002 | Planned |
| **FRS-ROOM-003** | Join Policy | Backend | WS-PROTO-002 | TC-ROOM-003 | Planned |
| **FRS-ROOM-004** | Room Lifecycle | Backend | - | TC-ROOM-004 | Planned |
| **FRS-PERM-001** | Default Move Rule | Backend | WS-PROTO-005 | TC-PERM-001 | Planned |
| **FRS-PERM-002** | Coach Restrictions | Backend | - | TC-PERM-002 | Planned |
| **FRS-LOCK-001** | Drag Concurrency | Shared | WS-PROTO-004, 006 | TC-LOCK-01 | Planned |
| **FRS-TEAM-001** | Team Structure | Backend | - | TC-TEAM-001 | Planned |
| **FRS-TEAM-002** | Team Configuration | Backend | WS-PROTO-007 | TC-TEAM-002 | Planned |
| **FRS-TEAM-003** | Bench Logic | Shared | WS-PROTO-005 | TC-TEAM-003 | Planned |
| **FRS-MOVE-001** | Movement Scope | Shared | WS-PROTO-005 | TC-MOVE-001 | Planned |
| **FRS-MOVE-002** | Boundary Handling | Shared | WS-PROTO-005 | TC-MOVE-002 | Planned |
| **FRS-MOVE-003** | Snap-to-Grid | Frontend | - | - | Deferred |
| **FRS-MOVE-004** | Collision Detection | Backend | - | - | N/A |
| **FRS-UI-001** | Cursor Visibility | Frontend | WS-PROTO-008 | TC-UI-001 | Planned |
| **FRS-UI-002** | Zoom and Pan | Frontend | - | TC-UI-002 | Planned |
| **FRS-DATA-001** | Autosave | Backend | - | TC-DATA-001 | Planned |
| **FRS-DATA-002** | Version History | Backend | WS-PROTO-007 | TC-DATA-002 | Planned |
| **FRS-DATA-003** | State Model | Backend | WS-PROTO-003, 007 | TC-DATA-003 | Planned |
| **FRS-DATA-004** | Multiple Formations | Backend | - | TC-DATA-004 | Planned |
| **FRS-NET-001** | Reconnect Logic | Shared | WS-PROTO-002 | TC-NET-001 | Planned |
| **FRS-NET-002** | Server Restart | Backend | - | TC-NET-002 | Planned |
| **FRS-NFR-001** | Performance (MVP) | Shared | WS-PROTO-008 | TC-LOAD-001 | Planned |
| **FRS-ROLE-001** | Role Tagging | Backend | - | TC-ROLE-001 | Planned |
| **FRS-MATCH-001** | Match Start Behavior | Backend | WS-PROTO-007 | TC-MATCH-001 | Planned |

## Coverage Analysis

*   **Total Requirements**: 27
*   **Protocol Coverage**: 14/27
*   **Test Case Coverage**: 25/27 (Snap-to-Grid deferred, Collision N/A)

## Gap Analysis

*   **Missing Tests**: Specific automation for `FRS-NET-002` (Server Restart) requires integration test env.

---

# Cross-References

*   **Primary Source**: [01-BRD.md](01-BRD.md), [02-FRS.md](02-FRS.md).
*   **Validation Target**: [07-Test-Plan-QA-Strategy.md](07-Test-Plan-QA-Strategy.md).

