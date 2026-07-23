# Accessibility

## Five-page PDF carousel

All five portrait pages use cobalt blue, near-black, warm white, pale blue,
and acid yellow in a high-contrast editorial layout.

### Page 1: Hook

Large type reads "4,320 track rows for one recording" followed by "I thought
this recording appeared everywhere." The footer identifies the MusicBrainz
full export dated 2026-07-15.

### Page 2: Reveal

The page contrasts "4,320 track rows" with "but only 1 release." It names the
recording "I Feel Bad For Your Hard Drive" and release ID 5055218. Supporting
text says the SQL counted correctly but the first interpretation did not.

### Page 3: Exact structure

One dark container represents release 5055218. Inside it, 180 small medium
symbols form a 15 by 12 grid. Every medium contains 24 acid-yellow markers,
for 4,320 visible markers in total. The equation reads "180 media x 24
matching track rows = 4,320," and the relationship is
`release -> medium -> track`.

### Page 4: SQL grain

The page shows the `recording_usage` CTE using `COUNT(track.id)` and
`GROUP BY track.recording`. It explains that one result row represents one
recording. `COUNT(track.id)` answers how many track rows exist; following
`track -> medium -> release` and using `COUNT(DISTINCT release.id)` checks
across how many releases they occur.

### Page 5: Lesson and limit

The main statement reads: "A correct count can still support a wrong
interpretation." The page advises stating what one row represents and what an
aggregate measures before interpreting it. It closes with the boundary that
these figures are MusicBrainz catalog metadata, not plays, sales, audience, or
popularity. The 4,320-row result is concentration within one release, not
evidence of broad reuse.
