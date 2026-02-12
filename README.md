# Agent Skills

Reusable capabilities for AI coding agents.

## Available Skills

| Skill | Description |
|-------|-------------|
| [gdrv-cli](./gdrv-cli/) | Manage Google Drive files, folders, Sheets, Docs, and Slides |
| [gpd-cli](./gpd-cli/) | Manage Google Play Developer Console for Android app publishing |
| [gpd-cli-usage](./gpd-cli-usage/) | Usage guidance for gpd commands (flags, output, auth) |
| [gpd-release-flow](./gpd-release-flow/) | End-to-end Google Play release workflows |
| [gpd-submission-health](./gpd-submission-health/) | Preflight and validate Play submissions |
| [gpd-metadata-sync](./gpd-metadata-sync/) | Sync store listings, assets, and Fastlane metadata |
| [gpd-ppp-pricing](./gpd-ppp-pricing/) | Region-specific pricing workflows |
| [gpd-build-lifecycle](./gpd-build-lifecycle/) | Track build processing and release state |
| [gpd-betagroups](./gpd-betagroups/) | Manage beta testing groups and distribution |
| [gpd-id-resolver](./gpd-id-resolver/) | Resolve Play identifiers and IDs |
| [ask-cli](./ask-cli/) | Manage App Store Server API and External Purchase Server API workflows |
| [ams-cli](./ams-cli/) | Interact with Apple Map Server APIs for geocoding and reverse geocoding |

## Installation

```bash
npx skills add dl-alexandre/Skills
```

Or install a specific skill:

```bash
npx skills add dl-alexandre/Skills --skill gdrv-cli
npx skills add dl-alexandre/Skills --skill gpd-cli
npx skills add dl-alexandre/Skills --skill gpd-release-flow
npx skills add dl-alexandre/Skills --skill gpd-metadata-sync
npx skills add dl-alexandre/Skills --skill gpd-betagroups
npx skills add dl-alexandre/Skills --skill ask-cli
npx skills add dl-alexandre/Skills --skill ams-cli
```

## Requirements

- [gdrv CLI](https://github.com/dl-alexandre/Google-Drive-CLI) - for gdrv-cli skill
- [gpd CLI](https://github.com/dl-alexandre/Google-Play-Developer-CLI) - for gpd-* skills
- [ask CLI](https://github.com/dl-alexandre/App-StoreKit-CLI) - for ask-cli skill
- [ams CLI](https://github.com/dl-alexandre/Apple-Map-Server-CLI) - for ams-cli skill

## GPD Quickstart

```bash
# Auth check
gpd auth check --package com.example.app

# Upload and release to internal
gpd publish upload app.aab --package com.example.app
gpd publish release --package com.example.app --track internal --status completed

# Promote to beta
gpd publish promote --package com.example.app --from-track internal --to-track beta

# Staged rollout to production
gpd publish release --package com.example.app --track production --status inProgress --version-code 123
gpd publish rollout --package com.example.app --track production --percentage 10
gpd publish rollout --package com.example.app --track production --percentage 100
```

## Compatible Agents

- Claude Code
- Cursor
- Codex
- Cline
- Windsurf
- GitHub Copilot

## License

MIT
