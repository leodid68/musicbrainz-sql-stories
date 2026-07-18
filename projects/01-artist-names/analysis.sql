\set ON_ERROR_STOP on

-- Query 1: inspect exact names used by several artist entities.
SELECT
    a.name,
    COUNT(*) AS artist_entities
FROM artist AS a
WHERE a.name <> '[no artist]'
  AND a.name <> '[unknown]'
GROUP BY a.name
HAVING COUNT(*) > 1
ORDER BY artist_entities DESC, a.name ASC
LIMIT 10;

-- Query 2: count duplicated names and the entities they cover.
WITH name_counts AS (
    SELECT
        a.name,
        COUNT(*) AS entity_count
    FROM artist AS a
    GROUP BY a.name
    HAVING COUNT(*) > 1
)
SELECT
    COUNT(*) AS duplicated_names,
    SUM(entity_count) AS entities_with_duplicated_name
FROM name_counts;

-- Enriched data used by the Plotly visual.
SELECT
    a.name,
    COUNT(*) AS artist_entities,
    COUNT(DISTINCT a.type) AS distinct_types,
    COUNT(DISTINCT a.area) AS distinct_areas
FROM artist AS a
WHERE a.name NOT IN ('[unknown]', '[no artist]')
GROUP BY a.name
HAVING COUNT(*) > 1
ORDER BY artist_entities DESC, a.name ASC
LIMIT 10;

\copy (SELECT a.name, COUNT(*) AS artist_entities, COUNT(DISTINCT a.type) AS distinct_types, COUNT(DISTINCT a.area) AS distinct_areas FROM artist AS a WHERE a.name NOT IN ('[unknown]', '[no artist]') GROUP BY a.name HAVING COUNT(*) > 1 ORDER BY artist_entities DESC, a.name ASC LIMIT 10) TO '/Users/leodidier/Developer/musicbrainz-sql-stories/projects/01-artist-names/data/top-duplicated-names.csv' WITH (FORMAT CSV, HEADER);
