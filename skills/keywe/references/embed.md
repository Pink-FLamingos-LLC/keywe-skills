# Embed Widget API Reference

## Contents

- Overview
- How It Works
- Quick Start
- CSS Custom Properties (Preferred)
- HTML Attributes (Alternative)
- The `success` Event
- Customization Options Table
- Preview Page
- AI-Themed Version
- textOptIn Behavior
- Embed API Endpoint

## Overview

The KeyWe embed widget lets you add a guest phone verification and SMS opt-in component to any webpage. Guests enter their phone number, consent to SMS, and the widget notifies your page when verification succeeds.

The widget renders as a `<keywe-verify-reservation>` custom element that creates a shadow DOM iframe, isolating it from host page styles.

## How It Works

```
Host Page -> <keywe-verify-reservation> -> Shadow DOM iframe -> /embed/verify/{id}
                                                                     |
                                                              PATCH /api/embed/reservations/{id}
                                                                     |
                                                              postMessage('keywe-verify-success')
                                                                     |
                                                              CustomEvent('success') on element
```

## Quick Start

### Step 1: Generate a Reservation ID

Before adding the embed widget, create a reservation to obtain a reservation ID. The reservation must exist in the system — the embed widget verifies and updates a real reservation record.

```bash
## Using the API
curl -X POST https://keywe.cloud/api/reservations \
  -H "Authorization: Bearer your_api_key" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "guestPhone": "+17155551234"}'
```

**Response:** `{"id": "res_<uuid>", "guestPhone": "+17155551234"}`

Store the returned `id` — this is the `reservation-id` you pass to the embed component.

### Step 2: Add the Script and Component

**Important:** Always set the `property-name` attribute — it appears in the SMS consent text the guest agrees to. Without it, the guest won't know which company or property they're consenting to receive messages from.

```html
<script src="https://keywe.cloud/embed.js"></script>

<!-- Prefer CSS variables for styling -->
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
```

### Step 3: Listen for the Success Event

```html
<script>
  document.querySelector("keywe-verify-reservation").addEventListener("success", (event) => {
    console.log("Verified:", event.detail);
    // event.detail = { reservationId, guestPhone, checked }
    // Unlock checkout step, redirect, etc.
  });
</script>
```

## CSS Custom Properties (Preferred)

Use CSS custom properties on the `<keywe-verify-reservation>` element to customize appearance. This is the recommended approach — it keeps styling separate from structure.

```html
<style>
  keywe-verify-reservation {
    --keywe-primary-color: #4f46e5;
    --keywe-border-radius: 12px;
    --keywe-font-family: "Inter", sans-serif;
    --keywe-bg-color: #ffffff;
    --keywe-text-primary: #111827;
    --keywe-text-secondary: #6b7280;
    --keywe-text-hint: #9ca3af;
    --keywe-border-color: #d1d5db;
    --keywe-input-bg: #f9fafb;
    --keywe-success-color: #10b981;
  }
</style>
```

| CSS Variable             | Default    | Description          |
| ------------------------ | ---------- | -------------------- |
| `--keywe-primary-color`  | `#4f46e5`  | Primary accent color |
| `--keywe-border-radius`  | `12px`     | Corner roundness     |
| `--keywe-font-family`    | `Inter`    | Font family          |
| `--keywe-bg-color`       | white      | Background color     |
| `--keywe-text-primary`   | dark gray  | Primary text color   |
| `--keywe-text-secondary` | gray       | Secondary text color |
| `--keywe-text-hint`      | light      | Hint/label text      |
| `--keywe-border-color`   | gray       | Input border color   |
| `--keywe-input-bg`       | near-white | Input background     |
| `--keywe-success-color`  | green      | Success indicator    |

## HTML Attributes (Alternative)

You can also pass customization as HTML attributes on the element. Hyphenated attribute names map to camelCase query params.

```html
<keywe-verify-reservation
  reservation-id="res_your_reservation_id"
  theme="dark"
  primary-color="#6366f1"
  border-radius="8px"
  font-family="Inter"
  heading-text="Verify Your Booking"
></keywe-verify-reservation>
```

## The `success` Event

When a guest completes verification, the embed dispatches a `CustomEvent('success')` on the `<keywe-verify-reservation>` element that bubbles through the shadow DOM boundary.

**Event `detail`:**

| Field           | Type   | Description                                  |
| --------------- | ------ | -------------------------------------------- |
| `reservationId` | string | The reservation UUID used                    |
| `guestPhone`    | string | The phone number the guest entered           |
| `checked`       | string | `"checked"` or `"unchecked"` (not a boolean) |

