# T109 – Re-create Encounter Test Data

**Status**: Shipped  
**Task Type**: Feature  
**Run Mode**: Sequential  

Replace synthetic Encounter seed data with **15** documents derived from real mentorship session notes in `Tasks/encounters/`. Sync each encounter's `plan_id` and `agenda` with the **Standard** and **First Encounter** plans shipped in T108, and wire `mentor_id` / `mentee_id` to existing Profile `$oid` values.

## User inputs (edit before running)

- **Dictionary file** `../configurator/dictionaries/Encounter.0.1.0.yaml`
- **Enumerators file** `../configurator/enumerators/enumerations.0.yaml`
- **Target test‑data file** `../configurator/test_data/Encounter.0.1.0.0.json`
- **Number of documents to generate**: `15`
- **Special requirements**
  - **Replace** the entire contents of `Encounter.0.1.0.0.json` (do not append to the legacy T107 documents).
  - Use **Marti the Mentor** (`Profile` `A00000000000000000000006`) as `mentor_id` for all encounters — this adjusts the attendee lists in markdown to match profile test data.
  - Map each source file to the correct mentee `Profile` `$oid`:

    | Mentee (source markdown) | Profile `$oid` | Profile `full_name` |
    | --- | --- | --- |
    | Mary Anderson | `A00000000000000000000004` | Mary Anderson |
    | Daniel Dissler | `A00000000000000000000002` | Daniel Dissler |
    | Lucky Minyard (also "Curtis (Lucky) Minyard") | `A00000000000000000000003` | Lucky Minyard |
    | Luther Still (also "Luke" in transcripts) | `A00000000000000000000005` | Luther Still |

  - Assign **plan_id** and **agenda** from the appropriate plan in `Plan.0.1.0.0.json`:

    | Plan | `plan_id` | Use for |
    | --- | --- | --- |
    | **Standard** (`name`: `Standard`) | `f00000000000000000000001` | Every encounter **except** each mentee's chronologically first session |
    | **First Encounter** (`name`: `FirstEncounter`) | `f00000000000000000000002` | Each mentee's **earliest** session only |

  - **First Encounter** sessions (one per mentee):

    | Source file | Mentee |
    | --- | --- |
    | `encounters/2026-05-05 Mary-Anderson.md` | Mary Anderson |
    | `encounters/2026-05-06 Daniel-Dissler.md` | Daniel Dissler |
    | `encounters/2026-05-07 Luther-Still.md` | Luther Still |
    | `encounters/2026-06-08 Lucky-Minyard.md` | Lucky Minyard |

  - All other source files use the **Standard** plan.

  - For each encounter, set `agenda` to a **copy** of the selected Plan's `checklist`, transformed into Encounter agenda items: each checklist sentence becomes `{ "step": "<sentence>", "checked": <boolean> }`. Copy step text **verbatim** from `Plan.0.1.0.0.json`. Every plan checklist step must appear in order; set all steps `checked`: `true` for completed sessions (all 15 source sessions are completed meetings or documented no-shows).

  - **Standard** plan checklist (8 steps — from T108):

    1. Start Whisper Recording
    2. What do you want to focus on today?
    3. How would you describe what's happening now?
    4. During our time together, what would you like to accomplish?
    5. What would you like to be able to share next time?
    6. How are your discoveries making a difference?
    7. How do you want to wrap up today?
    8. Stop Recording, Transcribe and Paste Updates

  - **First Encounter** plan checklist (7 steps — from T108):

    1. Start Whisper Recording
    2. Introduction - The Agile Learning Institute
    3. Introduction - Mentor / Mentee
    4. How many weeks are you commiting to?
    5. What do you want to be able to say at the end of that time?
    6. Introduce Mentee Journey interface.
    7. Stop Recording, Transcribe, and Paste Updates

  - Generate **15** encounter documents with deterministic `_id` values `E00000000000000000000001` through `E00000000000000000000015`, ordered by session **date** (ascending). Use this mapping:

    | `_id` | Source file | `date` (from front matter) |
    | --- | --- | --- |
    | `E00000000000000000000001` | `2026-05-05 Mary-Anderson.md` | 2026-05-05T09:31:00.000Z |
    | `E00000000000000000000002` | `2026-05-06 Daniel-Dissler.md` | 2026-05-06T09:58:00.000Z |
    | `E00000000000000000000003` | `2026-05-07 Luther-Still.md` | 2026-05-07T09:31:00.000Z |
    | `E00000000000000000000004` | `2026-05-12 Mary-Anderson.md` | 2026-05-12T09:50:00.000Z |
    | `E00000000000000000000005` | `2026-05-28 Luther-Still Mentoring.md` | 2026-05-28T10:33:00.000Z |
    | `E00000000000000000000006` | `2026-06-03 Daniel-Dissler.md` | 2026-06-03T09:22:00.000Z |
    | `E00000000000000000000007` | `2026-06-04 Luther-Still.md` | 2026-06-04T10:02:00.000Z |
    | `E00000000000000000000008` | `2026-06-08 Lucky-Minyard.md` | 2026-06-08T09:33:00.000Z |
    | `E00000000000000000000009` | `2026-06-09 Mary-Anderson.md` | 2026-06-09T09:58:00.000Z |
    | `E00000000000000000000010` | `2026-06-11 Luther-Still.md` | 2026-06-11T09:46:00.000Z |
    | `E00000000000000000000011` | `2026-06-15 Lucky-Minyard.md` | 2026-06-15T09:58:00.000Z |
    | `E00000000000000000000012` | `2026-06-16 Mary-Anderson.md` | 2026-06-16T10:08:00.000Z |
    | `E00000000000000000000013` | `2026-06-17 Daniel-Dissler.md` | 2026-06-17T09:58:00.000Z |
    | `E00000000000000000000014` | `2026-06-18 Luther-Still.md` | 2026-06-18T10:05:00.000Z |
    | `E00000000000000000000015` | `2026-06-22 Lucky-Minyard.md` | 2026-06-22T10:00:00.000Z |

  - Derive **`transcript`**, **`summary`**, and **`tldr`** from each source markdown file:
    - **`transcript`**: Convert the `## Transcript` section. Replace `#### Speaker` headings with markdown speaker lines (`**Marti:**`, `**Mary:**`, `**Daniel:**`, `**Lucky:**`, `**Luke:**` for Luther Still). Join consecutive lines from the same speaker into paragraphs separated by blank lines. Trim to the `markdown` type max (4096 characters); if truncation is required, keep the opening and closing portions of the dialogue and note truncation in the task implementation notes.
    - **`summary`**: Prefer the `## Summary by gpt-oss:120b` **Summary** paragraph when present. Format as markdown (e.g. `## Summary\n<text>`). If the front-matter `summary` is empty or whitespace-only, use the TL;DR from the gpt-oss section or a one-paragraph distillation from the transcript.
    - **`tldr`**: Use the front-matter `summary` when non-empty; otherwise use the **TL;DR** line from the gpt-oss section. Must conform to the `sentence` type (no tabs or newlines; max 255 characters).
  - Set `status`: `active` for all encounters unless a source session is explicitly documented as cancelled/archived (none are today).
  - Include `created` and `saved` breadcrumb objects consistent with other seed documents (see `Encounter.0.1.0.0.json` and [data standards](../../mentorhub/DeveloperEdition/standards/data_standards.md)).
  - Do **not** modify Plan, Profile, or Mentee test data in this task.

