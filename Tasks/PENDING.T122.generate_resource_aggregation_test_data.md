# T122 – Generate Resource Aggregation Test Data

**Status**: Pending  
**Task Type**: Feature  
**Run Mode**: Sequential  

## User inputs (edit before running)

- **Dictionary file** `../configurator/dictionaries/Resource_Aggregation.0.1.0.yaml`
- **Enumerators file** `../configurator/enumerators/enumerations.0.yaml`
- **Target test-data file** `../configurator/test_data/Resource_Aggregation.0.1.0.0.json`
- **Number of documents to generate**: one per unique Resource `$oid` referenced on any **mentee** Journey document (see **Expected document count** below; currently ~456 resources across T118 journeys)
- **Special requirements**
  - Drive aggregations from **Journey test data** in `Journey.0.1.0.0.json` (T118 mentee journeys only).
  - Create **one Resource_Aggregation per unique `resource_id`** that appears anywhere on a mentee Journey (`library`, `now`, or `next`). Do **not** include resources that appear only on the T117 template journey (`ffff00000000000000000001`, no `profile_id`).
  - **`note_count`** — total number of **Note** documents (T121) whose `resource_id` matches this resource (count all profiles).
  - **`completions`** — number of mentee Journeys that list this resource in **`library`** (completed resources only).
  - **`hits`** — vary by resource, but **always strictly greater than `completions`** (`hits > completions`). Prefer deriving from T119 **`link`** events for the resource where available; otherwise use a deterministic offset above `completions` (e.g. `completions + 1` to `completions + 5`) so popular EngineerKit resources show higher hit counts.
  - **`duration`** — a random ISO-8601 duration between **15 minutes** and **4 hours** inclusive (per `duration.yaml`, e.g. `PT45M`, `PT2H30M`, `PT4H`). Use a seeded or deterministic pseudo-random approach so regeneration is stable.
  - **`rating_count`** and **`rating_sum`** — compute by looking up all **Rating** documents (T120) for this `resource_id`; `rating_count` is the count of matching ratings, `rating_sum` is the sum of their `rating` values. Use `0` for both when no ratings exist (resources only in `now`/`next`).
  - **`created`** — set `created.at_time` to shortly after (minutes to days) the corresponding Resource's `created.at_time` from `Resource.0.1.0.0.json`.
  - **`last_saved`** — set `last_saved.at_time` to a random date **after** `created.at_time` (schema field is `last_saved`, not `saved`).
  - Use deterministic `_id` values starting at `H00000000000000000000001` (24-char hex ObjectIds throughout; prefix must be `0-9` or `A-F`).
  - Do **not** invent resources — only aggregate resources already referenced on mentee Journey documents.

## Goal

Generate EJSON **Resource_Aggregation** documents for every unique resource on mentee Journey documents (T118), with counts and metrics derived from Journey, Note, Rating, and Event test data, as input for downstream **Aggregation** API features (see `mentorhub/Specifications/features.md` → Data features → Aggregation).

## Context / Input files

These files must be treated as **inputs** and read before implementation:

- [Tasks/README.md](./README.md) — task workflow and change control.
- [Data standards](../../mentorhub/DeveloperEdition/standards/data_standards.md)
- `../configurator/dictionaries/Resource_Aggregation.0.1.0.yaml`
- `../configurator/types/duration.yaml` — ISO-8601 duration pattern
- `../configurator/types/breadcrumb.yaml` — `created` / `last_saved` shape
- `../configurator/test_data/Journey.0.1.0.0.json` — primary driver (T118); walk `library`, `now`, and `next`
- `../configurator/test_data/Resource.0.1.0.0.json` — resource `created` timestamps and `name` → `$oid` mapping for `now` entries
- `../configurator/test_data/Note.0.1.0.0.json` — T121; drive `note_count`
- `../configurator/test_data/Rating.0.1.0.0.json` — T120; drive `rating_count` and `rating_sum`
- `../configurator/test_data/Event.0.1.0.0.json` — T119; optional input for realistic `hits` (`link` events)
- [SHIPPED.T118.generate_mentee_journey_test_data.md](./SHIPPED.T118.generate_mentee_journey_test_data.md) — mentee journey progress model
- [SHIPPED.T119.generate_event_test_data.md](./SHIPPED.T119.generate_event_test_data.md) — event types and journey alignment
- [SHIPPED.T120.generate_rating_test_data.md](./SHIPPED.T120.generate_rating_test_data.md) — one rating per library completion
- [SHIPPED.T121.generate_note_test_data.md](./SHIPPED.T121.generate_note_test_data.md) — notes on library resources
- [mentorhub/Specifications/features.md](../../mentorhub/Specifications/features.md) — Data features → Aggregation

