# Recording Reuse LinkedIn Package Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reproducible third MusicBrainz SQL Story with checked SQL, CSV evidence, one original static visual, a natural first-person LinkedIn draft, and a reviewable publication package.

**Architecture:** PostgreSQL queries produce four evidence exports: catalog summary, outlier structure, high-reuse recordings, and validation summary. A small Python data contract loads those checked CSVs, and a Pillow renderer builds the 1200-by-1500 visual from the outlier metrics. Editorial files consume the same checked claims, while tests verify dimensions, symbol count, arithmetic, copy claims, and package completeness.

**Tech Stack:** PostgreSQL 18, SQL, Python 3, standard-library `csv` and `unittest`, Pillow, Markdown.

## Global Constraints

- Source snapshot: MusicBrainz full export dated 2026-07-15.
- Describe catalog metadata only; never call the counts plays, sales, popularity, audience, or audio usage.
- Static visual size: exactly 1200 by 1500 pixels.
- Static visual structure: exactly 180 medium symbols in a 15-by-12 grid.
- Visual arithmetic: 180 media multiplied by 24 matching track rows equals 4,320 track rows in one release.
- Visual method line: `COUNT(track.id) vs COUNT(DISTINCT release.id)`.
- LinkedIn draft: simple first-person English, at most one functional emoji, no engagement bait, no em dash, and no invented next episode.
- The public repository must not include credentials, private coaching notes, or conversation transcripts.
- Status remains `draft` until Leo rewrites and approves the copy and every publication artifact is checked.
- Do not push to GitHub or publish to LinkedIn without Leo's explicit confirmation immediately before the external action.

---

## File map

- `projects/03-recording-reuse/analysis.sql`: reproducible analysis and export queries.
- `projects/03-recording-reuse/checks.sql`: independent PostgreSQL assertions.
- `projects/03-recording-reuse/data/catalog-summary.csv`: checked catalog-wide metrics.
- `projects/03-recording-reuse/data/outlier-structure.csv`: checked one-row visual input.
- `projects/03-recording-reuse/data/high-reuse-recordings.csv`: the 3,766-recording comparison perimeter.
- `projects/03-recording-reuse/data/validation-summary.csv`: checked hierarchy controls.
- `projects/03-recording-reuse/scripts/data_contract.py`: typed CSV loaders and arithmetic validation.
- `projects/03-recording-reuse/scripts/build_visual.py`: deterministic Pillow renderer.
- `projects/03-recording-reuse/tests/test_data_contract.py`: evidence-contract tests.
- `projects/03-recording-reuse/tests/test_visual.py`: rendering and layout tests.
- `projects/03-recording-reuse/tests/test_package.py`: editorial and package consistency tests.
- `projects/03-recording-reuse/charts/recording-reuse.png`: rendered static visual.
- `projects/03-recording-reuse/README.md`: public project explanation and reproduction steps.
- `projects/03-recording-reuse/claim-ledger.md`: claim-to-evidence mapping.
- `projects/03-recording-reuse/data-post-brief.md`: editorial brief.
- `projects/03-recording-reuse/linkedin-post.md`: user-editable draft.
- `projects/03-recording-reuse/accessibility.md`: image description.
- `projects/03-recording-reuse/publish-ready/`: reviewed copies of publication-facing artifacts, still marked draft until user approval.
- `README.md`: series index including episodes two and three.

---

### Task 1: Reproducible SQL evidence

**Files:**
- Create: `projects/03-recording-reuse/analysis.sql`
- Create: `projects/03-recording-reuse/checks.sql`
- Create: `projects/03-recording-reuse/data/catalog-summary.csv`
- Create: `projects/03-recording-reuse/data/outlier-structure.csv`
- Create: `projects/03-recording-reuse/data/high-reuse-recordings.csv`
- Create: `projects/03-recording-reuse/data/validation-summary.csv`

**Interfaces:**
- Consumes: MusicBrainz tables `recording`, `track`, `medium`, and `release`.
- Produces: CSV columns consumed by `scripts/data_contract.py`: `recordings_with_tracks,total_track_appearances,used_once,used_at_least_twice,used_at_least_10,used_at_least_100,reuse_share_pct`; `recording_id,recording_name,release_id,release_name,distinct_releases,distinct_mediums,track_appearances,min_tracks_on_a_medium,max_tracks_on_a_medium`; `track_appearances,recording_id,distinct_mediums,distinct_releases`; and `recording_count,min_track_appearances,track_medium_violations,medium_release_violations`.

