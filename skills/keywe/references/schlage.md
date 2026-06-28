# Schlage Smart Lock API Reference

## Contents

- Architecture
- Proxy Endpoints (lock ops, access codes)
- Lock Sync Behavior
- MCP Tools
- Error Handling

## Architecture

KeyWe proxies all Schlage API calls through `/api/schlage/[...path]`. The pyschlage backend runs as a separate service accessed via `SCHLAGE_API_BASE_URL`.

```
Client → KeyWe Proxy → pyschlage API → Schlage Cloud
```

## Proxy Endpoints

All methods (GET, POST, PUT, PATCH, DELETE) accepted. Proxied paths:

### Lock Operations

| Endpoint                                | Method | Description                                      |
| --------------------------------------- | ------ | ------------------------------------------------ |
| `/api/schlage/locks`                    | GET    | List all Schlage locks. Auto-syncs to local DB.  |
| `/api/schlage/locks/{device_id}`        | GET    | Get single lock details. Auto-syncs to local DB. |
| `/api/schlage/locks/{device_id}/lock`   | POST   | Lock a door. No body.                            |
| `/api/schlage/locks/{device_id}/unlock` | POST   | Unlock a door. No body.                          |
| `/api/schlage/locks/{device_id}/logs`   | GET    | Get lock activity logs.                          |

### Access Codes

| Endpoint                                                | Method | Description                   |
| ------------------------------------------------------- | ------ | ----------------------------- |
| `/api/schlage/locks/{device_id}/access_codes`           | GET    | List access codes for a lock. |
| `/api/schlage/locks/{device_id}/access_codes`           | POST   | Create access code.           |
| `/api/schlage/locks/{device_id}/access_codes/{code_id}` | DELETE | Delete access code.           |

**Request body for creating access codes:**

```json
{
  "name": "Guest Code",
  "code": "1234",
  "start_date": "2025-07-15",
  "end_date": "2025-07-17"
}
```

## Lock Sync Behavior

On GET responses for `/locks` and `/locks/{id}`, the proxy auto-upserts lock data into the local DB:

```json
{
  "device_id": "SCH-12345",
  "name": "Front Door",
  "model_name": "Encode Plus",
  "battery_level": 85,
  "is_locked": true,
  "is_jammed": false,
  "firmware_version": "2.3.1",
  "mac_address": "AA:BB:CC:DD:EE:FF"
}
```

This means you do not need to manually create lock records — listing locks via the schlage proxy will populate the local DB automatically.

## MCP Tools

The MCP server exposes these Schlage tools:

- `schlage-credentials-status` — Check if Schlage credentials are configured
- `schlage-list-locks` — List all Schlage locks
- `schlage-get-lock` — Get a single lock by device ID
- `schlage-lock-door` — Lock a door
- `schlage-unlock-door` — Unlock a door
- `schlage-list-access-codes` — List access codes for a lock
- `schlage-create-access-code` — Create an access code
- `schlage-delete-access-code` — Delete an access code
- `schlage-get-logs` — Get lock activity logs

## Error Handling

- `401` with message matching `/invalid or expired auth/i` triggers automatic token refresh
- Failed refresh clears stored credentials
- Non-`auth/` paths with non-ok responses throw the raw error body
