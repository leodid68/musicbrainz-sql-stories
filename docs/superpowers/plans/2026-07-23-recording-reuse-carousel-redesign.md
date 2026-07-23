# Recording Reuse Carousel Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate and verify a five-page cobalt editorial PDF carousel from the checked episode-three MusicBrainz evidence.

**Architecture:** Extend the existing Pillow renderer with five deterministic page functions and exact medium/marker geometry. Add a small ReportLab orchestrator that embeds the five 1200 × 1500 PNGs into equal 576 × 720 point pages, copies the public artifacts into `publish-ready`, and exposes stable functions for `unittest`.

**Tech Stack:** Python 3.13, Pillow, ReportLab, pypdf, Poppler, `unittest`.

## Global Constraints

- Preserve all checked SQL and CSV evidence.
- Preserve the approved LinkedIn text.
- Render exactly five RGB pages at 1200 × 1500.
- Draw exactly 180 media in a 15 × 12 grid on page 3.
- Draw exactly 24 track markers per medium, totaling 4,320.
- Use only `#2446F5`, `#0B0D12`, `#F7F7F2`, `#D8FF3E`, `#B9C9FF`, plus antialiasing.
- Build five equal PDF pages at 576 × 720 points.
- Keep public and `publish-ready` copies byte-identical.
- Keep status `draft - final text approved; carousel review pending`.
- Do not push or publish before Leo reviews the rendered carousel.

---

### Task 1: Add exact carousel geometry

**Files:**
- Modify: `projects/03-recording-reuse/scripts/build_visual.py`
- Modify: `projects/03-recording-reuse/tests/test_visual.py`

**Interfaces:**
- Produces: `track_marker_positions(columns: int = 6, rows: int = 4) -> list[tuple[int, int]]`
- Produces: `carousel_page_paths(output_dir: Path) -> list[Path]`

- [ ] **Step 1: Write failing geometry and path tests**

```python
from scripts.build_visual import (
    build_visual,
    carousel_page_paths,
    medium_positions,
    track_marker_positions,
)

def test_each_medium_contains_exactly_24_track_markers(self):
    markers = track_marker_positions()
    self.assertEqual(len(markers), 24)
    self.assertEqual(len(set(markers)), 24)
    self.assertEqual(len(medium_positions()) * len(markers), 4320)

def test_carousel_has_five_stable_page_names(self):
    paths = carousel_page_paths(Path("/tmp/carousel"))
    self.assertEqual(
        [path.name for path in paths],
        [
            "page-01-hook.png",
            "page-02-reveal.png",
            "page-03-structure.png",
            "page-04-sql.png",
            "page-05-lesson.png",
        ],
    )
```

- [ ] **Step 2: Run focused tests and verify RED**

```bash
cd projects/03-recording-reuse
PYTHONPATH=. ../../.venv/bin/python -m unittest \
  tests.test_visual.VisualTest.test_each_medium_contains_exactly_24_track_markers \
  tests.test_visual.VisualTest.test_carousel_has_five_stable_page_names -v
```

Expected: import failure for the two new functions.

- [ ] **Step 3: Implement the pure helpers**

```python
PAGE_FILENAMES = (
    "page-01-hook.png",
    "page-02-reveal.png",
    "page-03-structure.png",
    "page-04-sql.png",
    "page-05-lesson.png",
)

def track_marker_positions(
    columns: int = 6,
    rows: int = 4,
) -> list[tuple[int, int]]:
    return [(column, row) for row in range(rows) for column in range(columns)]

def carousel_page_paths(output_dir: Path) -> list[Path]:
    return [output_dir / filename for filename in PAGE_FILENAMES]
```

- [ ] **Step 4: Run focused tests and verify GREEN**

Run the Step 2 command and expect two passing tests.

- [ ] **Step 5: Commit**

```bash
git add projects/03-recording-reuse/scripts/build_visual.py \
  projects/03-recording-reuse/tests/test_visual.py
git commit -m "test: lock carousel page and marker geometry"
```

---

### Task 2: Render all five cobalt pages

**Files:**
- Modify: `projects/03-recording-reuse/scripts/build_visual.py`
- Modify: `projects/03-recording-reuse/tests/test_visual.py`
- Create: `projects/03-recording-reuse/carousel/.gitkeep`

**Interfaces:**
- Produces: `build_carousel_pages(output_dir: Path = CAROUSEL_DIR) -> list[Path]`
- Preserves: `build_visual(output_path: Path = PNG_PATH) -> Path`, now rendering page 1.

- [ ] **Step 1: Write failing page-render tests**

