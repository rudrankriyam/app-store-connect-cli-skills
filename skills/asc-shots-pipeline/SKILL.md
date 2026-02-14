---
name: asc-shots-pipeline
description: Orchestrate iOS screenshot automation with xcodebuild/simctl for build-run, AXe for UI actions, JSON settings and plan files, Go-based framing (`asc shots frame`), and asc asset upload. Use when users ask for automated screenshot capture, AXe-driven simulator flows, frame composition, or screenshot to upload pipelines.
---

# ASC shots pipeline (xcodebuild -> AXe -> frame -> asc)

Use this skill for agent-driven screenshot workflows where the app is built and launched with Xcode CLI tools, UI is driven with AXe, and screenshots are uploaded with `asc`.

## Current scope
- Implemented now: build/run, AXe plan capture, frame composition, and upload.
- Device discovery is built-in via `asc shots frames list-devices`.

## Defaults
- Settings file: `.asc/shots.settings.json`
- Capture plan: `.asc/screenshots.json`
- Raw screenshots dir: `./screenshots/raw`
- Framed screenshots dir: `./screenshots/framed`
- Default frame device: `iphone-air`

## 1) Create settings JSON first

Create or update `.asc/shots.settings.json`:

```json
{
  "version": 1,
  "app": {
    "bundle_id": "com.example.app",
    "project": "MyApp.xcodeproj",
    "scheme": "MyApp",
    "simulator_udid": "booted"
  },
  "paths": {
    "plan": ".asc/screenshots.json",
    "raw_dir": "./screenshots/raw",
    "framed_dir": "./screenshots/framed"
  },
  "pipeline": {
    "frame_enabled": true,
    "upload_enabled": false
  },
  "upload": {
    "version_localization_id": "",
    "device_type": "IPHONE_65",
    "source_dir": "./screenshots/framed"
  }
}
```

If you intentionally skip framing, set:
- `"frame_enabled": false`
- `"upload.source_dir": "./screenshots/raw"`

## 2) Build and run app on simulator

Use Xcode CLI for build/install/launch:

```bash
xcrun simctl boot "$UDID" || true

xcodebuild \
  -project "MyApp.xcodeproj" \
  -scheme "MyApp" \
  -configuration Debug \
  -destination "platform=iOS Simulator,id=$UDID" \
  -derivedDataPath ".build/DerivedData" \
  build

xcrun simctl install "$UDID" ".build/DerivedData/Build/Products/Debug-iphonesimulator/MyApp.app"
xcrun simctl launch "$UDID" "com.example.app"
```

Use `xcodebuild -showBuildSettings` if the app bundle path differs from the default location.

## 3) Capture screenshots with AXe (or `asc shots run`)

Prefer plan-driven capture:

```bash
asc shots run --plan ".asc/screenshots.json" --udid "$UDID" --output json
```

Useful AXe primitives during plan authoring:

```bash
axe describe-ui --udid "$UDID"
axe tap --id "search_field" --udid "$UDID"
axe type "wwdc" --udid "$UDID"
axe screenshot --output "./screenshots/raw/home.png" --udid "$UDID"
```

Minimal `.asc/screenshots.json` example:

```json
{
  "version": 1,
  "app": {
    "bundle_id": "com.example.app",
    "udid": "booted",
    "output_dir": "./screenshots/raw"
  },
  "steps": [
    { "action": "launch" },
    { "action": "wait", "duration_ms": 800 },
    { "action": "screenshot", "name": "home" }
  ]
}
```

## 4) Frame screenshots with `asc shots frame`

List supported frame device values first:

```bash
asc shots frames list-devices --output json
```

Frame one screenshot (defaults to `iphone-air`):

```bash
asc shots frame \
  --input "./screenshots/raw/home.png" \
  --output-dir "./screenshots/framed" \
  --device "iphone-air" \
  --output json
```

Supported `--device` values:
- `iphone-air` (default)
- `iphone-17-pro`
- `iphone-17-pro-max`
- `iphone-16e`
- `iphone-17`

## 5) Upload screenshots with asc

Upload from the configured source directory (default `./screenshots/framed` when framing is enabled):

```bash
asc assets screenshots upload \
  --version-localization "LOC_ID" \
  --path "./screenshots/framed" \
  --device-type "IPHONE_65" \
  --output json
```

List or validate before upload when needed:

```bash
asc assets screenshots sizes --output table
asc assets screenshots list --version-localization "LOC_ID" --output table
```

## Agent behavior
- Always confirm exact flags with `--help` before running commands.
- Keep outputs deterministic: default to JSON for machine steps.
- Prefer `asc shots frames list-devices --output json` before selecting a frame device.
- Ensure screenshot files exist before upload.
- Use explicit long flags (`--app`, `--output`, `--version-localization`, etc.).

