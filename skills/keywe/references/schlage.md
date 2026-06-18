# Schlage Smart Lock API Reference

## Contents

- Architecture
- Authentication Flow (login, auto-refresh, logout)
- Proxy Endpoints (lock ops, access codes, auth)
- Lock Sync Behavior
- MCP Tools
- Error Handling

## Architecture

KeyWe proxies all Schlage API calls through `/api/schlage/[...path]`. The pyschlage backend runs as a separate service accessed via `SCHLAGE_API_BASE_URL`.

```
Client → KeyWe Proxy → pyschlage API → Schlage Cloud
```

## Authentication Flow

1. **Login**: `POST /api/schlage/auth/token` with form-encoded `username` + `password`
   - Proxy forwards to pyschlage `/auth/token`
   - On success, stores `access_token`, email, password in `auth_keys` table
   - Sets `token` cookie (httpOnly, secure, 24h)
   - Returns `{ "access_token": "...", "expires_in": 86400 }`

2. **Auto-refresh**: On `401` responses, proxy calls `refreshToken()` which:
   - Reads email + password from `auth_keys` table
   - Calls `/auth/token` again
   - Updates stored token
   - Retries the original request

3. **Logout**: `POST /api/schlage/auth/logout`
   - Clears `auth_keys` row for schlage provider
   - Clears `token` cookie

**Credentials stored in `auth_keys` table:**

- `key` (access token)
- `email` (Schlage account email)
- `password` (Schlage account password, stored for auto-refresh)
- `access_token_expires_at` (timestamp)

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

### Auth

| Endpoint                   | Method | Description                                    |
| -------------------------- | ------ | ---------------------------------------------- |
| `/api/schlage/auth/token`  | POST   | Login with username + password (form-encoded). |
| `/api/schlage/auth/logout` | POST   | Logout and clear stored credentials.           |

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

- `schlage-login` — Authenticate with Schlage credentials
- `schlage-logout` — Clear Schlage authentication
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
