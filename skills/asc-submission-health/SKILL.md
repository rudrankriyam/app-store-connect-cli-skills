---
name: asc-submission-health
description: Preflight App Store submissions, submit builds, and monitor review status with asc. Use when shipping or troubleshooting review submissions.
---

# asc submission health

Use this skill to reduce review submission failures and monitor status.

## Preconditions
- Auth configured and app/version/build IDs resolved.
- Build is processed (not in processing state).
- All required metadata is complete.

## Pre-submission Checklist

### 1. Verify Build Status
```bash
asc builds info --build "BUILD_ID"
```
Check:
- `processingState` is `VALID`
- `usesNonExemptEncryption` - if `true`, requires encryption declaration

### 2. Encryption Compliance
If `usesNonExemptEncryption: true`:
```bash
# If the app should be exempt, patch the local plist helper, rebuild, and re-upload
asc encryption declarations exempt-declare --plist "./Info.plist"

# List existing declarations
asc encryption declarations list --app "APP_ID"

# Create declaration if needed
asc encryption declarations create \
  --app "APP_ID" \
  --app-description "Uses standard HTTPS/TLS" \
  --contains-proprietary-cryptography=false \
  --contains-third-party-cryptography=true \
  --available-on-french-store=true

# Assign to build
asc encryption declarations assign-builds \
  --id "DECLARATION_ID" \
  --build "BUILD_ID"
```

If the app truly uses only exempt transport encryption, prefer `asc encryption declarations exempt-declare --plist "./Info.plist"` and rebuild instead of creating a declaration that does not match the binary.

### 3. Content Rights Declaration
Required for all App Store submissions:
```bash
# Check current status
asc apps content-rights view --app "APP_ID"

# Set it for most apps
asc apps content-rights edit --app "APP_ID" --uses-third-party-content=false
```
Valid values:
- `DOES_NOT_USE_THIRD_PARTY_CONTENT`
- `USES_THIRD_PARTY_CONTENT`

### 4. Version Metadata
```bash
# Check version details
asc versions view --version-id "VERSION_ID" --include-build

# Verify copyright is set
asc versions update --version-id "VERSION_ID" --copyright "2026 Your Company"
```

### 5. Localizations Complete
```bash
# List version localizations
asc localizations list --version "VERSION_ID"

# Check required fields: description, keywords, whatsNew, supportUrl
```

### 6. Screenshots Present
Each locale needs screenshots for the target platform.

### 7. App Info Localizations (Privacy Policy)
```bash
# List app info IDs (if multiple exist)
asc apps info list --app "APP_ID"

# Check privacy policy URL
asc localizations list --app "APP_ID" --type app-info --app-info "APP_INFO_ID"
```

### 8. App Privacy readiness advisory
`asc` can warn about App Privacy readiness, but the public App Store Connect API
cannot verify whether App Privacy is fully published. Before final submission:

```bash
asc submit preflight --app "APP_ID" --version "1.2.3" --platform IOS
asc validate --app "APP_ID" --version "1.2.3" --platform IOS
```

Prefer the version string form for top-level readiness checks in this skill so it stays aligned with `asc submit preflight`. Lower-level commands later in this guide still use `VERSION_ID` where the API requires it.

If either command reports an App Privacy advisory, the public API cannot verify
publish state. Use the web-session privacy workflow if you rely on those endpoints:

```bash
asc web privacy pull --app "APP_ID" --out "./privacy.json"
asc web privacy plan --app "APP_ID" --file "./privacy.json"
asc web privacy apply --app "APP_ID" --file "./privacy.json"
asc web privacy publish --app "APP_ID" --confirm
```

If you do not want to use the experimental `asc web privacy ...` commands,
confirm App Privacy manually in App Store Connect:

```text
https://appstoreconnect.apple.com/apps/APP_ID/appPrivacy
```

### 9. Digital goods readiness (IAPs / subscriptions)
If the app sells subscriptions or in-app purchases, validate those separately before submit:

```bash
asc validate iap --app "APP_ID" --output table
asc validate subscriptions --app "APP_ID" --output table
```

In `0.45.3+`, `asc validate subscriptions` expands `MISSING_METADATA` into a per-subscription diagnostics matrix. Use it to identify missing review screenshots, promotional images, pricing or availability coverage gaps, offer readiness, and app/build evidence before retrying submit or first-review attach.

Use `--output json --pretty` when you want exact territory gaps in machine-readable form.

## Submit

### Using Review Submissions API (Recommended)
```bash
# Create submission
asc review submissions-create --app "APP_ID" --platform IOS

# Add version to submission
asc review items-add \
  --submission "SUBMISSION_ID" \
  --item-type appStoreVersions \
  --item-id "VERSION_ID"

# Submit for review
asc review submissions-submit --id "SUBMISSION_ID" --confirm
```

### Using Submit Command
```bash
asc submit preflight --app "APP_ID" --version "1.2.3" --platform IOS
asc submit create --app "APP_ID" --version "1.2.3" --build "BUILD_ID" --confirm
```
Use `--platform` when multiple platforms exist.

## Monitor
```bash
# Check submission status
asc submit status --id "SUBMISSION_ID"
asc submit status --version-id "VERSION_ID"

# List all submissions
asc review submissions-list --app "APP_ID" --paginate
```

## Cancel / Retry
```bash
# Cancel submission
asc submit cancel --id "SUBMISSION_ID" --confirm

# Or via review API
asc review submissions-cancel --id "SUBMISSION_ID" --confirm
```
Fix issues, then re-submit.

## Common Submission Errors

### "Version is not in valid state"
Check:
1. Build is attached and VALID
2. Encryption declaration approved (or exempt)
3. Content rights declaration set
4. All localizations complete
5. Screenshots present for all locales
6. App Privacy has been reviewed and published in App Store Connect

### "Export compliance must be approved"
The build has `usesNonExemptEncryption: true`. Either:
- Upload export compliance documentation
- Or rebuild with `ITSAppUsesNonExemptEncryption = NO` in Info.plist

### "Multiple app infos found"
Use `--app-info` flag with the correct app info ID:
```bash
asc apps info list --app "APP_ID"
```

## Notes
- `asc submit create` uses the new reviewSubmissions API automatically.
- `asc submit preflight` can return non-blocking advisories; review them before submitting.
- App Privacy publish state is not verifiable via the public API.
- Prefer `asc apps content-rights view/edit` over ad-hoc app JSON inspection.
- `asc validate subscriptions` now provides much richer per-subscription diagnostics for `MISSING_METADATA` cases.
- If you use ASC web-session flows, `asc web privacy pull|plan|apply|publish` is the CLI path for App Privacy.
- If you avoid the experimental web-session commands, confirm App Privacy manually in App Store Connect.
- Use `--output table` when you want human-readable status.
- macOS submissions follow the same process but use `--platform MAC_OS`.
