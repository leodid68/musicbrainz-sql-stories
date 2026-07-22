\set ON_ERROR_STOP on
\set export_csv true

-- Execute the analysis queries once and write each result as its committed CSV.
\ir analysis.sql
