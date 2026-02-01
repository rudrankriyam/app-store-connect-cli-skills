---
name: asc-xcode-build
description: Build, archive, and export iOS/macOS apps with xcodebuild before uploading to App Store Connect. Use when you need to create an IPA or PKG for upload.
---

# Xcode Build and Export

Use this skill when you need to build an app from source and prepare it for upload to App Store Connect.

## Preconditions
- Xcode installed and command line tools configured
- Valid signing identity and provisioning profiles
- For macOS: `ITSAppUsesNonExemptEncryption` set in Info.plist (see Encryption section)

## iOS Build Flow

### 1. Clean and Archive
```bash
xcodebuild clean archive \
  -scheme "YourScheme" \
  -configuration Release \
  -archivePath /tmp/YourApp.xcarchive \
  -destination "generic/platform=iOS"
```

### 2. Create ExportOptions.plist
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>app-store-connect</string>
    <key>signingStyle</key>
    <string>automatic</string>
    <key>teamID</key>
    <string>YOUR_TEAM_ID</string>
    <key>uploadSymbols</key>
    <true/>
</dict>
</plist>
```

### 3. Export IPA
```bash
xcodebuild -exportArchive \
  -archivePath /tmp/YourApp.xcarchive \
  -exportPath /tmp/YourAppExport \
  -exportOptionsPlist ExportOptions.plist \
  -allowProvisioningUpdates
```

### 4. Upload with asc
```bash
asc builds upload --app "APP_ID" --ipa "/tmp/YourAppExport/YourApp.ipa"
```

## macOS Build Flow

### 1. Archive
```bash
xcodebuild archive \
  -scheme "YourMacScheme" \
  -configuration Release \
  -archivePath /tmp/YourMacApp.xcarchive \
  -destination "generic/platform=macOS"
```

### 2. Export PKG
Same ExportOptions.plist as iOS, then:
```bash
xcodebuild -exportArchive \
  -archivePath /tmp/YourMacApp.xcarchive \
  -exportPath /tmp/YourMacAppExport \
  -exportOptionsPlist ExportOptions.plist \
  -allowProvisioningUpdates
```

### 3. Upload PKG
macOS apps export as `.pkg` files. Use `xcrun altool`:
```bash
xcrun altool --upload-app \
  -f "/tmp/YourMacAppExport/YourApp.pkg" \
  --type macos \
  --apiKey "$ASC_KEY_ID" \
  --apiIssuer "$ASC_ISSUER_ID"
```

Note: The API key file must be in `~/.appstoreconnect/private_keys/AuthKey_<KEY_ID>.p8`

## Encryption Declaration (Critical)

If your build has `usesNonExemptEncryption: true`, you must either:

### Option 1: Mark as Exempt (Recommended for most apps)
Add to your app's Info.plist:
```xml
<key>ITSAppUsesNonExemptEncryption</key>
<false/>
```

This is appropriate if your app only uses:
- Standard HTTPS/TLS for network communication
- Apple's built-in encryption APIs

### Option 2: Provide Export Compliance Documentation
If you use custom encryption, create and upload documentation via:
```bash
asc encryption declarations create \
  --app "APP_ID" \
  --app-description "Description of encryption usage" \
  --contains-proprietary-cryptography=true \
  --available-on-french-store=true
```

### Check Build Encryption Status
```bash
asc builds info --build "BUILD_ID"
# Look for usesNonExemptEncryption field
```

## Build Number Management

Each upload requires a unique build number. Update in Xcode project:
- `CURRENT_PROJECT_VERSION` (build number, e.g., "316")
- `MARKETING_VERSION` (version string, e.g., "2.2.0")

Or via command line:
```bash
# Update build number in project.pbxproj
# Then rebuild
```

## Troubleshooting

### "No profiles for bundle ID" during export
- Use `-allowProvisioningUpdates` flag
- Ensure `signingStyle` is `automatic` in ExportOptions.plist
- Verify your Apple ID is logged into Xcode

### Build rejected for missing icon (macOS)
macOS requires ICNS format icons with all sizes:
- 16x16, 32x32, 128x128, 256x256, 512x512 (1x and 2x)

### CFBundleVersion too low
The build number must be higher than any previously uploaded build:
```bash
# Check existing builds
asc builds list --app "APP_ID" --platform MAC_OS --limit 5
```

## Notes
- Always clean before archive for release builds
- Use `xcodebuild -showBuildSettings` to verify configuration
- For CI/CD, consider using `xcodebuild -exportArchive` with `-allowProvisioningUpdates`
