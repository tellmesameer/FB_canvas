# 08. Requirements Traceability Matrix (RTM)

| FRS ID | Requirement Name | Protocol Ref | Test Case Ref | Status |
| :--- | :--- | :--- | :--- | :--- |
| **FRS-USER-001** | Access Policy | - | TC-USER-001 | Planned |
| **FRS-USER-002** | Roles (Coach/Player) | WS-PROTO-002 | TC-USER-002 | Planned |
| **FRS-ROOM-001** | Room Creation | - | TC-ROOM-001 | Planned |
| **FRS-ROOM-002** | Room Capacity | WS-PROTO-002 | TC-ROOM-002 | Planned |
| **FRS-ROOM-003** | Join Policy | WS-PROTO-002 | TC-ROOM-003 | Planned |
| **FRS-ROOM-004** | Room Lifecycle | - | TC-ROOM-004 | Planned |
| **FRS-PERM-001** | Default Move Rule | WS-PROTO-005 | TC-PERM-001 | Planned |
| **FRS-PERM-002** | Coach Restrictions | - | TC-PERM-002 | Planned |
| **FRS-LOCK-001** | Drag Concurrency | WS-PROTO-004, 006 | TC-LOCK-01 | Planned |
| **FRS-TEAM-001** | Team Structure | - | TC-TEAM-001 | Planned |
| **FRS-TEAM-002** | Team Configuration | WS-PROTO-007 | TC-TEAM-002 | Planned |
| **FRS-TEAM-003** | Bench Logic | WS-PROTO-005 | TC-TEAM-003 | Planned |
| **FRS-MOVE-001** | Movement Scope | WS-PROTO-005 | TC-MOVE-001 | Planned |
| **FRS-MOVE-002** | Boundary Handling | WS-PROTO-005 | TC-MOVE-002 | Planned |
| **FRS-MOVE-003** | Snap-to-Grid | - | - | Deferred |
| **FRS-MOVE-004** | Collision Detection | - | - | N/A |
| **FRS-UI-001** | Cursor Visibility | WS-PROTO-008 | TC-UI-001 | Planned |
| **FRS-UI-002** | Zoom and Pan | - | TC-UI-002 | Planned |
| **FRS-DATA-001** | Autosave | - | TC-DATA-001 | Planned |
| **FRS-DATA-002** | Version History | WS-PROTO-007 | TC-DATA-002 | Planned |
| **FRS-DATA-003** | State Model | WS-PROTO-003, 007 | TC-DATA-003 | Planned |
| **FRS-DATA-004** | Multiple Formations | - | TC-DATA-004 | Planned |
| **FRS-NET-001** | Reconnect Logic | WS-PROTO-002 | TC-NET-001 | Planned |
| **FRS-NET-002** | Server Restart | - | TC-NET-002 | Planned |
| **FRS-NFR-001** | Performance (MVP) | WS-PROTO-008 | TC-LOAD-001 | Planned |
| **FRS-ROLE-001** | Role Tagging | - | TC-ROLE-001 | Planned |
| **FRS-MATCH-001** | Match Start Behavior | WS-PROTO-007 | TC-MATCH-001 | Planned |

## Coverage Analysis

*   **Total Requirements**: 27
*   **Protocol Coverage**: 14/27
*   **Test Case Coverage**: 25/27 (Snap-to-Grid deferred, Collision N/A)

## Gap Analysis

*   **Missing Tests**: Specific automation for `FRS-NET-002` (Server Restart) requires integration test env.
