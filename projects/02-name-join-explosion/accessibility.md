# Accessibility

## Static chart

The chart compares the MusicBrainz artist table before and after an exact-name
self-join. The original analysis contains 2.93 million artist rows. Joining
the table to itself on `artist.name` returns 5.38 million rows. The additional
2.45 million rows connect different MusicBrainz artist IDs that share the same
exact primary name. This is an 83.52% increase.

## PDF carousel

Page 1 introduces the central tension: a syntactically valid SQL join can
produce the wrong analytical grain. Page 2 explains the multiplication with
the name `Indigo`: 249 artist entities create 62,001 joined rows, including
61,752 rows connecting different IDs. Page 3 presents the before-and-after
comparison chart. Page 4 gives a three-part join checklist covering grain, key
meaning, and expected cardinality. Page 5 states the methodological limits and
previews a future analysis about tracks and recordings.
