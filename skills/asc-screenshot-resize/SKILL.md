---
name: asc-screenshot-resize
description: Resize App Store screenshots to required dimensions for all device classes using sips. Use when preparing screenshots for App Store Connect submission.
---

# asc screenshot resize

Use this skill to resize screenshots to the exact pixel dimensions required by App Store Connect. Uses the built-in macOS `sips` tool — no third-party dependencies needed.

## Required Dimensions

### iPhone

| Display Size | Portrait | Landscape |
|---|---|---|
| 6.9" (iPhone 16 Pro Max) | 1320 × 2868 | 2868 × 1320 |
| 6.7" (iPhone 15 Plus, 14 Pro Max) | 1290 × 2796 | 2796 × 1290 |
| 6.5" (iPhone 14 Plus, 11 Pro Max) | 1284 × 2778 | 2778 × 1284 |
| 6.5" (iPhone 11 Pro Max, XS Max) | 1242 × 2688 | 2688 × 1242 |
| 5.5" (iPhone 8 Plus) | 1242 × 2208 | 2208 × 1242 |

### iPad

| Display Size | Portrait | Landscape |
|---|---|---|
| 13" (iPad Pro M4) | 2064 × 2752 | 2752 × 2064 |
| 12.9" (iPad Pro 6th gen) | 2048 × 2732 | 2732 × 2048 |
| 11" (iPad Pro M4) | 1668 × 2388 | 2388 × 1668 |

### Apple Watch

| Display Size | Dimensions |
|---|---|
| Ultra 2 (49mm) | 410 × 502 |
| Series 10 (46mm) | 416 × 496 |
| Series 10 (42mm) | 374 × 446 |

### Mac

| Dimensions |
|---|
| 1280 × 800 |
| 1440 × 900 |
| 2560 × 1600 |
| 2880 × 1800 |

### Apple TV

| Dimensions |
|---|
| 1920 × 1080 |
| 3840 × 2160 |

## Workflow

### 1. Check current dimensions

```bash
sips -g pixelWidth -g pixelHeight screenshot.png
```

### 2. Resize a single screenshot

```bash
# Portrait iPhone 6.5" (1284 × 2778)
sips -z 2778 1284 input.png --out output.png
```

**Note:** `sips -z` takes height first, then width: `sips -z <height> <width>`.

### 3. Batch resize all screenshots in a directory

```bash
mkdir -p resized
for f in *.png; do
  sips -z 2778 1284 "$f" --out "resized/$f"
done
```

### 4. Generate multiple device sizes from one source

```bash
mkdir -p appstore-screenshots
sips -z 2868 1320 input.png --out appstore-screenshots/6.9-inch.png
sips -z 2796 1290 input.png --out appstore-screenshots/6.7-inch.png
sips -z 2778 1284 input.png --out appstore-screenshots/6.5-inch.png
sips -z 2688 1242 input.png --out appstore-screenshots/6.5-inch-legacy.png
sips -z 2208 1242 input.png --out appstore-screenshots/5.5-inch.png
```

### 5. Verify output

```bash
sips -g pixelWidth -g pixelHeight resized/*.png
```

## Handling Unicode Filenames

macOS screenshots often contain hidden Unicode characters (e.g., `U+202F` narrow no-break space) that cause tools to fail with "not a valid file". Fix with:

```bash
python3 -c "
import os
for f in os.listdir('.'):
    clean = f.replace('\u202f', ' ')
    if f != clean:
        os.rename(f, clean)
        print(f'Renamed: {clean}')
"
```

## Guardrails

- `sips` stretches images to fit exact dimensions. For best results, use source screenshots captured at or near the target aspect ratio.
- Always output to a separate file or directory (`--out`) to preserve originals.
- App Store Connect requires PNG or JPEG format. `sips` preserves the input format by default.
- Screenshots must not include alpha transparency for the App Store. If needed, flatten with: `sips -s format png --setProperty formatOptions 100 input.png --out output.png`.
