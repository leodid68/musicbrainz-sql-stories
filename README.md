# MusicBrainz SQL Stories

Small, reproducible analyses of the MusicBrainz community-maintained metadata
catalog. The series starts with SQL foundations and adds tools only when they
improve reproducibility, validation, or communication.

## Projects

### [01. Artist names are not identifiers](projects/01-artist-names/)

How often does one exact primary name refer to several MusicBrainz artist
entities?

Status: local draft ready for review.

### [02. A valid SQL join can still create the wrong dataset](projects/02-name-join-explosion/)

What happens when two copies of the artist table are joined on an exact name
instead of a stable catalog identifier?

Status: Published.

Published: 22 July 2026 ([LinkedIn post](https://www.linkedin.com/posts/leodidierfr_sql-stories-p2-ugcPost-7484575799333875712-oHDE)).

### [03. A large count can hide a narrow concentration](projects/03-recording-reuse/)

Does a recording with 4,320 track rows really appear across thousands of
releases?

Status: Draft for review.

## Data boundary

The local database uses the MusicBrainz full export dated 2026-07-15. This
repository contains only small checked exports. It does not contain the
database dump, database volumes, or credentials.

MusicBrainz catalog counts are not measures of streams, sales, audience size,
or popularity.
