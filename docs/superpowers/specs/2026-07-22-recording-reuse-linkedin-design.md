# MusicBrainz SQL Stories #3: design specification

## Objective

Package the verified recording-reuse analysis as a public project and a
LinkedIn draft. The central lesson is that a correct row count can still be
misinterpreted when the result grain is unclear.

The episode remains a draft until the generated artifacts, claims, links, and
copy have been checked. Publishing and pushing to GitHub require Leo's explicit
confirmation immediately before those actions.

## Evidence and scope

The source is the local MusicBrainz PostgreSQL snapshot dated 2026-07-15.
Public claims may use only checked SQL outputs:

- 39,332,638 recordings have at least one track row.
- Those recordings account for 56,818,950 track appearances.
- 31,924,042 recordings appear once.
- 7,408,596 appear at least twice, equal to 18.8357465370108153% of recordings
  with tracks.
- 244,908 appear at least ten times.
- 3,766 appear at least one hundred times.
- Recording 42361496, `I Feel Bad For Your Hard Drive`, has 4,320 track rows
  but belongs to one distinct release.
- That release contains 180 media; every relevant medium contains 24 track
  rows, so 180 multiplied by 24 equals 4,320.
- For the 3,766-recording validation perimeter, the minimum track count is 100
  and both tested hierarchy violations return zero.

The analysis describes MusicBrainz catalog metadata, not plays, sales,
popularity, audience size, or audio content. A track is a recording's placement
on a medium, not a unique song or an observed listen.

## Static visual

Create one portrait image at 1200 by 1500 pixels. It must not reuse the beige
bar-chart language of episodes one and two.

Use a dark navy editorial background with off-white type and one vivid accent.
The page contains:

1. A short headline built around the mistaken first interpretation.
2. The contrast `4,320 track rows` versus `1 release`.
3. One outlined release container holding exactly 180 small medium symbols in
   a 15-by-12 grid.
4. A clear equation: `180 media x 24 tracks = 4,320`.
5. The recording name and a compact hierarchy legend:
   `release -> medium -> track`.
6. A restrained footer naming the MusicBrainz snapshot and catalog-data
   limitation.

The 180 symbols communicate structure rather than decorative density. They do
not each need a `24` label; one shared annotation states that every represented
medium contributes 24 matching track rows. Text must remain legible in the
LinkedIn feed and the image must still communicate when viewed without the
post body.

## LinkedIn draft

Write in simple first-person English. The draft should sound like a learner
describing a real correction, not like a polished motivational template.

Narrative order:

1. The count of 4,320 initially looked like broad reuse.
2. Counting distinct releases reduced the apparent breadth to one release.
3. Inspecting the medium grain explained the count: 180 media with 24 matching
   tracks each.
4. The query was valid, but the first interpretation of its unit was not.
5. The transferable lesson is to define one output row and the unit of every
   aggregate before interpreting a large number.
6. State the catalog-data limitation and link to the public project with a
   placeholder until the GitHub path is confirmed.

Use at most one functional emoji. Do not use engagement bait, an emoji list,
causal claims, popularity language, em dashes, or an invented next episode.
Leo will rewrite the draft in his own voice before it can become ready.

## Public project package

Create `projects/03-recording-reuse/` with the same durable categories as the
first two episodes, while using a single-image publication format:

- `README.md`
- `analysis.sql`
- `checks.sql`
- `claim-ledger.md`
- `data-post-brief.md`
- `linkedin-post.md`
- `accessibility.md`
- checked CSV exports under `data/`
- the source and rendered static visual under `charts/`
- reproducible build scripts under `scripts/`
- focused tests under `tests/`
- a `publish-ready/` package containing only reviewed publication artifacts

Private coaching notes and conversation transcripts must not enter the public
repository.

## Reproduction and validation

The build must derive displayed values from checked data files rather than
duplicating numbers manually across scripts. Tests must confirm:

- the image dimensions;
- the presence of exactly 180 medium symbols;
- the arithmetic 180 x 24 = 4,320;
- agreement between SQL outputs, CSVs, the claim ledger, the visual, and the
  post draft;
- the limitation language;
- the absence of placeholders in the publish-ready package, except for an
  explicitly documented repository URL before push.

Render the image and inspect it visually at full size and at a reduced feed-like
size. Verify the full project locally before requesting approval to push.

