#!/usr/bin/env python3
"""
Create a new App Store Connect app record via UI automation.

Prereqs:
  pip install playwright
  playwright install

Usage:
  python scripts/create_app_playwright.py \
    --app-name "My App" \
    --bundle-id "com.example.app" \
    --sku "com.example.app" \
    --platform IOS \
    --language "English (U.S.)" \
    --user-access full
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import time
from datetime import datetime

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ASC_APPS_URL = "https://appstoreconnect.apple.com/apps"

PLATFORM_LABELS = {
    "IOS": "iOS",
    "MAC_OS": "macOS",
    "TV_OS": "tvOS",
    "VISION_OS": "visionOS",
}

USER_ACCESS_LABELS = {
    "full": "Full Access",
    "limited": "Limited Access",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create an App Store Connect app via UI automation."
    )
    parser.add_argument("--app-name", required=True, help="App name to create")
    parser.add_argument(
        "--bundle-id",
        required=True,
        help="Bundle identifier (must already exist in developer portal)",
    )
    parser.add_argument(
        "--sku", required=True, help="SKU (usually same as bundle ID)"
    )
    parser.add_argument(
        "--platform",
        required=True,
        choices=sorted(PLATFORM_LABELS.keys()),
    )
    parser.add_argument(
        "--language",
        required=True,
        help='Primary language label (e.g., "English (U.S.)")',
    )
    parser.add_argument(
        "--user-access",
        required=False,
        default="full",
        choices=sorted(USER_ACCESS_LABELS.keys()),
        help="User access level: full or limited (default: full)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser headless (not recommended)",
    )
    parser.add_argument(
        "--trace-dir",
        default="",
        help="Directory to write Playwright trace zip on failure",
    )
    parser.add_argument(
        "--timeout-ms",
        type=int,
        default=15000,
        help="Default action timeout in ms",
    )
    return parser.parse_args()


def log(msg: str) -> None:
    print(msg, flush=True)


def prompt(msg: str) -> None:
    input(f"{msg}\nPress Enter to continue...")


def click_first(page, locators, description: str) -> None:
    """Try each locator in order; fall back to manual prompt."""
    for locator in locators:
        try:
            locator.click(timeout=3000)
            return
        except PlaywrightTimeoutError:
            continue
    log(f"Could not click {description}. Please complete it manually.")
    prompt("Once done, continue")


def fill_slowly(page, label_regex: str, value: str, description: str) -> None:
    """Clear and type value character-by-character to trigger form validation."""
    try:
        field = page.get_by_label(re.compile(label_regex, re.I))
        field.click()
        field.fill("")
        field.type(value, delay=30)
    except PlaywrightTimeoutError:
        log(f"Could not find {description} field. Please fill it manually.")
        prompt("Once done, continue")


def select_native(page, label_regex: str, option_text: str, description: str) -> None:
    """Select an option in a native <select> element by partial label match."""
    try:
        select = page.get_by_label(re.compile(label_regex, re.I))
        select.select_option(label=option_text)
    except PlaywrightTimeoutError:
        log(f"Could not select {description}. Please select it manually.")
        prompt("Once done, continue")


def click_radio_with_scroll(page, label_text: str, description: str) -> None:
    """Click a custom radio button by scrolling into view first.

    Apple's custom radios wrap <input type=radio> in <span> overlays.
    Direct .click() may be intercepted. scrollIntoViewIfNeeded + click
    on the input itself bypasses the overlay.
    """
    try:
        radio = page.get_by_role("radio", name=re.compile(re.escape(label_text), re.I))
        radio.scroll_into_view_if_needed()
        radio.click(force=True)
    except PlaywrightTimeoutError:
        log(f"Could not select {description}. Please select it manually.")
        prompt("Once done, continue")


def main() -> int:
    args = parse_args()
    platform_label = PLATFORM_LABELS[args.platform]
    access_label = USER_ACCESS_LABELS[args.user_access]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless)
        context = browser.new_context()
        context.set_default_timeout(args.timeout_ms)
        page = context.new_page()

        trace_path = ""
        if args.trace_dir:
            os.makedirs(args.trace_dir, exist_ok=True)
            trace_path = os.path.join(
                args.trace_dir,
                f"asc-create-app-trace-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}.zip",
            )
            context.tracing.start(screenshots=True, snapshots=True, sources=True)

        try:
            # Step 1: Navigate
            log(f"Opening {ASC_APPS_URL}...")
            page.goto(ASC_APPS_URL, wait_until="domcontentloaded")
            prompt("Log in to App Store Connect and complete 2FA if prompted")

            # Step 2: Open the New App dropdown menu
            log("Opening New App menu...")
            click_first(
                page,
                [
                    page.get_by_role("button", name=re.compile("New App", re.I)),
                ],
                "the New App button",
            )

            # Step 3: Click the "New App" menu item (not "New App Bundle")
            log("Clicking New App menu item...")
            click_first(
                page,
                [
                    page.get_by_role("menuitem", name=re.compile("^New App$", re.I)),
                    page.get_by_role("button", name=re.compile("^New App$", re.I)),
                ],
                "the New App menu item",
            )

            # Wait for the dialog to appear and Bundle ID dropdown to load
            log("Waiting for form to load...")
            page.wait_for_timeout(2000)

            # Step 4a: Platform checkbox
            log(f"Selecting platform: {platform_label}...")
            click_first(
                page,
                [
                    page.get_by_role("checkbox", name=re.compile(f"^{platform_label}$", re.I)),
                ],
                f"the {platform_label} platform checkbox",
            )

            # Wait for Bundle ID dropdown to finish loading after platform selection
            try:
                page.get_by_label(re.compile("Bundle ID", re.I)).wait_for(state="attached", timeout=10000)
                page.wait_for_timeout(2000)
            except PlaywrightTimeoutError:
                log("Bundle ID dropdown may still be loading...")

            # Step 4b: Name
            log(f"Filling name: {args.app_name}...")
            fill_slowly(page, r"^Name$", args.app_name, "Name")

            # Step 4c: Primary Language
            log(f"Selecting language: {args.language}...")
            select_native(page, r"Primary Language", args.language, "Primary Language")

            # Step 4d: Bundle ID
            log(f"Selecting bundle ID: {args.bundle_id}...")
            select_native(page, r"Bundle ID", args.bundle_id, "Bundle ID")

            # Step 4e: SKU
            log(f"Filling SKU: {args.sku}...")
            fill_slowly(page, r"^SKU$", args.sku, "SKU")

            # Step 4f: User Access (required -- Create stays disabled without this)
            log(f"Selecting user access: {access_label}...")
            click_radio_with_scroll(page, access_label, f"User Access ({access_label})")

            # Step 5: Confirm before creating
            prompt("Review the form and confirm everything looks correct")

            # Step 6: Click Create
            log("Clicking Create...")
            create_btn = page.get_by_role("button", name=re.compile("^Create$", re.I))
            try:
                create_btn.click(timeout=5000)
            except PlaywrightTimeoutError:
                log("Create button may be disabled. Check the form for missing fields.")
                prompt("Fix any issues and press Enter to retry")
                create_btn.click(timeout=5000)

            # Step 7: Wait for navigation to the new app page
            try:
                page.wait_for_url(re.compile(r"/apps/\d+"), timeout=20000)
                log("App created successfully!")
            except PlaywrightTimeoutError:
                log("Create completed, but did not detect navigation. Verify in the UI.")

            log("Done. Verify via: asc apps list --bundle-id \"" + args.bundle_id + "\"")
            return 0

        except PlaywrightError as exc:
            log(f"Playwright error: {exc}")
            try:
                screenshot_path = os.path.join(
                    args.trace_dir or ".",
                    f"asc-create-app-failure-{int(time.time())}.png",
                )
                page.screenshot(path=screenshot_path, full_page=True)
                log(f"Screenshot saved to: {screenshot_path}")
            except Exception:
                pass
            return 1

        finally:
            try:
                if args.trace_dir and trace_path:
                    context.tracing.stop(path=trace_path)
                    log(f"Trace saved to: {trace_path}")
            except Exception:
                pass
            context.close()
            browser.close()


if __name__ == "__main__":
    sys.exit(main())
