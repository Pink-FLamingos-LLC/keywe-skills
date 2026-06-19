---
name: keywe
description: Set up and automate vacation rental properties, smart locks, guest messaging, and reservations. Use when asked to "add a property", "create a reservation", "connect a lock", "automate guest messages", "set up check-in", "provision a rental", "add an access point", "link a Schlage lock", "create a message template", "configure automation triggers", "manage reservations", "set up Schlage", "send message to guest", "unlock door", "create access code", "monitor lock battery", or "smart lock setup".
---

# KeyWe Property and Lock Automation

Delegate all API operations to the CLI client. Do not construct custom curl strings.

## Setup Guide (New Users)

Follow these steps in order. Stop and check each step before moving to the next.

### Step 1: Create an Account

1. Open a web browser and go to the KeyWe app URL (your host will tell you the address).
2. Click **Sign Up** or **Register**.
3. Enter your name, email address, and a password.
4. Check your email inbox for a verification message. Click the link in it to verify your email.
5. Log in with your email and password.

### Step 2: Generate an API Key (The Secret Token)

An API key is a long secret code that lets the automation tool prove it is you. Think of it like a password for the tool to use.

1. After logging in, click **Settings** in the menu.
2. Scroll down to the **API Keys** section.
3. Click **Generate New API Key**.
4. Type a label like "AI Agent" (this is just so you can remember what it is for).
5. **Important**: A long secret code will appear one time only, starting with `keywe_`. Highlight and copy it right now — the page will never show the full code again! If you lose it, you will have to generate a new one.

### Step 3: Open Your Terminal

The terminal is the text-based window where you type commands. How to open it depends on your computer:

- **Mac**: Press `Cmd + Space`, type `Terminal`, press Enter.
- **Windows**: Press `Windows key`, type `cmd` or `PowerShell`, press Enter.
- **Linux**: Press `Ctrl + Alt + T`.

A dark or white window with a blinking cursor will appear. This is where you type the commands below.

### Step 4: Set Your API Key in the Terminal

You need to tell the tool your API key so it can make requests. You do this by pasting a command into the terminal.

1. Type (or copy) the following command into the terminal, but do NOT press Enter yet:
   ```bash
   export KEYWE_API_KEY=""
   ```
2. Move your cursor between the two quote marks `""` and paste your API key (the `keywe_...` code you copied in Step 2). The result should look like:
   ```bash
   export KEYWE_API_KEY="keywe_abc123def456ghi789"
   ```
3. Press Enter to run it. You will not see any confirmation message — that is normal. It just worked silently.
4. Now type or paste this and press Enter:
   ```bash
   export KEYWE_BASE_URL="https://keywe.cloud"
   ```

**What just happened?** You stored two pieces of information in your terminal session so the tool can find them. They will last as long as this terminal window stays open. If you close the terminal and come back later, you must run these two commands again.

### Step 5: (Optional) Set Up Schlage Smart Locks

If you have Schlage smart locks you want to control, you need to connect your Schlage account too.

1. If you have a Schlage account, find your Schlage email and password.
2. In the same terminal, type or paste these two commands (one at a time, pressing Enter after each):
   ```bash
   export SCHLAGE_EMAIL="you@example.com"
   export SCHLAGE_PASSWORD="your_schlage_password"
   ```
   Replace `you@example.com` with your actual Schlage email and `your_schlage_password` with your actual Schlage password.
3. Then run this command to log in and store the credentials with the platform:
   ```bash
   uv run <skill-dir>/scripts/client.py --action schlage-login
   ```
4. If it works, you will see a response like `{"access_token": "..."}`. You are now connected.
5. To disconnect later, run:
   ```bash
   uv run <skill-dir>/scripts/client.py --action schlage-logout
   ```

**Troubleshooting**: If you get an error, double-check that you typed the email and password correctly. Run `schlage-login` again after fixing them.

### How to Run Commands (Quick Reference)

Every command in this guide follows this pattern — type or paste it exactly, then press Enter:

```bash
uv run <skill-dir>/scripts/client.py --action add-property --name "Example Name"
```

- Do not type the `$` sign if you see one in examples — that is just showing the prompt.
- If you get an error like `command not found: uv`, you need to install Python's `uv` tool first. Ask your host for help with this.
- If you get a `401` or `Unauthorized` error, go back to Step 4 and make sure `KEYWE_API_KEY` is set correctly.

## Multi-Step Provisioning Workflows

Follow this structural hierarchy. Do not skip dependency layers.

### 1. Provisioning Infrastructure

**Step A — Add Property**: Root container. Create it first.
**Step B — Add Access Point**: Belongs to a property. Use the `propertyId` from Step A.
**Step C — Connect Lock**: Link physical smart hardware (e.g., `schlage_encode`) to the access point from Step B.

### 2. Guest Operations

**Create Message Templates**: Reusable templates with `{{guestName}}`, `{{propertyName}}`, `{{accessCode}}` substitutions.
**Book Reservations**: Log guest stays with phone/email.
**Create Automations**: Event-driven triggers (e.g., `reservation.added`, `lock.jammed`) linked to templates.

## CLI Execution Matrix

Script paths use `<skill-dir>` — replace with the actual skill directory path.

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

### Authenticate Schlage Credentials (Optional)

```bash
uv run <skill-dir>/scripts/client.py --action schlage-login
```

Reads `SCHLAGE_EMAIL` and `SCHLAGE_PASSWORD` env vars, authenticates with the Schlage API, and stores credentials with the platform for automatic token refresh.

**Response:** `{"access_token": "...", "expires_in": 86400}`

### Clear Schlage Credentials

```bash
uv run <skill-dir>/scripts/client.py --action schlage-logout
```

**Response:** `{"detail": "ok"}`

## Embed Widget (Guest-Facing Verification)

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

- NEVER ask the user to type their API key or Schlage credentials into a chat prompt.
- If an action returns 401, verify `KEYWE_API_KEY` is set in the environment.
- If Schlage operations fail with 401, run `schlage-login` first, or verify `SCHLAGE_EMAIL` and `SCHLAGE_PASSWORD` are correct.
