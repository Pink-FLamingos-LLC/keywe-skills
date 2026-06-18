# Properties, Access Points & Locks API Reference

## Contents

- Entity Hierarchy
- Properties (GET, POST, GET/{id}, PATCH/{id}, DELETE/{id})
- Access Points / Rooms (GET, POST, GET/{id}, PATCH/{id}, DELETE/{id})
- Locks (GET, POST, link, unlink)
- Lock Fields table

## Entity Hierarchy

```
Property
 └── Access Point (room)
      └── Lock (Schlage device)
```

## Properties

### `GET /api/properties`

List all properties with nested access points and locks.

**Response 200:**

```json
[
  {
    "id": "prop_abc123",
    "userId": "user_abc123",
    "name": "Lakefront Cabin",
    "address": "123 Pine Street, Lake Tahoe, CA",
    "createdAt": "2025-06-01T12:00:00.000Z",
    "updatedAt": "2025-06-15T08:30:00.000Z",
    "accessPoints": [
      {
        "id": "ap_abc123",
        "propertyId": "prop_abc123",
        "name": "Master Bedroom",
        "roomType": "bedroom",
        "createdAt": "...",
        "updatedAt": "...",
        "locks": []
      }
    ]
  }
]
```

### `POST /api/properties`

Create a property.

**Request:**

```json
{
  "name": "Lakefront Cabin",
  "address": "123 Pine Street, Lake Tahoe, CA"
}
```

`name` required (max 200). `address` optional (max 500).

**Response 201:** Single property object with `accessPoints: []`.

### `GET /api/properties/{id}`

Get single property with access points. `404` if not found or not owned.

### `PATCH /api/properties/{id}`

Partial update. Any field optional, at least one required. Set `address: null` to clear.

**Request:**

```json
{ "name": "Updated Name", "address": null }
```

### `DELETE /api/properties/{id}`

Delete property and cascade: access points unlink their locks, locks remain user-owned with `accessPointId` set to null. Returns `{ "success": true }`.

---

## Access Points (Rooms)

### `GET /api/access-points?propertyId={id}`

List access points for a property. Requires `propertyId` query param. Verifies property ownership.

### `POST /api/access-points`

Create an access point.

**Request:**

```json
{
  "name": "Master Bedroom",
  "propertyId": "prop_abc123",
  "roomType": "bedroom",
  "lockId": "lock_abc123"
}
```

`name` and `propertyId` required. `roomType` and `lockId` optional.

### `GET /api/access-points/{id}?propertyId={propertyId}`

Get single access point with its locks. Requires `propertyId` query param.

### `PATCH /api/access-points/{id}`

Partial update. Set `roomType: null` to clear.

**Request:**

```json
{ "name": "Updated Room", "roomType": null }
```

### `DELETE /api/access-points/{id}`

Delete access point. Unlinks its locks (sets `accessPointId` to null). Returns `{ "success": true }`.

---

## Locks

### `GET /api/locks?accessPointId={id}`

List locks. Without query param: returns all user locks. With `accessPointId`: only locks for that access point.

### `GET /api/locks/unlinked`

List locks not assigned to any access point.

### `POST /api/locks`

Create a lock record. For Schlage locks, use schlage proxy instead — this is for manual records.

**Request:**

```json
{
  "name": "Front Door Schlage",
  "accessPointId": "ap_abc123",
  "deviceId": "SCH-ENCODE-12345",
  "lockType": "schlage_encode"
}
```

`name` and `accessPointId` required. `deviceId` and `lockType` optional.

### `POST /api/locks/{id}/link`

Link a lock to an access point.

**Request:** `{ "accessPointId": "ap_abc123" }`

Error `404` if access point or lock not found/not owned.

### `POST /api/locks/{id}/unlink`

Unlink a lock from its access point. No body required. Returns `{ "success": true }`.

---

## Lock Fields

| Field             | Type    | Description  |
| ----------------- | ------- | ------------ | ------------------------------- |
| `id`              | string  | UUID         |
| `userId`          | string  | Owner        |
| `accessPointId`   | string  | null         | Linked room or null if unlinked |
| `name`            | string  | Display name |
| `deviceId`        | string  | null         | Schlage serial                  |
| `lockType`        | string  | null         | e.g. "schlage_encode"           |
| `modelName`       | string  | null         | e.g. "Encode Plus"              |
| `isLocked`        | boolean | null         | Current state                   |
| `isJammed`        | boolean | null         | Jammed state                    |
| `batteryLevel`    | number  | null         | 0–100                           |
| `firmwareVersion` | string  | null         | e.g. "2.3.1"                    |
| `macAddress`      | string  | null         | MAC address                     |
