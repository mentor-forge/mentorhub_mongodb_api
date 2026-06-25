# T120 – Generate Rating Test Data

**Status**: Shipped  
**Task Type**: Feature  
**Run Mode**: Sequential  

## User inputs (edit before running)

- **Dictionary file** `../configurator/dictionaries/Rating.0.1.0.yaml`
- **Enumerators file** `../configurator/enumerators/enumerations.0.yaml`
- **Target test-data file** `../configurator/test_data/Rating.0.1.0.0.json`
- **Number of documents to generate**: `88` (one per completed library resource across all mentee journeys; see T118 progress table)
- **Special requirements**
  - Drive ratings from **Journey test data** in `Journey.0.1.0.0.json` (T117 template + T118 mentee journeys).
  - Create **one Rating per resource in each mentee's `library`** — these are the Journey **completed** resources (each entry has `resource_id`, `started`, and `completed` dates).
  - Skip the T117 template journey (`ffff00000000000000000001`) — it has an empty `library`.
  - Tie `profile_id` to the journey owner's Profile `$oid` and `resource_id` to the library entry's Resource `$oid`.
  - `rating` values **1–4** (integer star scale per `rating.yaml`); assign a **variety of scores** across resources and mentees (see **Rating variety** below).
  - Include `default_status` enum coverage (`active` for nearly all; at least one `archived` rating if realistic — e.g. casey's archived journey).
  - Use deterministic `_id` values starting at `G00000000000000000000001` (24-char hex ObjectIds throughout).
  - Set `created.at_time` to align with (or shortly after) each library entry's `completed` date where possible.
  - Do **not** invent library resources — only rate resources already present in each mentee's Journey `library`.

## Goal

Generate EJSON **Rating** documents for every completed resource in mentee Journey `library` sections (T118), as input for downstream **Aggregation** test data (see `mentorhub/Specifications/features.md` → Data features → Rating).

## Context / Input files

These files must be treated as **inputs** and read before implementation:

- [Tasks/README.md](./README.md) — task workflow and change control.
- [Data standards](../../mentorhub/DeveloperEdition/standards/data_standards.md)
- `../configurator/dictionaries/Rating.0.1.0.yaml`
- `../configurator/types/rating.yaml` — star scale 1–4
- `../configurator/enumerators/enumerations.0.yaml` — `default_status` enum
- `../configurator/test_data/Journey.0.1.0.0.json` — primary driver (T117/T118); walk each mentee's `library`
- `../configurator/test_data/Profile.0.1.0.0.json` — profile `$oid` references
- `../configurator/test_data/Resource.0.1.0.0.json` — resource `$oid` and metadata for score variation
- [SHIPPED.T118.generate_mentee_journey_test_data.md](./SHIPPED.T118.generate_mentee_journey_test_data.md) — mentee journey progress model and library counts
- [mentorhub/Specifications/features.md](../../mentorhub/Specifications/features.md) — Data features → Rating

### Expected library counts (T118)

| Mentee | Profile `$oid` | Journey `_id` | `library` count |
| --- | --- | --- | --- |
| daniel | `A00000000000000000000002` | `D00000000000000000000001` | 4 |
| lucky | `A00000000000000000000003` | `D00000000000000000000002` | 10 |
| mary | `A00000000000000000000004` | `D00000000000000000000003` | 18 |
| luther | `A00000000000000000000005` | `D00000000000000000000004` | 30 |
| riley | `A00000000000000000000010` | `D00000000000000000000005` | 4 |
| taylor | `A00000000000000000000014` | `D00000000000000000000006` | 10 |
| casey | `A00000000000000000000015` | `D00000000000000000000007` | 12 |
| **Total** | | | **88** |

## Requirements

1. **EJSON encoding**
   - `_id`, `profile_id`, and `resource_id` as `{ "$oid": "..." }`
   - Breadcrumb `at_time` as `{ "$date": "..." }`

2. **Schema-driven generation**
   - Each Rating has `resource_id` (required), `profile_id`, `rating` (1–4 int), `status` (`default_status` enum), and `created` breadcrumb per `Rating.0.1.0.yaml`.

3. **Enum coverage**
   - `default_status`: `active` for the vast majority; include at least one `archived` rating where realistic.

4. **Journey alignment**
   - One Rating per library entry across all seven mentee journeys.
   - Do not rate resources in `now`, `next`, or `later` — only completed `library` resources.
   - Do not rate resources for journeys without a `profile_id` (template journey).

5. **Rating variety**
   - **Full scale coverage** — every star value **1, 2, 3, and 4** must appear at least once across the 88 documents.
   - **Per-resource spread** — when the same Resource `$oid` appears in multiple mentee `library` sections (18 resources overlap; the first four EngineerKit resources appear in all seven mentees), assign **different ratings per mentee** where realistic. Do not give every mentee the same score for the same resource.
   - **Resource-informed scores** — use `Resource.0.1.0.0.json` metadata to guide variation:
     - `skill_level` (e.g. Apprentice vs Journeyman) — harder resources may get lower scores from early mentees, higher from advanced mentees.
     - `type`, `cost`, and `technologies` — free introductory articles tend toward 3–4; dense or membership content may get more 2–3 from beginners.
   - **Mentee-informed scores** — higher-progress mentees (luther, mary) should skew slightly higher on early EngineerKit resources; early mentees (daniel, riley) may rate the same resources lower.
   - **Avoid uniformity** — do not assign the same rating to all 88 documents or to all ratings for a single resource. Target a realistic spread (roughly 10–20% each for 1 and 2, 30–40% for 3, 30–40% for 4).
   - **Document the distribution** — record rating-value counts and any notable per-resource spreads in implementation notes.

6. **Timestamps**
   - Spread `created.at_time` over the same date range as library `completed` dates (roughly Jan–Jun 2025 per T118).

## Testing expectations

- Run `make container` — build succeeds.
- `curl -X DELETE "http://localhost:8385/api/database/"` → SUCCESS
- `curl -X POST "http://localhost:8385/api/configurations/"` → SUCCESS
- If configure fails, inspect error JSON and fix test data.

## Dependencies / Ordering

- **T118 (Journey test data)** — must be shipped; ratings derive from `library` completed resources.
- **T119 (Event test data)** — should be shipped; events and ratings should tell a consistent story (completed events align with rated resources).
- **Verify** — drop and configure database before executing; stop if baseline configure fails.

## Change control checklist

- [x] Reviewed all **Context / Input files**.
- [x] Designed approach documented in this file.
- [x] Implemented `Rating.0.1.0.0.json` with 88 Rating documents.
- [x] Ran `make container` successfully.
- [x] Ran configure-database curl commands successfully.
- [x] Created a scoped commit referencing T120.

## Implementation notes (to be updated by the agent)

**Summary of changes**

Generated **88** EJSON Rating documents in `configurator/test_data/Rating.0.1.0.0.json` via `Tasks/scripts/generate_rating_test_data.py`.

**Approach**

- Walked each mentee Journey (T118) and emitted one Rating per `library` resource (completed resources only).
- Skipped the T117 template journey (`ffff00000000000000000001`) with empty `library`.
- Assigned deterministic `_id` values `G00000000000000000000001` through `G00000000000000000000088`, sorted by library `completed` date.
- Set `created.at_time` to 15+ minutes after each library entry's `completed` date.
- Varied star ratings by mentee progress tier, resource difficulty (`skill_level`, `cost`, `type`), and per-mentee spread on shared EngineerKit resources.
- Set all **casey** ratings to `archived` (archived profile/journey).

**Rating value counts**

| Rating | Count | Share |
| --- | --- | --- |
| 1 | 17 | 19% |
| 2 | 13 | 15% |
| 3 | 23 | 26% |
| 4 | 35 | 40% |

**Status counts**

| Status | Count |
| --- | --- |
| active | 76 |
| archived | 12 (all casey) |

**Notable per-resource spreads**

| Resource `$oid` | Ratings across 7 mentees |
| --- | --- |
| `B00000000000000000000107` (Stackshare) | 1, 1, 1, 2, 3, 3, 4 |
| `B00000000000000000000108` (StackOverflow survey) | 1, 1, 2, 2, 3, 3, 4 |

**Testing results**

- `make container` → SUCCESS.
- `DELETE /api/database/` on port 8385 → 200.
- `POST /api/configurations/` on port 8385 → SUCCESS.
- Note: local `make process` could not bind host port 27017 (centralized `mentorhub-mongodb-1` running); configure test succeeded via isolated compose stack with internal-only MongoDB.
