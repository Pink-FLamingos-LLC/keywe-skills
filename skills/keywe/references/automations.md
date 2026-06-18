# Automations API Reference

## Contents

- Automation Model (fields table)
- Endpoints (GET, POST, GET/{id}, PUT/{id}, DELETE/{id})
- Trigger Types (event triggers, time triggers)
- Condition Types
- Action Types
- Automation Send (internal endpoint)

## Automation Model

Automations have a three-part config: triggers → [conditions] → actions. All stored as JSON arrays in the database.

| Field         | Type              | Description                           |
| ------------- | ----------------- | ------------------------------------- | ------------------------ |
| `id`          | string            | UUID                                  |
| `name`        | string            | Display name (required)               |
| `description` | string            | null                                  | Optional description     |
| `icon`        | string            | Icon identifier e.g. "HandWavingIcon" |
| `triggers`    | TriggerConfig[]   | Events or times that start automation |
| `conditions`  | ConditionConfig[] | Filters (AND logic)                   |
| `actions`     | ActionConfig[]    | What to do when triggered             |
| `status`      | string            | "active" or "paused"                  |
| `runCount`    | number            | Auto-incremented                      |
| `lastRunAt`   | string            | null                                  | Last execution timestamp |

## Endpoints

### `GET /api/automations`

List all automations for authenticated user.

### `POST /api/automations`

Create automation. Requires `name` and at least one trigger.

**Request:**

```json
{
  "name": "Guest Welcome Sequence",
  "description": "Sends welcome instructions when a booking is confirmed",
  "icon": "HandWavingIcon",
  "triggers": [
    {
      "id": "trg_1",
      "kind": "trigger",
      "type": "event",
      "event": "reservation.added",
      "label": "On Reservation Added"
    }
  ],
  "conditions": [],
  "actions": [
    {
      "id": "act_1",
      "kind": "action",
      "type": "send_message",
      "label": "Send Welcome Message",
      "templateId": "tpl_abc123"
    }
  ]
}
```

### `GET /api/automations/{id}`

Get single automation.

### `PUT /api/automations/{id}`

Full update — all fields replaced. `status` can be set to `"paused"` to disable.

**Request:** Same shape as POST.

### `DELETE /api/automations/{id}`

Delete automation. Returns `{ "success": true }`.

---

## Trigger Types

### Event Triggers (`type: "event"`)

| Event                   | When It Fires            |
| ----------------------- | ------------------------ |
| `reservation.added`     | New reservation created  |
| `reservation.cancelled` | Reservation cancelled    |
| `lock.jammed`           | Lock enters jammed state |
| `message.received`      | Guest sends a message    |

### Time Triggers (`type: "time"`)

```json
{
  "id": "trg_2",
  "kind": "trigger",
  "type": "time",
  "timeConfig": {
    "relativeTo": "checkin",
    "value": 1,
    "unit": "hours"
  },
  "label": "1 Hour Before Check-in"
}
```

`relativeTo`: `"checkin"` | `"checkout"`
`unit`: `"minutes"` | `"hours"` | `"days"`

---

## Condition Types

| Type             | Description                              |
| ---------------- | ---------------------------------------- |
| `all_properties` | Applies to all properties                |
| `property`       | Filter by a specific property            |
| `rooms`          | Filter by specific rooms (access points) |

```json
{
  "id": "cond_1",
  "kind": "condition",
  "type": "rooms",
  "propertyId": "prop_abc123",
  "propertyName": "Lakefront Cabin",
  "accessPointIds": ["ap_abc123"],
  "accessPointNames": ["Master Bedroom"],
  "label": "Master Bedroom Only"
}
```

Conditions use AND logic — all must match for the automation to run.

---

## Action Types

| Type                       | Description                           |
| -------------------------- | ------------------------------------- |
| `send_message`             | Send an SMS or email using a template |
| `provision_access`         | Generate and send access codes        |
| `lock_command`             | Lock/unlock a door                    |
| `lock_command_and_message` | Lock command + send notification      |

```json
{
  "id": "act_2",
  "kind": "action",
  "type": "send_message",
  "label": "Send Check-in Instructions",
  "templateId": "tpl_abc123",
  "messageTemplateId": "tpl_abc123"
}
```

Both `templateId` and `messageTemplateId` are accepted for the template reference.

---

## Automation Send (Internal)

### `POST /api/automations/send`

Internal endpoint (authenticated via `X-API-Secret` header, not user API key). Used by the automation runtime to send messages.

**Request:**

```json
{
  "userId": "user_abc123",
  "reservationId": "res_abc123",
  "guestPhone": "+17155551234",
  "guestEmail": "john@example.com",
  "body": "Hi John, your reservation is confirmed!"
}
```
