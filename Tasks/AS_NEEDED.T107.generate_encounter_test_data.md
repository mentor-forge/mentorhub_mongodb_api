# T107 – Generate Encounter Test Data

**Status**: As Needed  
**Task Type**: Feature  
**Run Mode**: As Needed 

This is a reusable, parameterized task. A human should:

- Edit the **User inputs** section below to point at the desired dictionary, enumerators, and target test‑data file.
- Update `Status` from `As Needed` → `Pending`.
- Ask the agent/orchestrator to execute **pending** tasks.

## User inputs (edit before running)

- **Dictionary file** ../configurator/dictionaries/Encounter.0.1.0.yaml
- **Enumerators file** ../configurator/enumerators/enumerations.0.yaml
- **Target test‑data file** ../configurator/test_data/Encounter.0.1.0.0.json
- **Number of documents to generate**: `10`
- **Special requirements**
  - Use the existing Plan in `../configurator/test_data/Plan.0.1.0.0.json` (`name`: `basic`, `_id`: `f00000000000000000000001`) as `plan_id` for all encounters. Do **not** modify Plan test data.
  - For each encounter, set `agenda` to a **copy** of that Plan's `checklist`, transformed into Encounter agenda items: each checklist sentence becomes `{ "step": "<sentence>", "checked": <boolean> }`. Every Plan checklist step must appear in order; vary `checked` values to reflect meeting progress (e.g. completed sessions have most steps checked; archived sessions may have all checked).
  - Generate **10** encounter documents with deterministic `_id` values starting at `E00000000000000000000001`.
  - Use **Marti Lombardi** (`Profile` `A00000000000000000000006`) as `mentor_id` for all encounters.
  - Create encounters for these mentees (use their Profile `$oid` as `mentee_id`):
    - Daniel Dissler — 2 encounters (recent progress on Vue/API work)
    - Lucky Minyard — 2 encounters (backend and system-design topics)
    - Mary Anderson — 2 encounters (career pivot from music education to IT)
    - Luther Still — 2 encounters (longer-tenure mentee; one should use `archived` status for `default_status` enum coverage)
    - Riley Mentee — 1 encounter
    - Casey Archived — 1 encounter (`archived` status; historical session before archival)
  - Set `date` to realistic past meeting times spread over the last **6 months**, aligned where possible with `next_appointment` / `schedule` in `Mentee.0.1.0.0.json`.
  - Include believable `transcript` (markdown, mentor/mentee dialogue), a shorter `summary` (markdown), and a one-line `tldr` (sentence type — no newlines or tabs).
  - Transcripts should reference EngineerKit journey progress where appropriate (see `Journey.0.1.0.0.json` and `Path.0.1.0.0.json`).

## Goal

Given a **dictionary**, its **enumerators**, and the supporting **type files**, generate a set of EJSON documents that conform to the effective schema and write them to the configured test‑data file.

## Context / Input files

These files must be treated as **inputs** and read before implementation:

- The **Dictionary** and **Enumerators** linked in the **User inputs** section.
- The [type files](../configurator/types/) that map dictionary field types to JSON/BSON Schema fragments.
- [SHIPPED.T102.generate_profile_test_data.md](./SHIPPED.T102.generate_profile_test_data.md) — Profile `$oid` conventions and mentor/mentee relationships.
- [SHIPPED.T105.generate_journey_test_data.md](./SHIPPED.T105.generate_journey_test_data.md) — Journey progress context for realistic transcripts.
- `../configurator/dictionaries/Plan.0.1.0.yaml` — Plan schema (`checklist` as array of sentences).
- `../configurator/dictionaries/Encounter.0.1.0.yaml` — Encounter schema (`agenda` as array of `{ checked, step }` objects).
- `../configurator/test_data/Profile.0.1.0.0.json` — mentor and mentee Profile references.
- `../configurator/test_data/Mentee.0.1.0.0.json` — schedule and mentoring notes for transcript realism.
- `../configurator/test_data/Plan.0.1.0.0.json` — the `basic` plan used for `plan_id` and as the source for each encounter's `agenda`.
- `../configurator/test_data/Journey.0.1.0.0.json` — learning progress to mention in transcripts.

The agent may also consult:

- Existing test data in `../configurator/test_data/` for style and structure.
- `../Workshops/mentor_workshop.md` (in the mentorhub repo) for encounter-capture workflow context.

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
   - If special instructions mention specific enum values, obey those rules (for example, “use only `active` and `archived`”).

4. **Document count and variability**  
   - Generate exactly the number of documents specified in **User inputs** (default: `15`).  
   - Vary field values so the documents are realistic and cover diverse paths (different enum values, dates, and combinations where appropriate).

5. **Special instructions**  
   - Follow any additional constraints or preferences listed in the **Special requirements** bullet(s) above (for example, distributions, required relationships between fields, or edge cases to include).

6. **Field constraints**  
   - `transcript` and `summary` use the `markdown` type (max 4096 characters).
   - `tldr` uses the `sentence` type (no tabs or newlines; max 255 characters).
   - `agenda` is an array of objects with `step` (sentence) and `checked` (boolean). Copy steps verbatim from the Plan `checklist`; do not add, remove, or reorder steps.

7. **Plan → Encounter agenda mapping**  
   - `plan_id` must reference `{ "$oid": "f00000000000000000000001" }` (the `basic` plan).
   - Transform each Plan checklist string into an agenda item. Example for the first two steps of the `basic` plan:
     ```json
     "agenda": [
       { "step": "Start Session Recording in Whisper", "checked": true },
       { "step": "What do you want to focus on today?", "checked": true },
       { "step": "How would you describe what's happening now?", "checked": false }
     ]
     ```

## Testing expectations

- **Processing test**
  - Use `curl -X DELETE "http://localhost:8383/api/database/" -H "accept: application/json"` to drop the MongoDB database so it can be re-configured.
  - Use `curl -X POST "http://localhost:8383/api/configurations/" -H "accept: application/json"` to Configure the Database 
  - Validate the configure result passed with a `SUCCESS` status; if it fails, inspect the JSON Error message for details and update the test data accordingly. 

## Dependencies / Ordering

- **T102 (Profile)** — must be shipped; Encounter `mentor_id` and `mentee_id` reference Profile `$oid` values.
- **T106 (Mentee)** — Mentee schedule/notes inform realistic encounter dates and transcript content.
- **Plan test data** — `Plan.0.1.0.0.json` must already contain the `basic` plan (`f00000000000000000000001`). Do not seed or modify Plan test data in this task.
- **Verify** – Before executing this task, first drop the database and configure the database using the curl commands listed above to ensure that we are starting from a clean configuration. If this test fails, stop execution and report an error message.

## Change control checklist

- [ ] Reviewed all **Context / Input files**.
- [ ] Captured concrete values in **User inputs (edit before running)**.
- [ ] Designed and documented the solution approach in this file.
- [ ] Implemented Encounter test data in `Encounter.0.1.0.0.json` with `plan_id` and `agenda` copied from the `basic` plan.
- [ ] Ran `make container` successfully.
- [ ] Ran curl commands to drop and configure database successfully.
- [ ] Created a scoped commit referencing this task ID.

## Implementation notes (to be updated by the agent)

**Summary of changes**