```json
{
  "reservationId": "res_abc123",
  "guestPhone": "+1 (555) 000-0000",
  "checked": "checked"
}
```

**Use this event to gate your checkout flow.** Do not allow booking to proceed until the event fires with `checked === "checked"`. The guest must enter a valid phone and check the consent box before the event dispatches. Keep your "Complete Booking" button disabled until the event fires, then enable it.

## Customization Options

| Attribute        | CSS Variable             | Default               | Description                                                       |
| ---------------- | ------------------------ | --------------------- | ----------------------------------------------------------------- |
| `reservation-id` | —                        | **(required)**        | Reservation UUID                                                  |
| `theme`          | —                        | `light`               | `light` or `dark`                                                 |
| `primary-color`  | `--keywe-primary-color`  | `#4f46e5`             | Primary accent color                                              |
| `border-radius`  | `--keywe-border-radius`  | `12px`                | Corner roundness                                                  |
| `font-family`    | `--keywe-font-family`    | `Inter`               | Font family                                                       |
| `bg-color`       | `--keywe-bg-color`       | `#ffffff`             | Background color                                                  |
| `text-primary`   | `--keywe-text-primary`   | `#111827`             | Primary text color                                                |
| `text-secondary` | `--keywe-text-secondary` | `#6b7280`             | Secondary text color                                              |
| `text-hint`      | `--keywe-text-hint`      | `#9ca3af`             | Hint text color                                                   |
| `border-color`   | `--keywe-border-color`   | `#d1d5db`             | Input border color                                                |
| `input-bg`       | `--keywe-input-bg`       | `#f9fafb`             | Input background                                                  |
| `success-color`  | `--keywe-success-color`  | `#10b981`             | Success indicator                                                 |
| `heading-text`   | —                        | `Verify Your Booking` | Main heading text                                                 |
| `verifying-text` | —                        | `Verifying...`        | Loading state text                                                |
| `default-phone`  | —                        | —                     | Pre-filled phone number                                           |
| `logo-url`       | —                        | —                     | Custom logo image URL                                             |
| `logo-height`    | —                        | `32px`                | Logo image height                                                 |
| `property-name`  | —                        | —                     | **Required** — Company or property name shown in SMS consent text |
| `terms-url`      | —                        | —                     | Terms of service link                                             |
| `privacy-url`    | —                        | —                     | Privacy policy link                                               |

## Preview Page

You can preview the embed widget at `/embed/preview` on your KeyWe instance. This interactive playground lets you:

- Toggle between light and dark themes
- Choose from preset primary colors or pick your own
- Adjust border radius, font family, and heading text
- See live preview of the web component
- **Copy the embed code** (both CSS variables and HTML attributes versions)
- View event logs as they fire

**Note:** The preview uses mock data — no real API calls are made.

## AI-Themed Version

You can tell the AI to analyze your website's design and generate a themed version of the embed component tailored to your brand. The AI will:

1. Scan your page's color scheme, fonts, and visual style
2. Generate the appropriate CSS custom properties
3. Provide the complete embed code ready to paste into your page

The AI can fine-tune every CSS variable to match your existing design system.

## textOptIn Behavior

The embed widget sets the `textOptIn` and `textOptInAt` fields on the reservation:

- `textOptIn` (boolean) — Whether the guest consented to SMS messaging
- `textOptInAt` (timestamp) — When the guest provided consent

These fields are updated via `PATCH /api/embed/reservations/{id}` when the guest checks the consent checkbox. Only `guestPhone`, `textOptIn`, and `textOptInAt` can be modified through the embed endpoint.

## Embed API Endpoint

### `GET /api/embed/reservations/{id}`

Public endpoint (no auth). Fetches reservation details for the embed widget.

**Response 200:**

```json
{
  "id": "res_abc123",
  "propertyName": "Lakefront Cabin",
  "guestPhoneMasked": "***5551234",
  "textOptIn": false,
  "checkInStatus": "pending"
}
```

### `PATCH /api/embed/reservations/{id}`

Public endpoint (no auth). Updates guest phone and SMS opt-in. Origin-validated (only `localhost` and `*.keywe.cloud`).

```json
{
  "guestPhone": "+17155551234",
  "textOptIn": true
}
```

The `checked` alias is also accepted for `textOptIn` (values: `"checked"`, `"unchecked"`, or boolean).
