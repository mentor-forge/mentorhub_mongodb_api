# T108 – Generate Plan Test Data

**Status**: Shipped  
**Task Type**: Feature  
**Run Mode**: As Needed  

This is a reusable, parameterized task. A human should:

- Edit the **User inputs** section below to point at the desired dictionary, enumerators, and target test‑data file.
- Update `Status` from `As Needed` → `Pending`.
- Ask the agent/orchestrator to execute **pending** tasks.

## User inputs (edit before running)

- **Dictionary file** ../configurator/dictionaries/Plan.0.1.0.yaml
- **Enumerators file** ../configurator/enumerators/enumerations.0.yaml
- **Target test‑data file** ../configurator/test_data/Plan.0.1.0.0.json
- **Number of documents to generate**: `2`
- **Special requirements**
  - Replace the existing single `basic` plan in `Plan.0.1.0.0.json` with **two** plan documents as specified below.
  - Preserve `_id` `{ "$oid": "f00000000000000000000001" }` on the **Standard** plan so existing Encounter test data (`plan_id` references in `Encounter.0.1.0.0.json`) remain valid.
  - Assign the **First Encounter** plan `_id` `{ "$oid": "f00000000000000000000002" }`.
  - Use `status`: `active` for both plans.
  - Include `created` and `saved` breadcrumb objects consistent with other seed documents (see `Identity.0.1.0.0.json` and the current `Plan.0.1.0.0.json`).
  - Set human‑readable `description` values (sentence type) that match each plan's purpose.
  - Copy checklist step text **verbatim** from the lists below into each plan's `checklist` array (schema field name is `checklist`, not `steps`).

  **Plan 1 — `name`: `Standard`**

  | Order | Checklist step |
  | --- | --- |
  | 1 | Start Whisper Recording |
  | 2 | What do you want to focus on today? |
  | 3 | How would you describe what's happening now? |
  | 4 | During our time together, what would you like to accomplish? |
  | 5 | What would you like to be able to share next time? |
  | 6 | How are your discoveries making a difference? |
  | 7 | How do you want to wrap up today? |
  | 8 | Stop Recording, Transcribe and Paste Updates |

  **Plan 2 — `name`: `First Encounter`**

  | Order | Checklist step |
  | --- | --- |
  | 1 | Start Whisper Recording |
  | 2 | Introduction - The Agile Learning Institute |
  | 3 | Introduction - Mentor / Mentee |
  | 4 | How many weeks are you commiting to? |
  | 5 | What do you want to be able to say at the end of that time? |
  | 6 | Introduce Mentee Journey interface. |
  | 7 | Stop Recording, Transcribe, and Paste Updates |

## Goal

Given a **dictionary**, its **enumerators**, and the supporting **type files**, generate a set of EJSON documents that conform to the effective schema and write them to the configured test‑data file.

## Context / Input files

These files must be treated as **inputs** and read before implementation:

- The **Dictionary** and **Enumerators** linked in the **User inputs** section.
- The [type files](../configurator/types/) that map dictionary field types to JSON/BSON Schema fragments.
- [Data standards](../../mentorhub/DeveloperEdition/standards/data_standards.md) — collection naming, snake_case properties, and standard document fields (`_id`, `status`, `name`, `description`, `created`, `saved`).
- `../configurator/dictionaries/Plan.0.1.0.yaml` — Plan schema (`checklist` as array of sentences; unique index on `name`).
- `../configurator/test_data/Plan.0.1.0.0.json` — current seed file (single `basic` plan to be replaced).
- `../configurator/test_data/Encounter.0.1.0.0.json` — references `f00000000000000000000001` as `plan_id`; do **not** change Encounter data in this task, but be aware agendas still contain the old `basic` checklist text until a follow‑up sync.

The agent may also consult:

- Existing test data in `../configurator/test_data/` for EJSON structure and breadcrumb style.
- [SHIPPED.T107.generate_encounter_test_data.md](./SHIPPED.T107.generate_encounter_test_data.md) — documents the prior `basic` plan → Encounter `plan_id` / `agenda` relationship.

## Requirements

For the configured dictionary + enumerators (which together describe a single document type), generate test data into the configured test‑data JSON file. Each document should conform to the inferred schema and obey the following rules:

