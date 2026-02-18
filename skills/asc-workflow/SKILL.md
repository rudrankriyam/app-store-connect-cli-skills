---
name: asc-workflow
description: Define, validate, and run lane-style multi-step automation sequences using `asc workflow` and a repo-local `.asc/workflow.json`. Use when migrating from lane-based automation, building enterprise CI flows, or orchestrating multi-command `asc` runs.
---

# ASC Workflows (lane-style automation)

Use this skill when you need to create or run `.asc/workflow.json` workflows via:
- `asc workflow run`
- `asc workflow validate`
- `asc workflow list`

Workflows are a lane-style "lanes" replacement: named, multi-step automation sequences that compose existing `asc` commands and normal shell commands.

## Command discovery

- Always use `--help` to confirm flags and subcommands:
  - `asc workflow --help`
  - `asc workflow run --help`
  - `asc workflow validate --help`
  - `asc workflow list --help`

## Key commands (typical flow)

1. Validate the workflow file (CI gate):
   - `asc workflow validate`
2. Dry-run a workflow (no side effects):
   - `asc workflow run --dry-run beta`
3. Run the workflow with runtime parameters:
   - `asc workflow run beta BUILD_ID:123456789 GROUP_ID:abcdef`
4. List available workflows (for discovery):
   - `asc workflow list`
   - Include private workflows: `asc workflow list --all`

## File location and format

- Default file path: `.asc/workflow.json` (repo-local; commit it with your code).
- The workflow file supports JSONC comments (`//` and `/* */`).

## Output contract (agent-friendly)

- stdout: JSON-only (structured result)
- stderr: step/hook command output and dry-run previews

This makes it safe to do:

```bash
asc workflow run beta BUILD_ID:123 GROUP_ID:xyz | jq -e '.status == "ok"'
```

## Runtime params (KEY:VALUE / KEY=VALUE)

- `asc workflow run <name> [KEY:VALUE ...]` supports both separators:
  - `VERSION:2.1.0`
  - `VERSION=2.1.0`
- In steps, reference params via `$VAR` (shell expansion).
- Avoid putting secrets in `.asc/workflow.json`; pass them via CI secrets/env.

## Hooks

Workflows support definition-level hooks:
- `before_all`: runs once before any steps
- `after_all`: runs once after all steps (only if steps succeeded)
- `error`: runs on any failure

When hook output matters, keep hooks simple and write their logs to stderr.

## Conditionals (`if`)

- Add `"if": "VAR_NAME"` to a step to skip it when `VAR_NAME` is falsy.
- The conditional checks workflow env/params first, and then falls back to `os.Getenv(VAR_NAME)`.
- Truthy values: `1`, `true`, `yes`, `y`, `on` (case-insensitive).

## Sub-workflows and private workflows

- A step can call another workflow via `"workflow": "<name>"`.
- `"with"` env overrides are only valid on workflow steps (not run steps).
- `"private": true` workflows:
  - cannot be run directly from the CLI
  - can be called by other workflows as sub-workflows
  - are hidden from `asc workflow list` unless `--all` is used

## Recommended authoring approach (enterprise-friendly)

- Keep steps deterministic and explicit (prefer IDs where possible).
- Validate early (`asc workflow validate`) and keep the file in version control.
- Start with `--dry-run` before enabling real runs in CI.
- Use existing `asc` commands for the actual work (build upload, TestFlight distribution, submission).
- Use `--confirm` on destructive operations inside steps; workflows should never add interactive prompts.

## Example `.asc/workflow.json` template

This is a practical starting point for lane migration; adapt step commands to your org.

```json
{
  "env": {
    "APP_ID": "123456789",
    "VERSION": "1.0.0"
  },
  "before_all": "asc auth status",
  "after_all": "echo workflow_done",
  "error": "echo workflow_failed",
  "workflows": {
    "beta": {
      "description": "Distribute a build to a TestFlight group",
      "env": {
        "GROUP_ID": ""
      },
      "steps": [
        {
          "name": "list_builds",
          "run": "asc builds list --app $APP_ID --sort -uploadedDate --limit 5"
        },
        {
          "name": "list_groups",
          "run": "asc testflight beta-groups list --app $APP_ID --limit 20"
        },
        {
          "name": "add_build_to_group",
          "if": "BUILD_ID",
          "run": "asc builds add-groups --build $BUILD_ID --group $GROUP_ID"
        }
      ]
    },
    "release": {
      "description": "Submit a version for App Store review",
      "steps": [
        {
          "workflow": "sync-metadata",
          "with": {
            "METADATA_DIR": "./metadata"
          }
        },
        {
          "name": "submit",
          "run": "asc submit create --app $APP_ID --version $VERSION --build $BUILD_ID --confirm"
        }
      ]
    },
    "sync-metadata": {
      "private": true,
      "description": "Private helper workflow (callable only via workflow steps)",
      "steps": [
        {
          "name": "migrate_validate",
          "run": "echo METADATA_DIR_is_$METADATA_DIR"
        }
      ]
    }
  }
}
```