## Goal

Re-seed the Encounter collection with realistic demo data that reflects actual mentorship sessions, uses the current **Standard** / **First Encounter** plan checklists for agendas, and references the correct Profile documents for Marti Lombardi and her mentees.

## Context / Input files

These files must be treated as **inputs** and read before implementation:

- The **Dictionary** and **Enumerators** linked in the **User inputs** section.
- The [type files](../configurator/types/) that map dictionary field types to JSON/BSON Schema fragments.
- [Data standards](../../mentorhub/DeveloperEdition/standards/data_standards.md) — collection naming, snake_case properties, and standard document fields.
- [SHIPPED.T107.generate_encounter_test_data.md](./SHIPPED.T107.generate_encounter_test_data.md) — prior Encounter seed conventions (superseded by this task).
- [SHIPPED.T108.generate_plan_test_data.md](./SHIPPED.T108.generate_plan_test_data.md) — **Standard** and **First Encounter** plan definitions and `_id` conventions.
- [SHIPPED.T102.generate_profile_test_data.md](./SHIPPED.T102.generate_profile_test_data.md) — Profile `$oid` conventions.
- [SHIPPED.T106.mentee_collection_and_profile_schema.md](./SHIPPED.T106.mentee_collection_and_profile_schema.md) — Mentee `profile_id` linkage and schedule context.
- `../configurator/dictionaries/Encounter.0.1.0.yaml` — Encounter schema (`agenda` as array of `{ checked, step }` objects).
- `../configurator/dictionaries/Plan.0.1.0.yaml` — Plan schema (`checklist` as array of sentences).
- `../configurator/test_data/Plan.0.1.0.0.json` — **Standard** and **First Encounter** plans (agenda source).
- `../configurator/test_data/Profile.0.1.0.0.json` — mentor and mentee Profile references.
- `../configurator/test_data/Mentee.0.1.0.0.json` — schedule context for date alignment.
- `../configurator/test_data/Encounter.0.1.0.0.json` — current seed file to replace.
- All **15** markdown files under `./encounters/` — primary source for transcripts, summaries, and session dates (removed after generation; not committed).

The agent may also consult:

- Existing test data in `../configurator/test_data/` for EJSON structure and breadcrumb style.
- `../Workshops/mentor_workshop.md` (in the mentorhub repo) for encounter-capture workflow context.

