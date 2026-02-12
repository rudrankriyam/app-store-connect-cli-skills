---
name: gpd-build-lifecycle
description: Track build processing, status, and retention for Google Play using gpd publish commands. Use when waiting on processing or managing releases.
---

# GPD Build Lifecycle

Use this skill to manage build state, processing, and retention.

## Upload and validate
```bash
gpd publish upload app.aab --package com.example.app
```

## Inspect release status
```bash
gpd publish status --package com.example.app --track internal
gpd publish status --package com.example.app --track production
```

## Recent tracks and releases
```bash
gpd publish tracks --package com.example.app
```

## Internal app sharing
Use for fast distribution of a build without a full track release.

```bash
gpd publish internal-share upload app.aab --package com.example.app
```

## Cleanup and rollback
```bash
gpd publish halt --package com.example.app --track production --confirm
gpd publish rollback --package com.example.app --track production --confirm
```

## Notes
- Prefer `gpd publish release` for end-to-end flow instead of manual steps.
- Use a new version code for each uploaded build.
