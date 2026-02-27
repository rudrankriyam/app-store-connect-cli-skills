---
name: asc-wall-submit
description: Submit or update a Wall of Apps entry in the App-Store-Connect-CLI repository using the existing generate-and-PR flow. Use when the user says "submit to wall of apps", "add my app to the wall", "wall-of-apps", or asks for make generate app + PR help.
---

# asc wall submit

Use this skill to add or update a Wall of Apps entry without introducing new CLI surface area.

## When to use

- User wants to submit an app to the Wall of Apps
- User wants to update an existing Wall of Apps entry
- User asks for the exact Wall submission flow

## Required inputs

Collect and confirm all fields before running commands:

- `app`: app name
- `link`: app URL (`http`/`https`, usually App Store URL)
- `creator`: GitHub handle or creator name
- `platform`: comma-separated labels (for example: `iOS,macOS`)

If any value is missing, ask for it first.

## Submission workflow

1. Run commands from the `App-Store-Connect-CLI` repository root.
2. Run:
   `make generate app APP="Your App Name" LINK="https://apps.apple.com/app/id1234567890" CREATOR="your-handle" PLATFORM="iOS,macOS"`
3. Verify generated changes include:
   - `docs/wall-of-apps.json`
   - `README.md`
4. Review diff and confirm:
   - The JSON entry is added or updated correctly.
   - The README wall snippet is regenerated from markers.
5. Open a focused PR with only the Wall-related generated changes.

## Guardrails

- Do not hand-edit the Wall snippet in `README.md`.
- Do not modify unrelated entries in `docs/wall-of-apps.json`.
- If generation fails due to invalid input, fix inputs and rerun the generator.
- Keep submission path PR-based unless maintainers define an issue-based intake flow.

## Examples

Add new app:

`make generate app APP="My App" LINK="https://apps.apple.com/app/id1234567890" CREATOR="my-handle" PLATFORM="iOS"`

Update existing app (same app name updates in place):

`make generate app APP="My App" LINK="https://apps.apple.com/app/id1234567890" CREATOR="my-handle" PLATFORM="iOS,macOS"`
