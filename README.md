# Agent Skills

Reusable capabilities for AI coding agents.

## Available Skills

| Skill | Description |
|-------|-------------|
| [gdrive-cli](./gdrive-cli/) | Manage Google Drive files, folders, Sheets, Docs, and Slides |
| [gpd-cli](./gpd-cli/) | Manage Google Play Developer Console for Android app publishing |

## Installation

```bash
npx skills add dl-alexandre/Skills
```

Or install a specific skill:

```bash
npx skills add dl-alexandre/Skills --skill gdrive-cli
npx skills add dl-alexandre/Skills --skill gpd-cli
```

## Requirements

- [gdrive CLI](https://github.com/dl-alexandre/Google-Drive-CLI) - for gdrive-cli skill
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
