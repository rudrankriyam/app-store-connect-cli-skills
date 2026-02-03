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
    --language "English (U.S.)"
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create an App Store Connect app via UI automation.")
    parser.add_argument("--app-name", required=True, help="App name to create")
    parser.add_argument("--bundle-id", required=True, help="Bundle identifier (must exist in developer portal)")
    parser.add_argument("--sku", required=True, help="SKU (usually same as bundle ID)")
    parser.add_argument("--platform", required=True, choices=sorted(PLATFORM_LABELS.keys()))
    parser.add_argument("--language", required=True, help='Primary language label (e.g., "English (U.S.)")')
    parser.add_argument("--headless", action="store_true", help="Run browser headless (not recommended)")
    parser.add_argument("--trace-dir", default="", help="Directory to write Playwright trace zip on failure")
    parser.add_argument("--timeout-ms", type=int, default=15000, help="Default action timeout in ms")
    return parser.parse_args()


def log(msg: str) -> None:
    print(msg, flush=True)


def prompt(msg: str) -> None:
    input(f"{msg}\nPress Enter to continue...")


def click_first(page, locators, description: str) -> None:
    for locator in locators:
        try:
            locator.click(timeout=2000)
            return
        except PlaywrightTimeoutError:
            continue
    log(f"Could not click {description}. Please complete it manually.")
    prompt("Once done, continue")


def fill_with_fallback(page, label_regex: str, value: str, description: str) -> None:
    try:
        page.get_by_label(re.compile(label_regex, re.I)).fill(value)
    except PlaywrightTimeoutError:
        log(f"Could not find {description} field. Please fill it manually.")
        prompt("Once done, continue")


def select_option_by_label(page, label_regex: str, option_label: str, description: str) -> None:
    try:
        field = page.get_by_label(re.compile(label_regex, re.I))
        field.click()
        page.get_by_role("option", name=re.compile(re.escape(option_label), re.I)).click()
    except PlaywrightTimeoutError:
        log(f"Could not select {description}. Please select it manually.")
        prompt("Once done, continue")


def main() -> int:
    args = parse_args()
    platform_label = PLATFORM_LABELS[args.platform]

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
            log(f"Opening {ASC_APPS_URL}...")
            page.goto(ASC_APPS_URL, wait_until="domcontentloaded")
            prompt("Log in to App Store Connect and complete 2FA if prompted")

            # Open the create app dialog
            click_first(
                page,
                [
                    page.get_by_role("button", name=re.compile("New App", re.I)),
                    page.get_by_role("button", name=re.compile("Add App", re.I)),
                    page.get_by_role("button", name=re.compile("Create App", re.I)),
                ],
                "the New App button",
            )

            # Fill out the form
            click_first(
                page,
                [
                    page.get_by_role("button", name=re.compile(platform_label, re.I)),
                    page.get_by_role("radio", name=re.compile(platform_label, re.I)),
                ],
                "the platform selection",
            )
            fill_with_fallback(page, r"App Name", args.app_name, "App Name")
            select_option_by_label(page, r"Primary Language", args.language, "Primary Language")
            select_option_by_label(page, r"Bundle ID", args.bundle_id, "Bundle ID")
            fill_with_fallback(page, r"SKU", args.sku, "SKU")

            prompt("Review the form and confirm everything looks correct")

            # Final create
            click_first(
                page,
                [page.get_by_role("button", name=re.compile("^Create$", re.I))],
                "the Create button",
            )

            # Wait for navigation or success banner
            try:
                page.wait_for_url(re.compile(r"/apps/"), timeout=20000)
            except PlaywrightTimeoutError:
                log("Create completed, but did not detect navigation. Verify in the UI.")

            log("Done. Verify in App Store Connect and fetch the app ID via asc.")
            return 0
        except PlaywrightError as exc:
            log(f"Playwright error: {exc}")
            if args.trace_dir and trace_path:
                try:
                    context.tracing.stop(path=trace_path)
                    log(f"Trace saved to: {trace_path}")
                except Exception:
                    pass
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
            except Exception:
                pass
            context.close()
            browser.close()


if __name__ == "__main__":
    sys.exit(main())
