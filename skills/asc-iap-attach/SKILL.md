---
name: asc-iap-attach
description: Attach in-app purchases and subscriptions to an app version for App Store review via browser automation. Use when the user has IAPs or subscriptions in "Ready to Submit" state that need to be included with a first-time version submission. This is required because Apple's public API does not support first-time IAP/subscription attachment to versions.
---

# asc iap attach

Use this skill to attach in-app purchases and/or subscriptions to an app version for App Store review. This is the equivalent of clicking "Select In-App Purchases or Subscriptions" on the version page in App Store Connect and checking the items to include.

**Why browser automation?** Apple's `inAppPurchaseSubmissions` and `subscriptionSubmissions` APIs return `FIRST_SUBSCRIPTION_MUST_BE_SUBMITTED_ON_VERSION` for first-time IAP/subscription submissions. The `reviewSubmissionItems` API does not support `subscription` or `inAppPurchase` relationship types. The only way to attach first-time IAPs/subscriptions to a version is through the ASC web UI. For subsequent submissions (updates to already-approved IAPs/subscriptions), use the CLI approach documented at the end of this skill.

## When to use

- User is preparing an app version for submission and has IAPs or subscriptions to include for the first time
- User says "attach IAPs", "add subscriptions to version", "include in-app purchases for review", "select in-app purchases"
- The app version page in ASC shows an "In-App Purchases and Subscriptions" section with items to select
- IAPs/subscriptions have been created and are in "Ready to Submit" state
- The `asc subscriptions review submit` or `asc iap submit` commands fail with `FIRST_SUBSCRIPTION_MUST_BE_SUBMITTED_ON_VERSION`

## Preconditions

- A browser automation tool is available (Playwright, Cursor browser MCP, or equivalent).
- User is signed in to App Store Connect (or can complete login + 2FA).
- Auth configured for CLI preflight (`asc auth login` or `ASC_*` env vars).
- Know your app ID (`ASC_APP_ID` or `--app`).
- IAPs and/or subscriptions already exist and are in **Ready to Submit** state.
- A build is uploaded and attached to the current app version.
- Required IAP/subscription metadata is complete:
  - Reference name, product ID, pricing, and at least one localization (display name).
  - Review screenshot uploaded (required for first submission of each IAP/subscription).

## Safety Guardrails

- Never export or store cookies.
- Use a visible browser session only.
- Pause for confirmation before checking items if the user has not specified which ones to select.
- Do not retry the Done action automatically on failure.

## Workflow

### 1. Preflight: identify items to attach via CLI

```bash
# List all in-app purchases for the app
asc iap list --app "APP_ID" --output table

# List subscription groups
asc subscriptions groups list --app "APP_ID" --output table

# List subscriptions within each group
asc subscriptions list --group-id "GROUP_ID" --output table
```

Look for items with state `READY_TO_SUBMIT`. Note their reference names and product IDs — you will match these against the checkbox labels in the web UI modal.

### 2. Verify readiness before browser automation

```bash
# Check IAP has at least one localization
asc iap localizations list --iap-id "IAP_ID" --output table

# Check subscription has at least one localization
asc subscriptions localizations list --subscription-id "SUB_ID" --output table
```

If a review screenshot is missing, upload one before proceeding:

```bash
# Upload review screenshot for IAP
asc iap images create --iap-id "IAP_ID" --file "./review-screenshot.png"

# Upload review screenshot for subscription
asc subscriptions review screenshots create --subscription-id "SUB_ID" --file "./review-screenshot.png"
```

### 3. Navigate to the version page

Open the inflight version page in the browser:

```
https://appstoreconnect.apple.com/apps/{APP_ID}/distribution/ios/version/inflight
```

Ensure the user is signed in. If a login page appears, pause and let the user complete login + 2FA.

### 4. Open the IAP/subscription selection modal

Scroll down to the **"In-App Purchases and Subscriptions"** section on the version page.

Click the button labeled **"Select In-App Purchases or Subscriptions"**. If items have already been attached previously, this may instead be a **"+"** button or **"Manage"** link in the section header.

A modal dialog titled **"Add In-App Purchases or Subscriptions"** will appear.

### 5. Select the desired items

The modal displays a table with columns: checkbox, **Reference Name**, **Product ID**, **Type**.