```python
def test_carousel_exports_five_portrait_pages(self):
    with tempfile.TemporaryDirectory() as directory:
        pages = visual.build_carousel_pages(Path(directory))
        self.assertEqual(len(pages), 5)
        for page in pages:
            with Image.open(page) as image:
                self.assertEqual(image.size, (1200, 1500))
                self.assertEqual(image.mode, "RGB")

def test_cover_matches_page_one(self):
    with tempfile.TemporaryDirectory() as directory:
        directory = Path(directory)
        pages = visual.build_carousel_pages(directory / "pages")
        cover = visual.build_visual(directory / "cover.png")
        self.assertEqual(cover.read_bytes(), pages[0].read_bytes())
```

- [ ] **Step 2: Run focused tests and verify RED**

```bash
PYTHONPATH=. ../../.venv/bin/python -m unittest \
  tests.test_visual.VisualTest.test_carousel_exports_five_portrait_pages \
  tests.test_visual.VisualTest.test_cover_matches_page_one -v
```

Expected: `build_carousel_pages` is missing.

- [ ] **Step 3: Implement shared page primitives**

Add:

```python
COBALT = "#2446F5"
INK = "#0B0D12"
PAPER = "#F7F7F2"
ACID = "#D8FF3E"
PALE_BLUE = "#B9C9FF"

def _new_page(page_number: int) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (WIDTH, HEIGHT), COBALT)
    draw = ImageDraw.Draw(image)
    draw.text((72, 48), "MUSICBRAINZ SQL STORIES / 03",
              font=_font(23, bold=True), fill=INK)
    draw.text((1128, 48), f"{page_number:02d} / 05",
              font=_font(23, bold=True), fill=INK, anchor="ra")
    draw.line((72, 88, 1128, 88), fill=INK, width=3)
    return image, draw

def _save_page(image: Image.Image, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="PNG", optimize=True)
    return path
```

- [ ] **Step 4: Implement the five page functions**

Create `_render_hook`, `_render_reveal`, `_render_structure`, `_render_sql`,
and `_render_lesson`. Use only values from `load_outlier()` and the checked
catalog summary. Page 3 must loop over `medium_positions()` and, inside every
medium, over `track_marker_positions()`. Page 4 must render the exact approved
CTE line by line in a monospace font of at least 34 pixels.

The page functions return RGB `Image` objects and contain the exact copy from
the approved carousel specification.

- [ ] **Step 5: Implement the public builders**

```python
def build_carousel_pages(output_dir: Path = CAROUSEL_DIR) -> list[Path]:
    validate_evidence()
    outlier = load_outlier()
    renderers = (
        _render_hook,
        _render_reveal,
        _render_structure,
        _render_sql,
        _render_lesson,
    )
    paths = carousel_page_paths(output_dir)
    return [
        _save_page(renderer(outlier), path)
        for renderer, path in zip(renderers, paths, strict=True)
    ]

def build_visual(output_path: Path = PNG_PATH) -> Path:
    validate_evidence()
    return _save_page(_render_hook(load_outlier()), output_path)
```

- [ ] **Step 6: Run visual tests**

```bash
PYTHONPATH=. ../../.venv/bin/python -m unittest tests.test_visual -v
```

Expected: all visual tests pass.

- [ ] **Step 7: Commit**

```bash
git add projects/03-recording-reuse/scripts/build_visual.py \
  projects/03-recording-reuse/tests/test_visual.py \
  projects/03-recording-reuse/carousel/.gitkeep
git commit -m "feat: render recording reuse carousel pages"
```

---

### Task 3: Build and verify the five-page PDF

**Files:**
- Create: `projects/03-recording-reuse/scripts/build_carousel.py`
- Create: `projects/03-recording-reuse/tests/test_carousel.py`

**Interfaces:**
- Produces: `build_pdf(page_paths: list[Path], output_path: Path) -> Path`
- Produces: `build_carousel() -> tuple[list[Path], Path]`

- [ ] **Step 1: Write failing PDF tests**

```python
class CarouselPdfTest(unittest.TestCase):
    def test_pdf_has_five_equal_pages_and_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            pages = build_carousel_pages(directory / "pages")
            pdf = build_pdf(pages, directory / "carousel.pdf")
            reader = PdfReader(pdf)
            self.assertEqual(len(reader.pages), 5)
            self.assertEqual(
                {
                    (float(page.mediabox.width), float(page.mediabox.height))
                    for page in reader.pages
                },
                {(576.0, 720.0)},
            )
            self.assertEqual(
                reader.metadata.title,
                "MusicBrainz SQL Stories 03 - One Recording, 4,320 Track Rows",
            )
            self.assertEqual(reader.metadata.author, "Léo Didier")
            self.assertLess(pdf.stat().st_size, 100 * 1024 * 1024)
```

- [ ] **Step 2: Run the PDF test and verify RED**

```bash
PYTHONPATH=. ../../.venv/bin/python -m unittest \
  tests.test_carousel.CarouselPdfTest.test_pdf_has_five_equal_pages_and_metadata -v
```

Expected: import failure because `build_carousel.py` does not exist.

- [ ] **Step 3: Implement the ReportLab builder**

