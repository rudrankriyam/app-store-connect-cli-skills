---
name: asc-build-lifecycle
description: Track build processing, find latest builds, and clean up old builds with asc. Use when managing build retention or waiting on processing.
---

# asc build lifecycle

Use this skill to manage build state, processing, and retention.

## Find the right build
- Latest build:
  - `asc builds latest --app "APP_ID" --version "1.2.3" --platform IOS`
- Recent builds:
  - `asc builds list --app "APP_ID" --sort -uploadedDate --limit 10`

## Inspect processing state
- `asc builds info --build "BUILD_ID"`

## Distribution flows
- Prefer end-to-end:
  - `asc publish testflight --app "APP_ID" --ipa "./app.ipa" --group "GROUP_ID" --wait`
  - `asc publish appstore --app "APP_ID" --ipa "./app.ipa" --version "1.2.3" --wait --submit --confirm`

## Cleanup
- Preview expiration:
  - `asc builds expire-all --app "APP_ID" --older-than 90d --dry-run`
- Apply expiration:
  - `asc builds expire-all --app "APP_ID" --older-than 90d --confirm`
- Single build:
  - `asc builds expire --build "BUILD_ID"`

## Notes
- `asc builds upload` prepares upload operations only; use `asc publish` for end-to-end flows.
- For long processing times, use `--wait`, `--poll-interval`, and `--timeout` where supported.