- [ ] **Step 1: Write the independent checks first**

Create `checks.sql` with `\set ON_ERROR_STOP on`, a `DO` block, and explicit assertions for all public numbers:

```sql
\set ON_ERROR_STOP on

DO $$
DECLARE
    recordings_with_tracks bigint;
    total_track_appearances bigint;
    used_once bigint;
    used_at_least_twice bigint;
    used_at_least_10 bigint;
    used_at_least_100 bigint;
    reuse_share numeric;
    outlier_release_count bigint;
    outlier_medium_count bigint;
    outlier_track_count bigint;
    outlier_min_medium_tracks integer;
    outlier_max_medium_tracks integer;
    track_medium_violations bigint;
    medium_release_violations bigint;
BEGIN
    WITH recording_usage AS (
        SELECT track.recording AS recording_id, COUNT(track.id) AS track_appearances
        FROM track
        GROUP BY track.recording
    )
    SELECT
        COUNT(*),
        SUM(track_appearances),
        COUNT(*) FILTER (WHERE track_appearances = 1),
        COUNT(*) FILTER (WHERE track_appearances >= 2),
        COUNT(*) FILTER (WHERE track_appearances >= 10),
        COUNT(*) FILTER (WHERE track_appearances >= 100),
        100.0 * COUNT(*) FILTER (WHERE track_appearances >= 2) / COUNT(*)
    INTO recordings_with_tracks, total_track_appearances, used_once,
         used_at_least_twice, used_at_least_10, used_at_least_100, reuse_share
    FROM recording_usage;

    IF recordings_with_tracks <> 39332638 THEN
        RAISE EXCEPTION 'recording count mismatch: %', recordings_with_tracks;
    END IF;
    IF total_track_appearances <> 56818950 THEN
        RAISE EXCEPTION 'track total mismatch: %', total_track_appearances;
    END IF;
    IF used_once <> 31924042 OR used_at_least_twice <> 7408596 THEN
        RAISE EXCEPTION 'reuse threshold mismatch: % / %', used_once, used_at_least_twice;
    END IF;
    IF used_at_least_10 <> 244908 OR used_at_least_100 <> 3766 THEN
        RAISE EXCEPTION 'high reuse threshold mismatch: % / %', used_at_least_10, used_at_least_100;
    END IF;
    IF reuse_share <> 18.8357465370108153 THEN
        RAISE EXCEPTION 'reuse share mismatch: %', reuse_share;
    END IF;

    SELECT COUNT(DISTINCT release.id), COUNT(DISTINCT medium.id), COUNT(track.id),
           MIN(medium.track_count), MAX(medium.track_count)
    INTO outlier_release_count, outlier_medium_count, outlier_track_count,
         outlier_min_medium_tracks, outlier_max_medium_tracks
    FROM track
    JOIN medium ON medium.id = track.medium
    JOIN release ON release.id = medium.release
    WHERE track.recording = 42361496;

    IF outlier_release_count <> 1 OR outlier_medium_count <> 180
       OR outlier_track_count <> 4320 OR outlier_min_medium_tracks <> 24
       OR outlier_max_medium_tracks <> 24 THEN
        RAISE EXCEPTION 'outlier structure mismatch';
    END IF;

    WITH recording_usage AS (
        SELECT track.recording AS recording_id, COUNT(track.id) AS track_appearances
        FROM track
        GROUP BY track.recording
    ), recording_release_usage AS (
        SELECT recording_usage.recording_id, recording_usage.track_appearances,
               COUNT(DISTINCT medium.id) AS distinct_mediums,
               COUNT(DISTINCT release.id) AS distinct_releases
        FROM recording_usage
        JOIN track ON track.recording = recording_usage.recording_id
        JOIN medium ON medium.id = track.medium
        JOIN release ON release.id = medium.release
        WHERE recording_usage.track_appearances >= 100
        GROUP BY recording_usage.recording_id, recording_usage.track_appearances
    )
    SELECT
        COUNT(*) FILTER (WHERE distinct_mediums > track_appearances),
        COUNT(*) FILTER (WHERE distinct_releases > distinct_mediums)
    INTO track_medium_violations, medium_release_violations
    FROM recording_release_usage;

    IF track_medium_violations <> 0 OR medium_release_violations <> 0 THEN
        RAISE EXCEPTION 'hierarchy violations: % / %',
            track_medium_violations, medium_release_violations;
    END IF;
END
$$;

SELECT 'recording reuse checks passed' AS result;
```

