# T125 – Align Journey Ratings and Resource_Aggregation Test Data

**Status**: Shipped  
**Task Type**: Feature  
**Run Mode**: Sequential  

## User inputs (edit before running)

- **Journey test-data file** `../configurator/test_data/Journey.0.1.0.0.json`
- **Resource_Aggregation test-data file** `../configurator/test_data/Resource_Aggregation.0.1.0.0.json`
- **Rating test-data file (read-only source)** `../configurator/test_data/Rating.0.1.0.0.json`
- **Resource test-data file** `../configurator/test_data/Resource.0.1.0.0.json`
- **Note test-data file** `../configurator/test_data/Note.0.1.0.0.json`
- **Event test-data file** `../configurator/test_data/Event.0.1.0.0.json`
- **Generator scripts** (update as needed):
  - `Tasks/scripts/generate_resource_aggregation_test_data.py`
  - `Tasks/scripts/generate_rating_test_data.py` (deprecate or repoint — see **Generator scripts** below)

## Goal

Update test data so Journey **library** entries carry per-mentee **`rating`** values, Resource_Aggregation documents use the Resource `$oid` as **`_id`** (no `resource_id` field), and aggregation **`rating_sum`** / **`rating_count`** are consistent with the sum of library ratings across all mentee journeys.

## Context / Input files

These files must be treated as **inputs** and read before implementation:

- [Tasks/README.md](./README.md) — task workflow and change control.
- [Data standards](../../mentorhub/DeveloperEdition/standards/data_standards.md)
- `../configurator/dictionaries/Journey.0.1.0.yaml` — T123: `library.rating` (type `rating`, 1–4)
- `../configurator/dictionaries/Resource_Aggregation.0.1.0.yaml` — T124: no `resource_id`
- `../configurator/test_data/Rating.0.1.0.0.json` — T120: 88 ratings (one per library completion); **source of truth** for rating values to copy onto Journey library entries
- `../configurator/test_data/Journey.0.1.0.0.json` — T117 template + T118 mentee journeys
- `../configurator/test_data/Resource_Aggregation.0.1.0.0.json` — T122: 456 aggregations
- [SHIPPED.T118.generate_mentee_journey_test_data.md](./SHIPPED.T118.generate_mentee_journey_test_data.md)
- [SHIPPED.T120.generate_rating_test_data.md](./SHIPPED.T120.generate_rating_test_data.md)
- [SHIPPED.T122.generate_resource_aggregation_test_data.md](./SHIPPED.T122.generate_resource_aggregation_test_data.md)
- [SHIPPED.T123.add_journey_library_rating.md](./SHIPPED.T123.add_journey_library_rating.md) — must be shipped first
- [SHIPPED.T124.remove_resource_id_from_aggregation.md](./SHIPPED.T124.remove_resource_id_from_aggregation.md) — must be shipped first

### Rating alignment rule

For every Resource `$oid` that appears in any mentee Journey `library`:

| Check | Rule |
| --- | --- |
| **Per library entry** | Each completed `library` item has a `rating` integer 1–4 matching the T120 Rating for that `(profile_id, resource_id)` pair |
| **Per resource aggregation** | `rating_count` = number of library entries across all mentee journeys for that resource |
| **Per resource aggregation** | `rating_sum` = sum of all `library[].rating` values for that resource across all mentee journeys |
| **Consistency** | Sum of library ratings for a resource **must equal** that resource's aggregation `rating_sum` |

### Resource_Aggregation `_id` migration

**Before** removing `resource_id` from each aggregation document:

1. Set `_id` to the current `resource_id` `$oid` value (the Resource `$oid`).
2. Remove the `resource_id` property from the document.
3. Preserve all other fields (`note_count`, `completions`, `hits`, `duration`, `rating_count`, `rating_sum`, `created`, `last_saved`).

Example transformation:

```json
// Before (T122)
{
  "_id": { "$oid": "C00000000000000000000001" },
  "resource_id": { "$oid": "B00000000000000000000001" },
  "rating_sum": 0,
  ...
}

// After (T125)
{
  "_id": { "$oid": "B00000000000000000000001" },
  "rating_sum": 0,
  ...
}
```

Sort output by `_id` (Resource `$oid`) for stable diffs.

## Requirements

### 1. Journey test data — add `library.rating`

- Walk every **mentee** Journey document (those with `profile_id`; skip T117 template `ffff00000000000000000001`).
- For each `library` entry, add `rating` (integer 1–4) by matching T120 `Rating.0.1.0.0.json` on **`profile_id`** + **`resource_id`**.
- Every library entry must have a `rating` after this task (88 entries across seven mentees per T120).
- Preserve existing `resource_id`, `started`, `completed`, and `used` values.
- Do **not** add `rating` to `now` or `next` sections.

### 2. Resource_Aggregation test data — migrate `_id`, drop `resource_id`

- For all **456** aggregation documents (per T122):
  - Replace `_id` with the former `resource_id` `$oid`.
  - Remove `resource_id`.
