\set ON_ERROR_STOP on

-- Query 1: catalog-wide recording usage distribution.
DROP TABLE IF EXISTS pg_temp.recording_reuse_catalog_summary;
CREATE TEMP TABLE recording_reuse_catalog_summary AS
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

SELECT * FROM recording_reuse_catalog_summary;

-- Query 2: structure of the largest raw track-count outlier.
DROP TABLE IF EXISTS pg_temp.recording_reuse_outlier_structure;
CREATE TEMP TABLE recording_reuse_outlier_structure AS
WITH outlier_medium_usage AS (
    SELECT recording.id AS recording_id, recording.name AS recording_name,
           release.id AS release_id, release.name AS release_name,
           medium.id AS medium_id,
           COUNT(track.id) AS matching_track_rows
    FROM recording
    JOIN track ON track.recording = recording.id
    JOIN medium ON medium.id = track.medium
    JOIN release ON release.id = medium.release
    WHERE recording.id = 42361496
    GROUP BY recording.id, recording.name, release.id, release.name, medium.id
)
SELECT recording_id, recording_name,
       MIN(release_id) AS release_id,
       MIN(release_name) AS release_name,
       COUNT(DISTINCT release_id) AS distinct_releases,
       COUNT(DISTINCT medium_id) AS distinct_mediums,
       SUM(matching_track_rows) AS track_appearances,
       MIN(matching_track_rows) AS min_matching_track_rows_per_medium,
       MAX(matching_track_rows) AS max_matching_track_rows_per_medium
FROM outlier_medium_usage
GROUP BY recording_id, recording_name;

SELECT * FROM recording_reuse_outlier_structure;

-- Query 3: all recordings with at least 100 track appearances.
DROP TABLE IF EXISTS pg_temp.recording_reuse_high_reuse_recordings;
CREATE TEMP TABLE recording_reuse_high_reuse_recordings AS
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

SELECT *
FROM recording_reuse_high_reuse_recordings
ORDER BY track_appearances DESC, recording_id;

-- Query 4: validation summary for the high-reuse perimeter.
DROP TABLE IF EXISTS pg_temp.recording_reuse_validation_summary;
CREATE TEMP TABLE recording_reuse_validation_summary AS
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

SELECT * FROM recording_reuse_validation_summary;
