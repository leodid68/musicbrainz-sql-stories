🎧 I thought I had found one of the most reused recordings in MusicBrainz.

The query returned 4,320 track rows for one recording.
That looked enormous, so I checked the grain before drawing a conclusion.

All 4,320 track rows came from a single release.
That release contains 180 media, and each one contains 24 matching track rows:

180 × 24 = 4,320.

My SQL was counting correctly.
My first interpretation of the count was not.

Across this MusicBrainz snapshot, 39,332,638 recordings have track rows.
7,408,596 of them have at least two track rows, or 18.84%.
Only 3,766 have at least 100 track rows.

The first step was to change the result grain:

WITH recording_usage AS (
    SELECT track.recording AS recording_id,
           COUNT(track.id) AS track_appearances
    FROM track
    GROUP BY track.recording
)

This CTE returns one row per recording and counts how many track rows point to it.

But it only answers: “How many track rows?”
It does not answer: “Across how many releases?”

That is why I then followed track → medium → release and compared the count with COUNT(DISTINCT release.id).

The lesson for me was simple: before interpreting a large count, I need to state what one row represents and what the aggregate actually measures.

This is MusicBrainz catalog metadata from 2026-07-15. Track rows describe placements on media. They are not plays, sales, or audience measurements.

Project:
https://github.com/leodid68/musicbrainz-sql-stories/tree/main/projects/03-recording-reuse
