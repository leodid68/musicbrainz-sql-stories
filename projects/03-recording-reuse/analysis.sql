\set ON_ERROR_STOP on

-- Query 1: catalog-wide recording usage distribution.
WITH recording_usage AS (
    SELECT track.recording AS recording_id, COUNT(track.id) AS track_appearances
    FROM track
    GROUP BY track.recording
)
SELECT COUNT(*) AS recordings_with_tracks,
       SUM(track_appearances) AS total_track_appearances,
       COUNT(*) FILTER (WHERE track_appearances = 1) AS used_once,
       COUNT(*) FILTER (WHERE track_appearances >= 2) AS used_at_least_twice,
       COUNT(*) FILTER (WHERE track_appearances >= 10) AS used_at_least_10,
       COUNT(*) FILTER (WHERE track_appearances >= 100) AS used_at_least_100,
       100.0 * COUNT(*) FILTER (WHERE track_appearances >= 2) / COUNT(*) AS reuse_share_pct
FROM recording_usage;

-- Query 2: structure of the largest raw track-count outlier.
SELECT recording.id AS recording_id, recording.name AS recording_name,
       release.id AS release_id, release.name AS release_name,
       COUNT(DISTINCT release.id) AS distinct_releases,
       COUNT(DISTINCT medium.id) AS distinct_mediums,
       COUNT(track.id) AS track_appearances,
       MIN(medium.track_count) AS min_tracks_on_a_medium,
       MAX(medium.track_count) AS max_tracks_on_a_medium
FROM recording
JOIN track ON track.recording = recording.id
JOIN medium ON medium.id = track.medium
JOIN release ON release.id = medium.release
WHERE recording.id = 42361496
GROUP BY recording.id, recording.name, release.id, release.name;

-- Query 3: all recordings with at least 100 track appearances.
WITH recording_usage AS (
    SELECT track.recording AS recording_id, COUNT(track.id) AS track_appearances
    FROM track
    GROUP BY track.recording
)
SELECT recording_usage.track_appearances, recording_usage.recording_id,
       COUNT(DISTINCT medium.id) AS distinct_mediums,
       COUNT(DISTINCT release.id) AS distinct_releases
FROM recording_usage
JOIN track ON track.recording = recording_usage.recording_id
JOIN medium ON medium.id = track.medium
JOIN release ON release.id = medium.release
WHERE recording_usage.track_appearances >= 100
GROUP BY recording_usage.track_appearances, recording_usage.recording_id
ORDER BY recording_usage.track_appearances DESC, recording_usage.recording_id;

-- Query 4: validation summary for the high-reuse perimeter.
WITH recording_usage AS (
    SELECT track.recording AS recording_id, COUNT(track.id) AS track_appearances
    FROM track
    GROUP BY track.recording
), recording_release_usage AS (
    SELECT recording_usage.track_appearances, recording_usage.recording_id,
           COUNT(DISTINCT medium.id) AS distinct_mediums,
           COUNT(DISTINCT release.id) AS distinct_releases
    FROM recording_usage
    JOIN track ON track.recording = recording_usage.recording_id
    JOIN medium ON medium.id = track.medium
    JOIN release ON release.id = medium.release
    WHERE recording_usage.track_appearances >= 100
    GROUP BY recording_usage.track_appearances, recording_usage.recording_id
)
SELECT COUNT(*) AS recording_count,
       MIN(track_appearances) AS min_track_appearances,
       COUNT(*) FILTER (WHERE distinct_mediums > track_appearances) AS track_medium_violations,
       COUNT(*) FILTER (WHERE distinct_releases > distinct_mediums) AS medium_release_violations
FROM recording_release_usage;
