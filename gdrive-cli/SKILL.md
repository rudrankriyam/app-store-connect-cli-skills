---
name: gdrive-cli
description: Manage Google Drive files, folders, Sheets, Docs, and Slides using the gdrive CLI. Use when working with Google Drive operations, uploading/downloading files, managing Google Workspace documents, or when the user mentions Google Drive, gdrive, or cloud file storage.
---

# Google Drive CLI

Manage Google Drive using the `gdrive` command-line tool.

## Prerequisites

Ensure gdrive is installed and authenticated:

```bash
gdrive --version

export GDRIVE_CLIENT_ID="your-client-id"
export GDRIVE_CLIENT_SECRET="your-client-secret"
gdrive auth login --preset workspace-full
```

## File Operations

```bash
gdrive files list --json
gdrive files list --paginate --json
gdrive files list --query "name contains 'report'" --order-by "modifiedTime desc" --json
gdrive files upload myfile.txt --json
gdrive files download FILE_ID --output downloaded.txt
gdrive files download FILE_ID --doc
gdrive files delete FILE_ID --dry-run
gdrive files delete FILE_ID
gdrive files trash FILE_ID
gdrive files restore FILE_ID
```

## Folder Operations

```bash
gdrive folders create "My Folder" --json
gdrive folders list FOLDER_ID --json
gdrive folders delete FOLDER_ID
gdrive folders move FILE_ID PARENT_ID
```

## Permissions

```bash
gdrive permissions list FILE_ID --json
gdrive permissions create FILE_ID --type user --email user@example.com --role reader
gdrive permissions create FILE_ID --type user --email user@example.com --role writer
gdrive permissions public FILE_ID
gdrive permissions delete FILE_ID PERMISSION_ID
```

## Google Sheets

```bash
gdrive sheets list --json
gdrive sheets list --paginate --json
gdrive sheets create "My Sheet" --json
gdrive sheets create "My Sheet" --parent FOLDER_ID --json
gdrive sheets get SHEET_ID --json
gdrive sheets values get SHEET_ID "Sheet1!A1:B10" --json
gdrive sheets values update SHEET_ID "Sheet1!A1:B2" --values '[[1,2],[3,4]]'
gdrive sheets values update SHEET_ID "Sheet1!A1" --values-file data.json --value-input-option USER_ENTERED
gdrive sheets values append SHEET_ID "Sheet1!A1" --values '[[5,6]]'
gdrive sheets values clear SHEET_ID "Sheet1!A1:B10"
gdrive sheets batch-update SHEET_ID --requests-file batch-update.json
```

## Google Docs

```bash
gdrive docs list --json
gdrive docs list --paginate --json
gdrive docs create "My Doc" --json
gdrive docs create "My Doc" --parent FOLDER_ID --json
gdrive docs get DOC_ID --json
gdrive docs read DOC_ID
gdrive docs read DOC_ID --json
gdrive docs update DOC_ID --requests-file updates.json
```

## Google Slides

```bash
gdrive slides list --json
gdrive slides list --paginate --json
gdrive slides create "My Presentation" --json
gdrive slides create "My Presentation" --parent FOLDER_ID --json
gdrive slides get PRESENTATION_ID --json
gdrive slides read PRESENTATION_ID
gdrive slides read PRESENTATION_ID --json
gdrive slides update PRESENTATION_ID --requests-file updates.json
gdrive slides replace PRESENTATION_ID --data '{"{{NAME}}":"Alice","{{DATE}}":"2026-01-24"}'
gdrive slides replace PRESENTATION_ID --file replacements.json
```

## Shared Drives

```bash
gdrive drives list --json
gdrive drives list --paginate --json
gdrive drives get DRIVE_ID --json
gdrive files list --drive-id DRIVE_ID --json
```

## Multiple Profiles

```bash
gdrive auth login --profile work
gdrive auth login --profile personal
gdrive --profile work files list --json
```

## Agent Best Practices

1. **Always use `--json`** for machine-readable output
2. **Use `--paginate`** to get all results without missing items
3. **Use `--dry-run`** before destructive operations
4. **Use file IDs** not paths for Shared Drives
5. **Check exit codes**: 0=success, 2=auth required, 3=invalid argument, 4=not found, 5=permission denied, 6=rate limited

## Common Workflows

### Upload and Share

```bash
RESULT=$(gdrive files upload report.pdf --json)
FILE_ID=$(echo $RESULT | jq -r '.id')
gdrive permissions create $FILE_ID --type user --email user@example.com --role reader
```

### Search and Download

```bash
gdrive files list --query "mimeType = 'application/pdf'" --order-by "modifiedTime desc" --json
gdrive files download FILE_ID --output local-copy.pdf
```

### Create Sheet with Data

```bash
RESULT=$(gdrive sheets create "Data Report" --json)
SHEET_ID=$(echo $RESULT | jq -r '.spreadsheetId')
gdrive sheets values update $SHEET_ID "Sheet1!A1" --values '[["Name","Value"],["Item1",100],["Item2",200]]'
```
