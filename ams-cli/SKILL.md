---
name: ams-cli
description: Interact with Apple Map Server APIs using the ams CLI. Use for geocoding, reverse geocoding, token exchange, or when the user mentions Apple Map Server, Maps Token, or ams.
---

# Apple Map Server CLI

Interact with Apple Map Server APIs using the `ams` command-line tool.

## Prerequisites

```bash
ams version
ams ping
```

Environment variables:

- `AMS_MAPS_TOKEN` (required)
- `AMS_BASE_URL` (optional)
- `AMS_DEBUG=1` (optional)

## Authentication

```bash
ams auth token
ams auth token --raw
ams auth token --json
```

When `AMS_MAPS_TOKEN` expires, generate a new Maps Token in the Apple Developer portal and update the environment variable.

## Geocoding

```bash
ams geocode "1 Infinite Loop, Cupertino, CA"
ams geocode --json "1 Infinite Loop, Cupertino, CA"
ams geocode --limit 3 "1 Infinite Loop, Cupertino, CA"
```

## Reverse Geocoding

```bash
ams reverse 37.3317,-122.0301
ams reverse 37.3317,-122.0301 --limit 3
ams reverse 37.3317,-122.0301 --json
```

## Batch Geocode

```bash
ams geocode --file queries.txt --limit 3
ams geocode --file queries.txt --json
ams geocode --file queries.txt --concurrency 8
```

When `--file` is used with `--json`, output is JSONL (one object per input line).

## Exit Codes

- `0` success
- `1` runtime or API error
- `2` usage error

## Agent Best Practices

1. **Always set `AMS_MAPS_TOKEN`** and rotate it when expired.
2. **Use `--json`** for machine-readable geocode results.
3. **Use `--limit` and `--concurrency`** to control batch load.
4. **Use `AMS_BASE_URL`** when targeting non-default endpoints.
5. **Enable `AMS_DEBUG=1`** when diagnosing auth or token issues.
