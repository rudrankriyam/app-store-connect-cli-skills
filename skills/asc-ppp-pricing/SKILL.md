---
name: asc-ppp-pricing
description: Set territory-specific pricing for subscriptions and in-app purchases using purchasing power parity (PPP). Use when adjusting prices by country or implementing localized pricing strategies.
---

# PPP Pricing (Per-Territory Pricing)

Use this skill to set different prices for different countries based on purchasing power parity or custom pricing strategies.

## Preconditions
- Ensure credentials are set (`asc auth login` or `ASC_*` env vars).
- Use `ASC_APP_ID` or pass `--app` explicitly.
- Know your base territory (usually USA) and base price tier.

## Workflow: Set PPP-Based Subscription Pricing

### 1. List subscriptions for your app
```bash
asc subscriptions groups list --app "APP_ID"
asc subscriptions list --group "GROUP_ID"
```

### 2. Get price points for base territory (e.g., USA at $9.99)
```bash
asc subscriptions price-points list --id "SUB_ID" --territory "USA"
```
Note the price point ID for your desired tier.

### 3. Get equalizations (equivalent prices in all territories)
```bash
asc subscriptions price-points equalizations --id "PRICE_POINT_ID" --paginate
```
This returns price points for all territories with their local currency amounts.

### 4. Find target price points for each territory
From equalizations output, identify the price point IDs that match your PPP targets:
- India: Find price point near your PPP-adjusted target (e.g., ~$3 equivalent)
- Germany: Find price point for your EU target
- Japan: Find price point for your JP target

### 5. Set prices for each territory
```bash
# Set price for India
asc subscriptions prices add --id "SUB_ID" --price-point "IND_PRICE_POINT_ID" --territory "IND"

# Set price for Germany
asc subscriptions prices add --id "SUB_ID" --price-point "DEU_PRICE_POINT_ID" --territory "DEU"

# Set price for Japan
asc subscriptions prices add --id "SUB_ID" --price-point "JPN_PRICE_POINT_ID" --territory "JPN"
```

### 6. Verify current prices
```bash
asc subscriptions prices list --id "SUB_ID"
```

## Workflow: Set PPP-Based IAP Pricing

### 1. List in-app purchases
```bash
asc iap list --app "APP_ID"
```

### 2. Get price points for base territory
```bash
asc iap price-points list --id "IAP_ID" --territory "USA"
```

### 3. Get equalizations
```bash
asc iap price-points equalizations --id "PRICE_POINT_ID" --paginate
```

### 4. Create price schedule with base territory
```bash
asc iap price-schedule create --id "IAP_ID" --base-territory "USA" --price-point "PRICE_POINT_ID"
```

### 5. View manual and automatic prices
```bash
asc iap price-schedule manual-prices --schedule-id "SCHEDULE_ID"
asc iap price-schedule automatic-prices --schedule-id "SCHEDULE_ID"
```

## Updating Existing Prices

To change a territory's price:
1. List current prices to get the price ID:
   ```bash
   asc subscriptions prices list --id "SUB_ID"
   ```
2. Delete the old price:
   ```bash
   asc subscriptions prices delete --price-id "PRICE_ID" --confirm
   ```
3. Add the new price:
   ```bash
   asc subscriptions prices add --id "SUB_ID" --price-point "NEW_PRICE_POINT_ID" --territory "TERRITORY"
   ```

## Common PPP Strategies

### BigMac Index Approach
Adjust prices based on relative purchasing power:
- USA: $9.99 (baseline)
- India: $2.99-3.99 (~70% discount)
- Brazil: $4.99-5.99 (~50% discount)
- UK: $8.99-9.99 (similar)
- Switzerland: $11.99-12.99 (premium)

### Tiered Regional Pricing
Group countries into pricing tiers:
- Tier 1 (High): USA, UK, Germany, Australia, Switzerland
- Tier 2 (Medium): France, Spain, Italy, Japan, South Korea
- Tier 3 (Low): India, Brazil, Mexico, Indonesia, Turkey

## Listing All Territories
```bash
asc pricing territories list --paginate
```

## Notes
- Price changes may take up to 24 hours to reflect in the App Store.
- Use `--start-date "YYYY-MM-DD"` to schedule future price changes.
- Always verify with `prices list` after making changes.
- Some territories may have restrictions; check App Store Connect for eligibility.
