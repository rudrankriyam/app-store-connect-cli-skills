# App Store Connect CLI Skills

A collection of Agent Skills for shipping with the [App Store Connect CLI](https://github.com/rudrankriyam/App-Store-Connect-CLI) (`asc`). These skills are designed for zero-friction automation around builds, TestFlight, metadata, submissions, and signing.

Skills follow the Agent Skills format.

## Available Skills

### asc-cli-usage

Guidance for running `asc` commands (flags, pagination, output, auth).

**Use when:**
- You need the correct `asc` command or flag combination
- You want JSON-first output and pagination tips for automation

### asc-xcode-build

Build, archive, and export iOS/macOS apps with xcodebuild before uploading.

**Use when:**
- You need to create an IPA or PKG for upload
- You're setting up CI/CD build pipelines
- You need to configure ExportOptions.plist
- You're troubleshooting encryption compliance issues

### asc-shots-pipeline

Agent-first screenshot pipeline using xcodebuild/simctl, AXe, JSON plans, `asc shots frame`, and asc screenshot upload.

**Use when:**
- You need a repeatable simulator screenshot automation flow
- You want AXe-based UI driving before capture
- You need a staged pipeline (capture -> frame -> upload)
- You need to discover supported frame devices (`asc shots frames list-devices`)

### asc-release-flow

End-to-end release workflows for TestFlight and App Store.

**Use when:**
- You want to upload, distribute, and submit in one flow
- You need the manual sequence for fine-grained control
- You're releasing for iOS, macOS, visionOS, or tvOS

### asc-signing-setup

Bundle IDs, capabilities, certificates, and provisioning profiles.

**Use when:**
- You are onboarding a new app or bundle ID
- You need to create or rotate signing assets

### asc-id-resolver

Resolve IDs for apps, builds, versions, groups, and testers.

**Use when:**
- A command requires IDs and you only have names
- You want deterministic outputs for automation

### asc-metadata-sync

Metadata and localization sync (including Fastlane format).

**Use when:**
- You are updating App Store metadata or localizations
- You need to validate character limits before upload
- You need to update privacy policy URL or app-level metadata

### asc-submission-health

Preflight checks, submission, and review monitoring.

**Use when:**
- You want to reduce submission failures
- You need to track review status and re-submit safely
- You're troubleshooting "version not in valid state" errors

### asc-testflight-orchestration

Beta groups, testers, build distribution, and What to Test notes.

**Use when:**
- You manage multiple TestFlight groups and testers
- You need consistent beta rollout steps

### asc-build-lifecycle

Build processing, latest build resolution, and cleanup.

**Use when:**
- You are waiting on build processing
- You want automated cleanup and retention policies

### asc-ppp-pricing

Territory-specific pricing using purchasing power parity (PPP).

**Use when:**
- You want different prices for different countries
- You are implementing localized pricing strategies
- You need to adjust prices based on regional purchasing power

### asc-notarization

Archive, export, and notarize macOS apps with Developer ID signing.

**Use when:**
- You need to notarize a macOS app for distribution outside the App Store
- You want the full flow: archive → Developer ID export → zip → notarize → staple
- You're troubleshooting Developer ID signing or trust chain issues

## Installation

Install this skill pack:

```bash
npx skills add rudrankriyam/app-store-connect-cli-skills
```

## Usage

Skills are automatically available once installed. The agent will use them when relevant tasks are detected.

**Examples:**

```
Build and upload my macOS app to App Store Connect
```

```
Publish my `MyApp` build `1.2.3` to TestFlight group `Beta Testers` and wait for processing
```

```
Set up signing for bundle ID `com.example.app`: enable iCloud, create a distribution certificate, and create an App Store profile
```

```
Validate Fastlane metadata in `./metadata` and sync it to App Store Connect for version `1.2.3`
```

```
Submit my iOS app version 2.0 to App Store review
```

## Skill Structure

Each skill contains:
- `SKILL.md` - Instructions for the agent
- `scripts/` - Helper scripts for automation (optional)
- `references/` - Supporting documentation (optional)

## License

MIT
