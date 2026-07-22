# Draft for Leo to rewrite

This is an editable draft, not final publication copy.

🎧 I thought I had found one of the most reused recordings in MusicBrainz.

The query returned 4,320 track rows for one recording.
That looked enormous, so I checked the grain before drawing a conclusion.

The same recording appeared across only one release.
That release contains 180 media, and each one contains 24 track rows pointing
to the same recording: 180 x 24 = 4,320.

My SQL was counting correctly. My first interpretation of the count was not.

I built a recording-level CTE with `COUNT(track.id)`, then followed
`track -> medium -> release` and compared the result with
`COUNT(DISTINCT release.id)`. I also checked that track rows were never fewer
than distinct media, and that distinct media were never fewer than distinct
releases.

Across this MusicBrainz snapshot, 39,332,638 recordings have track rows.
7,408,596 of them have at least two track rows, or 18.84%.
Only 3,766 appear at least 100 times.

The lesson for me was simple: before interpreting a large count, I need to
state what one row represents and what the aggregate actually measures.

This is MusicBrainz catalog metadata from 2026-07-15. Track rows describe
placements on media. They are not plays, sales, or audience measurements.

Project:
https://github.com/leodid68/musicbrainz-sql-stories/tree/main/projects/03-recording-reuse
