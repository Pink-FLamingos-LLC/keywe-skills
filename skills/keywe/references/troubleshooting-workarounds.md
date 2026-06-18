# Troubleshooting and Workarounds

## Contents

1. API Key Not Set or Invalid
2. Schlage Authentication Failures (401)
3. Schlage Auto-Refresh Credential Loss
4. Phone Number Not Accepted
5. Lock Not Appearing in Schlage List
6. Email Bounced or Blocked
7. Property or Room Not Found
8. Automation Not Triggering
9. Access Code Creation Fails
10. Lock Shows as Jammed

## 1. API Key Not Set or Invalid

**Symptom:** All API calls return 401.

**Cause:** `KEYWE_API_KEY` environment variable is missing, expired, or the user copied the wrong value.

**Fix:** Verify the env var is set in the current terminal session:

```bash
echo $KEYWE_API_KEY
```

If empty, ask the user to generate a new API key from the dashboard (`/settings`) and export it:

```bash
export KEYWE_API_KEY="keywe_<rest_of_key>"
```

---

## 2. Schlage Authentication Failures (401)

**Symptom:** Schlage operations return 401 with message matching "invalid or expired auth".

**Cause:** The stored access token has expired and auto-refresh failed, or credentials have never been set up.

**Fix:**

1. Run `schlage-login` to re-authenticate:
   ```bash
   uv run <skill-dir>/scripts/client.py --action schlage-login
   ```
2. If that fails, verify `SCHLAGE_EMAIL` and `SCHLAGE_PASSWORD` env vars are set correctly.
3. If credentials are wrong, ask the user to update them in the dashboard settings or re-export correct values.

---

## 3. Schlage Auto-Refresh Credential Loss

**Symptom:** Schlage operations fail with 401 after successful prior use. The stored credentials were cleared.

**Cause:** The auto-refresh mechanism calls `/auth/token` with stored email+password. If the Schlage API is unreachable or credentials are rejected, the stored credentials are deleted from `auth_keys` table as a safety measure.

**Fix:** Run `schlage-login` again. This re-stores the credentials and obtains a fresh access token.

---

## 4. Phone Number Not Accepted

**Symptom:** Reservation creation succeeds but the phone number looks wrong or messaging fails.

**Cause:** Phone numbers are normalized via `libphonenumber-js`. Invalid numbers are stored as-is without error, but US numbers that don't normalize to E.164 may cause SMS delivery failures.

**Fix:** Provide a complete US number including area code. The system accepts E.164 (`+17155551234`), US national (`(715) 555-1234`), or 10-digit (`7155551234`). For non-US numbers, ensure they include the country code with `+`.

---

## 5. Lock Not Appearing in Schlage List

**Symptom:** `schlage-list-locks` returns fewer locks than expected, or a specific lock isn't found.

**Cause:** The lock may not be registered with the Schlage account being used, or it was recently added and hasn't synced.

**Fix:** Verify the lock appears on the Schlage Encode app or web dashboard. If it does, try:

1. Run `schlage-login` to refresh the session
2. Re-list locks via `GET /api/schlage/locks`
3. If still missing, ask the user to confirm the lock is enrolled with their Schlage account

---

## 6. Email Bounced or Blocked

**Symptom:** Email sending fails with "Email address is blocked" or similar error.

**Cause:** The recipient email address previously bounced (hard bounce) or was marked as spam (complaint). It's in the `email_blocklist` table.

**Fix:**

1. Check if the email is blocked via the database or dashboard
2. Bounces are automatically cleared from the `transient_bounce_log` after retries
3. Permanent bounces and complaints are not automatically removed
4. Ask the user to remove the block from the dashboard if they've confirmed the email is valid
5. As a workaround, use SMS instead of email for that guest

---

## 7. Property or Room Not Found

**Symptom:** Operations on a property, access point, or lock return 404.

**Cause:** The ID is incorrect, the resource belongs to a different user, or it was deleted.

**Fix:**

1. List all properties via `GET /api/properties` to verify the ID
2. Verify the resource is not deleted (deleted properties cascade-delete their access points)
3. Confirm the API key belongs to the correct user account

---

## 8. Automation Not Triggering

**Symptom:** An automation is set up but never runs. Events happen but no messages are sent.

**Cause:**

- Automation is in `"paused"` status
- Conditions don't match the triggered event
- The referenced template was deleted
- The automation references an invalid template ID

**Fix:**

1. Check automation status via `GET /api/automations/{id}` — ensure `status` is `"active"`
2. Verify conditions use AND logic — all conditions must match
3. Confirm the `templateId` in the action still exists via `GET /api/templates/{id}`
4. Check `automation_log` entries for error details

---

## 9. Access Code Creation Fails

**Symptom:** Creating an access code on a Schlage lock returns an error.

**Cause:** The code format, lock compatibility, or date range is invalid.

**Fix:**

1. Ensure the code is a 4-digit number (Schlage Encode standard)
2. Verify `start_date` is before `end_date`
3. Ensure dates are in ISO 8601 format (e.g., `"2025-07-15"`)
4. Check that the lock is online (not jammed) via `GET /api/schlage/locks/{device_id}`
5. If the lock is offline, the code can't be programmed until it reconnects

---

## 10. Lock Show as Jammed

**Symptom:** Lock's `isJammed` field is `true`, and lock/unlock commands fail.

**Cause:** The lock mechanism is physically obstructed or the battery is critically low.

**Fix:**

1. Check `batteryLevel` — replace batteries if below 15%
2. Verify the door alignment — a misaligned door can cause the bolt to bind
3. Clear the jammed state by manually operating the lock via the Schlage app
4. If the problem persists, schedule maintenance to inspect the lock mechanism
5. In the meantime, unlink the lock from its access point and provide the guest with a physical key or backup entry method
