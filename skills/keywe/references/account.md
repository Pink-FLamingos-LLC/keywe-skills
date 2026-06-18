# Account & Auth API Reference

## Contents

- API Keys (GET, DELETE)
- Account Export (GET /api/account/export)
- Account Deletion (POST /api/account/delete, cascade order)
- Schlage Credentials (stored fields, setting, clearing, auto-cleanup)
- Better Auth Endpoints (table)

## API Keys

### `GET /api/account/keys`

List API keys for the authenticated user. Full key value is never returned — only prefix.

**Response 200:**

```json
[
  {
    "id": "ak_abc123def456",
    "keyPrefix": "keywe_ab",
    "label": "Production API Key",
    "createdAt": "2025-06-01T12:00:00.000Z"
  }
]
```

### `DELETE /api/account/keys/{id}`

Delete an API key. Immediate revocation. Returns `{ "success": true }`.

API keys are generated via Better Auth (settings page or Better Auth API). The full key is shown once at creation time. Stored as SHA-256 hash.

---

## Account Export

### `GET /api/account/export`

Download all account data as a JSON file attachment. Includes:

- Account info
- User profile
- Sessions
- Connected accounts (OAuth providers)
- Secondary emails
- API keys (without full key value)
- Schlage integration status (password masked as `"***"`)
- Properties with nested rooms and locks
- Unlinked locks
- Reservations with message history
- Message templates

**Response:** JSON file download with `content-disposition: attachment`.

---

## Account Deletion

### `POST /api/account/delete`

Permanently delete account and all associated data.

**Request:**

```json
{ "confirm": "DELETE" }
```

**Deletion cascade order:**

1. Messages (by reservation IDs)
2. Reservations
3. Message templates
4. Access points (with locks unlinked)
5. Locks
6. Properties
7. Auth keys (Schlage credentials)
8. API keys
9. Secondary emails
10. Sessions
11. Accounts (Better Auth)
12. User record

**Response:** Redirect to `/login?deleted=1`.

---

## Schlage Credentials

Schlage credentials are stored in the `auth_keys` table with `provider = "schlage"`.

### Stored Fields

- `key` - Current access token
- `email` - Schlage account email
- `password` - Schlage account password (stored for auto-refresh on 401)
- `access_token_expires_at` - Token expiration timestamp

### Setting Credentials

- Via the app UI (Schlage settings page)
- Via the MCP `schlage-login` tool
- Via `POST /api/schlage/auth/token` with form-encoded `username` + `password`

### Clearing Credentials

- Via the app UI
- Via the MCP `schlage-logout` tool
- Via `POST /api/schlage/auth/logout`

### Auto-cleanup on Failed Refresh

If `refreshToken()` fails (Schlage API unreachable or credentials invalid), the stored credentials are deleted from the `auth_keys` table. The user must re-authenticate.

---

## Better Auth Endpoints

Better Auth handles authentication at `/api/auth/*`:

| Endpoint                         | Purpose                           |
| -------------------------------- | --------------------------------- |
| `POST /api/auth/register`        | Create account (email + password) |
| `POST /api/auth/login`           | Sign in                           |
| `POST /api/auth/logout`          | Sign out                          |
| `GET /api/auth/session`          | Get current session               |
| `POST /api/auth/forgot-password` | Request password reset            |
| `POST /api/auth/reset-password`  | Reset password with token         |
| `POST /api/auth/verify-email`    | Verify email address              |
| `GET /api/auth/api-key`          | Generate an API key               |

Auth routes are excluded from rate limiting and CORS checks. All custom API routes require a valid Bearer token (API key or session cookie).
