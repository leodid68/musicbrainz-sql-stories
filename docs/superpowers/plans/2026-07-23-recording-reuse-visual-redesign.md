# Recording Reuse Visual Redesign Implementation Plan

> **Status:** Superseded before implementation by the approved five-page PDF
> carousel. Do not execute this plan.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the episode-three navy dashboard visual with a deterministic cobalt editorial poster that draws all 180 media and all 4,320 matching track markers.

**Architecture:** Keep the checked CSV loader and Pillow renderer. Add a pure geometry helper for the 24 markers inside each medium, test the exact `180 × 24` visual contract, then replace only the drawing layer and update its accessibility description.

**Tech Stack:** Python 3.13, Pillow, `unittest`, checked CSV exports.

## Global Constraints

- Canvas stays exactly 1200 × 1500 pixels.
- Preserve the checked values: 4,320 track rows, one release, 180 media, and 24 matching track rows per medium.
- Preserve the exact 15-column × 12-row medium grid.
- Draw exactly 24 track markers in every medium symbol.
- Use cobalt `#2446F5`, near-black `#0B0D12`, paper white `#F7F7F2`, acid yellow `#D8FF3E`, and pale blue `#B9C9FF`.
- Do not change SQL, CSV evidence, the claim ledger, or the approved LinkedIn text.
- Keep `charts/recording-reuse.png` and `publish-ready/recording-reuse.png` byte-identical.
- Keep the visual status as draft until Leo reviews the rendered output.

---

### Task 1: Lock the exact marker geometry

**Files:**
- Modify: `projects/03-recording-reuse/tests/test_visual.py`
- Modify: `projects/03-recording-reuse/scripts/build_visual.py`

**Interfaces:**
- Consumes: existing `medium_positions(columns: int, rows: int)`.
- Produces: `track_marker_positions(columns: int = 6, rows: int = 4) -> list[tuple[int, int]]`.

- [ ] **Step 1: Write the failing marker-count test**

Add this import and test:

```python
from scripts.build_visual import (
    build_visual,
    medium_positions,
    track_marker_positions,
)

def test_each_medium_contains_24_track_markers(self):
    markers = track_marker_positions()
    self.assertEqual(len(markers), 24)
    self.assertEqual(len(set(markers)), 24)
    self.assertEqual(len(medium_positions()) * len(markers), 4320)
```

- [ ] **Step 2: Run the focused test and verify RED**

Run:

```bash
cd projects/03-recording-reuse
PYTHONPATH=. ../../.venv/bin/python -m unittest \
  tests.test_visual.VisualTest.test_each_medium_contains_24_track_markers -v
```

Expected: import failure because `track_marker_positions` does not exist.

- [ ] **Step 3: Add the pure geometry helper**

Add below `medium_positions`:

```python
def track_marker_positions(
    columns: int = 6,
    rows: int = 4,
) -> list[tuple[int, int]]:
    """Return 24 logical marker positions for one medium."""
    return [(column, row) for row in range(rows) for column in range(columns)]
```

- [ ] **Step 4: Run the focused test and verify GREEN**

Run the command from Step 2.

Expected: one passing test.

- [ ] **Step 5: Commit the geometry contract**

```bash
git add \
  projects/03-recording-reuse/tests/test_visual.py \
  projects/03-recording-reuse/scripts/build_visual.py
git commit -m "test: lock recording reuse marker geometry"
```

---

### Task 2: Render the cobalt split-revelation poster

**Files:**
- Modify: `projects/03-recording-reuse/scripts/build_visual.py`
- Test: `projects/03-recording-reuse/tests/test_visual.py`

**Interfaces:**
- Consumes: `load_outlier()`, `validate_evidence()`, `medium_positions()`, and `track_marker_positions()`.
- Produces: a 1200 × 1500 RGB PNG at the caller-provided path.

- [ ] **Step 1: Add a failing palette contract**

Add:

```python
def test_editorial_palette_is_stable(self):
    self.assertEqual(visual.COBALT, "#2446F5")
    self.assertEqual(visual.INK, "#0B0D12")
    self.assertEqual(visual.PAPER, "#F7F7F2")
    self.assertEqual(visual.ACID, "#D8FF3E")
    self.assertEqual(visual.PALE_BLUE, "#B9C9FF")
```

- [ ] **Step 2: Run the palette test and verify RED**

```bash
PYTHONPATH=. ../../.venv/bin/python -m unittest \
  tests.test_visual.VisualTest.test_editorial_palette_is_stable -v
```

Expected: failure because the new palette constants do not exist.

- [ ] **Step 3: Replace the palette and medium renderer**

Use:

```python
COBALT = "#2446F5"
INK = "#0B0D12"
PAPER = "#F7F7F2"
ACID = "#D8FF3E"
PALE_BLUE = "#B9C9FF"
MUTED_COBALT = "#6F86FF"

def _draw_medium(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    *,
    width: int = 54,
    height: int = 27,
) -> None:
    """Draw one medium containing exactly 24 matching-track markers."""
    draw.rectangle(
        (x, y, x + width, y + height),
        outline=PALE_BLUE,
        width=1,
    )
    for column, row in track_marker_positions():
        marker_x = x + 6 + column * 8
        marker_y = y + 5 + row * 5
        draw.rectangle(
            (marker_x, marker_y, marker_x + 2, marker_y + 2),
            fill=ACID,
        )
```

- [ ] **Step 4: Replace the `build_visual` drawing body**

Keep the evidence loading and validation, then render:

```python
image = Image.new("RGB", (WIDTH, HEIGHT), COBALT)
draw = ImageDraw.Draw(image)

draw.text(
    (72, 48),
    "MUSICBRAINZ SQL STORIES / 03",
    font=_font(23, bold=True),
    fill=INK,
)
draw.line((72, 88, 1128, 88), fill=INK, width=3)

draw.text((66, 116), f"{track_rows:,}", font=_font(174, bold=True), fill=INK)
draw.text((78, 298), "TRACK ROWS", font=_font(36, bold=True), fill=PAPER)

draw.rectangle((716, 112, 1128, 378), fill=INK)
draw.text((752, 138), "BUT ONLY", font=_font(24, bold=True), fill=PALE_BLUE)
draw.text((748, 168), f"{releases:,}", font=_font(138, bold=True), fill=ACID)
draw.text((874, 270), "RELEASE", font=_font(34, bold=True), fill=PAPER)

draw.text((72, 414), "RECORDING", font=_font(19, bold=True), fill=INK)
draw.text((72, 442), recording_name, font=_font(33, bold=True), fill=PAPER)

container = (72, 520, 1128, 1080)
draw.rectangle(container, fill=INK)
draw.text(
    (98, 546),
    f"ONE RELEASE / ID {outlier['release_id']}",
    font=_font(22, bold=True),
    fill=ACID,
)
draw.text(
    (1102, 546),
    f"{media} MEDIA",
    font=_font(22, bold=True),
    fill=PALE_BLUE,
    anchor="ra",
)

grid_left = 96
grid_top = 600
column_step = 68
row_step = 36
for column, row in positions:
    _draw_medium(
        draw,
        grid_left + column * column_step,
        grid_top + row * row_step,
    )

draw.text(
    (96, 1040),
    "24 MATCHING TRACK ROWS INSIDE EVERY MEDIUM",
    font=_font(22, bold=True),
    fill=PAPER,
)

equation = f"{media} MEDIA × {tracks_per_medium} MATCHING TRACK ROWS = {track_rows:,}"
draw.text((72, 1122), equation, font=_font(43, bold=True), fill=INK)
draw.text(
    (74, 1184),
    "release  →  medium  →  track",
    font=_font(27, bold=True),
    fill=ACID,
    stroke_width=1,
    stroke_fill=INK,
)

draw.rectangle((0, 1248, WIDTH, HEIGHT), fill=INK)
draw.text(
    (72, 1280),
    "COUNT(track.id)  vs  COUNT(DISTINCT release.id)",
    font=_font(SUPPORT_TEXT_SIZES["sql_method"]),
    fill=PAPER,
)
draw.line((72, 1337, 1128, 1337), fill=MUTED_COBALT, width=2)
draw.text(
    (72, 1366),
    "MusicBrainz full export / 2026-07-15",
    font=_font(SUPPORT_TEXT_SIZES["snapshot"], bold=True),
    fill=PALE_BLUE,
)
draw.text(
    (72, 1413),
    "Catalog metadata, not plays, sales, or popularity.",
    font=_font(SUPPORT_TEXT_SIZES["catalog_limit"]),
    fill=PALE_BLUE,
)
```