- [ ] **Step 2: Run checks and confirm the baseline passes**

Run:

```sh
/Applications/Postgres.app/Contents/Versions/18/bin/psql \
  -h 127.0.0.1 -p 5433 -U musicbrainz -d musicbrainz_db \
  -X -f projects/03-recording-reuse/checks.sql
```

Expected: one row containing `recording reuse checks passed` and no exception.

- [ ] **Step 3: Write the analysis and export queries**

Create `analysis.sql` with four labeled queries. Reuse a recording-level CTE, use `COUNT(DISTINCT ...)` for media and releases, filter the comparison perimeter at 100 appearances, and use deterministic ordering:

```sql
\set ON_ERROR_STOP on

-- Query 1: catalog-wide recording usage distribution.
WITH recording_usage AS (
    SELECT track.recording AS recording_id, COUNT(track.id) AS track_appearances
    FROM track
    GROUP BY track.recording
)
SELECT COUNT(*) AS recordings_with_tracks,
       SUM(track_appearances) AS total_track_appearances,
       COUNT(*) FILTER (WHERE track_appearances = 1) AS used_once,
       COUNT(*) FILTER (WHERE track_appearances >= 2) AS used_at_least_twice,
       COUNT(*) FILTER (WHERE track_appearances >= 10) AS used_at_least_10,
       COUNT(*) FILTER (WHERE track_appearances >= 100) AS used_at_least_100,
       100.0 * COUNT(*) FILTER (WHERE track_appearances >= 2) / COUNT(*) AS reuse_share_pct
FROM recording_usage;

-- Query 2: structure of the largest raw track-count outlier.
SELECT recording.id AS recording_id, recording.name AS recording_name,
       release.id AS release_id, release.name AS release_name,
       COUNT(DISTINCT release.id) AS distinct_releases,
       COUNT(DISTINCT medium.id) AS distinct_mediums,
       COUNT(track.id) AS track_appearances,
       MIN(medium.track_count) AS min_tracks_on_a_medium,
       MAX(medium.track_count) AS max_tracks_on_a_medium
FROM recording
JOIN track ON track.recording = recording.id
JOIN medium ON medium.id = track.medium
JOIN release ON release.id = medium.release
WHERE recording.id = 42361496
GROUP BY recording.id, recording.name, release.id, release.name;

-- Query 3: all recordings with at least 100 track appearances.
WITH recording_usage AS (
    SELECT track.recording AS recording_id, COUNT(track.id) AS track_appearances
    FROM track
    GROUP BY track.recording
)
SELECT recording_usage.track_appearances, recording_usage.recording_id,
       COUNT(DISTINCT medium.id) AS distinct_mediums,
       COUNT(DISTINCT release.id) AS distinct_releases
FROM recording_usage
JOIN track ON track.recording = recording_usage.recording_id
JOIN medium ON medium.id = track.medium
JOIN release ON release.id = medium.release
WHERE recording_usage.track_appearances >= 100
GROUP BY recording_usage.track_appearances, recording_usage.recording_id
ORDER BY recording_usage.track_appearances DESC, recording_usage.recording_id;

-- Query 4: validation summary for the high-reuse perimeter.
WITH recording_usage AS (
    SELECT track.recording AS recording_id, COUNT(track.id) AS track_appearances
    FROM track
    GROUP BY track.recording
), recording_release_usage AS (
    SELECT recording_usage.track_appearances, recording_usage.recording_id,
           COUNT(DISTINCT medium.id) AS distinct_mediums,
           COUNT(DISTINCT release.id) AS distinct_releases
    FROM recording_usage
    JOIN track ON track.recording = recording_usage.recording_id
    JOIN medium ON medium.id = track.medium
    JOIN release ON release.id = medium.release
    WHERE recording_usage.track_appearances >= 100
    GROUP BY recording_usage.track_appearances, recording_usage.recording_id
)
SELECT COUNT(*) AS recording_count,
       MIN(track_appearances) AS min_track_appearances,
       COUNT(*) FILTER (WHERE distinct_mediums > track_appearances) AS track_medium_violations,
       COUNT(*) FILTER (WHERE distinct_releases > distinct_mediums) AS medium_release_violations
FROM recording_release_usage;
```

- [ ] **Step 4: Export checked CSVs directly from PostgreSQL**

