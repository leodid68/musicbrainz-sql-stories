🎧 Can an artist name be used as an identifier?

I am starting a small SQL series using MusicBrainz, an open and
community-maintained music metadata catalog.

For this first analysis, I explored 2.9 million artist entities stored in a
local PostgreSQL database.

My question was simple:

How often is the same exact name used by several artist entities?

I found:

• 126,415 exact names used by multiple entities  
• 419,770 artist entities affected  
• Indigo was the most duplicated name in the filtered ranking, with 249
entities across 52 non-null areas

The SQL used GROUP BY, HAVING, a CTE, COUNT(*), and SUM().

But the main lesson is about data modeling:

A name is an attribute, not a reliable identifier.

Joining tables using artist names could silently connect unrelated people or
groups. Stable identifiers, such as MusicBrainz IDs, are much safer.

This analysis only considers exact primary names. Aliases are excluded. I also
excluded [unknown] and [no artist] from the ranking.

MusicBrainz catalog counts are not measures of streams, sales, audience size,
or popularity.

Built with PostgreSQL and Plotly.

🔍 Next, I will test what actually happens when artist names are used as join
keys.

Project: https://github.com/leodid68/musicbrainz-sql-stories/tree/main/projects/01-artist-names
