# Reservations API Reference

## Contents

- Reservation Fields table
- Endpoints (GET, POST, GET/{id}, PATCH/{id}, DELETE/{id})
- Check-in (POST /api/checkin)
- Phone Normalization

## Reservation Fields

| Field           | Type   | Description                              |
| --------------- | ------ | ---------------------------------------- | ----------------------------------------------------------------- | ------ |
| `id`            | string | UUID                                     |
| `name`          | string | Guest name (required, max 200)           |
| `email`         | string | null                                     | Guest email (optional, must be valid format if provided, max 254) |
| `guestPhone`    | string | null                                     | E.164 format (auto-normalized via libphonenumber-js, max 30)      |
| `notes`         | string | null                                     | Internal notes (max 2000)                                         |
| `accessPointId` | string | null                                     | Assigned room                                                     |
| `checkIn`       | string | null                                     | ISO 8601 datetime                                                 |
| `checkOut`      | string | null                                     | ISO 8601 datetime                                                 |
| `status`        | string | e.g. "confirmed", "pending", "cancelled" |
| `guestEmail`    | string | null                                     | Secondary guest email for messaging                               |
| `checkInStatus` | string | null                                     | "pending"                                                         | "sent" |
| `propertyName`  | string | null                                     | (Read-only, populated on list/get)                                |
| `roomName`      | string | null                                     | (Read-only, populated on list/get)                                |

## Endpoints

### `GET /api/reservations`

List all reservations for the authenticated user. Includes `propertyName` and `roomName` from joined access point/property data.

**Response 200:**

```json
[
  {
    "id": "res_abc123",
    "name": "John Doe",
    "guestPhone": "+17155551234",
    "accessPointId": "ap_abc123",
    "propertyName": "Lakefront Cabin",
    "roomName": "Master Bedroom",
    "checkIn": "2025-07-15T15:00:00Z",
    "checkOut": "2025-07-17T11:00:00Z",
    "status": "confirmed",
    "checkInStatus": "pending"
  }
]
```

### `POST /api/reservations`

Create a reservation. Phone is auto-normalized to E.164.

**Request:**

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "guestPhone": "17155551234",
  "notes": "Late check-in"
}
```

### `GET /api/reservations/{id}`

Get single reservation. `404` if not found.

### `PATCH /api/reservations/{id}`

Partial update. All fields optional except at least one required.

**Request:**

```json
{
  "name": "John Updated",
  "accessPointId": "ap_def456",
  "checkIn": "2025-07-15T16:00:00Z",
  "checkOut": null,
  "status": "cancelled",
  "checkInStatus": "sent"
}
```

Date validation: strings must parse as valid ISO 8601.

### `DELETE /api/reservations/{id}`

Delete reservation. Cascade deletes associated messages. Returns `{ "success": true }`.

---

## Check-in

### `POST /api/checkin`

Send a check-in notification to a guest.

**Request:**

```json
{
  "channel": "sms",
  "phone": "+17155551234"
}
```

or

```json
{
  "channel": "email",
  "email": "john@example.com"
}
```

**Behavior:**

1. Looks up reservation by phone or email
2. Sends SMS via AWS Pinpoint or email via AWS SES
3. Records message in DB with direction: "outbound"
4. Sets reservation `checkInStatus` to "sent"

**Response 200:**

```json
{
  "message": { "id": "msg_abc123", ... },
  "reservation": { "checkInStatus": "sent", ... }
}
```

**Error cases:**

- `400` if required field missing for channel
- `404` if no reservation found
- `400` if email address is blocked (bounced/complained)

## Phone Normalization

All phone numbers are normalized via `libphonenumber-js`:

- Input can be E.164 (`+17155551234`), US national (`(715) 555-1234`), or 10-digit (`7155551234`)
- Stored as E.164 (`+17155551234`)
- Invalid phone numbers return as-is (no error)
