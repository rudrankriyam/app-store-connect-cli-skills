---
name: asc-submission-health
description: Preflight App Store submissions, submit builds, and monitor review status with asc. Use when shipping or troubleshooting review submissions.
---

# ASC Submission Health

Use this skill to reduce review submission failures and monitor status.

## Preconditions
- Auth configured and app/version/build IDs resolved.
- Build is processed (not in processing state).

## Preflight checks
- Build info:
  - `asc builds info --build "BUILD_ID"`
- Metadata validity:
  - `asc migrate validate --fastlane-dir "./metadata"`

## Submit
- `asc submit create --app "APP_ID" --version "1.2.3" --build "BUILD_ID" --confirm`
- Use `--platform` when multiple platforms exist.

## Monitor
- `asc submit status --id "SUBMISSION_ID"`
- `asc submit status --version-id "VERSION_ID"`
- More detail:
  - `asc review submissions-list --app "APP_ID" --paginate`
  - `asc review submissions-get --id "SUBMISSION_ID"`

## Cancel / retry
- `asc submit cancel --id "SUBMISSION_ID" --confirm`
- Fix issues, then re-run `asc submit create`.

## Notes
- `asc submit create` uses the new reviewSubmissions API automatically.
- Use `--output table` when you want human-readable status.
