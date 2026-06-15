# Resume — HTML to PDF (Playwright)

A single-page, A4, ATS-friendly resume built as plain HTML/CSS and rendered
to PDF with Playwright (Chromium). Edit the HTML, run one script, get a PDF.

## Folder structure

```
resume-project/
├── resume.html              ← all content + styling (edit this)
├── generate_pdf.py             ← run this to generate the PDF
├── README.md                 ← this file
├── fonts/
│   ├── Carlito-Regular.ttf
│   ├── Carlito-Bold.ttf
│   ├── Carlito-Italic.ttf
│   └── Carlito-BoldItalic.ttf
└── Maharshi_Reddy_Resume.pdf  ← generated output (overwritten each run)
```

## One-time setup

```bash
pip install playwright pypdf
python3 -m playwright install chromium
```

`pypdf` is optional — it's only used by the script to report the final
page count after generation.

## Generate the PDF

```bash
python3 generate_pdf.py
```

Output:

```
Pages generated: 1
Saved: /path/to/Maharshi_Reddy_Resume.pdf
```

If `Pages generated` shows more than 1, see **Fitting on one page** below.

## Editing content

Open `resume.html` in any text editor. The file has a documentation
comment block at the top of `<head>` and another at the top of `<body>`
explaining the structure — but the short version:

- **Change text**: find the sentence you want to edit (search for a
  unique word from it) and edit it directly inside the `<li>`, `<div>`,
  etc. Save, re-run `python3 generate_pdf.py`.

- **Add a job or project**: copy an entire block that looks like this:

  ```html
  <div class="keep-together block-gap">
    <div class="row">
      <div class="left job-title">Job Title — Company</div>
      <div class="right date">Start – End</div>
    </div>
    <div class="location">City, Country</div>
    <ul class="bullets">
      <li>Bullet point one.</li>
      <li>Bullet point two.</li>
    </ul>
  </div>
  ```

  Paste it where you want the new entry and edit the text.

- **Add a skill row**: inside `<table class="skills-table">`, copy one
  `<tr>...</tr>` and change the label/value.

- **Add a certification**: inside `<ul class="cert-bullets">`, copy one
  `<li>...</li>`.

## Fitting on one page

All spacing is controlled by a handful of CSS rules near the top of the
`<style>` block. If `generate_pdf.py` reports 2 pages, search for these
class names and reduce the values slightly (try -0.5pt to -1pt at a
time), then re-run:

| CSS class        | Controls                                        |
| ---------------- | ----------------------------------------------- |
| `.section-title` | Space _above_ each section heading (margin-top) |
| `.block-gap`     | Space _after_ each job/project/education block  |
| `.bullets li`    | Space between bullet lines (line-height/margin) |

If there's empty space at the bottom of the page instead, you can
_increase_ these values for a more evenly-spread layout.

## Fonts (why Carlito?)

The resume uses **Carlito**, an open-source font that is
metric-compatible with Microsoft Calibri — meaning identical letter
widths and spacing, so the layout looks the same as if Calibri were
used, but without any licensing restrictions.

The four Carlito font files are bundled in `fonts/` and loaded via
`@font-face` in `resume.html`. This means:

- The resume renders **identically on every machine** — your laptop,
  a colleague's Mac, a CI server — regardless of what fonts are
  installed system-wide.
- No font installation step is required.
- The fonts are embedded directly into the output PDF, so it displays
  correctly even on machines without Carlito installed.

## Page size: A4 vs Letter

The resume defaults to **A4** (595 × 842pt), the standard paper size
everywhere except the US and Canada. To switch to **US Letter**
(612 × 792pt), open `resume.html` and change:

```css
@page {
  size: A4; /* change to: size: letter; */
  margin: 0.45in 0.5in 0.4in 0.5in;
}
```

Letter is wider than A4, so existing content will still fit on one page
without further adjustment.

## ATS-friendliness

This setup is designed to pass Applicant Tracking System parsers:

- All text is real, selectable text (not images or vector outlines).
- Semantic HTML structure (`<ul>`, `<li>`, `<table>`, headings as
  styled `<div>`s in reading order).
- Standard Unicode bullet characters (`•`), no icon fonts.
- Fonts are embedded as proper font objects in the PDF.
- Single column layout, no text boxes or multi-column tricks that
  confuse parsers.

**To verify**: open the generated PDF, select all text (Cmd/Ctrl+A),
copy, and paste into a plain text editor. The text should come out
clean and in the correct top-to-bottom reading order — that's a strong
practical signal that ATS parsers will read it correctly too.

## Color palette

All colors are defined once as CSS variables in `resume.html`:

```css
:root {
  --navy: #16325b; /* name, job/project titles */
  --steel: #1d5fa6; /* section headings */
  --teal: #0e7490; /* project tech stack lines */
  --body: #1c1c1c; /* default text, skill labels */
  --sub: #3a3a3a; /* bullet text */
  --muted: #6b7280; /* dates, locations */
  --rule: #7a90a8; /* divider lines under section headings */
  --con: #4a5568; /* contact line */
}
```

Change a value here to re-theme the entire resume in one place.

## Troubleshooting

**"Pages generated: 2"** — see _Fitting on one page_ above.

**Text looks different / wraps differently than expected** — make sure
the `fonts/` folder is in the same directory as `resume.html`. If the
font files are missing, the browser falls back to a default sans-serif
font with different character widths, which can change line wrapping
and push content onto a second page.

**Playwright errors on first run** — make sure you ran
`python3 -m playwright install chromium` after `pip install playwright`.
This downloads the actual browser binary Playwright drives.