```python
from pathlib import Path
from reportlab.pdfgen import canvas

PDF_PAGE_SIZE = (576, 720)
PDF_TITLE = "MusicBrainz SQL Stories 03 - One Recording, 4,320 Track Rows"
PDF_AUTHOR = "Léo Didier"
PDF_SUBJECT = "SQL grain, track rows, media, and release structure"

def build_pdf(page_paths: list[Path], output_path: Path) -> Path:
    if len(page_paths) != 5:
        raise ValueError("carousel requires exactly five pages")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    document = canvas.Canvas(str(output_path), pagesize=PDF_PAGE_SIZE)
    document.setTitle(PDF_TITLE)
    document.setAuthor(PDF_AUTHOR)
    document.setSubject(PDF_SUBJECT)
    for page_path in page_paths:
        document.drawImage(
            str(page_path),
            0,
            0,
            width=PDF_PAGE_SIZE[0],
            height=PDF_PAGE_SIZE[1],
            preserveAspectRatio=False,
            mask="auto",
        )
        document.showPage()
    document.save()
    return output_path
```

- [ ] **Step 4: Implement package orchestration**

`build_carousel()` renders the five pages, writes
`recording-reuse-carousel.pdf`, copies page 1 to both cover paths, and copies
the PDF to `publish-ready/recording-reuse-carousel.pdf`.

- [ ] **Step 5: Run the PDF and visual tests**

```bash
PYTHONPATH=. ../../.venv/bin/python -m unittest \
  tests.test_carousel tests.test_visual -v
```

Expected: all tests pass.

- [ ] **Step 6: Commit**

```bash
git add projects/03-recording-reuse/scripts/build_carousel.py \
  projects/03-recording-reuse/tests/test_carousel.py
git commit -m "feat: build recording reuse PDF carousel"
```

---

### Task 4: Package, document, render, and inspect

**Files:**
- Modify: `projects/03-recording-reuse/README.md`
- Modify: `projects/03-recording-reuse/accessibility.md`
- Modify: `projects/03-recording-reuse/data-post-brief.md`
- Modify: `projects/03-recording-reuse/publish-ready/README.md`
- Modify: `projects/03-recording-reuse/publish-ready/accessibility.txt`
- Modify: `projects/03-recording-reuse/publish-ready/publication-notes.md`
- Modify: `projects/03-recording-reuse/tests/test_package.py`
- Generate: carousel PNGs, cover PNG copies, and PDF copies.

**Interfaces:**
- Consumes: `build_carousel()`.
- Produces: complete draft publication package and rendered PDF previews.

- [ ] **Step 1: Update package tests**

Require:

- the five carousel page PNGs;
- `recording-reuse-carousel.pdf` in public and publish-ready locations;
- byte-identical PDF copies;
- byte-identical page-one and cover PNG;
- the publication note `Format: five-page PDF carousel plus text post.`;
- status `draft; final text approved, carousel review pending`.

- [ ] **Step 2: Run package tests and verify RED**

```bash
PYTHONPATH=. ../../.venv/bin/python -m unittest tests.test_package -v
```

Expected: failures for the missing carousel artifacts and old publication copy.

- [ ] **Step 3: Update README, brief, accessibility, and publication notes**

Document the five-page sequence and add a page-by-page accessibility
description. Preserve the unconfirmed LinkedIn URL/date fields and the draft
status.

- [ ] **Step 4: Generate final artifacts**

```bash
../../.venv/bin/python scripts/build_carousel.py
```

- [ ] **Step 5: Run the complete suite**

```bash
PYTHONPATH=. ../../.venv/bin/python -m unittest discover -s tests -v
```

Expected: all tests pass with zero failures.

- [ ] **Step 6: Verify PDF structure and package integrity**

```bash
pdfinfo recording-reuse-carousel.pdf
cmp -s recording-reuse-carousel.pdf \
  publish-ready/recording-reuse-carousel.pdf
cmp -s carousel/page-01-hook.png charts/recording-reuse.png
cmp -s charts/recording-reuse.png publish-ready/recording-reuse.png
git diff --check
```

Expected: five pages, equal 4:5 size, all comparisons exit 0.

- [ ] **Step 7: Render the PDF with Poppler**

```bash
mkdir -p tmp/pdfs
pdftoppm -png -r 150 recording-reuse-carousel.pdf \
  tmp/pdfs/recording-reuse-carousel
```

Expected: five PNG previews.

- [ ] **Step 8: Inspect all five pages**

Check original and rendered previews for clipping, overlap, missing glyphs,
contrast, marker separation, page order, and mobile legibility. Correct only
the identified defect, rebuild, rerun all tests, and rerender before handoff.

- [ ] **Step 9: Commit without pushing**

```bash
git add projects/03-recording-reuse
git commit -m "feat: package recording reuse PDF carousel"
```

Keep the carousel in draft status and ask Leo to review the rendered pages.