Retain the existing save logic.

- [ ] **Step 5: Run the visual tests**

```bash
PYTHONPATH=. ../../.venv/bin/python -m unittest tests.test_visual -v
```

Expected: all visual tests pass.

- [ ] **Step 6: Render both package copies**

```bash
../../.venv/bin/python scripts/build_visual.py
cp charts/recording-reuse.png publish-ready/recording-reuse.png
```

- [ ] **Step 7: Commit the renderer**

```bash
git add \
  projects/03-recording-reuse/scripts/build_visual.py \
  projects/03-recording-reuse/tests/test_visual.py \
  projects/03-recording-reuse/charts/recording-reuse.png \
  projects/03-recording-reuse/publish-ready/recording-reuse.png
git commit -m "feat: redesign recording reuse visual"
```

---

### Task 3: Synchronize accessibility copy and verify the package

**Files:**
- Modify: `projects/03-recording-reuse/accessibility.md`
- Modify: `projects/03-recording-reuse/publish-ready/accessibility.txt`
- Test: `projects/03-recording-reuse/tests/test_package.py`

**Interfaces:**
- Consumes: the rendered cobalt poster and its exact data contract.
- Produces: matching accessibility descriptions and a fully verified draft package.

- [ ] **Step 1: Update the accessibility description**

Use this exact description in both files:

```markdown
# Accessibility

## Static visual

The cobalt editorial poster contrasts 4,320 track rows with one release for
the recording "I Feel Bad For Your Hard Drive."

The number 4,320 dominates the upper left. A sharp black block on the upper
right reveals "1 RELEASE" in acid yellow and white.

A single black rectangular release boundary contains 180 pale-blue medium
symbols arranged in 15 columns and 12 rows. Every medium contains 24 small
acid-yellow markers, so the poster deterministically draws 4,320 matching
track markers. The equation reads: "180 MEDIA × 24 MATCHING TRACK ROWS =
4,320."

The relationship line reads `release → medium → track`. The SQL method compares
`COUNT(track.id)` with `COUNT(DISTINCT release.id)`.

The footer identifies the MusicBrainz full export dated 2026-07-15 and states
that the figures describe catalog metadata, not plays, sales, or popularity.
The outlier is concentrated within one release and does not prove broad reuse
across the catalog.
```

- [ ] **Step 2: Run all tests**

```bash
PYTHONPATH=. ../../.venv/bin/python -m unittest discover -s tests -v
```

Expected: 20 tests pass with zero failures.

- [ ] **Step 3: Verify file integrity**

```bash
cmp -s charts/recording-reuse.png publish-ready/recording-reuse.png
git diff --check
```

Expected: both commands exit 0.

- [ ] **Step 4: Inspect the rendered PNG**

Open `projects/03-recording-reuse/charts/recording-reuse.png` at original size.
Confirm:

- the upper contrast reads in under three seconds;
- the single release boundary is unambiguous;
- the 15 × 12 medium grid is complete;
- the marker texture does not merge into solid blocks;
- the equation and footer remain readable;
- no text is clipped.

- [ ] **Step 5: Commit the synchronized package**

```bash
git add \
  projects/03-recording-reuse/accessibility.md \
  projects/03-recording-reuse/publish-ready/accessibility.txt
git commit -m "docs: update recording reuse visual accessibility"
```

Do not mark the package `ready` and do not push until Leo reviews the rendered
poster.
