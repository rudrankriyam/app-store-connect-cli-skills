---
name: asc-metadata-sync
description: Sync and validate App Store metadata and localizations with asc, including Fastlane format migration. Use when updating metadata or translations.
---

# ASC Metadata Sync

Use this skill to keep local metadata in sync with App Store Connect.

## Workflow
1. Export the current state:
   - `asc migrate export --app "APP_ID" --output "./metadata"`
   - or `asc localizations download --version "VERSION_ID" --path "./localizations"`
2. Validate local files:
   - `asc migrate validate --fastlane-dir "./metadata"`
3. Import updates:
   - `asc migrate import --app "APP_ID" --fastlane-dir "./metadata"`
   - or `asc localizations upload --version "VERSION_ID" --path "./localizations"`
4. Update single fields quickly:
   - `asc app-info set --app "APP_ID" --locale "en-US" --whats-new "Bug fixes"`
   - `asc build-localizations create --build "BUILD_ID" --locale "en-US" --whats-new "TestFlight notes"`

## Notes
- Version localizations and app info localizations are different; use the right command.
- `asc migrate validate` enforces character limits before upload.
- Use `asc localizations list` to confirm available locales and IDs.
