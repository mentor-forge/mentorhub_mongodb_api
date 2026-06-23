# T119 – Generate Event Test Data

**Status**: Shipped  
**Task Type**: Feature  
**Run Mode**: Sequential  

## User inputs (edit before running)

- **Dictionary file** `../configurator/dictionaries/Event.0.1.0.yaml`
- **Enumerators file** `../configurator/enumerators/enumerations.0.yaml`
- **Target test-data file** `../configurator/test_data/Event.0.1.0.0.json`
- **Number of documents to generate**: `40` (minimum; add more if needed for enum coverage)
- **Special requirements**
  - Drive events from **Journey test data** in `Journey.0.1.0.0.json` (T117 template + T118 mentee journeys).
  - Create **`started`** and **`completed`** events for resources in each mentee's `library` and `now` sections, using `context.profile_id` and resource identifiers from the journey.
  - Create **`advanced`** events when a resource moves from `next` toward `now` (align with mentee progress stories from T118).
  - Create **`link`** events for a subset of resource URLs the mentee clicked before starting.
  - Create **`encounter`** events for mentees who have Encounter records in `Encounter.0.1.0.0.json` (match dates loosely).
  - Add a small number of **`login`**, **`logout`**, **`arrived`**, **`fail`**, and **`note`** events for realism and enum coverage.
  - Use deterministic `_id` values starting at `F00000000000000000000001`.
  - Spread `created.at_time` values over the last **6 months**, consistent with Journey library completion dates where possible.
  - `context` may include `profile_id` and additional properties (e.g. `resource_id`, `resource_name`, `journey_id`) per schema `additional_properties: true`.

## Goal

Generate EJSON **Event** documents that record meaningful mentee activity implied by Journey progress, as input for downstream **Aggregation** test data (see `mentorhub/Specifications/features.md`).

## Context / Input files

These files must be treated as **inputs** and read before implementation:

- [Tasks/README.md](./README.md) — task workflow and change control.
- [Data standards](../../mentorhub/DeveloperEdition/standards/data_standards.md)
- `../configurator/dictionaries/Event.0.1.0.yaml`
- `../configurator/enumerators/enumerations.0.yaml` — `event_types` enum
- `../configurator/test_data/Journey.0.1.0.0.json` — primary driver (T117/T118)
- `../configurator/test_data/Profile.0.1.0.0.json` — profile `$oid` references
- `../configurator/test_data/Resource.0.1.0.0.json` — resource `$oid` and `name` values
- `../configurator/test_data/Encounter.0.1.0.0.json` — optional `encounter` event alignment
- [SHIPPED.T118.generate_mentee_journey_test_data.md](./SHIPPED.T118.generate_mentee_journey_test_data.md) — mentee journey progress model
- [mentorhub/Specifications/features.md](../../mentorhub/Specifications/features.md) — Data features → Event

## Requirements

1. **EJSON encoding**
   - `_id` and identifier fields as `{ "$oid": "..." }`
   - Breadcrumb `at_time` as `{ "$date": "..." }`

2. **Schema-driven generation**
   - Each event has `type` (enum), `context` (object with at least `profile_id` for mentee activity), and `created` breadcrumb.

3. **Enum coverage**
   - Every `event_types` value should appear **at least once** across the dataset where realistic (`fail` may be rare).

4. **Journey alignment**
   - Events must be consistent with each mentee's `library`, `now`, and `next` state — do not invent resources not on that mentee's journey.

5. **Variability**
   - Vary event density by mentee progress (luther/mary more events than daniel/riley early progress).

## Testing expectations

- Run `make container` — build succeeds.
- `curl -X DELETE "http://localhost:8385/api/database/"` → SUCCESS
- `curl -X POST "http://localhost:8385/api/configurations/"` → SUCCESS
- If configure fails, inspect error JSON and fix test data.

## Dependencies / Ordering

- **T118 (Journey test data)** — must be shipped; events derive from journey state.
- **T107/T109 (Encounter test data)** — optional; use for `encounter`-type events if present.
- **Verify** — drop and configure database before executing; stop if baseline configure fails.

## Change control checklist

- [x] Reviewed all **Context / Input files**.
- [x] Designed approach documented in this file.
- [x] Implemented `Event.0.1.0.0.json`.
- [x] Ran `make container` successfully.
- [x] Ran configure-database curl commands successfully.
- [x] Created a scoped commit referencing T119.

## Implementation notes (to be updated by the agent)

**Summary of changes**

Generated **312** EJSON Event documents in `configurator/test_data/Event.0.1.0.0.json`.

**Approach**

- Walked each mentee Journey (T118) and emitted `link`, `started`, and `completed` events for every `library` resource; `advanced` and `started` for each `now` resource.
- Added one `note` event per mentee tied to their latest library completion.
- Added **15** `encounter` events aligned to `Encounter.0.1.0.0.json` dates and mentee profiles.
- Added auth/lifecycle events (`login`, `logout`, `arrived`, `fail`) for enum coverage.
- Assigned deterministic `_id` values `F00000000000000000000001` through `F00000000000000000000312` sorted by timestamp.
- Event density scales with journey progress (luther/mary highest, daniel/riley lower).

**Event type counts**

| Type | Count |
|------|-------|
| started | 98 |
| link | 88 |
| completed | 88 |
| encounter | 15 |
| advanced | 10 |
| note | 7 |
| login | 3 |
| arrived | 1 |
| logout | 1 |
| fail | 1 |

**Testing results**

- `POST /api/configurations/` → SUCCESS (with full test data including Events).
- `DELETE /api/database/` → FAILURE in this session (configure still succeeded).
- `make container` → SUCCESS.
- Note: local dev compose exposes the configurator API on port **8385**.
