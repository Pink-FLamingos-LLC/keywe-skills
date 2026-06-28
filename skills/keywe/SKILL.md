---
name: keywe
description: Set up and automate vacation rental properties, smart locks, guest messaging, and reservations. Use when asked to "add a property", "create a reservation", "connect a lock", "automate guest messages", "set up check-in", "provision a rental", "add an access point", "link a Schlage lock", "create a message template", "configure automation triggers", "manage reservations", "set up Schlage", "send message to guest", "unlock door", "lock door", "control locks", "send lock command", "list locks", "check lock status", "create access code", "monitor lock battery", or "smart lock setup".
---

# KeyWe Property and Lock Automation

Delegate all API operations to the CLI client. Do not construct custom curl strings.

The user never runs terminal commands — you (the agent) run everything. The user only creates files and tells you what they want done.

## Agent Workflow: Guiding the User Through Setup

This skill works in a back-and-forth conversation. Do NOT dump all steps at once. Follow this sequence:

1. **Ask the user** if they already have a KeyWe account and API key.
2. Walk through creation steps **one at a time** — wait for confirmation before proceeding to the next.
3. **When credentials are ready**, ask the user to create a `.env` file and tell you when it's done so you can proceed.

### Step 1: Create an Account

1. Open a web browser and go to https://keywe.cloud.
2. Click **Sign Up** or **Register**.
3. Enter your name, email address, and a password.
4. Check your email inbox for a verification message. Click the link in it to verify your email.
5. Log in with your email and password.

**Stop here.** Ask the user to confirm they have an account and are logged in.

### Step 2: Generate an API Key

1. After logging in, click **Settings** in the menu.
2. Scroll down to the **API Keys** section.
3. Click **Generate New API Key**.
4. Type a label like "AI Agent".
5. **Important**: A long secret code will appear one time only, starting with `keywe_`. Copy it now — the page will never show it again.

**Stop here.** Ask the user to confirm they have copied their API key. Tell them: _"I don't need you to send me the key — just save it in the `.env` file in the next step. I never want to see your secrets for security reasons."_

### Step 3: Create a `.env` File

First check if `.env` already exists in the project root. Do NOT read its contents — just check existence.

**If `.env` does not exist:** Create the file yourself with placeholder values. Write exactly this to `<project-root>/.env`:

```bash
KEYWE_API_KEY="keywe_YOUR_API_KEY_HERE"
SCHLAGE_EMAIL="you@example.com"
SCHLAGE_PASSWORD="your_schlage_password"
```

Then tell the user: _"I created a `.env` file at `<absolute-path>/.env`. Open it and replace the placeholder values with your API key from Step 2 and your Schlage account email/password. I don't want to see the actual values — your secrets stay on your machine for security. Let me know once you've saved it."_

**If `.env` already exists:** Tell the user: _"A `.env` file already exists at `<absolute-path>/.env`. Please open it and make sure `KEYWE_API_KEY`, `SCHLAGE_EMAIL`, and `SCHLAGE_PASSWORD` are set with your real credentials. I don't need to see the values — just let me know when it's ready."_

Replace each value with the actual credentials:

- `KEYWE_API_KEY` — the `keywe_...` code from Step 2.
- `SCHLAGE_EMAIL` — the email used for your Schlage account.
- `SCHLAGE_PASSWORD` — the password for your Schlage account.

**Important:** The `.env` file contains secrets. Never share it, commit it to git, or paste its contents into a chat.

**Stop and wait.** Do NOT proceed until the user confirms the `.env` file is in place.

### Step 4: Link Your Schlage Account

Once the user confirms `.env` is ready, tell them: _"I'm linking your Schlage account now."_