- Only items in "Ready to Submit" state appear in this list.
- Each item has a **checkbox** on the left side.
- A notice at the top says: "Your changes will be saved as soon as you select or deselect an in-app purchase or subscription."

For each IAP/subscription to attach:
1. Find the row matching the reference name or product ID from the preflight step.
2. Click the **checkbox** to select it. The checkbox is a standard HTML `<input type="checkbox">` — no special click handling is needed.
3. The change saves immediately upon checking — no separate save button.

If the user said "all", check every unchecked item in the list.

### 6. Close the modal

Click the **"Done"** button at the bottom-right of the modal to close it.

### 7. Verify on the version page

After the modal closes, the selected items should now appear listed in the "In-App Purchases and Subscriptions" section on the version page. Verify that all intended items are shown.

### 8. Verify via CLI

```bash
# Re-list IAPs and check their state
asc iap list --app "APP_ID" --output table

# Re-list subscriptions and check their state
asc subscriptions list --group-id "GROUP_ID" --output table
```

After attachment, items should transition from `READY_TO_SUBMIT` to `WAITING_FOR_REVIEW` (once the app version is also submitted for review).

## Known UI Automation Issues

### Modal may not appear immediately
The "Select In-App Purchases or Subscriptions" button triggers an asynchronous load. Wait for the modal to fully render before interacting with checkboxes. Look for the modal title "Add In-App Purchases or Subscriptions" to confirm it is ready.

### Empty modal
If the modal appears but has no items, it means no IAPs/subscriptions are in "Ready to Submit" state. Go back and ensure all required metadata (localizations, pricing, review screenshots) is complete.

### Checkbox clicks not registering
If a checkbox click does not register, try clicking the checkbox element directly rather than the row. Apple's ASC UI uses standard checkboxes without the overlay issues seen in other forms (unlike the "New App" form's radio buttons).

### Page requires scrolling
The "In-App Purchases and Subscriptions" section is typically below the fold. Scroll down past "App Review Information" to find it. Use `scrollIntoView` on the section heading if needed.

## CLI Approach (for subsequent submissions only)

For IAPs/subscriptions that have **already been approved** in a prior version and are being updated, the CLI commands work:

```bash
# Submit updated IAP for review
asc iap submit --iap-id "IAP_ID" --confirm

# Submit updated subscription for review
asc subscriptions review submit --subscription-id "SUB_ID" --confirm

# Submit entire subscription group for review
asc subscriptions review submit-group --group-id "GROUP_ID" --confirm
```

These commands will fail with `FIRST_SUBSCRIPTION_MUST_BE_SUBMITTED_ON_VERSION` for first-time submissions. In that case, fall back to the browser automation workflow above.

## Agent Behavior

- Always run the CLI preflight to identify which items are in `READY_TO_SUBMIT` state before opening the browser.
- First attempt CLI submission (`asc iap submit` / `asc subscriptions review submit`). If it fails with `FIRST_SUBSCRIPTION_MUST_BE_SUBMITTED_ON_VERSION`, proceed with browser automation.
- If the user specifies particular items, match by reference name or product ID.
- If the user says "all", select every unchecked item in the modal.
- After browser automation, always verify via CLI that items are now attached.
- If any step fails, capture a screenshot and report the last known step.
- Do not retry clicking Done automatically on failure.

## Failure Handling

- If the modal cannot be located, stop and request user help.
- If items are missing from the modal, check that metadata is complete (localizations, pricing, review screenshot).
- Capture a screenshot and report the last known step on any failure.
- On failure, the user should check the browser for validation errors or missing metadata warnings.

## Notes

- This skill handles the "attach to version" step only. Use `asc-submission-health` for the full submission flow.
- IAPs/subscriptions must be created first. Use CLI (`asc iap create`, `asc iap setup`, `asc subscriptions create`, `asc subscriptions setup`) to create them.
- This skill exists because Apple's public API does not support first-time IAP/subscription attachment to versions — similar to how `asc-app-create-ui` exists because there is no public API for app creation.
- Review screenshots are required for the first submission of each IAP/subscription, not for updates.
- The `reviewSubmissionItems` API supports `appStoreVersions` and other types but does NOT support `subscriptions` or `inAppPurchases` as item types.
