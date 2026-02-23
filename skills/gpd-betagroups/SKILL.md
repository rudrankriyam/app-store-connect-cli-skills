---
name: gpd-betagroups
description: Orchestrate Google Play beta testing groups and distribution using gpd. Use when managing testers, internal testing, or beta rollouts.
---

# GPD Beta Groups

Use this skill when managing beta testers, groups, and build distribution on Google Play.

## List and manage testers
```bash
gpd publish testers list --package com.example.app --track internal
gpd publish testers list --package com.example.app --track beta
gpd publish testers add --package com.example.app --track internal --group testers@example.com
```

## Distribute builds to testing tracks
```bash
gpd publish release --package com.example.app --track internal --status completed
gpd publish release --package com.example.app --track beta --status completed
```

## Promote between testing tracks
```bash
gpd publish promote --package com.example.app --from-track internal --to-track beta
gpd publish promote --package com.example.app --from-track beta --to-track production
```

## Notes
- Use `--track internal` for fast internal distribution.
- Prefer IDs for deterministic operations; use the ID resolver skill when needed.
