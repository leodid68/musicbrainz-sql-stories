\set ON_ERROR_STOP on

-- Query 1: demonstrate the effect on the most duplicated filtered name.
WITH indigo_artists AS (
    SELECT
        id,
        name
    FROM artist
    WHERE name = 'Indigo'
)
SELECT
    l.name,
    COUNT(*) AS name_join_rows,
    COUNT(*) FILTER (WHERE l.id <> r.id) AS cross_entity_matches
FROM indigo_artists AS l
JOIN indigo_artists AS r
  ON l.name = r.name
GROUP BY l.name;

-- Query 2: rank the exact names that create the most cross-entity matches.
WITH name_counts AS (
    SELECT
        name,
        COUNT(*) AS entity_count
    FROM artist
    WHERE name NOT IN ('[unknown]', '[no artist]')
    GROUP BY name
    HAVING COUNT(*) > 1
)
SELECT
    name,
    entity_count,
    entity_count * entity_count AS name_join_rows,
    entity_count * (entity_count - 1) AS cross_entity_matches
FROM name_counts
ORDER BY cross_entity_matches DESC, name ASC
LIMIT 10;

-- Query 3: measure the catalog-wide impact.
WITH name_counts AS (
    SELECT
        name,
        COUNT(*) AS entity_count
    FROM artist
    WHERE name NOT IN ('[unknown]', '[no artist]')
    GROUP BY name
)
SELECT
    SUM(entity_count) AS original_artist_rows,
    SUM(entity_count * entity_count) AS name_join_rows,
    SUM(entity_count * (entity_count - 1)) AS cross_entity_matches,
    ROUND(
        100.0 * SUM(entity_count * (entity_count - 1))
        / SUM(entity_count),
        2
    ) AS row_increase_pct
FROM name_counts;

-- Query 4: independently reproduce the modeled totals with an actual join.
SELECT
    COUNT(*) AS name_join_rows,
    COUNT(*) FILTER (WHERE l.id <> r.id) AS cross_entity_matches
FROM artist AS l
JOIN artist AS r
  ON l.name = r.name
WHERE l.name NOT IN ('[unknown]', '[no artist]');
