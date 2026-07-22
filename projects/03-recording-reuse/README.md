# A large count can hide a narrow concentration

## Question

When one MusicBrainz recording has thousands of track rows, does that mean it
appears across thousands of releases?

## Data and grain

- MusicBrainz full export: 2026-07-15
- One `recording` row represents a distinct audio or mix in the catalog
- One `track` row represents that recording's placement on one medium
- Checked exports contain only aggregated evidence, not the database dump

## Checked findings

- 39,332,638 recordings have at least one track row
- Those recordings account for 56,818,950 track rows
- 31,924,042 recordings appear once, while 7,408,596 appear at least twice
- The share appearing at least twice is 18.8357465370108153%
- 244,908 recordings have at least 10 track rows, and 3,766 have at least 100
- The largest raw count is 4,320 track rows, but they are concentrated in one
  release with 180 media and 24 matching track rows per medium

The outlier is a concentration example. It does not prove that this recording
is broadly reused across the catalog.

## SQL method

The analysis first creates one row per recording with `COUNT(track.id)`. It
then follows `track -> medium -> release` and compares the raw track-row count
with `COUNT(DISTINCT release.id)`. Independent checks confirm that track rows
are never fewer than distinct media and distinct media are never fewer than
distinct releases in the high-reuse result.

## Limitation

MusicBrainz is a community-maintained metadata catalog. Track rows describe
placements on media. They are not plays, sales, or audience measurements.
The figures describe the 2026-07-15 snapshot and may reflect unusual catalog
structures, including repeated media within one release.

## Outputs

- [SQL analysis](analysis.sql)
- [Independent checks](checks.sql)
- [Catalog summary](data/catalog-summary.csv)
- [High-reuse recordings](data/high-reuse-recordings.csv)
- [Outlier structure](data/outlier-structure.csv)
- [Validation summary](data/validation-summary.csv)
- [Static visual](charts/recording-reuse.png)
- [Data post brief](data-post-brief.md)
- [LinkedIn draft](linkedin-post.md)
- [Claim ledger](claim-ledger.md)
- [Accessibility text](accessibility.md)

## Reproduce

Run `checks.sql` and `analysis.sql` against the MusicBrainz PostgreSQL
snapshot. Then test the checked exports and public package from this directory:

```sh
PYTHONPATH=. ../../.venv/bin/python -m unittest discover -s tests -v
```
