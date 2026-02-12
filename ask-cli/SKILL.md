---
name: ask-cli
description: Manage App Store Server API and External Purchase Server API using the ask CLI. Use when working with StoreKit server transactions, subscriptions, notifications, refunds, consumption data, or external purchases, or when the user mentions App Store Server API, StoreKit, or ask.
---

# App StoreKit CLI

Manage the App Store Server API and External Purchase Server API using the `ask` command-line tool.

## Prerequisites

```bash
ask --version
ask config init
ask config validate
```

Default config path:

```
~/.config/ask/config.yaml
```

## Configuration

Environment variables:

- `ASK_ISSUER_ID`
- `ASK_KEY_ID`
- `ASK_BUNDLE_ID`
- `ASK_PRIVATE_KEY_PATH`
- `ASK_PRIVATE_KEY`
- `ASK_ENV` (`sandbox`, `production`, or `local-testing`)
- `ASK_MAX_RETRIES`
- `ASK_RETRY_BACKOFF_MS`

Precedence:

1. CLI flags
2. Environment variables
3. Config file

## Transactions

```bash
ask transaction get --transaction-id <id>
ask transaction history --transaction-id <id> --version v2
ask transaction app --transaction-id <id>
ask transaction app-account-token --original-transaction-id <id> --body request.json
```

## Notifications

```bash
ask notification test
ask notification test-status --test-notification-token <token>
ask notification history --body request.json
```

## Subscriptions

```bash
ask subscription status --transaction-id <id>
ask subscription extend --original-transaction-id <id> --body request.json
ask subscription extend-mass --body request.json
ask subscription extend-status --product-id <id> --request-id <uuid>
```

## Refunds and Orders

```bash
ask refund history --transaction-id <id>
ask order lookup --order-id <id>
```

## Consumption

```bash
ask consumption send --transaction-id <id> --body request.json
```

## External Purchases

```bash
ask external send --body report.json
ask external get --request-id <uuid>
```

## Messaging

```bash
ask messaging image list
ask messaging image upload --image-id <uuid> --file image.png
ask messaging image delete --image-id <uuid>
ask messaging message list
ask messaging message upload --message-id <uuid> --body request.json
ask messaging message delete --message-id <uuid>
ask messaging default configure --product-id <id> --locale <locale> --body request.json
ask messaging default delete --product-id <id> --locale <locale>
```

## Output and Filtering

- `--format json|table|raw`
- `--jq '<expression>'`
- `--query key=value` (repeatable)
- `--table-columns col1,col2` (table output only)
- `--debug`

## Agent Best Practices

1. **Use `--format json`** for machine-readable output.
2. **Validate config** with `ask config validate` before production calls.
3. **Use `--body` with files** for POST requests; `--body -` reads from stdin.
4. **Set `ASK_ENV`** to avoid mixing sandbox and production data.
5. **Tune retries** via `ASK_MAX_RETRIES` and `ASK_RETRY_BACKOFF_MS` for flaky endpoints.