### Expected document count (T118)

| Source | Approx. count | Notes |
| --- | --- | --- |
| Unique resources on mentee journeys | ~456 | Union of `library`, `now`, and `next` across seven mentees |
| Resources with `library` completions | ~30 | Shared EngineerKit resources; `completions` ranges 1–7 |
| Resources in `now`/`next` only | ~426 | `completions` = 0; `hits` must be ≥ 1 |

## Requirements

1. **EJSON encoding**
   - `_id` and `resource_id` as `{ "$oid": "..." }`
   - Breadcrumb `at_time` as `{ "$date": "..." }`
   - `duration` as an ISO-8601 duration string (not a `$date`)

2. **Schema-driven generation**
   - Each document has `resource_id`, `note_count`, `completions`, `hits`, `duration`, `rating_count`, `rating_sum`, `created`, and `last_saved` per `Resource_Aggregation.0.1.0.yaml`.
   - `rating_sum` is required even when `rating_count` is 0.

3. **Journey alignment**
   - One aggregation per unique Resource `$oid` on any mentee Journey.
   - Skip the T117 template journey.
   - Resolve `now.resource_id` name strings to Resource `$oid` values via `Resource.0.1.0.0.json`.

4. **Derived metrics**
   - **`note_count`**: count Note documents grouped by `resource_id`.
   - **`completions`**: count mentee Journey `library` entries grouped by `resource_id`.
   - **`hits`**: `hits > completions` always; vary across resources (higher for widely shared EngineerKit resources).
   - **`rating_count` / `rating_sum`**: aggregate from Rating documents; for resources with completions, counts should align with T120 (one rating per library entry → `rating_count` should equal `completions` for those resources).
   - **`duration`**: pseudo-random between `PT15M` and `PT4H`.

5. **Timestamps**
   - `created.at_time` shortly after the Resource document's `created.at_time`.
   - `last_saved.at_time` after `created.at_time` (spread over days to weeks).

6. **Implementation approach**
   - Prefer a generator script under `Tasks/scripts/` (e.g. `generate_resource_aggregation_test_data.py`) following T120/T121 patterns.
   - Sort output by `resource_id` for stable diffs.

## Testing expectations

- If the API is not running, you can use `make dev` to start it.
- Run `make container` — build succeeds.
- `curl -X DELETE "http://localhost:8385/api/database/"` → SUCCESS
- `curl -X POST "http://localhost:8385/api/configurations/"` → SUCCESS
- If configure fails, inspect error JSON and fix test data.

## Dependencies / Ordering

- **T118 (Journey test data)** — must be shipped; defines which resources to aggregate and `completions`.
- **T119 (Event test data)** — must be shipped; optional source for `hits`.
- **T120 (Rating test data)** — must be shipped; drives `rating_count` and `rating_sum`.
- **T121 (Note test data)** — must be shipped; drives `note_count`.
- **Verify** — drop and configure database before executing; stop if baseline configure fails.

## Change control checklist

- [ ] Reviewed all **Context / Input files**.
- [ ] Designed approach documented in this file.
- [ ] Implemented `Resource_Aggregation.0.1.0.0.json` (and generator script if used).
- [ ] Ran `make container` successfully.
- [ ] Ran configure-database curl commands successfully.
- [ ] Created a scoped commit referencing T122.

## Implementation notes (to be updated by the agent)

**Summary of changes**
- _Pending — to be filled when task is executed._

**Derived metric spot-checks**
- _Document sample `note_count`, `completions`, `hits`, `rating_count`, and `rating_sum` for a few shared EngineerKit resources and for a `next`-only resource._

**Testing results**
- _Pending — `make container`, configure-database curl commands._
