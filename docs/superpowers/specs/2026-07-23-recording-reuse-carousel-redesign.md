# Recording Reuse Carousel Redesign

Date: 2026-07-23  
Project: MusicBrainz SQL Stories #3  
Status: approved direction, implementation pending

## Objective

Replace the planned single-image publication format with a five-page native
LinkedIn PDF carousel. The carousel must preserve the approved cobalt
editorial direction and turn the checked analysis into a short sequence:
initial interpretation, reveal, structure, SQL method, and lesson.

The approved LinkedIn post text remains unchanged.

## Deliverables

- five deterministic page PNGs, each 1200 × 1500 pixels;
- one five-page PDF using a consistent 4:5 page size;
- `recording-reuse.png` retained as the page-one cover/export;
- matching public and `publish-ready` copies;
- updated accessibility and publication notes;
- automated data, page-count, dimension, and package-integrity checks.

Proposed public outputs:

- `carousel/page-01-hook.png`
- `carousel/page-02-reveal.png`
- `carousel/page-03-structure.png`
- `carousel/page-04-sql.png`
- `carousel/page-05-lesson.png`
- `recording-reuse-carousel.pdf`

The publish-ready directory contains the same PDF and cover PNG.

## Data Contract

All numerical claims come from the checked 2026-07-15 MusicBrainz snapshot:

- 39,332,638 recordings have track rows;
- 7,408,596 have at least two track rows;
- the checked share is 18.8357465370108153%, displayed as 18.84%;
- 3,766 recordings have at least 100 track rows;
- recording ID 42361496 is `I Feel Bad For Your Hard Drive`;
- its largest raw result is 4,320 matching track rows;
- those rows occur in one distinct release, ID 5055218;
- that release contains 180 distinct media;
- every medium contains 24 matching track rows;
- `180 × 24 = 4,320`.

The entity interpretation must remain explicit:

- one recording is the underlying audio entity;
- one track row is that recording's placement on a medium;
- a medium belongs to a release;
- track rows are not plays, sales, listeners, or popularity.

## Shared Visual System

Every page uses:

- cobalt background: `#2446F5`;
- near-black structure: `#0B0D12`;
- paper white text: `#F7F7F2`;
- acid-yellow reveal: `#D8FF3E`;
- pale-blue supporting marks: `#B9C9FF`.

Avoid cream backgrounds, navy dashboard cards, rounded UI panels, gradients,
shadows, glass effects, and decorative interface chrome.

Typography should resemble a contemporary music or culture poster:

- large condensed or tightly spaced bold sans serif for key figures;
- clean sans serif for explanation and limitations;
- monospace treatment for SQL;
- strong asymmetry and generous margins;
- no paragraph smaller than the existing 28-pixel supporting-text floor.

Each page includes:

- `MUSICBRAINZ SQL STORIES / 03`;
- a discreet page number, `01 / 05` through `05 / 05`;
- consistent 72-pixel outer margins;
- no swipe bait or engagement request.

## Page Sequence

### Page 1 - Hook

Primary copy:

`I THOUGHT THIS RECORDING APPEARED EVERYWHERE.`

Supporting copy:

`The query returned 4,320 track rows for one recording.`

The number `4,320` dominates the page. Do not reveal the one-release result
yet. This page also becomes the standalone `recording-reuse.png` cover.

### Page 2 - Reveal

Primary contrast:

`4,320 TRACK ROWS`

`BUT ONLY`

`1 RELEASE`

Supporting copy:

`My SQL was counting correctly. My first interpretation was not.`

The `1 RELEASE` block uses near-black with acid-yellow emphasis. This is a
poster composition, not two metric cards.

### Page 3 - Exact structure

One near-black release boundary contains an exact 15-column × 12-row matrix,
totalling 180 media.

Every medium contains exactly 24 deterministic track markers. The renderer
therefore draws exactly 4,320 markers.

Required copy:

`ONE RELEASE / ID 5055218`

`180 MEDIA`

`24 MATCHING TRACK ROWS PER MEDIUM`

`180 × 24 = 4,320`

The matrix must read as texture at feed size and remain countable when opened.

### Page 4 - SQL and grain

Show the checked first CTE:

```sql
WITH recording_usage AS (
    SELECT track.recording AS recording_id,
           COUNT(track.id) AS track_appearances
    FROM track
    GROUP BY track.recording
)
```

Required explanation:

`One result row = one recording`

`COUNT(track.id) answers: How many track rows?`

`It does not answer: Across how many releases?`

Then show:

`track → medium → release`

`COUNT(DISTINCT release.id)`

The SQL must remain legible at mobile-feed size.

### Page 5 - Lesson and limitation

Primary copy:

`A CORRECT COUNT CAN STILL SUPPORT A WRONG INTERPRETATION.`

Supporting copy:

`Before interpreting an aggregate, state what one row represents and what the
count actually measures.`

Boundary:

`MusicBrainz full export / 2026-07-15`

`Catalog metadata, not plays, sales, audience, or popularity.`

End with the project identifier, not an invented publication URL:

`github.com/leodid68/musicbrainz-sql-stories`

## PDF Construction

- Build each page as a deterministic RGB PNG at 1200 × 1500.
- Use ReportLab to place each PNG on a 576 × 720 point PDF page.
- Keep all five PDF pages exactly the same size.
- Set PDF metadata:
  - title: `MusicBrainz SQL Stories 03 - One Recording, 4,320 Track Rows`;
  - author: `Léo Didier`;
  - subject: `SQL grain, track rows, media, and release structure`.
- Do not add animation, layers, crop marks, or external fonts to the PDF.
- Keep the final PDF below LinkedIn's 100 MB document limit.

## Accessibility

The publication package must include a concise page-by-page description.
Important claims also remain in the LinkedIn post text, so the PDF is not the
only carrier of the evidence.

## Validation

Automated checks must confirm:

- exactly five source PNG pages exist;
- every PNG is 1200 × 1500 and RGB or RGBA;
- page 3 has exactly 180 medium positions;
- every medium has exactly 24 marker positions;
- total deterministic markers equal 4,320;
- the PDF has exactly five pages;
- all PDF pages have identical 576 × 720 point media boxes;
- PDF metadata matches the specification;
- the PDF remains below 100 MB;
- public and publish-ready PDF copies are byte-identical;
- the standalone cover equals page 1;
- all existing evidence and package tests still pass.

Render the completed PDF back to PNG using Poppler. Inspect all five rendered
pages for clipping, overlap, missing glyphs, weak contrast, and mobile
legibility before asking Leo for final visual approval.

## Status Boundary

The package remains `draft - final text approved; carousel review pending`
until Leo has reviewed the rendered five-page PDF. GitHub push, LinkedIn
upload, scheduling, and publication remain separate actions.
