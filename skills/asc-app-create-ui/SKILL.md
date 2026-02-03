---
name: asc-app-create-ui
description: Create a new App Store Connect app record via browser automation (direct Playwright). Use when there is no public API for app creation.
---

# ASC App Create (UI Automation)

Use this skill to create a new App Store Connect app by driving the web UI.
This is opt-in, local-only automation that requires the user to log in.

## Preconditions
- Playwright is available (Node or Python) and can open a real browser.
- User can complete login and 2FA in App Store Connect.
- Required inputs are known:
  - app name
  - bundle ID
  - SKU
  - platform (iOS, macOS, tvOS, visionOS)
  - primary language

## Safety Guardrails
- Never export or store cookies.
- Use a visible browser session only.
- Pause for a final confirmation before clicking "Create".

## Implementation Preference
- Prefer direct Playwright scripts over MCP for cache control and lower context use.
- Use a fresh browser context per run; close contexts explicitly.
- Keep selectors resilient (role/label/text over CSS).

## Script Template
This skill includes a ready-to-run script:

```bash
python scripts/create_app_playwright.py \
  --app-name "My App" \
  --bundle-id "com.example.app" \
  --sku "com.example.app" \
  --platform IOS \
  --language "English (U.S.)"
```

## Workflow
1. Preflight: check app does not already exist.
   - `asc apps list --bundle-id "com.example.app"`
2. Open App Store Connect and wait for login:
   - `https://appstoreconnect.apple.com/apps`
3. Navigate to "New App" and open the creation form.
4. Fill required fields:
   - Platform
   - Name
   - Primary language
   - Bundle ID
   - SKU
5. Pause and request confirmation from the user.
6. Click "Create" and wait for success.
7. Verify creation via API:
   - `asc apps list --bundle-id "com.example.app" --output json`
8. Return the new app ID and hand off to `asc app-setup` for categories, pricing,
   availability, and localizations.

## Failure Handling
- If any field or button cannot be located, stop and request user help.
- Capture a screenshot and report the last known step.
- Do not retry destructive actions automatically.

## Notes
- This skill is a workaround for a missing public API.
- UI labels change; prefer role or label-based selectors over CSS.
