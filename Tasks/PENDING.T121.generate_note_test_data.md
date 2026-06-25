# T121 – Generate Note Test Data

**Status**: Pending  
**Task Type**: Feature  
**Run Mode**: Sequential  

## User inputs (edit before running)

- **Dictionary file** `../configurator/dictionaries/Note.0.1.0.yaml`
- **Enumerators file** `../configurator/enumerators/enumerations.0.yaml`
- **Target test-data file** `../configurator/test_data/Note.0.1.0.0.json`
- **Number of documents to generate**: `35` (minimum; add more if needed for realistic coverage)
- **Special requirements**
  - Drive notes from **Journey test data** in `Journey.0.1.0.0.json` (T117 template + T118 mentee journeys).
  - Create notes for resources in each mentee's **`library`** (completed resources) and optionally **`now`** (in-progress resources).
  - Skip the T117 template journey (`ffff00000000000000000001`).
  - Tie `profile_id` to the journey owner and `resource_id` to the Resource `$oid` for that library/now entry.
  - Include **at least two notes per active mentee** and **at least one note per mentee overall**; higher-progress mentees (luther, mary) should have more notes.
  - `note` text must be valid **markdown** (per `markdown.yaml`, max 4096 chars); vary tone and length — short takeaways, questions, and reflections.
  - Include `default_status` enum coverage (`active` for nearly all; at least one `archived` note for **casey**).
  - Use deterministic `_id` values starting at `H00000000000000000000001` (24-char hex ObjectIds throughout).
  - Set `created.at_time` to align with (or shortly after) the resource's `completed` or `started` date where possible; set `saved.at_time` equal to or later than `created`.
  - Do **not** invent resources — only note resources already on each mentee's Journey `library` or `now`.
  - Notes should be **consistent with T120 ratings** where both exist for the same profile/resource pair (e.g. low ratings → critical or confused notes; high ratings → positive takeaways).

## Goal

Generate EJSON **Note** documents related to mentee Journey progress (T118), as input for downstream **Aggregation** test data (see `mentorhub/Specifications/features.md` → Data features → Note).

## Context / Input files

These files must be treated as **inputs** and read before implementation:

- [Tasks/README.md](./README.md) — task workflow and change control.
- [Data standards](../../mentorhub/DeveloperEdition/standards/data_standards.md)
- `../configurator/dictionaries/Note.0.1.0.yaml`
- `../configurator/types/markdown.yaml` — note text constraints
- `../configurator/enumerators/enumerations.0.yaml` — `default_status` enum
- `../configurator/test_data/Journey.0.1.0.0.json` — primary driver (T117/T118)
- `../configurator/test_data/Profile.0.1.0.0.json` — profile `$oid` references
- `../configurator/test_data/Resource.0.1.0.0.json` — resource names and metadata for note content
- `../configurator/test_data/Rating.0.1.0.0.json` — optional alignment with T120 ratings
- [SHIPPED.T118.generate_mentee_journey_test_data.md](./SHIPPED.T118.generate_mentee_journey_test_data.md) — mentee journey progress model
- [SHIPPED.T120.generate_rating_test_data.md](./SHIPPED.T120.generate_rating_test_data.md) — rating alignment for shared profile/resource pairs
- [mentorhub/Specifications/features.md](../../mentorhub/Specifications/features.md) — Data features → Note

### Suggested note counts by mentee

| Mentee | Profile `$oid` | Suggested notes | Focus |
| --- | --- | --- | --- |
| daniel | `A00000000000000000000002` | 2–3 | Early library resources; one `now` resource |
| lucky | `A00000000000000000000003` | 3–4 | Mid library; testing/TDD topics |
| mary | `A00000000000000000000004` | 5–6 | Library + `now`; user-story resources |
| luther | `A00000000000000000000005` | 8–10 | Deepest library; TDD/pyramid resources |
| riley | `A00000000000000000000010` | 2–3 | Early library only |
| taylor | `A00000000000000000000014` | 3–4 | Mid library |
| casey | `A00000000000000000000015` | 2–3 | Archived; mix of `archived` status |

## Requirements

1. **EJSON encoding**
   - `_id`, `profile_id`, and `resource_id` as `{ "$oid": "..." }`
   - Breadcrumb `at_time` as `{ "$date": "..." }`

2. **Schema-driven generation**
   - Each Note has `resource_id`, `profile_id`, `note` (markdown string), `status` (`default_status` enum), `created` breadcrumb, and `saved` breadcrumb per `Note.0.1.0.yaml`.

3. **Enum coverage**
   - `default_status`: `active` for the vast majority; include at least one `archived` note for casey.

4. **Journey alignment**
   - Notes must reference resources on the mentee's Journey `library` or `now` only.
   - Do not create notes for the template journey or for resources in `next`/`later` unless explicitly promoted to `now`.

5. **Note variety**
   - Vary note length (one sentence to several paragraphs).
   - Vary note style: takeaway summaries, questions, action items, comparisons to other resources.
   - Reference the Resource **name** or topic naturally in note text.
   - Avoid duplicate note text across documents.

6. **Timestamps**
   - Spread `created.at_time` over the same date range as Journey library `completed` dates (roughly Jan–Jun 2025 per T118).
   - `saved.at_time` should be equal to or after `created.at_time`.

## Testing expectations

- Run `make container` — build succeeds.
- `curl -X DELETE "http://localhost:8385/api/database/"` → SUCCESS
- `curl -X POST "http://localhost:8385/api/configurations/"` → SUCCESS
- If configure fails, inspect error JSON and fix test data.

## Dependencies / Ordering

- **T118 (Journey test data)** — must be shipped; notes derive from journey state.
- **T120 (Rating test data)** — must be shipped; align note tone with ratings where both exist.
- **Verify** — drop and configure database before executing; stop if baseline configure fails.

## Change control checklist

- [ ] Reviewed all **Context / Input files**.
- [ ] Designed approach documented in this file.
- [ ] Implemented `Note.0.1.0.0.json`.
- [ ] Ran `make container` successfully.
- [ ] Ran configure-database curl commands successfully.
- [ ] Created a scoped commit referencing T121.

## Implementation notes (to be updated by the agent)

**Summary of changes**

(To be filled in after implementation.)

**Testing results**

(To be filled in after testing.)
