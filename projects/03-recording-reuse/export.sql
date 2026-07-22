\set ON_ERROR_STOP on

-- Materialize the four analysis results once in this psql session.
\ir analysis.sql

\copy (SELECT * FROM recording_reuse_catalog_summary) TO 'projects/03-recording-reuse/data/catalog-summary.csv' WITH (FORMAT csv, HEADER, ENCODING 'UTF8')
\copy (SELECT * FROM recording_reuse_outlier_structure) TO 'projects/03-recording-reuse/data/outlier-structure.csv' WITH (FORMAT csv, HEADER, ENCODING 'UTF8')
\copy (SELECT * FROM recording_reuse_high_reuse_recordings ORDER BY track_appearances DESC, recording_id) TO 'projects/03-recording-reuse/data/high-reuse-recordings.csv' WITH (FORMAT csv, HEADER, ENCODING 'UTF8')
\copy (SELECT * FROM recording_reuse_validation_summary) TO 'projects/03-recording-reuse/data/validation-summary.csv' WITH (FORMAT csv, HEADER, ENCODING 'UTF8')
