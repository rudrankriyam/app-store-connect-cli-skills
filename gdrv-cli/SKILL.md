---
name: gdrv-cli
description: Manage Google Drive files, folders, Sheets, Docs, and Slides using the gdrv CLI. Use when working with Google Drive operations, uploading/downloading files, managing Google Workspace documents, or when the user mentions Google Drive, gdrv, or cloud file storage.
---

# Google Drive CLI

Manage Google Drive using the `gdrv` command-line tool.

## Prerequisites

Ensure gdrv is installed and authenticated:

```bash
gdrv --version

export GDRV_CLIENT_ID="your-client-id"
export GDRV_CLIENT_SECRET="your-client-secret"
gdrv auth login --preset workspace-full
```

## File Operations

```bash
gdrv files list --json
gdrv files list --paginate --json
gdrv files list --query "name contains 'report'" --order-by "modifiedTime desc" --json
gdrv files upload myfile.txt --json
gdrv files download FILE_ID --output downloaded.txt
gdrv files download FILE_ID --doc
gdrv files delete FILE_ID --dry-run
gdrv files delete FILE_ID
gdrv files trash FILE_ID
gdrv files restore FILE_ID
```

## Folder Operations

```bash
gdrv folders create "My Folder" --json
gdrv folders list FOLDER_ID --json
gdrv folders delete FOLDER_ID
gdrv folders move FILE_ID PARENT_ID
```

## Permissions

```bash
gdrv permissions list FILE_ID --json
gdrv permissions create FILE_ID --type user --email user@example.com --role reader
gdrv permissions create FILE_ID --type user --email user@example.com --role writer
gdrv permissions public FILE_ID
gdrv permissions delete FILE_ID PERMISSION_ID
```

## Google Sheets

```bash
gdrv sheets list --json
gdrv sheets list --paginate --json
gdrv sheets create "My Sheet" --json
gdrv sheets create "My Sheet" --parent FOLDER_ID --json
gdrv sheets get SHEET_ID --json
gdrv sheets values get SHEET_ID "Sheet1!A1:B10" --json
gdrv sheets values update SHEET_ID "Sheet1!A1:B2" --values '[[1,2],[3,4]]'
gdrv sheets values update SHEET_ID "Sheet1!A1" --values-file data.json --value-input-option USER_ENTERED
gdrv sheets values append SHEET_ID "Sheet1!A1" --values '[[5,6]]'
gdrv sheets values clear SHEET_ID "Sheet1!A1:B10"
gdrv sheets batch-update SHEET_ID --requests-file batch-update.json
```

## Google Docs

```bash
gdrv docs list --json
gdrv docs list --paginate --json
gdrv docs create "My Doc" --json
gdrv docs create "My Doc" --parent FOLDER_ID --json
gdrv docs get DOC_ID --json
gdrv docs read DOC_ID
gdrv docs read DOC_ID --json
gdrv docs update DOC_ID --requests-file updates.json
```

## Google Slides

```bash
gdrv slides list --json
gdrv slides list --paginate --json
gdrv slides create "My Presentation" --json
gdrv slides create "My Presentation" --parent FOLDER_ID --json
gdrv slides get PRESENTATION_ID --json
gdrv slides read PRESENTATION_ID
gdrv slides read PRESENTATION_ID --json
gdrv slides update PRESENTATION_ID --requests-file updates.json
gdrv slides replace PRESENTATION_ID --data '{"{{NAME}}":"Alice","{{DATE}}":"2026-01-24"}'
gdrv slides replace PRESENTATION_ID --file replacements.json
```

## Shared Drives

```bash
gdrv drives list --json
gdrv drives list --paginate --json
gdrv drives get DRIVE_ID --json
gdrv files list --drive-id DRIVE_ID --json
```

## Admin SDK

```bash
gdrv auth service-account --key-file ./service-account-key.json --impersonate-user admin@example.com --preset admin
gdrv admin users list --domain example.com --json
gdrv admin users get user@example.com --json
gdrv admin users create newuser@example.com --given-name "John" --family-name "Doe" --password "TempPass123!"
gdrv admin users update user@example.com --given-name "Jane" --family-name "Smith"
gdrv admin users suspend user@example.com
gdrv admin users delete user@example.com
gdrv admin groups list --domain example.com --json
gdrv admin groups create group@example.com "Team Group" --description "Team access group"
gdrv admin groups members list team@example.com --json
gdrv admin groups members add team@example.com user@example.com --role MEMBER
gdrv admin groups members remove team@example.com user@example.com
```

## Sync

```bash
gdrv sync init ./local-folder REMOTE_FOLDER_ID --json
gdrv sync init ./local-folder REMOTE_FOLDER_ID --direction push --conflict local-wins --json
gdrv sync init ./local-folder REMOTE_FOLDER_ID --exclude "*.tmp,node_modules" --json
gdrv sync list --json
gdrv sync status CONFIG_ID --json
gdrv sync CONFIG_ID --json
gdrv sync push CONFIG_ID --json
gdrv sync pull CONFIG_ID --json
gdrv sync CONFIG_ID --delete --json
gdrv sync CONFIG_ID --concurrency 10 --json
gdrv sync remove CONFIG_ID --json
```

## Config

```bash
gdrv config show
gdrv config set output_format json
gdrv config reset
```

## Multiple Profiles

```bash
gdrv auth login --profile work
gdrv auth login --profile personal
gdrv --profile work files list --json
```

## Agent Best Practices

1. **Always use `--json`** for machine-readable output
2. **Use `--paginate`** to get all results without missing items
3. **Use `--dry-run`** before destructive operations
4. **Use file IDs** not paths for Shared Drives
5. **Check exit codes**: 0=success, 1=general error, 2=auth required, 3=invalid argument, 4=not found, 5=permission denied, 6=rate limited

## Common Workflows

### Upload and Share

```bash
RESULT=$(gdrv files upload report.pdf --json)
FILE_ID=$(echo $RESULT | jq -r '.id')
gdrv permissions create $FILE_ID --type user --email user@example.com --role reader
```

### Search and Download

```bash
gdrv files list --query "mimeType = 'application/pdf'" --order-by "modifiedTime desc" --json
gdrv files download FILE_ID --output local-copy.pdf
```

### Create Sheet with Data

```bash
RESULT=$(gdrv sheets create "Data Report" --json)
SHEET_ID=$(echo $RESULT | jq -r '.spreadsheetId')
gdrv sheets values update $SHEET_ID "Sheet1!A1" --values '[["Name","Value"],["Item1",100],["Item2",200]]'
```

### Sync Local Folder with Drive

```bash
RESULT=$(gdrv sync init ./projects REMOTE_FOLDER_ID --json)
CONFIG_ID=$(echo $RESULT | jq -r '.id')
gdrv sync status $CONFIG_ID --json
gdrv sync $CONFIG_ID --json
```