## Requirements

For the configured dictionary + enumerators, generate test data into the configured test‑data JSON file. Each document should conform to the inferred schema and obey the following rules:

1. **EJSON encoding** for use with MongoDB  
   - Every `_id` type value (identifier type) must be wrapped as `{ "$oid": "<24-byte hex>" }`.  
   - Every `date-time` value must be wrapped as `{ "$date": "<ISO-8601>" }`.  
   - Reference IDs that are not the primary `_id` but still use the identifier type must also be encoded with `$oid`.

2. **Schema‑driven generation**  
   - Use the dictionary plus its referenced type definitions in `../configurator/types/` to infer field names, data types, enum membership, and required vs optional fields.
   - Generate values that are valid for each field type and consistent with any constraints expressed in the simplified schema.

3. **Enum values**  
   - Use `active` for all encounters in this task. Ensure at least one `archived` value appears elsewhere in the database if required for enum coverage (not required in Encounter documents for this task).

4. **Document count**  
   - Generate exactly **15** documents — one per source file in `./encounters/`.

5. **Plan → Encounter agenda mapping**  
   - Copy checklist steps verbatim from the selected plan; do not add, remove, or reorder steps.
   - Example for the first two steps of the **Standard** plan:
     ```json
     "agenda": [
       { "step": "Start Whisper Recording", "checked": true },
       { "step": "What do you want to focus on today?", "checked": true }
     ]
     ```

6. **Field constraints**  
   - `transcript` and `summary` use the `markdown` type (max 4096 characters).
   - `tldr` uses the `sentence` type (no tabs or newlines; max 255 characters).
   - `agenda` is an array of objects with `step` (sentence) and `checked` (boolean).

7. **Profile linkage**  
   - Resolve mentee identity from the filename and **Attendees** section in each source file.
   - Cross-check `mentee_id` against `Profile.0.1.0.0.json` `full_name` before writing each document.
   - Use Marti Lombardi (`A00000000000000000000006`) as `mentor_id` for all encounters.

## Testing expectations

- **Processing test**
  - Use `curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"` to drop the MongoDB database so it can be re-configured.
  - Use `curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"` to Configure the Database.
  - Validate the configure result passed with a `SUCCESS` status; if it fails, inspect the JSON error message for details and update the test data accordingly.
- **Packaging test**
  - Run `make container` successfully.
  - Run `make process` and confirm `SUCCESS` in `artifacts/process_all_configurations.json`.

## Dependencies / Ordering

- **T102 (Profile)** — must be shipped; Encounter `mentor_id` and `mentee_id` reference Profile `$oid` values.
- **T106 (Mentee)** — Mentee schedule informs date realism.
- **T108 (Plan)** — must be shipped; **Standard** and **First Encounter** plans must exist in `Plan.0.1.0.0.json`.
- **Verify** – Before executing this task, first drop the database and configure the database using the curl commands listed above to ensure that we are starting from a clean configuration. If this test fails, stop execution and report an error message.

## Change control checklist

- [x] Reviewed all **Context / Input files**.
- [x] Captured concrete values in **User inputs (edit before running)**.
- [x] Designed and documented the solution approach in this file.
- [x] Implemented Encounter test data in `Encounter.0.1.0.0.json` with plan-aligned agendas and Profile-linked mentor/mentee ids.
- [x] Ran `make container` successfully.
- [x] Ran curl commands (or `make process`) to drop and configure database successfully.
- [x] Created a scoped commit referencing this task ID.

## Implementation notes (to be updated by the agent)

**Summary of changes**

Replaced 10 synthetic Encounter documents with **15** EJSON documents in `configurator/test_data/Encounter.0.1.0.0.json`, sourced from real mentorship session notes. Temporary source files under `Tasks/encounters/` were removed before commit.

**Approach**

- Mapped each session to deterministic `_id` values `E00000000000000000000001`–`15` ordered by date.
- Set `mentor_id` to Marti Lombardi (`A00000000000000000000006`) and `mentee_id` to the matching Profile for Mary, Daniel, Lucky, and Luther.
- Assigned **First Encounter** plan (`f00000000000000000000002`) to each mentee's earliest session; all others use **Standard** (`f00000000000000000000001`).
- Copied plan checklists verbatim into `agenda` with all steps `checked: true`.
- Converted markdown transcripts (speaker headings → `**Marti:**` / mentee names); remapped source mentor "Mike" to Marti for profile consistency.
- Six sessions had empty source transcripts (no-shows or not yet transcribed); left `transcript` empty for those documents.
- Truncated long transcripts at the 4096-character markdown limit where needed (E09, E13).

**Testing results**

- `make container` → SUCCESS.
- Configure Database: Encounter configuration and test-data load → SUCCESS (15 documents inserted).
- Branch still has pre-existing Resource / Resource_Aggregation configuration failures unrelated to this task.
