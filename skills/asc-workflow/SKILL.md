---
name: asc-workflow
description: Define, validate, and run repo-local multi-step automations with `asc workflow` and `.asc/workflow.json`. Use when migrating from lane tools, wiring CI pipelines, or orchestrating repeatable `asc` + shell release flows with hooks, conditionals, and sub-workflows.
---

# asc workflow

Use this skill when you need lane-style automation inside the CLI using:
- `asc workflow run`
- `asc workflow validate`
- `asc workflow list`

This feature is best for deterministic automation that lives in your repo, is reviewable in PRs, and can run the same way locally and in CI.

## Command discovery

- Always use `--help` to confirm flags and subcommands:
  - `asc workflow --help`
  - `asc workflow run --help`
  - `asc workflow validate --help`
  - `asc workflow list --help`

## End-to-end flow

1. Author `.asc/workflow.json`
2. Validate structure and references:
   - `asc workflow validate`
3. Discover available workflows:
   - `asc workflow list`
   - `asc workflow list --all` (includes private helpers)
4. Preview execution without side effects:
   - `asc workflow run --dry-run beta`
5. Execute with runtime params:
   - `asc workflow run beta BUILD_ID:123456789 GROUP_ID:abcdef`

## File location and format

- Default path: `.asc/workflow.json`
- Override path: `asc workflow run --file ./path/to/workflow.json <name>`
- JSONC comments are supported (`//` and `/* ... */`)

## Output and CI contract

- `stdout`: structured JSON result (`status`, `steps`, durations)
- `stderr`: step command output, hook output, dry-run previews
- `asc workflow validate` always prints JSON and returns non-zero when invalid

This enables machine-safe checks:

```bash
asc workflow validate | jq -e '.valid == true'
asc workflow run beta BUILD_ID:123 GROUP_ID:xyz | jq -e '.status == "ok"'
```

## Schema (what the feature supports)

Top-level keys:
- `env`: global defaults
- `before_all`: command run once before steps
- `after_all`: command run once after successful steps
- `error`: command run when any failure occurs
- `workflows`: named workflow map

Workflow keys:
- `description`
- `private` (not directly runnable)
- `env`
- `steps`

Step forms:
- String shorthand: `"echo hello"` -> run step
- Object with:
  - `run`: shell command
  - `workflow`: call sub-workflow
  - `name`: label for reporting
  - `if`: conditional var name
  - `with`: env overrides for workflow-call steps only

## Runtime params (`KEY:VALUE` / `KEY=VALUE`)

- `asc workflow run <name> [KEY:VALUE ...]` supports both separators:
  - `VERSION:2.1.0`
  - `VERSION=2.1.0`
- If both separators exist, the first one wins.
- Repeated keys are last-write-wins.
- In step commands, reference params via shell expansion (`$VAR`).
- Avoid putting secrets in `.asc/workflow.json`; pass them via CI secrets/env.

## Run-tail flags

`asc workflow run` also accepts core flags after the workflow name:
- `--dry-run`
- `--pretty`
- `--file`

Examples:
- `asc workflow run beta --dry-run`
- `asc workflow run beta --file .asc/workflow.json BUILD_ID:123`

## Execution semantics

- `before_all` runs once before step execution
- `after_all` runs only when steps succeed
- `error` runs on failure (step failure, before/after hook failure)
- Sub-workflows are executed inline as part of the call step
- Maximum sub-workflow nesting depth is 16

## Env precedence

Main workflow run:
- `definition.env` < `workflow.env` < CLI params

Sub-workflow call step (`"workflow": "...", "with": {...}`):
- sub-workflow `env` defaults
- caller env (including CLI params) overrides
- step `with` overrides all

## Sub-workflows and private workflows

- Use `"workflow": "<name>"` to call helper workflows.
- Use `"private": true` for helper-only workflows.
- Private workflows:
  - cannot be run directly
  - can be called by other workflows
  - are hidden from `asc workflow list` unless `--all` is used
- Validation catches unknown workflow references and cyclic references.

## Conditionals (`if`)

- Add `"if": "VAR_NAME"` on a step.
- Step runs only if `VAR_NAME` is truthy.
- Truthy: `1`, `true`, `yes`, `y`, `on` (case-insensitive).
- Resolution order for `if` lookup:
  1. merged workflow env/params
  2. `os.Getenv(VAR_NAME)`

## Dry-run behavior

- `asc workflow run --dry-run <name>` does not execute commands.
- It prints previews to `stderr`.
- Dry-run shows raw commands (without env expansion), which helps avoid secret leakage in previews.

## Shell behavior

- Run steps use `bash -o pipefail -c` when bash is available.
- Fallback is `sh -c` when bash is unavailable.
- Pipelines therefore fail correctly in most CI shells when bash exists.

## Practical authoring rules

- Keep workflow files in version control.
- Use IDs in step commands where possible for deterministic automation.
- Use `--confirm` for destructive `asc` operations inside steps.
- Validate first, then dry-run, then real run.
- Keep hooks lightweight and side-effect aware.

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
      "description": "Distribute a build to a TestFlight group and notify",
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
        },
        {
          "name": "notify",
          "if": "SLACK_WEBHOOK",
          "run": "echo sent_release_notice"
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

## Useful invocations

```bash
# Validate and fail CI on invalid file
asc workflow validate | jq -e '.valid == true'

# Show discoverable workflows
asc workflow list --pretty

# Include private helpers
asc workflow list --all --pretty

# Preview a real run
asc workflow run --dry-run beta BUILD_ID:123 GROUP_ID:grp_abc

# Run with params and assert success
asc workflow run beta BUILD_ID:123 GROUP_ID:grp_abc | jq -e '.status == "ok"'
```
