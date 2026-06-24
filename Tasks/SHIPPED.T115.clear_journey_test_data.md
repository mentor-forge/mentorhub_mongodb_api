# T115 – Clear Journey Test Data

**Status**: Shipped  
**Task Type**: Chore  
**Run Mode**: Sequential  

## User inputs (edit before running)

- **Target test-data file**: `../configurator/test_data/Journey.0.1.0.0.json`
- **Replacement value**: `[]` (empty JSON array)

## Goal

Remove legacy Journey seed data so subsequent tasks can rebuild journeys from the updated Journey schema, current Path/Resource test data, and the new template journey specification.

## Context / Input files

These files must be treated as **inputs** and read before implementation:

- [Data standards](../../mentorhub/DeveloperEdition/standards/data_standards.md) — collection naming, snake_case properties, and standard document fields.
- `../configurator/dictionaries/Journey.0.1.0.yaml` — current Journey schema (`library`, `now`, `next` modules/topics, `later` as Path `$oid` references).
- `../configurator/test_data/Journey.0.1.0.0.json` — legacy seed file (~8k lines, 4 mentee journeys from [SHIPPED.T105](./SHIPPED.T105.generate_journey_test_data.md); uses old flat `next` topic structure and no `later` field).
- `../configurator/test_data/Profile.0.1.0.0.json` — **read only**; downstream tasks will create journeys for profiles with `mentor_id`.
- `../configurator/test_data/Path.0.1.0.0.json` and `../configurator/test_data/Resource.0.1.0.0.json` — **read only**; do not modify in this task.

The agent may also consult:

- [SHIPPED.T105.generate_journey_test_data.md](./SHIPPED.T105.generate_journey_test_data.md) — prior Journey id conventions (`D000…` mentee journeys).
- [mentorhub/Specifications/features.md](../../mentorhub/Specifications/features.md) — Journey data features (template journey, mentee roadmap UX).

## Requirements

1. Replace the entire contents of `Journey.0.1.0.0.json` with a single empty JSON array: `[]`.
2. Do **not** modify dictionaries, enumerators, Path, Resource, Profile, Plan, Encounter, or other test-data files.
3. Preserve valid JSON (no trailing commas; UTF-8 encoding).
4. Document in **Implementation notes** how many Journey documents were removed.

## Testing expectations

- **Processing test**
  - Use `curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"` to drop the MongoDB database.
  - Use `curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"` to Configure the Database.
  - Validate the configure result reports `SUCCESS`. An empty Journey collection is expected and acceptable.
- **Packaging test**
  - Run `make container` successfully.
  - Run `make process` and confirm `SUCCESS` in `artifacts/process_all_configurations.json`.

## Dependencies / Ordering

- **First task** in the T115–T118 sequence. Must complete before [SHIPPED.T116](./SHIPPED.T116.add_onboarding_journey_resources.md).
- **Prerequisite** — T111–T114 Path and Resource test data should already be shipped, including the **EngineerKit** path (`C00000000000000000000006`). Downstream T118 distributes EngineerKit resources across mentee `library`/`now`/`next`.

## Change control checklist

- [x] Reviewed all **Context / Input files**.
- [x] Cleared `Journey.0.1.0.0.json` to `[]`.
- [x] Ran `make container` successfully.
- [x] Ran `make process` (or curl drop/configure) successfully.
- [x] Created a scoped commit referencing this task ID.

## Implementation notes (to be updated by the agent)

**Summary of changes**

Cleared `configurator/test_data/Journey.0.1.0.0.json` — removed **4** legacy mentee Journey documents (daniel, lucky, mary, luther) that used the old flat `next` topic structure and lacked `later`.

**Testing results**

- `make container` → SUCCESS.
- `POST /api/configurations/` on port 8385 → SUCCESS (empty Journey collection).
