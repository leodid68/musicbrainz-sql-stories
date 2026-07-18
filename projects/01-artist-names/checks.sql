\set ON_ERROR_STOP on

DO $$
DECLARE
    total_artists bigint;
    duplicated_names bigint;
    duplicated_entities numeric;
    top_name text;
    top_count bigint;
BEGIN
    SELECT COUNT(*) INTO total_artists FROM artist;
    IF total_artists <> 2931347 THEN
        RAISE EXCEPTION 'artist count mismatch: %', total_artists;
    END IF;

    WITH name_counts AS (
        SELECT name, COUNT(*) AS entity_count
        FROM artist
        GROUP BY name
        HAVING COUNT(*) > 1
    )
    SELECT COUNT(*), SUM(entity_count)
    INTO duplicated_names, duplicated_entities
    FROM name_counts;

    IF duplicated_names <> 126415 THEN
        RAISE EXCEPTION 'duplicated name count mismatch: %', duplicated_names;
    END IF;
    IF duplicated_entities <> 419770 THEN
        RAISE EXCEPTION 'duplicated entity count mismatch: %', duplicated_entities;
    END IF;

    SELECT name, COUNT(*)
    INTO top_name, top_count
    FROM artist
    WHERE name NOT IN ('[unknown]', '[no artist]')
    GROUP BY name
    HAVING COUNT(*) > 1
    ORDER BY COUNT(*) DESC, name ASC
    LIMIT 1;

    IF top_name <> 'Indigo' OR top_count <> 249 THEN
        RAISE EXCEPTION 'top name mismatch: % (%)', top_name, top_count;
    END IF;
END
$$;

SELECT 'analysis checks passed' AS result;

