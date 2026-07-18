# Artist names are not identifiers

## Question

How often does the same exact primary artist name refer to different
MusicBrainz artist entities?

## Data

- MusicBrainz full export: 2026-07-15
- Grain: one row in `artist` is one MusicBrainz artist entity
- Exact primary names only
- Aliases excluded

The published ranking excludes `[unknown]` and `[no artist]`. MusicBrainz is a
community-maintained metadata catalog. These counts are not measures of
streams, sales, audience size, or popularity.

## Checked findings

- 2,931,347 artist entities
- 126,415 exact names used by several artist entities
- 419,770 artist entities covered by those names
- Indigo leads the filtered ranking with 249 entities

## Outputs

- [SQL analysis](analysis.sql)
- [Independent checks](checks.sql)
- [Checked chart data](data/top-duplicated-names.csv)
- [Static Plotly chart](charts/top-duplicated-names.png)
- [Interactive Plotly chart](charts/top-duplicated-names.html)
- [Five-page PDF carousel](output/pdf/musicbrainz-sql-stories-01.pdf)
- [LinkedIn draft](linkedin-post.md)
- [Claim ledger](claim-ledger.md)
- [Accessibility text](accessibility.md)
- [LinkedIn publish-ready package](publish-ready/README.md)

## Reproduce

Run `checks.sql` and `analysis.sql` against the MusicBrainz PostgreSQL snapshot.
Then create the Python environment from the repository root:

```sh
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
```

Build the visual package:

```sh
cd projects/01-artist-names
../../.venv/bin/python scripts/build_chart.py
../../.venv/bin/python scripts/build_carousel.py
PYTHONPATH=. ../../.venv/bin/python -m unittest discover -s tests -v
```
