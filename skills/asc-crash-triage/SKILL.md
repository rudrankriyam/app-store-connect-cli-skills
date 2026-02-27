---
name: asc-crash-triage
description: Triage TestFlight crashes, beta feedback, and performance diagnostics using asc. Use when the user asks about TF crashes, TestFlight crash reports, beta tester feedback, app hangs, disk writes, launch diagnostics, or wants a crash summary for a build or app.
---

# asc crash triage

Use this skill to fetch, analyze, and summarize TestFlight crash reports, beta feedback, and performance diagnostics.

## Workflow

1. Resolve the app ID if not provided (use `asc apps list`).
2. Fetch data with the appropriate command.
3. Parse JSON output and present a human-readable summary.

## TestFlight crash reports

List recent crashes (newest first):

- `asc crashes --app "APP_ID" --sort -createdDate --limit 10`
- Filter by build: `asc crashes --app "APP_ID" --build "BUILD_ID" --sort -createdDate --limit 10`
- Filter by device/OS: `asc crashes --app "APP_ID" --device-model "iPhone16,2" --os-version "18.0"`
- All crashes: `asc crashes --app "APP_ID" --paginate`
- Table view: `asc crashes --app "APP_ID" --sort -createdDate --limit 10 --output table`

## TestFlight beta feedback

List recent feedback (newest first):

- `asc feedback --app "APP_ID" --sort -createdDate --limit 10`
- With screenshots: `asc feedback --app "APP_ID" --sort -createdDate --limit 10 --include-screenshots`
- Filter by build: `asc feedback --app "APP_ID" --build "BUILD_ID" --sort -createdDate`
- All feedback: `asc feedback --app "APP_ID" --paginate`

## Performance diagnostics (hangs, disk writes, launches)

Requires a build ID. Resolve via `asc builds latest --app "APP_ID" --platform IOS` or `asc builds list --app "APP_ID" --sort -uploadedDate --limit 5`.

- List diagnostic signatures: `asc performance diagnostics list --build "BUILD_ID"`
- Filter by type: `asc performance diagnostics list --build "BUILD_ID" --diagnostic-type "HANGS"`
  - Types: `HANGS`, `DISK_WRITES`, `LAUNCHES`
- Get logs for a signature: `asc performance diagnostics get --id "SIGNATURE_ID"`
- Download all metrics: `asc performance download --build "BUILD_ID" --output ./metrics.json`

## Resolving IDs

- App ID from name: `asc apps list --name "AppName"` or `asc apps list --bundle-id "com.example.app"`
- Latest build ID: `asc builds latest --app "APP_ID" --platform IOS`
- Recent builds: `asc builds list --app "APP_ID" --sort -uploadedDate --limit 5`
- Set default: `export ASC_APP_ID="APP_ID"`

## Summary format

When presenting results, organize by severity and frequency:

1. **Total count** — how many crashes/feedbacks in the result set.
2. **Top crash signatures** — group by exception type or crash reason, ranked by count.
3. **Affected builds** — which build versions are impacted.
4. **Device & OS breakdown** — most affected device models and OS versions.
5. **Timeline** — when crashes started or spiked.

For performance diagnostics, highlight the highest-weight signatures first.

## Notes

- Default output is JSON; use `--output table` or `--output markdown` for quick human review.
- Use `--paginate` to fetch all pages when doing a full analysis.
- Use `--pretty` with JSON for debugging command output.
- Crash data from App Store Connect may have 24-48h delay.
