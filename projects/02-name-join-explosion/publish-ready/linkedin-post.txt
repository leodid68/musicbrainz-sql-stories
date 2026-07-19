🎧 A SQL query can run perfectly and still create the wrong dataset.

In the first episode, I found 126,415 exact artist names used by multiple
MusicBrainz entities.

For the second episode of my SQL series, I tested the practical consequence:

What happens if two copies of the artist table are joined on `name` instead of
a stable artist ID?

Before the join, the analysis contained 2,931,345 artist rows.

After joining on the exact primary name:

• 5,379,621 rows were returned
• 2,448,276 rows connected different MusicBrainz artist IDs
• The row count increased by 83.52%

For `Indigo` alone, 249 artist entities generated 62,001 joined rows. Of
those, 61,752 connected different IDs.

The SQL was valid. The join condition was the problem.

A join key does not always need to be unique. One-to-many relationships can be
intentional. But before trusting a join, I should be able to state:

• what one row represents in each input
• whether the key identifies an entity or only describes it
• which cardinality I expect after the join

Here, `artist.name` is an attribute. `artist.id` and `artist.gid` are stable
catalog identifiers.

This was a controlled self-join using exact primary names from the 2026-07-15
MusicBrainz snapshot. Aliases, `[unknown]`, and `[no artist]` were excluded.
Different MusicBrainz IDs mean different catalog entities, not necessarily
different real-world people or groups.

Built with PostgreSQL.

🔍 Next, I want to test another identity problem: why a track is not always the
same thing as a recording.

Project:
https://github.com/leodid68/musicbrainz-sql-stories/tree/main/projects/02-name-join-explosion
