# Publication claim ledger

| Claim | Verified evidence | Reproduction path | Limitation |
|---|---|---|---|
| 2,931,347 artist entities | `checks.sql` and `artist` count | Run `../checks.sql` | Catalog entities, not unique people or popularity |
| 126,415 duplicated exact names | `name_counts` CTE | Run `../analysis.sql` and `../checks.sql` | Exact primary names; case-sensitive comparison |
| 419,770 affected artist entities | `SUM(entity_count)` | Run `../analysis.sql` and `../checks.sql` | Includes special-purpose names in the aggregate |
| Indigo maps to 249 entities | Filtered ranking and checked CSV | Rebuild the CSV from `../analysis.sql` | `[unknown]` and `[no artist]` excluded |
| Indigo covers 52 non-null areas | `COUNT(DISTINCT artist.area)` | Rebuild the CSV from `../analysis.sql` | Missing areas are not counted |
