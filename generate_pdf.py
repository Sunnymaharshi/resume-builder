import os

from playwright.sync_api import sync_playwright


def html_to_pdf(html_filename, output_pdf_filename):
    print("Launching headless browser...")
    with sync_playwright() as p:
        # Launch Chromium in headless mode
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Construct the absolute path to your local HTML file
        absolute_path = os.path.abspath(html_filename)
        file_url = f"file://{absolute_path}"

        print(f"Loading {html_filename}...")
        page.goto(file_url)

        # Generate the PDF with standard resume dimensions and margins
        page.pdf(
            path=output_pdf_filename,
            format="A4",
            print_background=True,
            margin={
                "top": "0.5in",
                "right": "0.5in",
                "bottom": "0.5in",
                "left": "0.5in",
            },
        )

        browser.close()
        print(f"Success! Resume saved to {output_pdf_filename}")


if __name__ == "__main__":
    html_to_pdf("resume.html", "Maharshi_Reddy_Resume.pdf")
