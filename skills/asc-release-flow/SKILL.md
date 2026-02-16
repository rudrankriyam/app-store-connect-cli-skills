---
name: asc-release-flow
description: End-to-end release workflows for TestFlight and App Store using asc publish, builds, versions, and submit commands. Use when asked to upload a build, distribute to TestFlight, or submit to App Store.
---

# Release flow (TestFlight and App Store)

Use this skill when you need to get a new build into TestFlight or submit to the App Store.

## Preconditions
- Ensure credentials are set (`asc auth login` or `ASC_*` env vars).
- Use a new build number for each upload.
- Prefer `ASC_APP_ID` or pass `--app` explicitly.
- Build must have encryption compliance resolved (see asc-submission-health skill).

## iOS Release

### Preferred end-to-end commands
- TestFlight:
  - `asc publish testflight --app <APP_ID> --ipa <PATH> --group <GROUP_ID>[,<GROUP_ID>]`
  - Optional: `--wait`, `--notify`, `--platform`, `--poll-interval`, `--timeout`
- App Store:
  - `asc publish appstore --app <APP_ID> --ipa <PATH> --version <VERSION>`
  - Optional: `--wait`, `--submit --confirm`, `--platform`, `--poll-interval`, `--timeout`

### Manual sequence (when you need more control)
1. Upload the build:
   - `asc builds upload --app <APP_ID> --ipa <PATH>`
2. Find the build ID if needed:
   - `asc builds latest --app <APP_ID> [--version <VERSION>] [--platform <PLATFORM>]`
3. TestFlight distribution:
   - `asc builds add-groups --build <BUILD_ID> --group <GROUP_ID>[,<GROUP_ID>]`
4. App Store attach + submit:
   - `asc versions attach-build --version-id <VERSION_ID> --build <BUILD_ID>`
   - `asc submit create --app <APP_ID> --version <VERSION> --build <BUILD_ID> --confirm`
5. Check or cancel submission:
   - `asc submit status --id <SUBMISSION_ID>` or `--version-id <VERSION_ID>`
   - `asc submit cancel --id <SUBMISSION_ID> --confirm`

## macOS Release

macOS apps are distributed as `.pkg` files, not `.ipa`.

### Build and Export
See `asc-xcode-build` skill for full build/archive/export workflow.

### Upload PKG
Upload the exported `.pkg` using `asc`:
```bash
asc builds upload \
  --app <APP_ID> \
  --pkg <PATH_TO_PKG> \
  --version <VERSION> \
  --build-number <BUILD_NUMBER> \
  --wait
```

Notes:
- `--pkg` automatically sets platform to `MAC_OS`.
- `asc publish appstore` currently supports `--ipa` workflows; for macOS `.pkg`, use `asc builds upload --pkg` + attach/submit steps below.

### Attach and Submit
Same as iOS, but use `--platform MAC_OS`:
```bash
# Wait for build to process
asc builds list --app <APP_ID> --platform MAC_OS --limit 5

# Attach to version
asc versions attach-build --version-id <VERSION_ID> --build <BUILD_ID>

# Create submission
asc review submissions-create --app <APP_ID> --platform MAC_OS

# Add version item
asc review items-add \
  --submission <SUBMISSION_ID> \
  --item-type appStoreVersions \
  --item-id <VERSION_ID>

# Submit
asc review submissions-submit --id <SUBMISSION_ID> --confirm
```

## visionOS / tvOS Release

Same as iOS flow, use appropriate `--platform`:
- `VISION_OS`
- `TV_OS`

## Multi-Platform Release

When releasing the same version across platforms:
1. Upload each platform's build separately
2. Create version for each platform if not exists
3. Attach builds to respective versions
4. Submit each platform separately (or together via reviewSubmissions API)

## Pre-submission Checklist
Before submitting, verify:
- [ ] Build status is `VALID` (not processing)
- [ ] Encryption compliance resolved
- [ ] Content rights declaration set
- [ ] Copyright field populated
- [ ] All localizations complete
- [ ] Screenshots present

See `asc-submission-health` skill for detailed preflight checks.

## Notes
- Always use `--help` to verify flags for the exact command.
- Use `--output table` / `--output markdown` for human-readable output; default is JSON.
- macOS builds require `ITSAppUsesNonExemptEncryption` in Info.plist to avoid encryption issues.
