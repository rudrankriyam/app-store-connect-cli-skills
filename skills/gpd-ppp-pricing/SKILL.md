---
name: gpd-ppp-pricing
description: Set region-specific pricing for Google Play subscriptions and products using gpd monetization commands. Use when adjusting prices by territory or PPP strategy.
---

# PPP Pricing (Per-Region Pricing)

Use this skill to set different prices per region for subscriptions and one-time products.

## Preconditions
- Ensure credentials are set (`GPD_SERVICE_ACCOUNT_KEY`).
- Use `--package` explicitly.
- Know target region codes and price micros.

## Subscription base plan pricing

### Migrate prices for a base plan
```bash
gpd monetization baseplans migrate-prices --package com.example.app sub123 plan456 --region-code US --price-micros 9990000
```

### Batch migrate prices
```bash
gpd monetization baseplans batch-migrate-prices --package com.example.app sub123 --file migrate.json
```

Example `migrate.json`:
```json
{
  "requests": [
    {
      "basePlanId": "plan456",
      "regionalPriceMigrations": [
        {
          "regionCode": "US",
          "priceMicros": 9990000
        }
      ]
    }
  ],
  "regionsVersion": {
    "version": "2024-01-01"
  }
}
```

## One-time products pricing

```bash
gpd monetization onetimeproducts create --package com.example.app --product-id sku123 --type consumable
gpd monetization onetimeproducts update --package com.example.app sku123 --default-price 1990000
```

## Offers and regional variants

```bash
gpd monetization offers list --package com.example.app sub123 plan456
gpd monetization offers create --package com.example.app sub123 plan456 --offer-id offer789 --file offer.json
gpd monetization offers batchUpdate --package com.example.app sub123 plan456 --file offers.json
```

## Verify current pricing

```bash
gpd monetization subscriptions get sub123 --package com.example.app
gpd monetization baseplans batch-update-states --package com.example.app sub123 --file states.json
```

## Notes
- Use `priceMicros` values to avoid rounding errors.
- Keep region codes consistent (for example: `US`, `GB`, `IN`, `BR`).
- Use batch files for large region sets to avoid partial updates.
