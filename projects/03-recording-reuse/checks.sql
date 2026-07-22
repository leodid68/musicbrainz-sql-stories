\set ON_ERROR_STOP on

DO $$
DECLARE
    recordings_with_tracks bigint;
    total_track_appearances bigint;
    used_once bigint;
    used_at_least_twice bigint;
    used_at_least_10 bigint;
    used_at_least_100 bigint;
    reuse_share numeric;
    outlier_release_count bigint;
    outlier_medium_count bigint;
    outlier_track_count bigint;
    outlier_release_id integer;
    outlier_release_name text;
    outlier_min_matching_track_rows bigint;
    outlier_max_matching_track_rows bigint;
    track_medium_violations bigint;
    medium_release_violations bigint;
BEGIN
    WITH recording_usage AS (
        SELECT track.recording AS recording_id, COUNT(track.id) AS track_appearances
        FROM track
        GROUP BY track.recording
    )
    SELECT
        COUNT(*),
        SUM(track_appearances),
        COUNT(*) FILTER (WHERE track_appearances = 1),
        COUNT(*) FILTER (WHERE track_appearances >= 2),
        COUNT(*) FILTER (WHERE track_appearances >= 10),
        COUNT(*) FILTER (WHERE track_appearances >= 100),
        100.0 * COUNT(*) FILTER (WHERE track_appearances >= 2) / COUNT(*)
    INTO recordings_with_tracks, total_track_appearances, used_once,
         used_at_least_twice, used_at_least_10, used_at_least_100, reuse_share
    FROM recording_usage;

    IF recordings_with_tracks <> 39332638 THEN
        RAISE EXCEPTION 'recording count mismatch: %', recordings_with_tracks;
    END IF;
    IF total_track_appearances <> 56818950 THEN
        RAISE EXCEPTION 'track total mismatch: %', total_track_appearances;
    END IF;
    IF used_once <> 31924042 OR used_at_least_twice <> 7408596 THEN
        RAISE EXCEPTION 'reuse threshold mismatch: % / %', used_once, used_at_least_twice;
    END IF;
    IF used_at_least_10 <> 244908 OR used_at_least_100 <> 3766 THEN
        RAISE EXCEPTION 'high reuse threshold mismatch: % / %', used_at_least_10, used_at_least_100;
    END IF;
    IF reuse_share <> 18.8357465370108153 THEN
        RAISE EXCEPTION 'reuse share mismatch: %', reuse_share;
    END IF;

    WITH outlier_medium_usage AS (
        SELECT release.id AS release_id, release.name AS release_name,
               medium.id AS medium_id,
               COUNT(track.id) AS matching_track_rows
        FROM track
        JOIN medium ON medium.id = track.medium
        JOIN release ON release.id = medium.release
        WHERE track.recording = 42361496
        GROUP BY release.id, release.name, medium.id
    )
    SELECT MIN(release_id), MIN(release_name),
           COUNT(DISTINCT release_id), COUNT(DISTINCT medium_id),
           SUM(matching_track_rows), MIN(matching_track_rows),
           MAX(matching_track_rows)
    INTO outlier_release_id, outlier_release_name,
         outlier_release_count, outlier_medium_count, outlier_track_count,
         outlier_min_matching_track_rows, outlier_max_matching_track_rows
    FROM outlier_medium_usage;

    IF outlier_release_id <> 5055218
       OR outlier_release_name <> 'I Feel Bad For Your Hard Drive'
       OR outlier_release_count <> 1 OR outlier_medium_count <> 180
       OR outlier_track_count <> 4320
       OR outlier_min_matching_track_rows <> 24
       OR outlier_max_matching_track_rows <> 24 THEN
        RAISE EXCEPTION 'outlier structure mismatch: release % (%), % releases, % media, % matching rows, min %, max %',
            outlier_release_id, outlier_release_name, outlier_release_count,
            outlier_medium_count, outlier_track_count,
            outlier_min_matching_track_rows,
            outlier_max_matching_track_rows;
    END IF;

    WITH recording_usage AS (
        SELECT track.recording AS recording_id, COUNT(track.id) AS track_appearances
        FROM track
        GROUP BY track.recording
    ), recording_release_usage AS (
        SELECT recording_usage.recording_id, recording_usage.track_appearances,
               COUNT(DISTINCT medium.id) AS distinct_mediums,
               COUNT(DISTINCT release.id) AS distinct_releases
        FROM recording_usage
        JOIN track ON track.recording = recording_usage.recording_id
        JOIN medium ON medium.id = track.medium
        JOIN release ON release.id = medium.release
        WHERE recording_usage.track_appearances >= 100
        GROUP BY recording_usage.recording_id, recording_usage.track_appearances
    )
    SELECT
        COUNT(*) FILTER (WHERE distinct_mediums > track_appearances),
        COUNT(*) FILTER (WHERE distinct_releases > distinct_mediums)
    INTO track_medium_violations, medium_release_violations
    FROM recording_release_usage;

    IF track_medium_violations <> 0 OR medium_release_violations <> 0 THEN
        RAISE EXCEPTION 'hierarchy violations: % / %',
            track_medium_violations, medium_release_violations;
    END IF;
END
$$;

SELECT 'recording reuse checks passed' AS result;
