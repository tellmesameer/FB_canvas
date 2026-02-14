# 14. Change Management & Versioning

## 1. Documentation Versioning

*   **Format**: `v[Major].[Minor]`, e.g., `v1.2`.
*   **Tracked in**: `00-Architecture-Index.md` (Version History Table).
*   **Policy**: Major version bump for breaking architectural changes. Minor for additions/corrections.

## 2. API Versioning (Semantic Versioning)

### 2.1 REST API
*   URI Path Versioning: `/api/v1/rooms`.
*   Breaking changes require `/api/v2/...`.
*   Deprecation policy: 1 month warning before v1 retirement.

### 2.2 WebSocket Protocol
*   Handshake includes protocol version: `CONNECT /ws?v=1.0`.
*   Server rejects mismatched client versions to prevent undefined behavior.

## 3. Database Migration Rules

1.  **Never rewrite history**: Migrations are strictly additive.
2.  **Backwards Compatibility**: New columns must be `NULLABLE` or have `DEFAULT`.
3.  **Destructive Changes**: Done in two phases (Deprecate -> Drop).

## 4. Breaking Change Policy

If a change breaks existing clients (e.g. changing event payload structure):
1.  Bump Protocol Version.
2.  Force client refresh (Server sends `FORCE_RELOAD` event).
3.  Deploy during maintenance window.