- Recompute **`rating_count`** and **`rating_sum`** from Journey `library` ratings (not from `Rating.0.1.0.0.json` at runtime — the Journey file is the persisted source after this task).
- Keep `note_count`, `completions`, and `hits` logic aligned with T122 (Notes, Journey library counts, Events) unless recomputation is required to stay consistent.
- Verify: for every aggregation, `rating_sum` equals the sum of `library[].rating` for that Resource `$oid` across all mentee journeys.

### 3. Validation spot-checks

After migration, confirm these T120/T122 exemplars still hold (values may shift only if recomputation changes them — document any deltas):

| Resource `$oid` | Resource name | Expected completions | Notes |
| --- | --- | --- | --- |
| `B00000000000000000000107` | Stackshare | 7 | Shared EngineerKit; 7 distinct library ratings |
| `B00000000000000000000108` | StackOverflow survey | 7 | Shared EngineerKit |
| `B00000000000000000000001` | A11y | 0 | `rating_count` / `rating_sum` = 0 |

Print or record a summary table in implementation notes: total library ratings (88), total `rating_sum` across all aggregations, and count of resources with `rating_count` > 0 (~30 per T122).

### 4. Generator scripts

- Update `Tasks/scripts/generate_resource_aggregation_test_data.py`:
  - Emit `_id` = Resource `$oid` (no `resource_id`).
  - Derive `rating_count` / `rating_sum` from Journey `library[].rating` instead of `Rating.0.1.0.0.json`.
- Update or annotate `Tasks/scripts/generate_rating_test_data.py` — ratings now live on Journey library entries; script should either write ratings into Journey (preferred) or be marked deprecated in implementation notes. Do **not** leave scripts that regenerate stale `Rating.0.1.0.0.json` without a comment.

### 5. Rating collection test data

- Leave `Rating.0.1.0.0.json` unchanged in this task unless configure-database fails because of it. If removal is required, note as a follow-up task rather than expanding scope here.

### 6. EJSON encoding

- `_id` and Resource references as `{ "$oid": "..." }`.
- `rating` as a plain integer (1–4), not `$numberInt`.
- Breadcrumb `at_time` as `{ "$date": "..." }`.

## Testing expectations

- Run `make container` — build succeeds.
- `curl -X DELETE "http://localhost:8385/api/database/"` → SUCCESS
- `curl -X POST "http://localhost:8385/api/configurations/"` → SUCCESS
- If configure fails, inspect error JSON and fix test data.

### Post-configure sanity script (optional but recommended)

Run a quick local validation (Python or `jq`) that asserts:

- 88 library entries across mentee journeys have `rating` ∈ {1, 2, 3, 4}.
- No Resource_Aggregation document contains `resource_id`.
- Every aggregation `_id` matches a Resource `$oid` referenced on a mentee Journey.
- For each aggregation, `rating_sum` equals the sum of matching Journey library ratings.

## Dependencies / Ordering

- **T123** — Journey dictionary `library.rating` must be shipped.
- **T124** — Resource_Aggregation dictionary without `resource_id` must be shipped.
- **T118, T120, T121, T122** — prior test data tasks (already shipped).

## Change control checklist

- [x] Reviewed all **Context / Input files**.
- [x] Designed approach documented in this file.
- [x] Updated `Journey.0.1.0.0.json` with `library.rating` on all 88 completed entries.
- [x] Migrated `Resource_Aggregation.0.1.0.0.json` (`_id` = Resource `$oid`, no `resource_id`).
- [x] Verified `rating_sum` alignment between Journey library and aggregations.
- [x] Updated generator script(s) as needed.
- [x] Ran `make container` successfully.
- [x] Ran configure-database curl commands successfully.
- [x] Created a scoped commit referencing T125.

## Implementation notes (to be updated by the agent)

**Summary of changes**

- Applied 88 T120 rating values onto Journey `library` entries via `Tasks/scripts/apply_journey_library_ratings_from_rating.py`.
- Regenerated 456 Resource_Aggregation documents via updated `Tasks/scripts/generate_resource_aggregation_test_data.py` (`_id` = Resource `$oid`, no `resource_id`; ratings derived from Journey library).
- Updated `Tasks/scripts/generate_rating_test_data.py` to write ratings onto Journey library entries (legacy `Rating.0.1.0.0.json` no longer generated).
- Left `Rating.0.1.0.0.json` unchanged.

**Rating alignment summary**

| Metric | Value |
| --- | --- |
| Library entries with `rating` | 88 |
| Total `rating_sum` (all aggregations) | 252 |
| Resources with `rating_count` > 0 | 30 |

**Spot-checks**

| Resource `$oid` | completions | rating_count | rating_sum |
| --- | --- | --- | --- |
| `B00000000000000000000107` (Stackshare) | 7 | 7 | 15 |
| `B00000000000000000000108` (StackOverflow survey) | 7 | 7 | 16 |
| `B00000000000000000000001` (A11y) | 0 | 0 | 0 |

**Testing results**

- Local validation script → all assertions passed.
- `make container` → SUCCESS.
- `DELETE /api/database/` on port 8385 → SUCCESS.
- `POST /api/configurations/` on port 8385 → SUCCESS.
