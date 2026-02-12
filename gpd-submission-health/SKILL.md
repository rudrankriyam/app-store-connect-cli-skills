---
name: gpd-submission-health
description: Preflight Google Play releases, validate edits, and verify listing completeness with gpd. Use when shipping to production or troubleshooting a failed release.
---

# GPD Submission Health

Use this skill to reduce Play Console submission failures and validate readiness.

## Preconditions
- Auth configured and package name resolved.
- Build uploaded and available for the target track.
- Store listing metadata and assets updated.

## Pre-submission checklist

### 1. Validate edit (if using edit lifecycle)
```bash
gpd publish edit validate EDIT_ID --package com.example.app
```

### 2. Confirm release status
```bash
gpd publish status --package com.example.app --track production
```
Check:
- Release status is expected (`draft`, `inProgress`, or `completed`).
- Version code matches the uploaded build.

### 3. Verify store listing metadata
```bash
gpd publish listing get --package com.example.app
gpd publish details get --package com.example.app
```

### 4. Verify screenshots and assets
```bash
gpd publish images list phoneScreenshots --package com.example.app --locale en-US
gpd publish assets spec
```

### 5. Upload deobfuscation mapping (if needed)
```bash
gpd publish deobfuscation upload mapping.txt --package com.example.app --type proguard --version-code 123
```

## Submit to production
```bash
gpd publish release --package com.example.app --track production --status inProgress --version-code 123
```

## Common submission issues

### Release not in valid state
Check:
1. Version code uploaded and attached to the track.
2. Edit validation passes.
3. Required store listing fields present for all locales.

### Missing screenshots or assets
Use:
```bash
gpd publish images list phoneScreenshots --package com.example.app --locale en-US
gpd publish images upload icon icon.png --package com.example.app --locale en-US
```

### Policy declarations not complete
Some policy/compliance items must be completed in Play Console UI. Confirm in the console if CLI operations pass but submission is blocked.

## Notes
- Use `gpd publish edit validate` before committing large changes.
- Use `--dry-run` where available before destructive actions.