Use `\copy` wrappers around the four query bodies. Export UTF-8 CSV with headers to the four exact data paths. Confirm `high-reuse-recordings.csv` has 3,767 lines including its header:

```sh
wc -l projects/03-recording-reuse/data/high-reuse-recordings.csv
```

Expected: `3767`.

- [ ] **Step 5: Commit the SQL evidence**

```sh
git add projects/03-recording-reuse/analysis.sql \
  projects/03-recording-reuse/checks.sql \
  projects/03-recording-reuse/data
git commit -m "feat: add recording reuse SQL evidence"
```

---

### Task 2: Checked data contract

**Files:**
- Create: `projects/03-recording-reuse/scripts/__init__.py`
- Create: `projects/03-recording-reuse/scripts/data_contract.py`
- Create: `projects/03-recording-reuse/tests/test_data_contract.py`

**Interfaces:**
- Consumes: the four CSV files from Task 1.
- Produces: `load_catalog_summary() -> dict[str, Decimal]`, `load_outlier() -> dict[str, str | int]`, `load_validation() -> dict[str, int]`, and `validate_evidence() -> None`.

- [ ] **Step 1: Write failing evidence tests**

```python
import unittest
from decimal import Decimal

from scripts.data_contract import (
    load_catalog_summary,
    load_outlier,
    load_validation,
    validate_evidence,
)


class DataContractTest(unittest.TestCase):
    def test_checked_catalog_metrics(self):
        metrics = load_catalog_summary()
        self.assertEqual(metrics["recordings_with_tracks"], Decimal("39332638"))
        self.assertEqual(metrics["total_track_appearances"], Decimal("56818950"))
        self.assertEqual(metrics["used_once"], Decimal("31924042"))
        self.assertEqual(metrics["used_at_least_twice"], Decimal("7408596"))
        self.assertEqual(metrics["used_at_least_10"], Decimal("244908"))
        self.assertEqual(metrics["used_at_least_100"], Decimal("3766"))
        self.assertEqual(metrics["reuse_share_pct"], Decimal("18.8357465370108153"))

    def test_outlier_arithmetic_and_hierarchy(self):
        outlier = load_outlier()
        self.assertEqual(outlier["recording_id"], 42361496)
        self.assertEqual(outlier["track_appearances"], 4320)
        self.assertEqual(outlier["distinct_mediums"], 180)
        self.assertEqual(outlier["distinct_releases"], 1)
        self.assertEqual(outlier["min_tracks_on_a_medium"], 24)
        self.assertEqual(outlier["max_tracks_on_a_medium"], 24)
        self.assertEqual(180 * 24, 4320)

    def test_validation_summary(self):
        validation = load_validation()
        self.assertEqual(validation["recording_count"], 3766)
        self.assertEqual(validation["min_track_appearances"], 100)
        self.assertEqual(validation["track_medium_violations"], 0)
        self.assertEqual(validation["medium_release_violations"], 0)
        validate_evidence()


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and verify it fails**

Run:

```sh
cd projects/03-recording-reuse
PYTHONPATH=. ../../.venv/bin/python -m unittest tests.test_data_contract -v
```

Expected: failure because `scripts.data_contract` does not exist.

- [ ] **Step 3: Implement the CSV loaders and validation**

Use `csv.DictReader`, `Decimal`, and exact paths relative to the project root. Parse integer fields as `int`, preserve names as strings, and raise `ValueError` when the outlier arithmetic or hierarchy checks fail. The public outlier CSV must include a `distinct_releases` column with value `1` even if the SQL export is grouped by one release.

- [ ] **Step 4: Run the evidence tests**

Run the command from Step 2.

Expected: three tests pass.

- [ ] **Step 5: Commit the data contract**

```sh
git add projects/03-recording-reuse/scripts \
  projects/03-recording-reuse/tests/test_data_contract.py
git commit -m "test: validate recording reuse evidence"
```

---

### Task 3: Original single-image visual

**Files:**
- Create: `projects/03-recording-reuse/scripts/build_visual.py`
- Create: `projects/03-recording-reuse/tests/test_visual.py`
- Create: `projects/03-recording-reuse/charts/recording-reuse.png`

**Interfaces:**
- Consumes: `load_outlier()` and `validate_evidence()` from `scripts.data_contract`.
- Produces: `medium_positions(columns: int = 15, rows: int = 12) -> list[tuple[int, int]]` and `build_visual(output_path: Path = PNG_PATH) -> Path`.

- [ ] **Step 1: Write the failing visual tests**

```python
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts.build_visual import build_visual, medium_positions