Then run this yourself (the user doesn't need to know about this endpoint — just do it):

```bash
uv run <skill-dir>/scripts/client.py --action schlage-login
```

If it succeeds, tell the user: _"Your Schlage account is linked. Let me list your locks."_

If it fails, ask the user to double-check their Schlage credentials in `.env` and confirm when fixed.

**Note:** The Schlage session is maintained automatically by the platform after this initial link.

### Step 5: List Locks

Once everything is set up, list the user's locks (run this yourself):

```bash
curl -H "Authorization: Bearer <api-key>" https://keywe.cloud/api/schlage/locks
```

Show the user the results and explain their options:

**Locks can be controlled immediately** via the lock/unlock API using their `device_id` — no provisioning needed. If the user just wants to lock/unlock doors, you're done here.

**Optionally**, locks can be provisioned into properties and rooms for automations, guest access codes, and messaging. If the user wants that, ask them for property/room names and run:

```bash
uv run <skill-dir>/scripts/client.py --action add-property --name "Property Name"
uv run <skill-dir>/scripts/client.py --action add-access-point --name "Room Name" --property-id "prop_<id>" --room-type "bedroom"
uv run <skill-dir>/scripts/client.py --action add-lock --name "Door Name" --access-point-id "ap_<id>" --device-id "SCH-ENCODE-XXXXX" --lock-type "schlage_encode"
```

Ask the user what they want to do: _"Your locks are ready to use. I can lock/unlock them anytime. Would you also like to set up properties and rooms for automations and guest access codes?"_

## Using KeyWe as an API to Control Locks

When the user wants to lock or unlock a door, run the commands yourself. Never ask the user to run curl.

### List Locks

```bash
curl -H "Authorization: Bearer <api-key>" https://keywe.cloud/api/schlage/locks
```

### Check a Specific Lock's Status

```bash
curl -H "Authorization: Bearer <api-key>" https://keywe.cloud/api/schlage/locks/SCH-ENCODE-12345
```

### Lock a Door

```bash
curl -X POST -H "Authorization: Bearer <api-key>" -H "Content-Type: application/json" https://keywe.cloud/api/schlage/locks/SCH-ENCODE-12345/lock
```

### Unlock a Door

```bash
curl -X POST -H "Authorization: Bearer <api-key>" -H "Content-Type: application/json" https://keywe.cloud/api/schlage/locks/SCH-ENCODE-12345/unlock
```

### Quick Reference

| Action      | Method | Endpoint                                |
| ----------- | ------ | --------------------------------------- |
| List locks  | GET    | `/api/schlage/locks`                    |
| Lock status | GET    | `/api/schlage/locks/{device_id}`        |
| Lock door   | POST   | `/api/schlage/locks/{device_id}/lock`   |
| Unlock door | POST   | `/api/schlage/locks/{device_id}/unlock` |

### Troubleshooting Lock Commands

- **401 Unauthorized**: The Schlage session may have expired. Ask the user to re-link their Schlage account in the KeyWe web UI (Settings → Schlage).
- **404 Not Found**: The `device_id` may be wrong. List locks to see valid device IDs.
- **No locks shown**: Ask the user to verify they've added locks in the KeyWe web UI (Locks → Sync Locks).
- **Lock doesn't respond**: Check the lock's battery level via status endpoint. If below 10%, batteries may need replacing.
- **Auth/connection errors**: Ask the user to confirm `.env` exists and `KEYWE_API_KEY` is set correctly.

## Multi-Step Provisioning Workflows

Provisioning is optional — locks work standalone for lock/unlock without any of this. Only use this flow if the user wants automations, guest access codes, or messaging tied to specific properties.

If provisioning, follow this structural hierarchy. Do not skip dependency layers.

### 1. Provisioning Infrastructure

**Step A — Add Property**: Root container. Create it first.
**Step B — Add Access Point**: Belongs to a property. Use the `propertyId` from Step A.
**Step C — Connect Lock**: Link physical smart hardware (e.g., `schlage_encode`) to the access point from Step B.

### 2. Guest Operations

**Create Message Templates**: Reusable templates with `{{guestName}}`, `{{propertyName}}`, `{{accessCode}}` substitutions.
**Book Reservations**: Log guest stays with phone/email.
**Create Automations**: Event-driven triggers (e.g., `reservation.added`, `lock.jammed`) linked to templates.

## CLI Execution Matrix (Agent Runs These)

Script paths use `<skill-dir>` — replace with the actual skill directory path. All commands below are for the agent to run, not the user.

### Add a Property

```bash
uv run <skill-dir>/scripts/client.py --action add-property --name "Lakefront Cabin" --address "123 Pine St, Lake Tahoe, CA"
```

**Response:** `{"id": "prop_<id>", "name": "...", "address": "..."}`

### Add an Access Point (Room)

```bash
uv run <skill-dir>/scripts/client.py --action add-access-point --name "Master Suite" --property-id "prop_<id>" --room-type "bedroom"
```

**Response:** `{"id": "ap_<id>", "name": "...", "propertyId": "prop_<id>", "roomType": "..."}`

### Add/Link a Schlage Lock

```bash
uv run <skill-dir>/scripts/client.py --action add-lock --name "Front Door Lock" --access-point-id "ap_<id>" --device-id "SCH-ENCODE-12345" --lock-type "schlage_encode"
```

**Response:** `{"id": "lock_<id>", "name": "...", "accessPointId": "ap_<id>", "deviceId": "...", "lockType": "..."}`

### Add a Message Template

```bash
uv run <skill-dir>/scripts/client.py --action add-template --name "Welcome SMS" --category "check-in" --channel "sms" --content "Hi {{guestName}}, welcome to {{propertyName}}! Your door code is {{accessCode}}."
```

**Response:** `{"id": "tpl_<id>", "name": "...", "category": "...", "channel": "sms", "content": "...", "status": "active"}`

### Add a Guest Reservation

```bash
uv run <skill-dir>/scripts/client.py --action add-reservation --name "John Doe" --email "john@example.com" --phone "+17155551234" --notes "Late arrival"
```

**Response:** `{"id": "res_<id>", "name": "...", "email": "...", "guestPhone": "...", "notes": "..."}`

### Add a Booking Automation

Pass trigger config as a valid JSON string:

```bash
uv run <skill-dir>/scripts/client.py --action add-automation --name "Welcome Sequence" --triggers '[{"id": "trg_1", "kind": "trigger", "type": "event", "event": "reservation.added", "label": "On Reservation Added"}]'
```

**Response:** `{"id": "auto_<id>", "name": "...", "triggers": [...], "conditions": [], "actions": []}`

## Embed Widget (Guest-Facing Verification)

When the user wants to add guest-facing booking verification to their website, explain what the widget does and provide the embed code. The user adds this HTML to their own website — you don't run this.

The Embed Widget is a web component that you put on your own website to let guests verify their booking and opt in to SMS. It renders a phone input + consent checkbox inside a shadow DOM iframe.

**Workflow:**

1. Create a reservation to get a reservation ID
2. Put the embed component on your page with that reservation ID
3. Guest enters phone, checks consent, and the widget dispatches a `success` event
4. The success updates `textOptIn` and `textOptInAt` on the reservation record

### Quick Start

**Important:** Always set `property-name` — it appears in the SMS consent text the guest agrees to. The guest must see which company they're consenting to.

```html
<script src="https://keywe.cloud/embed.js"></script>

<style>
  keywe-verify-reservation {
    --keywe-primary-color: #4f46e5;
    --keywe-border-radius: 12px;
    --keywe-font-family: Inter;
  }
</style>

<keywe-verify-reservation
  reservation-id="res_your_reservation_id"
  property-name="Clear Water Properties"
  theme="light"
></keywe-verify-reservation>

<script>
  const widget = document.querySelector("keywe-verify-reservation");
  let bookingEnabled = false;

  widget.addEventListener("success", (event) => {
    // event.detail = { reservationId, guestPhone, checked }
    // checked is "checked" (string) when guest consented
    if (event.detail.checked === "checked") {
      bookingEnabled = true;
      // Enable "Complete Booking" button
    }
  });
</script>
```

### Embed Code

Always prefer the CSS variables approach for styling (shown above). All customization options are available as either CSS variables or HTML attributes. See `references/embed.md` for the full option table.

### Preview and Theming

Visit `/embed/preview` on your KeyWe instance to interactively configure the widget, see live preview, and copy the generated embed code. You can also ask the AI to analyze your website's design and produce a themed version with CSS variables matched to your brand.

### Reservation IDs

You must create a reservation first before using the embed widget. The `reservation-id` attribute on the component must match an existing reservation in the system. Use the API or MCP `create-reservation` tool to generate one, then pass its `id` to the embed component.

## Reference Files

Detailed API schemas, request/response examples, and field-level documentation for each domain:

| Reference                                   | Covers                                                                      |
| ------------------------------------------- | --------------------------------------------------------------------------- |
| `references/properties.md`                  | Properties, access points, locks CRUD, link/unlink, field tables            |
| `references/schlage.md`                     | Schlage auth flow, proxy endpoints, lock ops, access codes, logs, auto-sync |
| `references/reservations.md`                | Reservations CRUD, check-in, phone normalization, textOptIn                 |
| `references/messaging.md`                   | Templates CRUD, send message, message history/list                          |
| `references/automations.md`                 | Automation CRUD, trigger/condition/action configs, events                   |
| `references/account.md`                     | API keys, account export/delete, Schlage credentials, Better Auth           |
| `references/embed.md`                       | Embed widget setup, CSS variables, attributes, events, preview page         |
| `references/common-use-cases.md`            | Common multi-step provisioning and guest management workflows               |
| `references/troubleshooting-workarounds.md` | Known issues, error conditions, and resolution steps                        |

Load the relevant reference when the agent needs full field schemas, validation rules, or endpoint-level detail beyond what this SKILL.md provides.

## Safety Guardrails

- NEVER ask the user to type their API key into a chat prompt. Always use the `.env` file approach.
- NEVER ask the user to paste the contents of `.env` into the chat.
- NEVER ask the user to run terminal commands. You run all commands yourself.
- Explicitly tell the user you don't want to see their secrets for security reasons whenever credentials come up.
- If an action returns 401, ask the user to re-link their Schlage account in the KeyWe web UI.
- If no locks are shown, ask the user to verify they've added locks in the KeyWe web UI.
