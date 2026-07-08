# T123 – Add Rating to Journey Library Items

**Status**: Pending  
**Task Type**: Feature  
**Run Mode**: Sequential  

## User inputs (edit before running)

- **Dictionary file** `../configurator/dictionaries/Journey.0.1.0.yaml`
- **Type file** `../configurator/types/rating.yaml` — star scale 1–4 (integer)
- **Enumerators file** `../configurator/enumerators/enumerations.0.yaml`

## Goal

Add an optional **`rating`** field to each **library** array item in the Journey dictionary so a mentee's star rating for a completed resource is stored on the Journey document (alongside `resource_id`, `started`, `completed`, and `used`).

Ratings apply only to **completed** resources in `library` — not to `now` or `next` entries.

## Context / Input files

These files must be treated as **inputs** and read before implementation:

- [Tasks/README.md](./README.md) — task workflow and change control.
- [Data standards](../../mentorhub/DeveloperEdition/standards/data_standards.md)
- `../configurator/dictionaries/Journey.0.1.0.yaml` — current `library` item shape
- `../configurator/types/rating.yaml` — `rating` type (int 1–4)
- [SHIPPED.T118.generate_mentee_journey_test_data.md](./SHIPPED.T118.generate_mentee_journey_test_data.md) — mentee journey `library` model
- [SHIPPED.T120.generate_rating_test_data.md](./SHIPPED.T120.generate_rating_test_data.md) — prior per-profile Rating documents (source values for downstream test-data task T125)

### Current `library` item properties

| Property | Type | Notes |
| --- | --- | --- |
| `resource_id` | identifier | Resource `$oid` |
| `started` | date-time | First link follow |
| `completed` | date-time | Marked done |
| `used` | count | Link follow count |

## Requirements

1. **Dictionary change only** — update `Journey.0.1.0.yaml`; do **not** modify test data in this task (T125 handles test data).

2. **Add `rating` property** to the `library` items object, after `used`:
   ```yaml
   - description: The mentee's star rating for this completed resource
     name: rating
     required: false
     type: rating
   ```

3. **Scope** — add `rating` only under `library.items.properties`. Do **not** add `rating` to `now` or `next` items.

4. **Pre-release** — edit the existing **0.1.0** dictionary in place; no version bump or migration pipeline.

5. **Fix unrelated issues only if blocking** — if dictionary validation fails due to an obvious copy/paste error in another file touched by this branch, note it in implementation notes but do not expand scope.

## Testing expectations

- Run `make container` — build succeeds.
- `curl -X DELETE "http://localhost:8385/api/database/"` → SUCCESS
- `curl -X POST "http://localhost:8385/api/configurations/"` → SUCCESS (existing test data must still import; Journey documents simply omit the new optional field until T125).

## Dependencies / Ordering

- **None** — this is the first task in the Journey-rating / Resource_Aggregation refactor sequence.
- **Blocks** — T125 (test data) depends on this schema change.

## Change control checklist

- [ ] Reviewed all **Context / Input files**.
- [ ] Designed approach documented in this file.
- [ ] Updated `Journey.0.1.0.yaml` with `library.rating`.
- [ ] Ran `make container` successfully.
- [ ] Ran configure-database curl commands successfully.
- [ ] Created a scoped commit referencing T123.

## Implementation notes (to be updated by the agent)

**Summary of changes**

_To be filled in by the executing agent._

**Testing results**

_To be filled in by the executing agent._
