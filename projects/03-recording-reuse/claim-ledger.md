# Claim ledger

Each row records one numerical claim used in the public package. The outlier
is a concentration example, not proof of broad reuse across the catalog.

| Numerical claim | Verified evidence | Reproduction path | Limitation |
|---|---|---|---|
| 39,332,638 recordings have track rows | `recordings_with_tracks` | `analysis.sql`, `checks.sql`, and `data/catalog-summary.csv` | Counts catalog records in this snapshot |
| The recordings account for 56,818,950 track rows | `total_track_appearances` from `COUNT(track.id)` | `analysis.sql`, `checks.sql`, and `data/catalog-summary.csv` | Track rows are placements on media, not listening events |
| 31,924,042 recordings have one track row | `used_once` | `analysis.sql`, `checks.sql`, and `data/catalog-summary.csv` | Exact count for this snapshot |
| 7,408,596 recordings have at least two track rows | `used_at_least_twice` | `analysis.sql`, `checks.sql`, and `data/catalog-summary.csv` | Multiple rows can be concentrated within one release |
| 18.8357465370108153% of recordings with track rows have at least two | `reuse_share_pct` | `analysis.sql`, `checks.sql`, and `data/catalog-summary.csv` | Denominator is recordings with at least one track row |
| 244,908 recordings have at least 10 track rows | `used_at_least_10` | `analysis.sql`, `checks.sql`, and `data/catalog-summary.csv` | Track count does not measure audience reach |
| 3,766 recordings have at least 100 track rows | `used_at_least_100` and `recording_count` | `analysis.sql`, `checks.sql`, `data/catalog-summary.csv`, and `data/validation-summary.csv` | Threshold describes raw track rows |
| The largest raw result has 4,320 track rows | `track_appearances` | `analysis.sql`, `checks.sql`, `data/high-reuse-recordings.csv`, and `data/outlier-structure.csv` | A concentration example, not evidence of broad reuse |
| Those 4,320 rows belong to one release | `distinct_releases` equals 1 | `analysis.sql`, `checks.sql`, `data/high-reuse-recordings.csv`, and `data/outlier-structure.csv` | One catalog release may contain many media |
| The release contains 180 distinct media | `distinct_mediums` | `analysis.sql`, `checks.sql`, `data/high-reuse-recordings.csv`, and `data/outlier-structure.csv` | Media count is not release count |
| Each of the 180 media has 24 matching track rows | 4,320 track rows divided by 180 media, with both medium track-count bounds equal to 24 | `analysis.sql`, `checks.sql`, and `data/outlier-structure.csv` | Describes this unusual release structure |
| 180 media x 24 matching track rows equals 4,320 | Derived from the checked outlier fields | `checks.sql` and `data/outlier-structure.csv` | Explains concentration within one release only |

The SQL also checks the ordering expected from the catalog hierarchy:
`COUNT(track.id)` is at least the distinct-medium count, which is at least
`COUNT(DISTINCT release.id)`, for every recording in the 100-or-more perimeter.
The result is recorded in `checks.sql` and `data/validation-summary.csv`.
