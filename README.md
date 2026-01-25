# Agent Skills

Reusable capabilities for AI coding agents.

## Available Skills

| Skill | Description |
|-------|-------------|
| [gdrv-cli](./gdrv-cli/) | Manage Google Drive files, folders, Sheets, Docs, and Slides |
| [gpd-cli](./gpd-cli/) | Manage Google Play Developer Console for Android app publishing |

## Installation

```bash
npx skills add dl-alexandre/Skills
```

Or install a specific skill:

```bash
npx skills add dl-alexandre/Skills --skill gdrv-cli
npx skills add dl-alexandre/Skills --skill gpd-cli
```

## Requirements

- [gdrv CLI](https://github.com/dl-alexandre/Google-Drive-CLI) - for gdrv-cli skill
- [gpd CLI](https://github.com/dl-alexandre/Google-Play-Developer-CLI) - for gpd-cli skill

## Compatible Agents

- Claude Code
- Cursor
- Codex
- Cline
- Windsurf
- GitHub Copilot

## License

MIT
