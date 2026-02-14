# REST API Specification (OpenAPI-Level Contract)

## Project: Real-Time Collaborative Football Tactical Canvas

## Base Path: `/api/v1`

## Auth Model (MVP): Role + room-bound context (no JWT yet)

## Content-Type: `application/json`

## Error Format: Standardized

This REST layer handles:

* Room creation
* Formation management
* Team configuration
* Match control
* Health checks

Real-time mutations remain WebSocket-only.

---

# 1. Global Conventions

## 1.1 Standard Response Wrapper

Successful response:

```json
{
  "data": { ... },
  "meta": {
    "timestamp": "ISO-8601",
    "request_id": "uuid"
  }
}
```

Error response:

```json
{
  "error": {
    "code": 400,
    "type": "ValidationError",
    "message": "Description",
    "details": {}
  }
}
```

---

# 2. Room Management

---

## 2.1 Create Room (Ref: SM-ROOM-01)

**POST** `/rooms`

Creates a new room. Only Coach role allowed.

### Request

```json
{
  "room_name": "Training Match",
  "match_duration_minutes": 90,
  "custom_slug": "optional-slug"
}
```

### Validation Rules

* match_duration_minutes > 0
* custom_slug unique if provided

### Response

```json
{
  "data": {
    "room_id": "uuid-or-slug",
    "match_duration_minutes": 90,
    "created_at": "ISO"
  }
}
```

---

## 2.2 Get Room Info

**GET** `/rooms/{room_id}`

Returns room metadata.

### Response

```json
{
  "data": {
    "room_id": "uuid",
    "match_status": "setup",
    "match_duration_minutes": 90,
    "created_at": "ISO",
    "expires_at": "ISO"
  }
}
```

---

## 2.3 Delete Room (Coach Only) (Ref: SM-ROOM-01)

**DELETE** `/rooms/{room_id}`

Soft deletes room.

### Response

```json
{
  "data": {
    "deleted": true,
    "scheduled_purge_at": "ISO-7-days-later"
  }
}
```

**Policy:**
* Immediate soft-delete (hidden from API).
* Hard delete data + formations after 7 days.


---

# 3. Team Management

---

## 3.1 Get Teams

**GET** `/rooms/{room_id}/teams`

```json
{
  "data": [
    {
      "team_id": "home",
      "name": "Home",
      "color": "#0055ff"
    },
    {
      "team_id": "away",
      "name": "Away",
      "color": "#ff0000"
    }
  ]
}
```

---

## 3.2 Update Team (Before Match Start Only)

**PUT** `/rooms/{room_id}/teams/{team_id}`

Coach only.

### Request

```json
{
  "name": "Blue Team",
  "color": "#0000ff"
}
```

### Validation

* Reject if match_status != setup

---

# 4. Match Control

---

## 4.1 Start Match (Ref: SM-MATCH-01)

**POST** `/rooms/{room_id}/match/start`

Coach only.

### Response

```json
{
  "data": {
    "match_status": "live",
    "started_at": "ISO"
  }
}
```

Effects:

* Locks team rename
* Locks color change
* Locks role editing

---

## 4.2 End Match (Ref: SM-MATCH-01)

**POST** `/rooms/{room_id}/match/end`

Coach only.

Response:

```json
{
  "data": {
    "match_status": "expired"
  }
}
```

---

# 5. Formation Management

---

## 5.1 List Formations

**GET** `/rooms/{room_id}/formations`

```json
{
  "data": [
    {
      "formation_id": "v1",
      "version": 32,
      "created_at": "ISO",
      "author": "Coach"
    }
  ]
}
```

---

## 5.2 Create Formation (Manual Save)

**POST** `/rooms/{room_id}/formations`

Coach only.

### Request

```json
{
  "name": "4-4-2 Defensive"
}
```

Server captures current canonical state.

### Response

```json
{
  "data": {
    "formation_id": "uuid",
    "version": 45,
    "created_at": "ISO"
  }
}
```

---

## 5.3 Get Formation Snapshot

**GET** `/rooms/{room_id}/formations/{formation_id}`

Returns full canonical snapshot.

```json
{
  "data": {
    "snapshot": { ...canonical_room_state_json... }
  }
}
```

---

## 5.4 Delete Formation

**DELETE** `/rooms/{room_id}/formations/{formation_id}`

Coach only.

---

# 6. Autosave Configuration

---

## 6.1 Update Autosave Interval

**PUT** `/rooms/{room_id}/autosave`

Coach only.

### Request

```json
{
  "interval_seconds": 30
}
```

Validation:

* Minimum 10 seconds
* Maximum 300 seconds

---

# 7. User Management (REST Metadata Only)

---

## 7.1 List Users

**GET** `/rooms/{room_id}/users`

```json
{
  "data": [
    {
      "client_id": "uuid",
      "display": "Sam #9",
      "role": "player",
      "status": "online"
    }
  ]
}
```

---

# 8. Health & System

---

## 8.1 Basic Health

**GET** `/health`

```json
{
  "status": "ok"
}
```

---

## 8.2 DB Health

**GET** `/health/db`

---

## 8.3 Redis Health

**GET** `/health/redis`

---

# 9. Status Codes

| Code | Meaning          |
| ---- | ---------------- |
| 200  | Success          |
| 201  | Created          |
| 400  | Validation Error |
| 401  | Unauthorized     |
| 403  | Forbidden        |
| 404  | Not Found        |
| 409  | Conflict         |
| 429  | Rate Limit       |
| 500  | Server Error     |

---

# 10. Validation Rules (Global)

* JSON body max size limited.
* Display name length ≤ 30.
* Team color must be valid HEX.
* Formation name length ≤ 50.
* Match duration ≤ 300 minutes.
* **Team Roster Limit**: Max 25 (includes active + bench).
* **On-Field Limit**: Max 11.


---

# 11. Idempotency Rules

For:

* Create Room
* Create Formation
* Start Match (Reason: avoid race conditions)


Optional header:

```
Idempotency-Key: uuid
```

Prevents duplicate creation on retry.

---

# 12. OpenAPI Compliance Notes

* All endpoints documented in Swagger.
* Schemas defined in Pydantic models.
* Request/response examples included.
* Strict typing enforced.

---

# Boundary Clarification

REST handles:

* Setup
* Configuration
* Persistence
* Metadata
* Match lifecycle

WebSocket handles:

* Real-time mutations
* Movement
* Locking
* Cursor updates

Strict separation maintained.

---

System contract layer now fully defined:

* [WebSocket Protocol](03-WebSocket-Protocol-Spec.md)
* [REST API](04-REST-API-Spec.md)
* [Frontend TDD](06-Frontend-TDD.md)
* [Backend TDD](05-Backend-TDD.md)
* [FRS](02-FRS.md)
* [BRD](01-BRD.md)
