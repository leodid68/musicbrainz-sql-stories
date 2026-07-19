\set ON_ERROR_STOP on

DO $$
DECLARE
    original_artist_rows numeric;
    modeled_name_join_rows numeric;
    modeled_cross_entity_matches numeric;
    row_increase_pct numeric;
    actual_name_join_rows bigint;
    actual_cross_entity_matches bigint;
    indigo_entities bigint;
    indigo_name_join_rows bigint;
    indigo_cross_entity_matches bigint;
BEGIN
    WITH name_counts AS (
        SELECT name, COUNT(*) AS entity_count
        FROM artist
        WHERE name NOT IN ('[unknown]', '[no artist]')
        GROUP BY name
    )
    SELECT
        SUM(entity_count),
        SUM(entity_count * entity_count),
        SUM(entity_count * (entity_count - 1)),
        ROUND(
            100.0 * SUM(entity_count * (entity_count - 1))
            / SUM(entity_count),
            2
        )
    INTO
        original_artist_rows,
        modeled_name_join_rows,
        modeled_cross_entity_matches,
        row_increase_pct
    FROM name_counts;

    SELECT
        COUNT(*),
        COUNT(*) FILTER (WHERE l.id <> r.id)
    INTO actual_name_join_rows, actual_cross_entity_matches
    FROM artist AS l
    JOIN artist AS r
      ON l.name = r.name
    WHERE l.name NOT IN ('[unknown]', '[no artist]');

    SELECT COUNT(*)
    INTO indigo_entities
    FROM artist
    WHERE name = 'Indigo';

    SELECT
        COUNT(*),
        COUNT(*) FILTER (WHERE l.id <> r.id)
    INTO indigo_name_join_rows, indigo_cross_entity_matches
    FROM artist AS l
    JOIN artist AS r
      ON l.name = r.name
    WHERE l.name = 'Indigo';

    IF original_artist_rows <> 2931345 THEN
        RAISE EXCEPTION 'original artist row mismatch: %',
            original_artist_rows;
    END IF;
    IF modeled_name_join_rows <> 5379621 THEN
        RAISE EXCEPTION 'modeled name join row mismatch: %',
            modeled_name_join_rows;
    END IF;
    IF modeled_cross_entity_matches <> 2448276 THEN
        RAISE EXCEPTION 'modeled cross-entity mismatch: %',
            modeled_cross_entity_matches;
    END IF;
    IF row_increase_pct <> 83.52 THEN
        RAISE EXCEPTION 'row increase percentage mismatch: %',
            row_increase_pct;
    END IF;
    IF actual_name_join_rows <> modeled_name_join_rows THEN
        RAISE EXCEPTION 'actual/model name join mismatch: % versus %',
            actual_name_join_rows, modeled_name_join_rows;
    END IF;
    IF actual_cross_entity_matches <> modeled_cross_entity_matches THEN
        RAISE EXCEPTION 'actual/model cross-entity mismatch: % versus %',
            actual_cross_entity_matches, modeled_cross_entity_matches;
    END IF;
    IF indigo_entities <> 249 THEN
        RAISE EXCEPTION 'Indigo entity mismatch: %', indigo_entities;
    END IF;
    IF indigo_name_join_rows <> 62001 THEN
        RAISE EXCEPTION 'Indigo join row mismatch: %',
            indigo_name_join_rows;
    END IF;
    IF indigo_cross_entity_matches <> 61752 THEN
        RAISE EXCEPTION 'Indigo cross-entity mismatch: %',
            indigo_cross_entity_matches;
    END IF;
END
$$;

SELECT 'name join analysis checks passed' AS result;
