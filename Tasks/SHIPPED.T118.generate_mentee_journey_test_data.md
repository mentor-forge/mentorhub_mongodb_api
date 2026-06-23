# T118 – Generate Mentee Journey Test Data

**Status**: Shipped  
**Task Type**: Feature  
**Run Mode**: Sequential  

## User inputs (edit before running)

- **Dictionary file** `../configurator/dictionaries/Journey.0.1.0.yaml`
- **Enumerators file** `../configurator/enumerators/enumerations.0.yaml`
- **Target test-data file** `../configurator/test_data/Journey.0.1.0.0.json`
- **Curriculum path** `EngineerKit` — `C00000000000000000000006`
- **Number of mentee journeys**: `7` (one per Profile with `mentor_id`)

## Goal

Append Journey documents for **every Profile that has a `mentor_id`**, using the **new Journey schema**. Each journey tracks progress through the **EngineerKit** path in `library`, `now`, and `next`, includes exactly **one non-EngineerKit Path** in `later`, and varies progress depth per mentee. Preserve the template Journey from T117.

Journey roadmaps use **Paths** and **Resources** only — not Plans. The `later` field is an array of **Path** `$oid` values.

## Context / Input files

These files must be treated as **inputs** and read before implementation:

- [Data standards](../../mentorhub/DeveloperEdition/standards/data_standards.md)
- `../configurator/dictionaries/Journey.0.1.0.yaml` — `later` = Path `$oid` array.
- `../configurator/test_data/Profile.0.1.0.0.json` — mentee `profile_id` values.
- `../configurator/test_data/Path.0.1.0.0.json` — **EngineerKit** module/topic/resource hierarchy (`C00000000000000000000006`) and other paths for `later`.
- `../configurator/test_data/Resource.0.1.0.0.json` — Resource `name` values for `now.resource_id`.
- `../configurator/test_data/Journey.0.1.0.0.json` — must contain T117 template (`ffff00000000000000000001`); **append** mentee journeys.
- [SHIPPED.T117](./SHIPPED.T117.create_journey_template.md) — template document.
- [SHIPPED.T105](./SHIPPED.T105.generate_journey_test_data.md) — prior EngineerKit progress-splitting approach (update for new module/topic `next` schema).
- [mentorhub/Specifications/features.md](../../mentorhub/Specifications/features.md) — Journey UX.

### Profiles with `mentor_id` (one Journey each)

| Profile `name` | `profile_id` | Journey `_id` | `later` path (non-EngineerKit) | Progress |
| --- | --- | --- | --- | --- |
| `daniel` | `A00000000000000000000002` | `D00000000000000000000001` | `PractitionerUIUXEngineer` (`C00000000000000000000013`) | Early |
| `lucky` | `A00000000000000000000003` | `D00000000000000000000002` | `PractitionerSRE` (`C00000000000000000000012`) | Mid |
| `mary` | `A00000000000000000000004` | `D00000000000000000000003` | `Databases` (`C00000000000000000000004`) | Mid–high |
| `luther` | `A00000000000000000000005` | `D00000000000000000000004` | `Design` (`C00000000000000000000005`) | High |
| `riley` | `A00000000000000000000010` | `D00000000000000000000005` | `Odin` (`C00000000000000000000008`) | Early |
| `taylor` | `A00000000000000000000014` | `D00000000000000000000006` | `CypressTesting` (`C00000000000000000000003`) | Mid |
| `casey` | `A00000000000000000000015` | `D00000000000000000000007` | `Python` (`C00000000000000000000009`) | Archived; moderate |

### Path rules

- **`library` / `now` / `next`** — resources from the **EngineerKit** path only, in module → topic → resource order (same order as `Path.0.1.0.0.json`).
- **`later`** — exactly **one** Path `$oid` that is **not** EngineerKit.
- Do **not** include EngineerKit in mentee `later` (active mentees are already working that path in `library`/`now`/`next`).
- Do **not** reference Plan documents or Plan `$oid` values on Journey documents.

## Requirements

### 1. Progress model (EngineerKit → library / now / next)

Walk the **EngineerKit** path in module → topic → resource order. For each mentee, choose a different cut point:

1. **`library`** — completed EngineerKit resources before the cut point (`resource_id` `$oid`, `started`, `completed`, `used`).
2. **`now`** — 1–2 in-progress resources after the library section (`resource_id` = Resource **`name`**, `added`, optional `started`, `used`).
3. **`next`** — remaining EngineerKit content as **modules** with **topics** and Resource `$oid` arrays.
   - Mirror EngineerKit module/topic names and descriptions from `Path.0.1.0.0.json`.
   - Include only topics/resources **not** already in `library` or `now`.
   - Do **not** use the legacy flat topic list from T105.

**Varying progress** across the seven mentees:

| Mentee | Approx. completed EngineerKit resources | `now` count |
| --- | --- | --- |
| daniel, riley | 3–5 | 1 |
| lucky, taylor | 8–12 | 1–2 |
| mary | 15–20 | 2 |
| luther | 25–35 | 2 |
| casey | 10–15 | 1 |

### 2. `later` scope

Exactly **one** non-EngineerKit Path `$oid` per mentee (see table).

### 3. Status and enums

- **casey** → `status`: `archived`.
- All others → `status`: `active`.

### 4. Identifiers and breadcrumbs

- Journey `_id` values `D00000000000000000000001`–`07`.
- `created` and `saved` on every mentee journey.
- Final file: **8** documents (1 template + 7 mentees).

### 5. Validation

- All Resource `$oid` values exist in `Resource.0.1.0.0.json`.
- All Path `$oid` values in `later` exist in `Path.0.1.0.0.json`.
- No duplicate `profile_id`.

## Testing expectations

- Drop/configure on port **8385** → `SUCCESS`; **8** Journey documents import.
- `make container` and `make process` succeed.
- Spot check: template unchanged; each mentee `later` has one non-EngineerKit Path id; `library`/`now`/`next` use EngineerKit resources only.

## Dependencies / Ordering

- Depends on T115, T116, and T117.
- **Last task** in the T115–T118 sequence.
- EngineerKit path must exist from T112 (`C00000000000000000000006`).

## Change control checklist

- [x] Reviewed EngineerKit path hierarchy in `Path.0.1.0.0.json`.
- [x] Appended 7 mentee Journey documents without removing the T117 template.
- [x] EngineerKit resources in `library`/`now`/`next`; one non-EngineerKit Path per `later`.
- [x] Varied progress across mentees; casey journey is `archived`.
- [x] Ran `make container` and `make process` successfully.
- [x] Created a scoped commit referencing this task ID.

## Implementation notes (to be updated by the agent)

**Summary of changes**

Appended **7** mentee Journey documents (463 EngineerKit resources walked in path order). Final file: **8** documents (1 template + 7 mentees).

| Mentee | `library` | `now` | `later` Path |
| --- | --- | --- | --- |
| daniel | 4 | 1 | PractitionerUIUXEngineer |
| lucky | 10 | 2 | PractitionerSRE |
| mary | 18 | 2 | Databases |
| luther | 30 | 2 | Design |
| riley | 4 | 1 | Odin |
| taylor | 10 | 1 | CypressTesting |
| casey | 12 | 1 | Python (`archived`) |

`next` uses EngineerKit module/topic hierarchy (not legacy flat topics from T105).

**Testing results**

- `make container` → SUCCESS.
- `POST /api/configurations/` on port 8385 → SUCCESS (8 Journey documents imported).