1. **EJSON encoding** for use with MongoDB  
   - Every `_id` type value (identifier type) must be wrapped as `{ "$oid": "<24-byte hex>" }`.  
   - Every `date-time` value must be wrapped as `{ "$date": "<ISO-8601>" }`.  
   - Reference IDs that are not the primary `_id` but still use the identifier type must also be encoded with `$oid`.

2. **Schema‑driven generation**  
   - Use the dictionary plus its referenced type definitions in `../configurator/types/` to infer:
     - Field names, data types, enum membership, and required vs optional fields.
   - Generate values that are valid for each field type (e.g., strings, numbers, enums, nested objects, arrays) and consistent with any constraints expressed in the simplified schema.

3. **Enum values**  
   - When a property is an enum, assign values at random **but ensure that every listed enum value appears at least once** across the generated documents.  
   - For this task, both plans use `active` from the `default_status` enum.

4. **Document count and variability**  
   - Generate exactly **2** plan documents as specified in **User inputs**.  
   - Plan names must be unique (`Standard`, `First Encounter`) to satisfy the `name` unique index on the Plan collection.

5. **Special instructions**  
   - Follow the exact checklist content and ordering in the **User inputs** tables.  
   - Do not add, remove, or reword checklist steps unless explicitly instructed.  
   - Replace the entire contents of `Plan.0.1.0.0.json` — do not append a third plan alongside the obsolete `basic` plan.

6. **Field constraints**  
   - `name` uses the `word` type (indexed, unique per collection).  
   - `description` uses the `sentence` type.  
   - Each `checklist` item uses the `sentence` type (no tabs or newlines within a step).

7. **Identifier conventions**  
   - **Standard** plan: `_id` `f00000000000000000000001` (replaces legacy `basic` plan at the same id).  
   - **First Encounter** plan: `_id` `f00000000000000000000002`.

## Testing expectations

- **Processing test**
  - Use `curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"` to drop the MongoDB database so it can be re-configured.
  - Use `curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"` to Configure the Database.
  - Validate the configure result passed with a `SUCCESS` status; if it fails, inspect the JSON error message for details and update the test data accordingly.
- **Packaging test**
  - Run `make container` successfully.
  - Run `make process` and confirm `SUCCESS` in `artifacts/process_all_configurations.json`.

## Dependencies / Ordering

- **Verify** – Before executing this task, first drop the database and configure the database using the curl commands listed above to ensure that we are starting from a clean configuration. If this test fails, stop execution and report an error message.
- **Downstream note** – [SHIPPED.T107.generate_encounter_test_data.md](./SHIPPED.T107.generate_encounter_test_data.md) copied agenda steps from the old `basic` plan. After T108 ships, Encounter `agenda` step text will be stale relative to the **Standard** checklist. That inconsistency does not block Configure Database, but a future task should resync Encounter agendas if realistic demo data is required.

## Change control checklist

- [x] Reviewed all **Context / Input files**.
- [x] Captured concrete values in **User inputs (edit before running)**.
- [x] Designed and documented the solution approach in this file.
- [x] Implemented Plan test data in `Plan.0.1.0.0.json` with **Standard** and **First Encounter** plans.
- [ ] Ran `make container` successfully.
- [ ] Ran curl commands (or `make process`) to drop and configure database successfully — **skipped** per user request (branch has breaking changes; validate after PR is opened).
- [ ] Created a scoped commit referencing this task ID.

## Implementation notes (to be updated by the agent)

**Summary of changes**

Replaced the single legacy `basic` plan in `configurator/test_data/Plan.0.1.0.0.json` with two EJSON plan documents: **Standard** (8 checklist steps) and **First Encounter** (7 checklist steps).

**Approach**

- Kept `_id` `f00000000000000000000001` on **Standard** so existing Encounter `plan_id` references remain valid.
- Assigned `_id` `f00000000000000000000002` to the onboarding plan.
- Copied checklist step text verbatim from the task specification.
- Used `name`: `FirstEncounter` for the second plan because the `word` type pattern (`^[^\s]{1,40}$`) does not allow spaces; the human label "First Encounter" is reflected in the `description`.
- Reused breadcrumb structure and timestamps from the prior Plan seed data; updated correlation ids to `seed-plan-*` / `save-plan-*`.

**Testing results**

- Configure Database / `make process` — **skipped** per user request (breaking changes on branch; to be validated after PR is opened).
