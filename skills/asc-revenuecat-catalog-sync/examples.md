# Examples: asc RevenueCat catalog sync

Use these examples as execution templates for realistic catalog synchronization workflows.

## Example 1: Drift audit only (read-only)

Goal: compare ASC and RevenueCat, produce a no-write reconciliation report.

### User request
`Audit my ASC subscriptions and IAP catalog against RevenueCat and show what is missing on either side.`

### Expected behavior
1. Read ASC:
   - `asc subscriptions groups list --app "APP_ID" --paginate --output json`
   - `asc iap list --app "APP_ID" --paginate --output json`
   - `asc subscriptions list --group "GROUP_ID" --paginate --output json` (for each group)
2. Read RevenueCat via MCP:
   - list apps/products/entitlements/offerings/packages for `project_id`
3. Build and present a diff:
   - missing in ASC
   - missing in RevenueCat
   - type mismatch
   - app/platform mismatch
4. Stop for confirmation (no writes).

## Example 2: Create missing ASC subscriptions, then map to RevenueCat

Goal: bootstrap both systems when store products are partially missing.

### User request
`Ensure monthly and annual subscriptions exist in ASC for app APP_ID, then sync them to RevenueCat project PROJECT_ID under my iOS app.`

### Expected behavior
1. Audit existing resources first.
2. If missing in ASC:
   - create group:
     - `asc subscriptions groups create --app "APP_ID" --reference-name "Premium"`
   - create subscriptions:
     - `asc subscriptions create --group "GROUP_ID" --ref-name "Monthly" --product-id "com.example.premium.monthly" --subscription-period ONE_MONTH`
     - `asc subscriptions create --group "GROUP_ID" --ref-name "Annual" --product-id "com.example.premium.annual" --subscription-period ONE_YEAR`
3. Re-read ASC to capture authoritative IDs.
4. In RevenueCat:
   - create app if missing (`type: app_store`, same bundle identifier)
   - create products with matching `store_identifier`
   - create entitlement (for example `premium`) and attach products
   - optionally create `default` offering with `$rc_monthly` and `$rc_annual`
5. Verify with final summary and failures list.

## Example 3: Sync one-time IAP and keep consumables entitlement-free

Goal: model recommended entitlement behavior by product type.

### User request
`Sync my non-consumable lifetime IAP and consumable coin pack to RevenueCat.`

### Expected behavior
1. Confirm product type mapping:
   - `NON_CONSUMABLE` -> `non_consumable`
   - `CONSUMABLE` -> `consumable`
2. Create missing ASC IAPs if requested:
   - `asc iap create --app "APP_ID" --type NON_CONSUMABLE --ref-name "Lifetime" --product-id "com.example.lifetime"`
   - `asc iap create --app "APP_ID" --type CONSUMABLE --ref-name "Coins 100" --product-id "com.example.coins.100"`
3. In RevenueCat:
   - create both products
   - attach **non-consumable** product to an entitlement (for example `lifetime_access`)
   - skip entitlement attachment for consumable by default (unless user explicitly asks)
4. Return created/skipped/failed counts.

## Example 4: Controlled apply in CI-style automation

Goal: make apply mode safe and repeatable in team workflows.

### User request
`Run a full sync and apply missing resources.`

### Expected behavior
1. Run audit and print plan.
2. Request explicit approval.
3. Apply in deterministic order:
   - ASC group/subscription/IAP
   - RC app/product
   - RC entitlement + attachments
   - RC offering/package + attachments
4. Continue after item failures and aggregate errors.
5. Print machine-readable summary plus human-readable recap.

## Suggested natural-language prompts for MCP

- `List all apps in RevenueCat project PROJECT_ID and show which one matches bundle id com.example.app`
- `Create RevenueCat product com.example.premium.monthly as subscription in app APP_ID`
- `Create entitlement premium and attach product PRODUCT_ID`
- `Create offering default with packages $rc_monthly and $rc_annual`
- `Show complete offering configuration including packages and attached products`
