# T110 – Clear Resource and Path Test Data

**Status**: Shipped  
**Task Type**: Chore  
**Run Mode**: Sequential  

## User inputs (edit before running)

- **Target test-data files to clear**:
  - `../configurator/test_data/Resource.0.1.0.0.json`
  - `../configurator/test_data/Path.0.1.0.0.json`
  - `../configurator/test_data/Resource_Aggregation.0.1.0.0.json`
- **Replacement value**: `[]` (empty JSON array) in each file.

## Goal

Remove legacy EngineerKit-harvested Resource and Path seed data so subsequent tasks can rebuild test data from Mike's Obsidian vault exports.

## Context / Input files

These files must be treated as **inputs** and read before implementation:

- [Data standards](../../mentorhub/DeveloperEdition/standards/data_standards.md) — collection naming, snake_case properties, and standard document fields.
- `../configurator/test_data/Resource.0.1.0.0.json` — current Resource seed file (482 legacy documents from [SHIPPED.T103](./SHIPPED.T103.generate_resource_test_data.md) when populated).
- `../configurator/test_data/Path.0.1.0.0.json` — current Path seed file (15 legacy documents from [SHIPPED.T104](./SHIPPED.T104.generate_path_test_data.md) when populated).
- `../configurator/test_data/Resource_Aggregation.0.1.0.0.json` — aggregation seed file; clear to avoid dangling references.
- `../configurator/test_data/Journey.0.1.0.0.json` — **read only**; contains `library.resource_id` and roadmap references to legacy `B000…` / `C000…` ids. Do **not** modify Journey data in this task.

The agent may also consult:

- [SHIPPED.T103.generate_resource_test_data.md](./SHIPPED.T103.generate_resource_test_data.md) and [SHIPPED.T104.generate_path_test_data.md](./SHIPPED.T104.generate_path_test_data.md) for prior id conventions.

## Requirements

1. Replace the entire contents of each target test-data file with a single empty JSON array: `[]`.
2. Do **not** modify dictionaries, enumerators, Journey, Encounter, Plan, Identity, Profile, or Mentee test data.
3. Preserve valid JSON (no trailing commas; UTF-8 encoding).
4. Document in **Implementation notes** how many documents were removed from each file (if any were present).

## Testing expectations

- **Processing test**
  - Use `curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"` to drop the MongoDB database.
  - Use `curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"` to Configure the Database.
  - Validate the configure result reports `SUCCESS`. Journey test data may still load even with stale resource/path references; that is acceptable for this task.
- **Packaging test**
  - Run `make container` successfully.
  - Run `make process` and confirm `SUCCESS` in `artifacts/process_all_configurations.json`.

## Dependencies / Ordering

- **First task** in the T110–T114 sequence. Must complete before [PENDING.T111](./PENDING.T111.import_obsidian_resources_test_data.md).
- **Downstream note** — Journey test data will reference removed Resource/Path ids until a future Journey refresh task runs. That stale linkage does not block Configure Database for empty Resource/Path collections.

## Change control checklist

- [x] Reviewed all **Context / Input files**.
- [x] Cleared Resource, Path, and Resource_Aggregation test-data files.
- [x] Ran `make container` successfully.
- [x] Ran `make process` (or curl drop/configure) successfully.
- [ ] Created a scoped commit referencing this task ID.

## Implementation notes (to be updated by the agent)

**Summary of changes**

Cleared `Resource.0.1.0.0.json`, `Path.0.1.0.0.json`, and `Resource_Aggregation.0.1.0.0.json` to empty arrays. Files were already empty (`[]`) at task start (legacy EngineerKit data had been cleared previously).

**Testing results**

- `make container` → SUCCESS.
- `POST /api/configurations/` on port 8385 → SUCCESS (after brief API startup wait).
