---
name: gpd-release-flow
description: End-to-end release workflows for Google Play using gpd publish commands, tracks, rollouts, and edit lifecycle. Use when uploading builds or managing releases.
---

# Release flow (Google Play)

Use this skill when you need to upload a build, publish to a track, or manage rollout.

## Preconditions
- Ensure credentials are set (`GPD_SERVICE_ACCOUNT_KEY`).
- Use a new version code for each upload.
- Always pass `--package` explicitly.

## Preferred end-to-end commands

### Upload and release to a track
```bash
gpd publish upload app.aab --package com.example.app
gpd publish release --package com.example.app --track internal --status completed
```

### Promote between tracks
```bash
gpd publish promote --package com.example.app --from-track beta --to-track production
```

## Manual sequence with edit lifecycle
Use when you need precise control or multiple changes in one commit.

```bash
# 1. Create edit
EDIT_ID=$(gpd publish edit create --package com.example.app | jq -r '.data.editId')

# 2. Upload build without auto-commit
gpd publish upload app.aab --package com.example.app --edit-id $EDIT_ID --no-auto-commit

# 3. Configure release
gpd publish release --package com.example.app --track internal --status draft --edit-id $EDIT_ID

# 4. Validate and commit
gpd publish edit validate $EDIT_ID --package com.example.app
gpd publish edit commit $EDIT_ID --package com.example.app
```

## Staged rollout
```bash
gpd publish release --package com.example.app --track production --status inProgress --version-code 123
gpd publish rollout --package com.example.app --track production --percentage 5
gpd publish rollout --package com.example.app --track production --percentage 50
gpd publish rollout --package com.example.app --track production --percentage 100
```

## Halt or rollback
```bash
gpd publish halt --package com.example.app --track production --confirm
gpd publish rollback --package com.example.app --track production --confirm
```

## Track status
```bash
gpd publish status --package com.example.app --track production
gpd publish tracks --package com.example.app
```

## Notes
- Use `--status draft` first for risky releases.
- Use `--confirm` only after reviewing `gpd publish status` output.
