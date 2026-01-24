---
name: gpd-cli
description: Manage Google Play Developer Console using the gpd CLI. Use when working with Android app publishing, Play Store releases, app reviews, Android vitals, in-app purchases, subscriptions, or when the user mentions Google Play, Play Store, Android publishing, or gpd.
---

# Google Play Developer CLI

Manage Google Play Developer Console using the `gpd` command-line tool.

## Prerequisites

```bash
gpd --version

export GPD_SERVICE_ACCOUNT_KEY='{"type": "service_account", ...}'
gpd auth status
gpd auth check --package com.example.app
```

## Publishing

### Upload & Release

```bash
gpd publish upload app.aab --package com.example.app
gpd publish release --package com.example.app --track internal --status draft
gpd publish release --package com.example.app --track production --status inProgress --version-code 123
gpd publish status --package com.example.app --track production
gpd publish tracks --package com.example.app
```

### Rollouts

```bash
gpd publish rollout --package com.example.app --track production --percentage 10
gpd publish promote --package com.example.app --from-track beta --to-track production
gpd publish halt --package com.example.app --track production --confirm
gpd publish rollback --package com.example.app --track production --confirm
```

### Edit Lifecycle

```bash
gpd publish edit create --package com.example.app
gpd publish edit list --package com.example.app
gpd publish edit validate EDIT_ID --package com.example.app
gpd publish edit commit EDIT_ID --package com.example.app
gpd publish edit delete EDIT_ID --package com.example.app
gpd publish upload app.aab --package com.example.app --edit-id EDIT_ID --no-auto-commit
```

### Store Listing

```bash
gpd publish listing get --package com.example.app
gpd publish listing update --package com.example.app --locale en-US --title "My App"
gpd publish details get --package com.example.app
gpd publish details update --package com.example.app --contact-email support@example.com
```

### Images

```bash
gpd publish images list phoneScreenshots --package com.example.app --locale en-US
gpd publish images upload icon icon.png --package com.example.app --locale en-US
gpd publish images delete phoneScreenshots IMAGE_ID --package com.example.app --locale en-US
```

### Testers

```bash
gpd publish testers list --package com.example.app --track internal
gpd publish testers add --package com.example.app --track internal --group testers@example.com
```

## Reviews

```bash
gpd reviews list --package com.example.app --min-rating 1 --max-rating 3
gpd reviews list --package com.example.app --include-review-text --scan-limit 200
gpd reviews reply --package com.example.app --review-id REVIEW_ID --text "Thank you!"
```

## Android Vitals

```bash
gpd vitals crashes --package com.example.app --start-date 2024-01-01 --end-date 2024-01-31
gpd vitals anrs --package com.example.app --start-date 2024-01-01 --end-date 2024-01-31
gpd vitals excessive-wakeups --package com.example.app --start-date 2024-01-01 --end-date 2024-01-31
gpd vitals slow-rendering --package com.example.app --start-date 2024-01-01 --end-date 2024-01-31
gpd vitals slow-start --package com.example.app --start-date 2024-01-01 --end-date 2024-01-31
gpd vitals errors issues search --package com.example.app --query "NullPointerException" --interval last30Days
gpd vitals anomalies list --package com.example.app --metric crashRate --time-period last30Days
```

## Monetization

### Products

```bash
gpd monetization products list --package com.example.app
gpd monetization products get sku123 --package com.example.app
gpd monetization products create --package com.example.app --product-id sku123 --type managed --default-price 990000
gpd monetization products update --package com.example.app sku123 --status inactive
gpd monetization products delete --package com.example.app sku123
```

### Subscriptions

```bash
gpd monetization subscriptions list --package com.example.app
gpd monetization subscriptions get sub123 --package com.example.app
gpd monetization subscriptions create --package com.example.app --product-id sub123 --file subscription.json
gpd monetization subscriptions archive --package com.example.app sub123
gpd monetization subscriptions batchGet --package com.example.app --ids sub1,sub2,sub3
```

### Base Plans & Offers

```bash
gpd monetization baseplans activate --package com.example.app sub123 plan456
gpd monetization baseplans deactivate --package com.example.app sub123 plan456
gpd monetization offers list --package com.example.app sub123 plan456
gpd monetization offers activate --package com.example.app sub123 plan456 offer789
```

## Purchases

```bash
gpd purchases verify --package com.example.app --token TOKEN --product-id sku123
gpd purchases voided list --package com.example.app --start-time 2024-01-01T00:00:00Z --type product
gpd purchases products acknowledge --package com.example.app --product-id sku123 --token TOKEN
gpd purchases products consume --package com.example.app --product-id sku123 --token TOKEN
gpd purchases subscriptions cancel --package com.example.app --subscription-id sub123 --token TOKEN
gpd purchases subscriptions refund --package com.example.app --subscription-id sub123 --token TOKEN
```

## Permissions

```bash
gpd permissions users list --developer-id DEV_ID
gpd permissions users create --developer-id DEV_ID --email user@example.com --developer-permissions CAN_VIEW_FINANCIAL_DATA_GLOBAL
gpd permissions grants create --package com.example.app --email user@example.com --app-permissions CAN_REPLY_TO_REVIEWS
```

## Analytics

```bash
gpd analytics query --package com.example.app --start-date 2024-01-01 --end-date 2024-01-31
```

## Agent Best Practices

1. **JSON output by default** - all commands output minified JSON
2. **Use `--pretty`** for readable JSON during debugging
3. **Use `--dry-run`** before destructive operations
4. **Check exit codes**: 0=success, 2=auth failure, 3=permission denied, 4=validation error, 5=rate limited, 7=not found
5. **Use edit lifecycle** for complex multi-step publishing with `--edit-id` and `--no-auto-commit`

## Common Workflows

### Deploy to Internal Track

```bash
gpd publish upload app.aab --package com.example.app
gpd publish release --package com.example.app --track internal --status completed
```

### Staged Rollout to Production

```bash
gpd publish release --package com.example.app --track production --status inProgress --version-code 123
gpd publish rollout --package com.example.app --track production --percentage 5
gpd publish rollout --package com.example.app --track production --percentage 50
gpd publish rollout --package com.example.app --track production --percentage 100
```

### Monitor App Health

```bash
gpd vitals crashes --package com.example.app --start-date 2024-01-01 --end-date 2024-01-31
gpd reviews list --package com.example.app --min-rating 1 --max-rating 2
```