class VisualTest(unittest.TestCase):
    def test_medium_grid_contains_exactly_180_symbols(self):
        positions = medium_positions()
        self.assertEqual(len(positions), 180)
        self.assertEqual(len(set(positions)), 180)

    def test_visual_exports_expected_portrait_png(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "recording-reuse.png"
            build_visual(output)
            with Image.open(output) as image:
                self.assertEqual(image.size, (1200, 1500))
                self.assertIn(image.mode, {"RGB", "RGBA"})


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and verify they fail**

```sh
cd projects/03-recording-reuse
PYTHONPATH=. ../../.venv/bin/python -m unittest tests.test_visual -v
```

Expected: failure because `scripts.build_visual` does not exist.

- [ ] **Step 3: Implement the deterministic grid and renderer**

In `build_visual.py`:

- set `WIDTH = 1200`, `HEIGHT = 1500`, `COLUMNS = 15`, and `ROWS = 12`;
- use dark navy `#071521`, off-white `#F5F1E8`, cyan `#4DD6C8`, coral `#FF7657`, and muted blue `#7795A6`;
- load a system sans font with an explicit fallback;
- draw the headline `I thought this recording appeared everywhere.`;
- draw `4,320 TRACK ROWS` and `1 RELEASE` as the main contrast;
- draw a labeled release container containing the 15-by-12 grid;
- draw one shared `24 matching tracks per medium` annotation;
- draw `180 media x 24 tracks = 4,320`;
- draw `COUNT(track.id) vs COUNT(DISTINCT release.id)`;
- draw the recording name, hierarchy legend, snapshot, and catalog-data limit;
- save an optimized RGB PNG.

Keep `medium_positions()` independent of Pillow so its symbol count can be tested directly. Use the checked data values rather than hard-coding alternative values.

- [ ] **Step 4: Run tests, build the visual, and inspect it**

```sh
cd projects/03-recording-reuse
PYTHONPATH=. ../../.venv/bin/python -m unittest tests.test_data_contract tests.test_visual -v
../../.venv/bin/python scripts/build_visual.py
```

Expected: five passing tests and a 1200-by-1500 PNG. Inspect the image at original size and a 360-pixel-wide preview. Confirm readable type, exactly 180 visible symbols, and no resemblance to the prior beige bar charts.

- [ ] **Step 5: Commit the visual**

```sh
git add projects/03-recording-reuse/scripts/build_visual.py \
  projects/03-recording-reuse/tests/test_visual.py \
  projects/03-recording-reuse/charts/recording-reuse.png
git commit -m "feat: add recording reuse editorial visual"
```

---

### Task 4: Editorial package and claim ledger

**Files:**
- Create: `projects/03-recording-reuse/README.md`
- Create: `projects/03-recording-reuse/claim-ledger.md`
- Create: `projects/03-recording-reuse/data-post-brief.md`
- Create: `projects/03-recording-reuse/linkedin-post.md`
- Create: `projects/03-recording-reuse/accessibility.md`
- Create: `projects/03-recording-reuse/tests/test_package.py`
- Modify: `README.md`

**Interfaces:**
- Consumes: checked evidence and `charts/recording-reuse.png`.
- Produces: public explanations, one user-editable post draft, alt text, and a current series index.

- [ ] **Step 1: Write failing package tests**

Create tests that read the five Markdown files and assert:

```python
required_claims = [
    "39,332,638",
    "56,818,950",
    "18.8357465370108153%",
    "3,766",
    "4,320",
    "180",
    "24",
    "one release",
]
for claim in required_claims:
    self.assertIn(claim, combined_public_text)

self.assertIn("COUNT(track.id)", combined_public_text)
self.assertIn("COUNT(DISTINCT release.id)", combined_public_text)
self.assertIn("catalog", combined_public_text.lower())
self.assertNotIn("popularity", linkedin_text.lower())
self.assertNotIn("—", linkedin_text)
self.assertLessEqual(linkedin_text.count("🎧"), 1)
```

Also assert that the root `README.md` links episodes `02-name-join-explosion` and `03-recording-reuse` and labels episode three `Draft for review`.

- [ ] **Step 2: Run tests and verify they fail**

```sh
cd projects/03-recording-reuse
PYTHONPATH=. ../../.venv/bin/python -m unittest tests.test_package -v
```

Expected: failures because the editorial files do not exist.

- [ ] **Step 3: Write the claim ledger, brief, README, and accessibility text**

Use one ledger row per numerical claim. Every row must name `analysis.sql`, `checks.sql`, or an exact CSV. State that the outlier is a concentration example and does not prove broad reuse. Describe the image's one release container, 180 medium symbols, 24 matching rows per medium, equation, SQL method line, and catalog limitation in `accessibility.md`.

- [ ] **Step 4: Write the natural English draft**

Use this structure and preserve the verified meaning:

```text
🎧 I thought I had found one of the most reused recordings in MusicBrainz.

The query returned 4,320 track rows for one recording.
That looked enormous, so I checked the grain before drawing a conclusion.

The same recording appeared across only one release.
That release contains 180 media, and each one contains 24 track rows pointing
to the same recording: 180 x 24 = 4,320.

My SQL was counting correctly. My first interpretation of the count was not.

I built a recording-level CTE with COUNT(track.id), then followed
track -> medium -> release and compared the result with
COUNT(DISTINCT release.id). I also checked that track rows were never fewer
than distinct media, and that distinct media were never fewer than distinct
releases.

Across this MusicBrainz snapshot, 39,332,638 recordings have track rows.
7,408,596 of them appear at least twice, or 18.8357465370108153%.
Only 3,766 appear at least 100 times.

The lesson for me was simple: before interpreting a large count, I need to
state what one row represents and what the aggregate actually measures.

This is MusicBrainz catalog metadata from 2026-07-15. Track rows describe
placements on media. They are not plays, sales, or audience measurements.

Project:
https://github.com/leodid68/musicbrainz-sql-stories/tree/main/projects/03-recording-reuse
```

Keep this file explicitly labeled as a draft for Leo to rewrite.

- [ ] **Step 5: Update the root series index and run package tests**

Add episode two as published and episode three as `Draft for review`. Run all three project test modules.

Expected: all tests pass.

- [ ] **Step 6: Commit the editorial package**

```sh
git add README.md projects/03-recording-reuse
git commit -m "docs: add recording reuse story package"
```

---

### Task 5: Review bundle and end-to-end verification

**Files:**
- Create: `projects/03-recording-reuse/publish-ready/README.md`
- Create: `projects/03-recording-reuse/publish-ready/accessibility.txt`
- Create: `projects/03-recording-reuse/publish-ready/claim-ledger.md`
- Create: `projects/03-recording-reuse/publish-ready/linkedin-post.txt`
- Create: `projects/03-recording-reuse/publish-ready/publication-notes.md`
- Create: `projects/03-recording-reuse/publish-ready/recording-reuse.png`

**Interfaces:**
- Consumes: checked project artifacts from Tasks 1 through 4.
- Produces: one review bundle that is mechanically complete but explicitly marked `draft` until Leo approves his rewritten post.

- [ ] **Step 1: Copy only publication-facing artifacts**

Copy the rendered PNG, accessibility text, claim ledger, and current post draft. `publication-notes.md` must state:

```text
Status: draft, awaiting Leo's rewrite and final approval.
Planned publication: Friday, 24 July 2026.
Format: one static image plus text post.
Do not publish or push without explicit confirmation.
```

- [ ] **Step 2: Add bundle checks**

Extend `test_package.py` to assert the six expected publish-ready files exist, the PNG matches the source bytes, the post text matches `linkedin-post.md`, and the notes contain `Status: draft`.

- [ ] **Step 3: Run the complete local verification**

```sh
cd projects/03-recording-reuse
PYTHONPATH=. ../../.venv/bin/python -m unittest discover -s tests -v
cd ../..
git diff --check
git status --short
```

Expected: all tests pass, `git diff --check` has no output, and only intentional Task 5 files are uncommitted.

- [ ] **Step 4: Render and visually inspect the final PNG**

Inspect `charts/recording-reuse.png` and `publish-ready/recording-reuse.png` at full size. Confirm the 180-symbol grid is visible, the title and arithmetic are readable, the SQL line is secondary, and the footer does not compete with the main contrast.

- [ ] **Step 5: Commit the review bundle**

```sh
git add projects/03-recording-reuse/publish-ready \
  projects/03-recording-reuse/tests/test_package.py
git commit -m "chore: package recording reuse draft for review"
```

- [ ] **Step 6: Stop before external actions**

Show Leo the final visual, post draft, checked files, tests, and local commits. Request separate explicit confirmation before pushing the commits to GitHub. LinkedIn publication remains a separate later confirmation after Leo rewrites the post.
