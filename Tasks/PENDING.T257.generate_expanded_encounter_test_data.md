# T257 – Generate expanded Encounter test data with relative schedules and no-shows (F-D33)

**Status:** Pending  
**Type:** Feature  
**Depends On:** T256  
**Description:** Create `Tasks/scripts/generate_encounter_test_data.py` and regenerate `configurator/test_data/Encounter.0.1.0.0.json` so every Mentee has at least 12 weekly encounter records, relative `Now() +/- days` windows, `actual` appointment times on completed/active sessions, `no_show` flags on select completed sessions (without transcript/summary/tldr), `FirstEncounter` vs `Standard` plans, Obsidian-aligned transcript/summary formats, and required persona status distributions.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`, `Tasks/scripts/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- GitHub: [F-D33 Encounter Test Data #79](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/79)
- `Tasks/PENDING.T256.add_encounter_actual_and_no_show_properties.md` — schema predecessor (`actual` and `no_show` properties)
- `configurator/test_data/Encounter.0.1.0.0.json` — current Encounter test data
- `configurator/test_data/Plan.0.1.0.0.json` — `Standard` plan (`f00000000000000000000001`) and `FirstEncounter` plan (`f00000000000000000000002`)
- `configurator/test_data/Mentee.0.1.0.0.json` — persona mentees (Daniel, Lucky, Mary, Linda)
- `configurator/test_data/Profile.0.1.0.0.json` — persona profiles and mentor relationships (Paula, Danny, Marti, Elon)
- `Tasks/scripts/persona_ids.json` — canonical persona ObjectIds
- `Tasks/scripts/generate_event_test_data.py` — reference script pattern for repeatable test data generation
- `../mentorhub/Workshops/2026-07-21 Mary-Anderson (2).md` — reference Obsidian encounter structure (frontmatter summary `tldr`, gpt summary, transcript dialogue, agenda questions)
- `Tasks/SHIPPED.T213.realign_encounter_test_data_for_personas.md` — persona relationship narrative context
- `Tasks/SHIPPED.T237.seed_roster_encounter_activity.md` — roster empty-state rules (pat `A...19` has 0 encounters)
- **Out of scope:** Modifying dictionary schemas or enumerators; modifying other collection seed data (`Event`, `Profile`, `Mentee`); changing Profile/Customer stable IDs; adding encounters for empty-roster personas (`pat`, `helen`, `nora`, `donny`).

### Mentee Persona Allocation

The 4 canonical mentees from `Mentee.0.1.0.0.json` and `persona_ids.json` are allocated to satisfy issue #79's status requirements:

| Mentee | Profile `_id` | Primary Mentor | Required Distribution | Schedule / Session Breakdown |
| --- | --- | --- | --- | --- |
| **Linda Left** | `A00000000000000000000005` | Marti (`A...06`) | **Only historical completed encounters** (1 mentee) | 12 completed sessions in past (weeks -12 to -1). One session flagged `no_show: true`. Archived dossier context. |
| **Mary Anderson** | `A00000000000000000000004` | Marti (`A...06`) | **Only future scheduled encounters** (1 mentee) | 12 scheduled sessions in future (weeks +1 to +12). No past sessions. |
| **Daniel Dissler** | `A00000000000000000000002` | Paula (`A...10`) / Elon (`A...11`) | **Mixture of scheduled and completed** (most mentees) | 8 completed sessions (weeks -8 to -1; includes 1 Elon money session and 1 `no_show: true`) + 4 scheduled sessions (weeks +1 to +4). |
| **Lucky Minyard** | `A00000000000000000000003` | Danny (`A...14`) / Elon (`A...11`) | **Mixture of scheduled, 1 active, and completed** (some mentees) | 7 completed sessions (weeks -7 to -1; includes 1 Elon money session) + 1 active session in progress (week 0) + 4 scheduled sessions (weeks +1 to +4). |
| **Pat Persevere** | `A00000000000000000000019` | Paula (`A...10`) | **None (0 encounters)** | Preserved empty-activity row on populated Persevere roster per T236/T237 empty-state test requirements. |

### Document Transformation and Field Rules

1. **Relative Weekly Scheduling (`Now() +/- days`)**:
   - Generator script computes timestamps relative to `now = datetime.now(timezone.utc)` (rounded to standard meeting hour):
     - Past completed sessions: `appointment.from = now - timedelta(days=7 * week_offset)`
     - Active session: `appointment.from = now - timedelta(minutes=15)` (session started 15 minutes ago)
     - Future scheduled sessions: `appointment.from = now + timedelta(days=7 * week_offset)`
     - Scheduled duration: 1 hour (`appointment.to = appointment.from + timedelta(hours=1)`).

2. **Actual Encounter Window (`actual`)**:
   - For attended completed sessions: `actual` object contains `from` and `to` date-times reflecting realistic slight variations (e.g. started 2–3 minutes after scheduled, ended 50–58 minutes later).
   - For the active session: `actual` contains `from` date-time matching when the meeting started.
   - For `no_show: true` encounters and `scheduled` encounters: `actual` is omitted.

3. **No-Show Handling (`no_show`)**:
   - At least two completed encounters (one for Daniel, one for Linda) are flagged with `"no_show": true`.
   - For `no_show: true` encounters:
     - `transcript`, `summary`, and `tldr` MUST BE OMITTED.
     - `actual` MUST BE OMITTED.
     - `agenda` steps remain all `{ "checked": false }`.
   - For attended completed sessions: `"no_show": false`.

4. **Plan & Agenda Mapping**:
   - **Encounter #1** for each mentee:
     - `plan_id = { "$oid": "f00000000000000000000002" }` (`FirstEncounter`).
     - `agenda`: 7 checklist items copied verbatim from `FirstEncounter` plan in `Plan.0.1.0.0.json`.
   - **Encounters #2–#12+** for each mentee:
     - `plan_id = { "$oid": "f00000000000000000000001" }` (`Standard`).
     - `agenda`: 8 checklist items copied verbatim from `Standard` plan in `Plan.0.1.0.0.json`.
   - `agenda.checked` state:
     - Completed attended sessions: all or majority (6–8) steps `checked: true`.
     - Active session: first 2–3 steps `checked: true`, remaining `checked: false`.
     - Scheduled sessions & no-shows: all steps `checked: false`.

5. **Transcripts, Summaries, and TLDRs (Obsidian Style)**:
   - For attended completed sessions:
     - `transcript`: realistic dialogue between mentor and mentee formatted in markdown.
     - `summary`: multi-line markdown summary following Obsidian notes format (`## Summary ...`).
     - `tldr`: single sentence summary conforming to `sentence` type (no tabs or newlines, max 255 characters), matching the Obsidian YAML frontmatter `summary:` field.
   - For `scheduled` sessions: `transcript`, `summary`, and `tldr` are omitted.

6. **Deterministic Identifiers**:
   - Generate exactly 48 encounter documents (12 per mentee * 4 mentees).
   - Use deterministic ObjectId strings `E00000000000000000000001` through `E00000000000000000000030` (48 in hex).
   - Preserve existing IDs `E...01` through `E...0b` for their respective persona pairings to maintain cross-collection event compatibility.

## Goals

- Create `Tasks/scripts/generate_encounter_test_data.py` to automate repeatable Encounter generation.
- Regenerate `configurator/test_data/Encounter.0.1.0.0.json` with 48 valid EJSON documents.
- Every Mentee (Daniel, Lucky, Mary, Linda) has at least 12 weekly encounter records.
- Linda has only historical completed encounters.
- Mary has only future scheduled encounters.
- Daniel has a mixture of scheduled and completed encounters.
- Lucky has a mixture of scheduled, 1 active, and completed encounters.
- At least two completed encounters are flagged as `no_show: true` and omit `transcript`, `summary`, `tldr`, and `actual`.
- Attended completed encounters include `actual` appointment windows.
- First encounter uses `FirstEncounter` plan; subsequent encounters use `Standard` plan.
- Configure-database returns HTTP **200** with top-level **`status: SUCCESS`**.

## Testing Expectations

### Test Data Generation

```sh
python3 Tasks/scripts/generate_encounter_test_data.py
```

### Database Drop & Configure Test

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200** and top-level **`status: SUCCESS`**.
- `CFG-05-Encounter.yaml` step must import all 48 documents cleanly without schema validation errors.

### MongoDB Spot Checks (`mongosh mentor_hub`)

```javascript
// Total count
db.Encounter.countDocuments({}) // >= 48

// Per-mentee counts
db.Encounter.countDocuments({ mentee_id: ObjectId("A00000000000000000000002") }) // Daniel == 12
db.Encounter.countDocuments({ mentee_id: ObjectId("A00000000000000000000003") }) // Lucky == 12
db.Encounter.countDocuments({ mentee_id: ObjectId("A00000000000000000000004") }) // Mary == 12
db.Encounter.countDocuments({ mentee_id: ObjectId("A00000000000000000000005") }) // Linda == 12

// Preserved empty-state check for Pat
db.Encounter.countDocuments({ mentee_id: ObjectId("A00000000000000000000019") }) // 0

// Status distributions
db.Encounter.countDocuments({ mentee_id: ObjectId("A00000000000000000000005"), status: "complete" }) // Linda == 12
db.Encounter.countDocuments({ mentee_id: ObjectId("A00000000000000000000004"), status: "scheduled" }) // Mary == 12
db.Encounter.countDocuments({ mentee_id: ObjectId("A00000000000000000000003"), status: "active" }) // Lucky == 1

// No-show validation
db.Encounter.countDocuments({ no_show: true }) // >= 2
db.Encounter.countDocuments({ no_show: true, transcript: { $exists: true } }) // 0
db.Encounter.countDocuments({ no_show: true, summary: { $exists: true } }) // 0
db.Encounter.countDocuments({ no_show: true, tldr: { $exists: true } }) // 0
db.Encounter.countDocuments({ no_show: true, actual: { $exists: true } }) // 0

// Actual window validation
db.Encounter.countDocuments({ status: "complete", no_show: { $ne: true }, "actual.from": { $exists: true } }) // > 0

// FirstEncounter plan validation (each mentee's first encounter)
db.Encounter.countDocuments({ plan_id: ObjectId("f00000000000000000000002") }) // 4
```

### Packaging Verification

```sh
make down
make container
mh up mongodb
```

- Confirm container image builds and full local stack reaches healthy status.

## Outputs

- `Tasks/scripts/generate_encounter_test_data.py` — generator script for expanded relative encounter data
- `configurator/test_data/Encounter.0.1.0.0.json` — 48 encounter documents matching issue #79 requirements
- `Tasks/PENDING.T257.generate_expanded_encounter_test_data.md` — this file (Execution Notes)

## Execution Notes

*Reserved for the task execution agent to record plan, commands run, test results, and follow-ups.*
