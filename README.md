# asc cli skills

A collection of Agent Skills for shipping with the [asc cli](https://github.com/rudrankriyam/App-Store-Connect-CLI) (`asc`). These skills are designed for zero-friction automation around builds, TestFlight, metadata, submissions, and signing.

This is a community-maintained, unofficial skill pack and is not affiliated with Apple.

Skills follow the Agent Skills format.

## Available Skills

### asc-cli-usage

Guidance for running `asc` commands (flags, pagination, output, auth).

**Use when:**
- You need the correct `asc` command or flag combination
- You want JSON-first output and pagination tips for automation

### asc-workflow

Define and run repo-local automation graphs using `asc workflow` and `.asc/workflow.json`.

**Use when:**
- You are migrating from lane-based automation to repo-local workflows
- You need multi-step orchestration with machine-parseable JSON output for CI/agents
- You need hooks (`before_all`, `after_all`, `error`), conditionals (`if`), and private helper sub-workflows
- You want validation (`asc workflow validate`) with cycle/reference checks before execution

### asc-app-create-ui

Create a new App Store Connect app via browser automation when no API exists.

**Use when:**
- You need to create an app record (name, bundle ID, SKU, primary language)
- You are comfortable logging in to App Store Connect in a real browser

### asc-xcode-build

Build, archive, and export iOS/macOS apps with xcodebuild before uploading.

**Use when:**
- You need to create an IPA or PKG for upload
- You're setting up CI/CD build pipelines
- You need to configure ExportOptions.plist
- You're troubleshooting encryption compliance issues

### asc-shots-pipeline

Agent-first screenshot pipeline using xcodebuild/simctl, AXe, JSON plans, `asc screenshots frame` (experimental), and `asc screenshots upload`.

**Use when:**
- You need a repeatable simulator screenshot automation flow
- You want AXe-based UI driving before capture
- You need a staged pipeline (capture -> frame -> upload)
- You need to discover supported frame devices (`asc screenshots list-frame-devices`)
- You want pinned Koubou guidance for deterministic framing (`koubou==0.13.0`)

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

Metadata and localization sync (including legacy metadata format migration).

**Use when:**
- You are updating App Store metadata or localizations
- You need to validate character limits before upload
- You need to update privacy policy URL or app-level metadata

### asc-localize-metadata

Translate App Store metadata (description, keywords, what's new, subtitle) to multiple locales using LLM translation prompts and push via `asc`.

**Use when:**
- You want to localize an app's App Store listing from a source locale (usually en-US)
- You need locale-aware keywords (not literal translations) and strict character limit enforcement
- You want a review-before-upload workflow for translations

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

### asc-subscription-localization

Bulk-localize subscription and IAP display names across all App Store locales.

**Use when:**
- You want to set the same subscription display name in every language at once
- You need to fill in missing subscription/group/IAP localizations
- You're tired of clicking through each locale in App Store Connect manually

### asc-notarization

Archive, export, and notarize macOS apps with Developer ID signing.

**Use when:**
- You need to notarize a macOS app for distribution outside the App Store
- You want the full flow: archive → Developer ID export → zip → notarize → staple
- You're troubleshooting Developer ID signing or trust chain issues

### asc-crash-triage

Triage TestFlight crashes, beta feedback, and performance diagnostics.

**Use when:**
- You want to review recent TestFlight crash reports
- You need a crash summary grouped by signature, device, and build
- You want to check beta tester feedback and screenshots
- You need performance diagnostics (hangs, disk writes, launches) for a build

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
Validate metadata in `./metadata` and sync it to App Store Connect for version `1.2.3`

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
