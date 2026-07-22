# Data Post Brief

## Purpose

**Audience:** Data practitioners, hiring teams, and people learning SQL

**Professional objective:** Show how defining grain and checking aggregation
levels can change the interpretation of a correct query

**Series and episode:** MusicBrainz SQL Stories #3

**Language:** Simple English

## Evidence

**Core question:** Does a very large track-row count mean that a recording is
reused across many releases?

**Catalog summary:** 39,332,638 recordings account for 56,818,950 track rows.
7,408,596 recordings appear at least twice, or 18.8357465370108153%. Of the
recordings with track rows, 31,924,042 appear once, 244,908 appear at least 10
times, and 3,766 appear at least 100 times.

**Outlier structure:** The largest raw result has 4,320 track rows. Those rows
are concentrated in one release containing 180 media, with 24 matching track
rows per medium counted directly in a per-medium CTE: 180 x 24 = 4,320.

**Reproduction path:** `analysis.sql`, `checks.sql`, the exact CSV files in
`data/`, and `claim-ledger.md`

**Dataset grain and snapshot:** One row per MusicBrainz recording in the
first CTE; one track row is one placement on a medium; 2026-07-15 full export

**Limitation:** MusicBrainz is a metadata catalog. Track rows are not plays,
sales, or audience measurements. The outlier shows concentration within one
unusual release and does not prove broad reuse.

## Story

**Hook:** I thought I had found one of the most reused recordings in
MusicBrainz.

**Turn:** The 4,320 rows were real, but all of them came from one release.

**Technical lesson:** Start by stating the result grain. Compare
`COUNT(track.id)` with `COUNT(DISTINCT release.id)` before interpreting a large
aggregate.

**Professional meaning:** A correct count can still support a wrong first
interpretation if the counted entity is unclear.

## Visual

**Format:** One static editorial diagram

**Visual question:** How can one release produce 4,320 track rows for the same
recording?

**Visual answer:** One release contains 180 medium symbols. Each symbol stands
for a medium with 24 matching track rows, giving 180 x 24 = 4,320.

**Method line:** `COUNT(track.id)` versus `COUNT(DISTINCT release.id)`

## Publication package

**Post text:** `linkedin-post.md`, explicitly a draft for Leo to rewrite

**Repository link:** https://github.com/leodid68/musicbrainz-sql-stories/tree/main/projects/03-recording-reuse

**Status:** Draft for review
