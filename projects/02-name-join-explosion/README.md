# A valid SQL join can still create the wrong dataset

## Question

What happens when two copies of the MusicBrainz `artist` table are joined on
the exact primary artist name instead of a stable artist identifier?

## Data

- MusicBrainz full export: 2026-07-15
- Source grain: one `artist` row is one MusicBrainz artist entity
- Exact primary `artist.name` values only
- `[unknown]` and `[no artist]` excluded
- Aliases excluded

## Checked findings

- 2,931,345 artist rows enter the analysis
- An exact-name self-join produces 5,379,621 rows
- 2,448,276 joined rows connect different MusicBrainz artist IDs
- The join increases the row count by 83.52%
- For `Indigo`, 249 entities produce 62,001 joined rows, including 61,752
  cross-entity matches

## Technical lesson

SQL can be syntactically valid and still produce the wrong analytical grain.
A join key does not always need to be unique, because one-to-many joins can be
intentional. The analyst must define the grain of both inputs and validate the
expected cardinality before trusting the result.

## Limitations

This is a controlled self-join between identical table snapshots, not an
observed production incident. A cross-entity match means that two different
MusicBrainz artist IDs were connected by the exact same primary name. It does
not establish whether the catalog entities represent different real-world
people or groups.

## Outputs

- [SQL analysis](analysis.sql)
- [Independent checks](checks.sql)
- [Checked chart data](data/join-impact.csv)
- [Static Plotly chart](charts/name-join-impact.png)
- [Interactive Plotly chart](charts/name-join-impact.html)
- [Five-page PDF carousel](output/pdf/musicbrainz-sql-stories-02.pdf)
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

Build and test the visual package:

```sh
cd projects/02-name-join-explosion
../../.venv/bin/python scripts/build_chart.py
../../.venv/bin/python scripts/build_carousel.py
PYTHONPATH=. ../../.venv/bin/python -m unittest discover -s tests -v
```
