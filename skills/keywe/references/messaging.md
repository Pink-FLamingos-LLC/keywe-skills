# Messaging & Templates API Reference

## Contents

- Message Templates (fields, endpoints: GET, POST, GET/{id}, PATCH/{id}, DELETE/{id})
- Messages / History (GET /api/messages, GET /api/messages/{id})
- Send Message (POST /api/messages/send, reservation resolution, error cases)

## Message Templates

Templates are reusable message content with `{{variable}}` substitution. Variables include `{{guestName}}`, `{{propertyName}}`, `{{accessCode}}`, `{{checkInDate}}`, `{{checkOutDate}}`, `{{supportPhone}}`.

### Template Fields

| Field         | Type    | Description                                             |
| ------------- | ------- | ------------------------------------------------------- | --------------------------------------------------- |
| `id`          | string  | UUID                                                    |
| `name`        | string  | Display name (required, max 200)                        |
| `category`    | string  | e.g. "check-in", "check-out", "maintenance" (required)  |
| `channel`     | string  | "sms" or "email" (default: "sms")                       |
| `subject`     | string  | null                                                    | Email subject (required for email channel, max 500) |
| `content`     | string  | Message body with `{{variables}}` (required, max 10000) |
| `senderEmail` | string  | null                                                    | Verified sender email for email channel             |
| `status`      | string  | "active" or "inactive" (default: "active")              |
| `usageCount`  | number  | Auto-incremented on use                                 |
| `isPriority`  | boolean | Sends before non-priority in automation queues          |

### Endpoints

#### `GET /api/templates?category={category}`

List templates. Optionally filter by category.

#### `POST /api/templates`

Create a template.

**Request:**

```json
{
  "name": "Check-in Welcome",
  "category": "check-in",
  "channel": "sms",
  "content": "Hi {{guestName}}, welcome to {{propertyName}}! Your door code is {{accessCode}}.",
  "status": "active"
}
```

#### `GET /api/templates/{id}`

Get single template.

#### `PATCH /api/templates/{id}`

Partial update. Set `status: "inactive"` to disable without deleting.

**Request:**

```json
{ "name": "Updated Name", "isPriority": true }
```

#### `DELETE /api/templates/{id}`

Permanently delete template. Automations referencing it will continue to exist but may fail.

---

## Messages (History)

### `GET /api/messages?reservationId={id}`

List messages. Optionally filter by reservation. Sorted by creation date (newest first? check DB query — no explicit sort, likely DB default).

**Response 200:**

```json
[
  {
    "id": "msg_abc123",
    "reservationId": "res_abc123",
    "guestPhone": "+17155551234",
    "channel": "sms",
    "direction": "outbound",
    "body": "Welcome! Your check-in has been confirmed.",
    "createdAt": "2025-07-15T14:00:00Z"
  }
]
```

### `GET /api/messages/{id}`

Get single message by ID.

---

## Send Message

### `POST /api/messages/send`

Send an SMS or email. Resolves reservation automatically by ID, phone, or email.

**Request (SMS):**

```json
{
  "channel": "sms",
  "phone": "+17155551234",
  "body": "Hi John, your reservation is confirmed!",
  "reservationId": "res_abc123"
}
```

**Request (Email):**

```json
{
  "channel": "email",
  "email": "john@example.com",
  "subject": "Your stay details",
  "body": "Hi John, your reservation is confirmed!",
  "reservationId": "res_abc123"
}
```

**Reservation resolution order:**

1. If `reservationId` provided, look up by ID
2. If not found (or not provided), look up by phone (SMS) or email (email)
3. `404` if no reservation found

**Error cases:**

- `400` if email is blocked (bounced/complained in `email_blocklist` table)
- `400` if required field missing for channel (e.g., `email` + `subject` for email, `phone` for SMS)
