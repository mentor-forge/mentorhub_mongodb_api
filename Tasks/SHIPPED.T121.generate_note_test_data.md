# T121 – Generate Note Test Data

**Status**: Shipped  
**Task Type**: Feature  
**Run Mode**: Sequential  

## User inputs (edit before running)

- **Dictionary file** `../configurator/dictionaries/Note.0.1.0.yaml`
- **Enumerators file** `../configurator/enumerators/enumerations.0.yaml`
- **Target test-data file** `../configurator/test_data/Note.0.1.0.0.json`
- **Number of documents to generate**: `35` (minimum; add more if needed for realistic coverage)
- **Special requirements**
  - Drive notes from **Journey test data** in `Journey.0.1.0.0.json` (T117 template + T118 mentee journeys).
  - Create notes for resources in each mentee's **`library`** (completed resources) only. In-progress (`now`) resources do **not** need notes.
  - Skip the T117 template journey (`ffff00000000000000000001`).
  - Tie `profile_id` to the journey owner and `resource_id` to the Resource `$oid` for that library entry.
  - Include **at least two notes per active mentee** and **at least one note per mentee overall**; higher-progress mentees (luther, mary) should have more notes.
  - `note` text must be valid **markdown** (per `markdown.yaml`, max 4096 chars); vary tone and length — short takeaways, questions, and reflections.
  - Include `default_status` enum coverage (`active` for nearly all; at least one `archived` note for **casey**).
  - Use deterministic `_id` values starting at `E00000000000000000000001` (24-char hex ObjectIds throughout; prefix must be `0-9` or `A-F`).
  - Set `created.at_time` to align with (or shortly after) the resource's `completed` date where possible; set `saved.at_time` equal to or later than `created`.
  - Do **not** invent resources — only note resources already on each mentee's Journey `library`.
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

- If the API is not running, you can use `make dev` to start it.
- Run `make container` — build succeeds.
- `curl -X DELETE "http://localhost:8385/api/database/"` → SUCCESS
- `curl -X POST "http://localhost:8385/api/configurations/"` → SUCCESS
- If configure fails, inspect error JSON and fix test data.

## Dependencies / Ordering

- **T118 (Journey test data)** — must be shipped; notes derive from journey state.
- **T120 (Rating test data)** — must be shipped; align note tone with ratings where both exist.
- **Verify** — drop and configure database before executing; stop if baseline configure fails.

## Change control checklist

- [x] Reviewed all **Context / Input files**.
- [x] Designed approach documented in this file.
- [x] Implemented `Note.0.1.0.0.json`.
- [x] Ran `make container` successfully.
- [x] Ran configure-database curl commands successfully.
- [x] Created a scoped commit referencing T121.

## Implementation notes (to be updated by the agent)

**Summary of changes**

Generated **35** EJSON Note documents in `configurator/test_data/Note.0.1.0.0.json` via `Tasks/scripts/generate_note_test_data.py`.

**Approach**

- Walked each mentee Journey (T118) and selected library resources only (no `now` notes).
- Assigned deterministic `_id` values `E00000000000000000000001` through `E00000000000000000000035`, sorted by library `completed` date.
- Set `created.at_time` shortly after each library `completed` date; `saved.at_time` 2+ hours later.
- Varied markdown note tone using T120 ratings (low → critical/confused; high → positive takeaways).
- All **casey** notes use `archived` status.

**Note counts by mentee**

| Mentee | Notes |
| --- | --- |
| daniel | 3 |
| lucky | 4 |
| mary | 6 |
| luther | 12 |
| riley | 3 |
| taylor | 4 |
| casey | 3 |

**Status counts**

| Status | Count |
| --- | --- |
| active | 32 |
| archived | 3 (all casey) |

**Testing results**

- `make container` → SUCCESS.
- `DELETE /api/database/` on port 8385 → 200.
- `POST /api/configurations/` on port 8385 → SUCCESS.
