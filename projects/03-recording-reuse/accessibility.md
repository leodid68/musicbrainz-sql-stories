# Accessibility

## Static visual

The dark navy visual is titled "I thought this recording appeared everywhere."
Near the top, it contrasts 4,320 track rows with one release for the recording
"I Feel Bad For Your Hard Drive."

A large outlined container represents that one release. Inside it are 180
small turquoise medium symbols arranged in a grid. Each medium symbol contains
an orange mark for the matching recording, and the legend says that each
medium has 24 matching track rows, counted directly from `track.id`. Below the
container, the equation reads: "180 media x 24 tracks = 4,320."

The relationship line reads `release -> medium -> track`. The SQL method line
compares `COUNT(track.id)` with `COUNT(DISTINCT release.id)`.

The visual closes with the data boundary: MusicBrainz full export dated
2026-07-15. These figures describe catalog metadata, not plays, sales, or
audience measurements. The 4,320-row outlier is a concentration within one
release and does not prove broad reuse across the catalog.
