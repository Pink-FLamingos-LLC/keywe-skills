# Common Use Cases

## Contents

1. Full Property Onboarding (Schlage Lock)
2. Bulk Property Setup (Multiple Rooms)
3. Guest Check-In With Access Code
4. Smart Lock Maintenance and Monitoring
5. Emergency Lockout Resolution
6. Guest Communication Thread
7. Multi-Property Account Management
8. Automation Sequence With Conditions

## 1. Full Property Onboarding (Schlage Lock)

Provision a new property with a Schlage lock and guest welcome automation.

```bash
# Step 1: Add property
uv run <skill-dir>/scripts/client.py --action add-property --name "Lakefront Cabin" --address "123 Pine St, Lake Tahoe, CA"

# Step 2: Add access point (bedroom)
uv run <skill-dir>/scripts/client.py --action add-access-point --name "Master Bedroom" --property-id "prop_<id>" --room-type "bedroom"

# Step 3: Add and link lock
uv run <skill-dir>/scripts/client.py --action add-lock --name "Front Door" --access-point-id "ap_<id>" --device-id "SCH-ENCODE-12345" --lock-type "schlage_encode"

# Step 4: Create check-in template
uv run <skill-dir>/scripts/client.py --action add-template --name "Check-in Instructions" --category "check-in" --channel "sms" --content "Hi {{guestName}}, welcome to {{propertyName}}! Your door code is {{accessCode}}. Wi-Fi: GuestNetwork / welcome2025."

# Step 5: Create welcome automation
uv run <skill-dir>/scripts/client.py --action add-automation --name "Welcome Sequence" --triggers '[{"id":"trg_1","kind":"trigger","type":"event","event":"reservation.added","label":"On Reservation"}]'

# Step 6: Add reservation
uv run <skill-dir>/scripts/client.py --action add-reservation --name "Jane Smith" --email "jane@example.com" --phone "+12025551234" --notes "Arriving late, after 9pm"
```

**Outcome:** Fully automated rental with lock control, check-in messaging, and guest booking.

---

## 2. Bulk Property Setup (Multiple Rooms)

Set up a large property with multiple rooms, each with its own access point.

```bash
# Create property
uv run <skill-dir>/scripts/client.py --action add-property --name "Beachfront Villa" --address "456 Ocean Dr, Malibu, CA"

# Add multiple access points
uv run <skill-dir>/scripts/client.py --action add-access-point --name "Master Suite" --property-id "prop_<id>" --room-type "bedroom"
uv run <skill-dir>/scripts/client.py --action add-access-point --name "Guest Room 1" --property-id "prop_<id>" --room-type "bedroom"
uv run <skill-dir>/scripts/client.py --action add-access-point --name "Guest Room 2" --property-id "prop_<id>" --room-type "bedroom"
uv run <skill-dir>/scripts/client.py --action add-access-point --name "Living Room" --property-id "prop_<id>" --room-type "common_area"
uv run <skill-dir>/scripts/client.py --action add-access-point --name "Pool House" --property-id "prop_<id>" --room-type "exterior"

# Link locks to each access point (repeat for each room)
uv run <skill-dir>/scripts/client.py --action add-lock --name "Master Door" --access-point-id "ap_<id>" --device-id "SCH-ENCODE-67890"
uv run <skill-dir>/scripts/client.py --action add-lock --name "Guest 1 Door" --access-point-id "ap_<id>" --device-id "SCH-ENCODE-67891"
```

---

## 3. Guest Check-In With Access Code

Send check-in instructions with a Schlage access code to an arriving guest.

```bash
# Create reservation
uv run <skill-dir>/scripts/client.py --action add-reservation --name "Bob Wilson" --email "bob@example.com" --phone "+14155551234"

# Add Schlage access code (requires schlage-login first)
# Use the MCP or schlage proxy to create an access code on the lock
# POST /api/schlage/locks/{device_id}/access_codes
# Body: {"name": "Bob's Code", "code": "4582", "start_date": "2025-07-20", "end_date": "2025-07-22"}

# Send check-in message
# POST /api/checkin with {"channel": "sms", "phone": "+14155551234"}
```

