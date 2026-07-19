# Claim ledger

| Claim | Verified evidence | Reproduction path | Limitation |
|---|---|---|---|
| 2,931,345 artist rows enter the analysis | `SUM(entity_count)` after exclusions | Run `analysis.sql` and `checks.sql` | Excludes `[unknown]` and `[no artist]` |
| The name join produces 5,379,621 rows | Count model and actual self-join agree | Run queries 3 and 4 in `analysis.sql` | Controlled self-join, not an observed production incident |
| 2,448,276 rows connect different artist IDs | `l.id <> r.id` and the count model agree | Run `analysis.sql` and `checks.sql` | Different catalog IDs do not prove different real-world people |
| The row count increases by 83.52% | Cross-entity matches divided by original rows | Run query 3 in `analysis.sql` | Percentage describes this snapshot and exact-name rule |
| Indigo has 249 entities | Direct filtered count | Run `checks.sql` | Exact primary name only |
| Indigo produces 62,001 joined rows | Actual self-join and `249 * 249` | Run query 1 in `analysis.sql` | Demonstration of join cardinality |
| 61,752 Indigo rows connect different IDs | `COUNT(*) FILTER (WHERE l.id <> r.id)` | Run query 1 in `analysis.sql` | Cross-entity catalog matches, not proven false people matches |