## 6) Multi-locale capture (optional)

To capture screenshots in multiple App Store locales, pass localization launch arguments to `xcrun simctl launch`:

```bash
# Define target locales
LOCALES=("en-US" "de-DE" "fr-FR" "es-ES" "ja-JP" "ko-KR" "zh-Hans" "zh-Hant")

for LOCALE in "${LOCALES[@]}"; do
  echo "Capturing $LOCALE..."

  # Boot simulator for this locale (format: "iPhone 16 Pro (en-US)")
  xcrun simctl boot "iPhone 16 Pro ($LOCALE)" || true

  # Launch app with specific locale
  xcrun simctl launch booted com.example.app -AppleLanguages "($LOCALE)"

  # Capture screenshot
  asc screenshots capture \
    --bundle-id "com.example.app" \
    --name "home" \
    --output-dir "./screenshots/raw/$LOCALE" \
    --output json
done
```

Key `simctl launch` localization arguments:
- `-AppleLanguages "(LOCALE)"` - Sets the app's preferred language list
- `-AppleLocale "LOCALE"` - Sets the locale (affects dates/currency)

## 7) Parallel execution for speed

To capture multiple locales simultaneously, run captures in background processes:

```bash
#!/bin/bash
# parallel-capture.sh

LOCALES=("en-US" "de-DE" "fr-FR" "ja-JP")
DEVICE="iphone-air"

capture_locale() {
  LOCALE=$1
  echo "Starting capture for $LOCALE"

  xcrun simctl boot "iPhone 16 Pro ($LOCALE)" || true
  xcrun simctl launch booted com.example.app -AppleLanguages "($LOCALE)"

  asc screenshots capture \
    --bundle-id "com.example.app" \
    --name "home" \
    --output-dir "./screenshots/raw/$LOCALE"

  echo "Completed $LOCALE"
}

# Launch all captures in parallel
for LOCALE in "${LOCALES[@]}"; do
  capture_locale "$LOCALE" &
done

# Wait for all to complete
wait

echo "All captures done. Now framing..."

# Frame all screenshots (can also run in parallel)
for LOCALE in "${LOCALES[@]}"; do
  asc screenshots frame \
    --input "./screenshots/raw/$LOCALE/home.png" \
    --device "$DEVICE" \
    --output "./screenshots/framed/$LOCALE/home.png"
done
```

Or use `xargs` for parallel execution:

```bash
echo -e "en-US\nde-DE\nfr-FR\nja-JP" | xargs -P 4 -I {} bash -c '
  LOCALE={}
  xcrun simctl boot "iPhone 16 Pro ($LOCALE)"
  xcrun simctl launch booted com.example.app -AppleLanguages "($LOCALE)"
  asc screenshots capture --bundle-id "com.example.app" --name "home" --output-dir "./screenshots/raw/$LOCALE"
'
```

## 8) Full multi-locale pipeline example

```bash
#!/bin/bash
# full-pipeline-multi-locale.sh

LOCALES=("en-US" "de-DE" "fr-FR" "es-ES" "ja-JP")
DEVICE="iphone-air"
RAW_DIR="./screenshots/raw"
FRAMED_DIR="./screenshots/framed"

# Step 1: Parallel capture
for LOCALE in "${LOCALES[@]}"; do
  (
    xcrun simctl boot "iPhone 16 Pro ($LOCALE)" || true
    xcrun simctl launch booted com.example.app -AppleLanguages "($LOCALE)"
    asc screenshots capture \
      --bundle-id "com.example.app" \
      --name "home" \
      --output-dir "$RAW_DIR/$LOCALE" \
      --output json
    echo "Captured $LOCALE"
  ) &
done
wait

# Step 2: Parallel framing
for LOCALE in "${LOCALES[@]}"; do
  (
    asc screenshots frame \
      --input "$RAW_DIR/$LOCALE/home.png" \
      --device "$DEVICE" \
      --output "$FRAMED_DIR/$LOCALE/home.png" \
      --output json
    echo "Framed $LOCALE"
  ) &
done
wait

# Step 3: Generate review (single run, aggregates all locales)
asc screenshots review-generate \
  --framed-dir "$FRAMED_DIR" \
  --output-dir "./screenshots/review"

# Step 4: Upload (run per locale if needed)
for LOCALE in "${LOCALES[@]}"; do
  asc assets screenshots upload \
    --version-localization "LOC_ID_FOR_$LOCALE" \
    --path "$FRAMED_DIR/$LOCALE" \
    --device-type "IPHONE_65" \
    --output json
done
```
