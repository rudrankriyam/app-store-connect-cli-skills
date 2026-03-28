---
name: asc-screenshot-resize
description: Resize and validate App Store screenshots for all device classes using macOS sips. Use when preparing or fixing screenshots for App Store Connect submission.
---

# asc screenshot resize

Use this skill to resize screenshots to the exact pixel dimensions required by App Store Connect and validate they pass upload requirements. Uses the built-in macOS `sips` tool — no third-party dependencies needed.

## Required Dimensions

### iPhone

| Display Size | Accepted Dimensions (portrait × landscape) |
|---|---|
| 6.9" | 1260 × 2736, 2736 × 1260, 1320 × 2868, 2868 × 1320, 1290 × 2796, 2796 × 1290 |
| 6.5" | 1242 × 2688, 2688 × 1242, 1284 × 2778, 2778 × 1284 |
| 6.3" | 1206 × 2622, 2622 × 1206, 1179 × 2556, 2556 × 1179 |
| 6.1" | 1125 × 2436, 2436 × 1125, 1080 × 2340, 2340 × 1080, 1170 × 2532, 2532 × 1170 |
| 5.5" | 1242 × 2208, 2208 × 1242 |
| 4.7" | 750 × 1334, 1334 × 750 |
| 4" | 640 × 1096, 640 × 1136, 1136 × 600, 1136 × 640 |
| 3.5" | 640 × 920, 640 × 960, 960 × 600, 960 × 640 |

**Note:** 6.9" accepts screenshots from 6.5", 6.7", and 6.9" devices. 6.3" accepts from 6.1" and 6.3". 6.1" accepts from 5.4", 5.8", and 6.1".

### iPad

| Display Size | Accepted Dimensions |
|---|---|
| 13" | 2064 × 2752, 2752 × 2064, 2048 × 2732, 2732 × 2048 |
| 11" | 1668 × 2420, 2420 × 1668, 1668 × 2388, 2388 × 1668, 1640 × 2360, 2360 × 1640, 1488 × 2266, 2266 × 1488 |
| iPad Pro 2nd gen 12.9" | 2048 × 2732, 2732 × 2048 |
| 10.5" | 1668 × 2224, 2224 × 1668 |
| 9.7" | 1536 × 2008, 1536 × 2048, 2048 × 1496, 2048 × 1536, 768 × 1004, 768 × 1024, 1024 × 748, 1024 × 768 |

### Apple Watch

| Device | Dimensions |
|---|---|
| Ultra 3 (49mm) | 422 × 514, 410 × 502 |
| Series 11 (46mm) | 416 × 496 |
| Series 9 (45mm) | 396 × 484 |
| Series 6 (44mm) | 368 × 448 |
| Series 3 (42mm) | 312 × 390 |

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

### 1. Fix Unicode filenames

macOS screenshots often contain hidden Unicode characters (e.g., `U+202F` narrow no-break space) that cause `sips` and other tools to fail with "not a valid file". Always sanitize first:

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

### 2. Check current dimensions

```bash
sips -g pixelWidth -g pixelHeight screenshot.png
```

### 3. Validate App Store readiness

Check for alpha channel and color space issues before uploading:

```bash
sips -g hasAlpha -g space screenshot.png
```

App Store Connect rejects screenshots with alpha transparency. Remove it by round-tripping through JPEG:

```bash
sips -s format jpeg input.png --out /tmp/temp.jpg
sips -s format png /tmp/temp.jpg --out output.png
rm /tmp/temp.jpg
```

Batch-strip alpha from all PNGs in a directory:

```bash
for f in *.png; do
  if sips -g hasAlpha "$f" | grep -q "yes"; then
    sips -s format jpeg "$f" --out /tmp/temp.jpg
    sips -s format png /tmp/temp.jpg --out "$f"
    rm /tmp/temp.jpg
    echo "Stripped alpha: $f"
  fi
done
```

### 4. Resize a single screenshot

```bash
# Portrait iPhone 6.5" (1284 × 2778)
sips -z 2778 1284 input.png --out output.png
```

**Note:** `sips -z` takes height first, then width: `sips -z <height> <width>`.

### 5. Batch resize all screenshots in a directory

```bash
mkdir -p resized
for f in *.png; do
  sips -z 2778 1284 "$f" --out "resized/$f"
done
```

### 6. Generate multiple device sizes from one source

```bash
mkdir -p appstore-screenshots
# iPhone
sips -z 2868 1320 input.png --out appstore-screenshots/iphone-6.9.png
sips -z 2778 1284 input.png --out appstore-screenshots/iphone-6.5.png
sips -z 2622 1206 input.png --out appstore-screenshots/iphone-6.3.png
sips -z 2532 1170 input.png --out appstore-screenshots/iphone-6.1.png
sips -z 2208 1242 input.png --out appstore-screenshots/iphone-5.5.png
```

### 7. Verify output

```bash
sips -g pixelWidth -g pixelHeight -g hasAlpha resized/*.png
```

Confirm all files show the target dimensions and `hasAlpha: no`.

## Guardrails

- `sips` stretches images to fit exact dimensions. For best results, use source screenshots captured at or near the target aspect ratio.
- Always output to a separate file or directory (`--out`) to preserve originals.
- App Store Connect requires PNG or JPEG format. `sips` preserves the input format by default.
- Screenshots **must not** include alpha transparency. Always validate with `sips -g hasAlpha` before upload.
- Color space must be sRGB. If screenshots use Display P3, convert with: `sips -m "/System/Library/ColorSync/Profiles/sRGB IEC61966-2.1.icc" input.png --out output.png`.
