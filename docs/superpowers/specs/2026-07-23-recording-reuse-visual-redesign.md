# Recording Reuse Visual Redesign

Date: 2026-07-23  
Project: MusicBrainz SQL Stories #3  
Status: approved direction, implementation pending

## Objective

Redesign the episode-three static visual as a bold editorial poster rather
than a corporate dashboard. Preserve every checked data relationship and keep
the visual reproducible from the existing CSV evidence.

The poster must communicate one reveal:

> 4,320 track rows, but only one release.

## Data Contract

The visual must load the existing checked export and display:

- 4,320 track rows
- 1 distinct release
- 180 distinct media
- 24 matching track rows per medium
- `180 × 24 = 4,320`
- MusicBrainz snapshot date: 2026-07-15
- recording: `I Feel Bad For Your Hard Drive`
- release ID: `5055218`

The limitations remain:

- track rows are catalog placements, not plays;
- track rows are not sales or audience measurements;
- the outlier does not demonstrate broad reuse across releases.

## Art Direction

Use a full-bleed electric editorial palette:

- cobalt background: `#2446F5`
- near-black structure: `#0B0D12`
- paper white text: `#F7F7F2`
- acid-yellow reveal: `#D8FF3E`
- pale-blue supporting marks: `#B9C9FF`

Avoid cream backgrounds, navy dashboard panels, rounded cards, gradients,
glass effects, shadows, and decorative interface chrome.

Typography should feel like a music or culture poster:

- condensed or tightly spaced bold sans serif for the main figures;
- clean sans serif for labels and limitations;
- monospace only where it improves the SQL line;
- strong scale contrast and asymmetric alignment.

## Composition

Canvas remains 1200 × 1500 pixels.

### 1. Masthead

Keep `MUSICBRAINZ SQL STORIES / 03` small and secondary.

### 2. Split revelation

The upper portion is a single typographic composition:

- `4,320` is the dominant figure;
- `TRACK ROWS` explains the measure;
- `BUT ONLY` acts as a small transition;
- `1 RELEASE` is the acid-yellow reveal.

Do not place these values in separate dashboard cards.

### 3. Exact release structure

The lower-middle section contains one near-black rectangular release boundary.
It must visibly contain an exact 15-column × 12-row matrix, totaling 180 media.

Each medium symbol contains exactly 24 small deterministic track markers.
The generated poster therefore contains 4,320 track markers in total, rather
than merely claiming the multiplication in a legend.

The matrix should read first as texture at feed size and become countable on
closer inspection.

### 4. Equation and method

Display:

`180 MEDIA × 24 MATCHING TRACK ROWS = 4,320`

Keep the SQL comparison secondary:

`COUNT(track.id) vs COUNT(DISTINCT release.id)`

Avoid enclosing the SQL line in a dashboard-style card.

### 5. Footer

Include the snapshot and limitation:

`MusicBrainz full export / 2026-07-15`

`Catalog metadata, not plays, sales, or popularity.`

## Implementation Boundaries

- Modify the deterministic Pillow renderer, not the evidence files.
- Keep the existing output paths:
  - `charts/recording-reuse.png`
  - `publish-ready/recording-reuse.png`
- Do not change the approved LinkedIn text.
- Do not change checked CSV values or SQL.
- Preserve the 4:5 feed format.
- Keep required supporting text readable at a 30% preview.

## Validation

Automated checks must confirm:

- output is exactly 1200 × 1500;
- the visual contains exactly 180 medium positions;
- each medium contains exactly 24 track-marker positions;
- total visual markers equal 4,320;
- both PNG copies are byte-identical;
- required labels, equation, snapshot, and limitation remain represented by
  the renderer;
- all existing evidence and package tests still pass.

The final rendered PNG must also receive a visual inspection at original size
and feed-preview size before the visual status can move from `draft` to
`ready`.
