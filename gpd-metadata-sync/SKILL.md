---
name: gpd-metadata-sync
description: Sync and validate Google Play metadata, listings, and assets with gpd, including Fastlane-style workflows. Use when updating store listings or translations.
---

# GPD Metadata Sync

Use this skill to keep local metadata in sync with Google Play.

## Store listing fields

```bash
gpd publish listing get --package com.example.app
gpd publish listing update --package com.example.app --locale en-US --title "My App"
gpd publish details get --package com.example.app
gpd publish details update --package com.example.app --contact-email support@example.com
```

## Images and assets

```bash
gpd publish images list phoneScreenshots --package com.example.app --locale en-US
gpd publish images upload icon icon.png --package com.example.app --locale en-US
gpd publish images delete phoneScreenshots IMAGE_ID --package com.example.app --locale en-US
gpd publish images deleteall featureGraphic --package com.example.app --locale en-US
gpd publish assets upload ./assets --package com.example.app
gpd publish assets spec
```

## Fastlane metadata workflow

### Export current state
```bash
gpd migrate fastlane export --package com.example.app --output fastlane/metadata/android
```

### Validate local files
```bash
gpd migrate fastlane validate --dir fastlane/metadata/android
```

### Import updates
```bash
gpd migrate fastlane import --package com.example.app --dir fastlane/metadata/android
```

### Import with options
```bash
gpd migrate fastlane import --package com.example.app --dir fastlane/metadata/android --replace-images
gpd migrate fastlane import --package com.example.app --dir fastlane/metadata/android --skip-images --dry-run
```

## Multi-language workflow

1. Export localizations:
```bash
gpd migrate fastlane export --package com.example.app --output fastlane/metadata/android
```

2. Translate files in `fastlane/metadata/android`.

3. Import all at once:
```bash
gpd migrate fastlane import --package com.example.app --dir fastlane/metadata/android
```

## Notes
- Use `gpd migrate fastlane validate` before import to catch missing fields.
- Use `--dry-run` when available before overwriting assets.
