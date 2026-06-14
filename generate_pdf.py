"""
Render resume.html to a single-page PDF using Playwright (Chromium).

The HTML embeds the Carlito font directly via @font-face (see fonts/
folder), so this works identically on every machine — no system font
dependency, no installation needed.

The HTML defines exact page size and margins via @page CSS (A4,
0.5in sides, 0.45in top, 0.4in bottom) — Playwright's print_to_pdf
with prefer_css_page_size honors these so no extra margin config
is needed here.

Folder structure required:
    resume.html
    resume_pdf.py
    fonts/
        Carlito-Regular.ttf
        Carlito-Bold.ttf
        Carlito-Italic.ttf
        Carlito-BoldItalic.ttf

Usage:
    python3 resume_pdf.py
Output:
    Maharshi_Reddy_Resume.pdf (next to this script)
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

        # Wait for the embedded Carlito font files to finish loading
        # before rendering — ensures accurate text measurements
        await page.evaluate("document.fonts.ready")

        # print_to_pdf with prefer_css_page_size=True uses the @page rule
        # in the CSS for page size and margins — A4, 0.5in sides,
        # 0.45in top, 0.4in bottom
        await page.pdf(
            path=str(OUT_PATH),
            prefer_css_page_size=True,
            print_background=True,
        )

        await browser.close()

    # Report resulting page count
    try:
        from pypdf import PdfReader

        page_count = len(PdfReader(str(OUT_PATH)).pages)
        print(f"Pages generated: {page_count}")
        if page_count > 1:
            print(
                "⚠️  Resume is more than 1 page — content needs trimming or spacing adjustment."
            )
    except ImportError:
        pass

    print(f"Saved: {OUT_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
