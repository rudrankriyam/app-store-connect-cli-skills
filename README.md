# App Store Connect CLI Skills

A collection of Agent Skills for shipping with the [App Store Connect CLI](https://github.com/rudrankriyam/App-Store-Connect-CLI) (`asc`). These skills are designed for zero-friction automation around builds, TestFlight, metadata, submissions, and signing.

Skills follow the Agent Skills format.

## Available Skills

### asc-cli-usage

Guidance for running `asc` commands (flags, pagination, output, auth).

**Use when:**
- You need the correct `asc` command or flag combination
- You want JSON-first output and pagination tips for automation

### asc-release-flow

End-to-end release workflows for TestFlight and App Store.

**Use when:**
- You want to upload, distribute, and submit in one flow
- You need the manual sequence for fine-grained control

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

### asc-submission-health

Preflight checks, submission, and review monitoring.

**Use when:**
- You want to reduce submission failures
- You need to track review status and re-submit safely

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

## Installation

Install this skill pack:

```bash
npx add-skill rudrankriyam/asc-skills
```

## Usage

Skills are automatically available once installed. The agent will use them when relevant tasks are detected.

**Examples:**

```
Publish my `MyApp` build `1.2.3` to TestFlight group `Beta Testers` and wait for processing
```

```
Set up signing for bundle ID `com.example.app`: enable iCloud, create a distribution certificate, and create an App Store profile
```

```
Validate Fastlane metadata in `./metadata` and sync it to App Store Connect for version `1.2.3`
```

## Skill Structure

Each skill contains:
- `SKILL.md` - Instructions for the agent
- `scripts/` - Helper scripts for automation (optional)
- `references/` - Supporting documentation (optional)

## License

MIT