---

## 4. Smart Lock Maintenance and Monitoring

Monitor battery levels and respond to lock jams or low battery.

```
Procedure:
1. List all locks via GET /api/locks to check battery levels
2. Identify locks below 30% battery from the batteryLevel field
3. If a lock is jammed (isJammed: true), notify maintenance
4. Replace batteries for low-battery locks and verify after replacement
5. If a lock doesn't respond (401), re-authenticate with schlage-login
```

**Relevant reference:** `references/properties.md` (lock fields), `references/schlage.md` (error handling)

---

## 5. Emergency Lockout Resolution

Guest is locked out and needs immediate door unlock.

```bash
# 1. Verify guest reservation exists
# GET /api/reservations?phone=+17155551234

# 2. If authenticated with Schlage, unlock the door
# POST /api/schlage/locks/{device_id}/unlock

# 3. Send a message to the guest confirming the door is unlocked
# POST /api/messages/send with {"channel": "sms", "phone": "+17155551234", "body": "The door has been unlocked. Please enter and lock it behind you."}
```

---

## 6. Guest Communication Thread

Full guest communication lifecycle: pre-arrival, check-in, mid-stay, check-out.

```
Flow:
1. Pre-arrival (automation): Send welcome message 1 day before check-in
   - Trigger: time trigger with relativeTo: "checkin", value: 1, unit: "days"

2. Check-in (automation): Send door code and Wi-Fi instructions on arrival day
   - Trigger: reservation.added event
   - Template: Check-in Instructions (SMS or email)

3. Mid-stay (manual): Respond to guest inquiries via send-message
   - POST /api/messages/send with reservation ID and message body

4. Check-out (automation): Send departure reminder and thank you
   - Trigger: time trigger with relativeTo: "checkout", value: 1, unit: "hours"
```

**Relevant references:** `references/automations.md` (trigger configs), `references/messaging.md` (send message)

---

## 7. Multi-Property Account Management

Manage a portfolio of properties across different locations, each with its own configuration.

```bash
# Create multiple properties
uv run <skill-dir>/scripts/client.py --action add-property --name "Downtown Condo" --address "789 Main St, Austin, TX"
uv run <skill-dir>/scripts/client.py --action add-property --name "Mountain Cabin" --address "321 Pine Rd, Aspen, CO"
uv run <skill-dir>/scripts/client.py --action add-property --name "Beach House" --address "555 Shore Dr, Miami, FL"

# Each property gets its own access points, locks, and automations
# Use the property IDs from each creation response for subsequent steps

# Get an overview of all properties:
# GET /api/properties — returns all properties with nested access points and locks

# Export all data for backup or analysis:
# GET /api/account/export
```

---

## 8. Automation Sequence With Conditions

Create an automation that only triggers for specific rooms.

```bash
uv run <skill-dir>/scripts/client.py --action add-automation --name "Premium Suite Welcome" --triggers '[{"id":"trg_1","kind":"trigger","type":"event","event":"reservation.added","label":"On Reservation"}]'
```

After creating the bare automation, update it via `PUT /api/automations/{id}` with conditions:

```json
{
  "name": "Premium Suite Welcome",
  "description": "Only for Master Suite bookings",
  "icon": "HandWavingIcon",
  "triggers": [
    {
      "id": "trg_1",
      "kind": "trigger",
      "type": "event",
      "event": "reservation.added",
      "label": "On Reservation"
    }
  ],
  "conditions": [
    {
      "id": "cond_1",
      "kind": "condition",
      "type": "rooms",
      "propertyId": "prop_abc123",
      "propertyName": "Beachfront Villa",
      "accessPointIds": ["ap_abc123"],
      "accessPointNames": ["Master Suite"],
      "label": "Master Suite Only"
    }
  ],
  "actions": [
    {
      "id": "act_1",
      "kind": "action",
      "type": "send_message",
      "label": "Send Welcome",
      "templateId": "tpl_abc123"
    }
  ],
  "status": "active"
}
```

**Relevant reference:** `references/automations.md` (condition types and action types)
