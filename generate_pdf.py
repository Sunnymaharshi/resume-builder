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

        # Diagnostic: check if Carlito actually loaded.
        # If not installed on this machine, Chromium silently falls back
        # to a different font with different metrics -> more line wraps
        # -> content overflows to page 2.
        font_check = await page.evaluate("""
            () => {
                const testText = "Software Engineer II — Hashedin AWS Build";
                // Measure width with Carlito explicitly
                const span1 = document.createElement('span');
                span1.style.fontFamily = 'Carlito';
                span1.style.fontSize = '11pt';
                span1.style.position = 'absolute';
                span1.style.visibility = 'hidden';
                span1.style.whiteSpace = 'nowrap';
                span1.textContent = testText;
                document.body.appendChild(span1);
                const carlitoWidth = span1.getBoundingClientRect().width;
                document.body.removeChild(span1);

                // Measure width with a definitely-available fallback (sans-serif)
                const span2 = document.createElement('span');
                span2.style.fontFamily = 'sans-serif';
                span2.style.fontSize = '11pt';
                span2.style.position = 'absolute';
                span2.style.visibility = 'hidden';
                span2.style.whiteSpace = 'nowrap';
                span2.textContent = testText;
                document.body.appendChild(span2);
                const fallbackWidth = span2.getBoundingClientRect().width;
                document.body.removeChild(span2);

                return {
                    carlitoWidth,
                    fallbackWidth,
                    fontsAvailable: Array.from(document.fonts).map(f => f.family),
                    carlitoLoaded: document.fonts.check('11pt Carlito'),
                };
            }
        """)

        if (
            not font_check["carlitoLoaded"]
            or abs(font_check["carlitoWidth"] - font_check["fallbackWidth"]) < 0.5
        ):
            print("⚠️  WARNING: Carlito font does not appear to be installed.")
            print("   Chromium is likely falling back to a different font,")
            print("   which changes text width and can push content to page 2.")
            print()
            print("   Fix (macOS):")
            print("     brew tap homebrew/cask-fonts")
            print("     brew install --cask font-carlito")
            print()
            print("   Fix (Linux/Debian):")
            print("     sudo apt install fonts-crosextra-carlito")
            print()
            print("   After installing, re-run this script.")
            print()

        # print_to_pdf with prefer_css_page_size=True uses the @page rule
        # in the CSS for page size and margins — matches the ReportLab
        # layout exactly (A4, 0.5in sides, 0.45in top, 0.4in bottom)
        await page.pdf(
            path=str(OUT_PATH),
            prefer_css_page_size=True,
            print_background=True,
        )

        # Report page count
        await browser.close()

    # Report resulting page count
    try:
        from pypdf import PdfReader

        page_count = len(PdfReader(str(OUT_PATH)).pages)
        print(f"Pages generated: {page_count}")
        if page_count > 1:
            print("⚠️  Resume is more than 1 page. See font warning above if shown.")
            print(
                "   If no font warning appeared, try the troubleshooting steps below."
            )
    except ImportError:
        print("(install pypdf to auto-check page count: pip install pypdf)")

    print(f"Saved: {OUT_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
