"""
Render resume.html to a single-page PDF using Playwright (Chromium).

The HTML file already defines exact page size and margins via @page CSS
(US Letter, 0.5in sides, 0.45in top, 0.36in bottom) — Playwright's
print_to_pdf with prefer_css_page_size honors these so no extra
margin config is needed here.

Usage:
    python3 resume_pdf.py
Output:
    /mnt/user-data/outputs/Maharshi_Reddy_Resume_html.pdf
"""

import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

HTML_PATH = Path(__file__).parent / "resume.html"
OUT_PATH = Path(__file__).parent / "Maharshi_Reddy_Resume.pdf"


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Load the HTML file directly from disk
        await page.goto(f"file://{HTML_PATH.resolve()}")

        # Wait for fonts to load so measurements are accurate
        await page.evaluate("document.fonts.ready")

        # print_to_pdf with prefer_css_page_size=True uses the @page rule
        # in the CSS for page size and margins — matches the ReportLab
        # layout exactly (Letter, 0.5in sides, 0.45in top, 0.36in bottom)
        await page.pdf(
            path=str(OUT_PATH),
            prefer_css_page_size=True,
            print_background=True,
        )

        await browser.close()

    print(f"Saved: {OUT_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
