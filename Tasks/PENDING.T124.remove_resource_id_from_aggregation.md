# T124 – Remove resource_id from Resource_Aggregation

**Status**: Pending  
**Task Type**: Refactor  
**Run Mode**: Sequential  

## User inputs (edit before running)

- **Dictionary file** `../configurator/dictionaries/Resource_Aggregation.0.1.0.yaml`
- **Configuration file** `../configurator/configurations/Resource_Aggregation.yaml`
- **Enumerators file** `../configurator/enumerators/enumerations.0.yaml`

## Goal

Remove the redundant **`resource_id`** property from the Resource_Aggregation dictionary. The aggregation document's **`_id`** is the Resource `$oid` — one aggregation per resource, keyed by `_id` instead of a separate `resource_id` field.

## Context / Input files

These files must be treated as **inputs** and read before implementation:

- [Tasks/README.md](./README.md) — task workflow and change control.
- [Data standards](../../mentorhub/DeveloperEdition/standards/data_standards.md)
- `../configurator/dictionaries/Resource_Aggregation.0.1.0.yaml` — current schema (note: `file_name` in the YAML header currently reads `Resource_Ratings.1.0.0.yaml`; correct it to `Resource_Aggregation.0.1.0.yaml` and set `root.name` to `Resource_Aggregation` while editing)
- `../configurator/configurations/Resource_Aggregation.yaml` — collection config and indexes
- [SHIPPED.T122.generate_resource_aggregation_test_data.md](./SHIPPED.T122.generate_resource_aggregation_test_data.md) — prior aggregation test-data model (`_id` + `resource_id` both present today)
- `../mentorhub_mentee_api/src/services/aggregation_service.py` — currently queries `{"resource_id": resource_object_id}`; **out of scope** for this repo task but noted for downstream API work

### Current Resource_Aggregation properties (0.1.0)

| Property | Type | Notes |
| --- | --- | --- |
| `_id` | identifier | Today: sequential `C000…` ids (T122) |
| `resource_id` | identifier | **Remove** — duplicate of Resource `$oid` |
| `note_count` | count | |
| `completions` | count | |
| `hits` | count | |
| `duration` | duration | |
| `rating_count` | count | |
| `rating_sum` | count | required |
| `created` | breadcrumb | |
| `last_saved` | breadcrumb | |

### Current configuration index

`Resource_Aggregation.yaml` version `0.1.0.0` defines a non-unique index on `resource_id`. After this change, aggregation lookups use `_id` (the Resource `$oid`); remove the `resource_id` index.

## Requirements

1. **Dictionary change only** — update `Resource_Aggregation.0.1.0.yaml` and `Resource_Aggregation.yaml`; do **not** modify test data in this task (T125 handles test data).

2. **Remove `resource_id`** property from `Resource_Aggregation.0.1.0.yaml` `root.properties`.

3. **Fix dictionary metadata** while editing:
   - `file_name: Resource_Aggregation.0.1.0.yaml`
   - `root.name: Resource_Aggregation`
   - `root.description` — keep or refine (resource-level rating, duration, and note metrics)

4. **Update configuration** `Resource_Aggregation.yaml`:
   - Remove the `resource_id` index from `add_indexes` for version `0.1.0.0`.
   - Do **not** add a redundant index on `_id` (MongoDB already indexes `_id`).

5. **Pre-release** — edit existing **0.1.0** dictionary and configuration in place; no version bump or migration pipeline.

6. **Leave test data unchanged** — configure-database will fail validation until T125 migrates `Resource_Aggregation.0.1.0.0.json`. That is expected; document the failure in implementation notes if configure does not pass.

## Testing expectations

- Run `make container` — build succeeds.
- Configure-database (`POST /api/configurations/`) may **fail** until T125 ships — that is acceptable for this schema-only task. If it fails, confirm the error is specifically about `resource_id` still present in test data (or missing required fields), not a dictionary/config syntax error.

## Dependencies / Ordering

- **Runs after** T123 (same refactor sequence; no hard dependency, but keep task order T123 → T124 → T125).
- **Blocks** — T125 (test data) depends on this schema change.

## Change control checklist

- [ ] Reviewed all **Context / Input files**.
- [ ] Designed approach documented in this file.
- [ ] Updated `Resource_Aggregation.0.1.0.yaml` (removed `resource_id`, fixed metadata).
- [ ] Updated `Resource_Aggregation.yaml` (removed `resource_id` index).
- [ ] Ran `make container` successfully.
- [ ] Documented configure-database result (pass or expected fail pending T125).
- [ ] Created a scoped commit referencing T124.

## Implementation notes (to be updated by the agent)

**Summary of changes**

_To be filled in by the executing agent._

**Testing results**

_To be filled in by the executing agent._
