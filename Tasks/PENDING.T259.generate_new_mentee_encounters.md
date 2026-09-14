# T259 – Generate encounters for new mentees with relative scheduling

**Status:** Pending  
**Type:** Feature  
**Depends On:** T258  
**Description:** Extend `Tasks/scripts/generate_encounter_test_data.py` and regenerate `configurator/test_data/Encounter.0.1.0.0.json` to include encounter records for all 11 new mentees. The majority of new mentees must have a combination of scheduled and completed encounters, with the "next" encounter scheduled for `now + random days (< 7)`.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`, `Tasks/scripts/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `Tasks/PENDING.T258.seed_mentee_profiles_and_dossiers.md` — predecessor task adding 11 mentee profiles
- `Tasks/scripts/generate_encounter_test_data.py` — generator script from T257
- `Tasks/scripts/persona_ids.json` — persona IDs map including new mentees
- `configurator/test_data/Encounter.0.1.0.0.json` — target encounter test data
- `configurator/test_data/Plan.0.1.0.0.json` — `Standard` plan (`f...01`) and `FirstEncounter` plan (`f...02`)
- `configurator/dictionaries/Encounter.0.1.0.yaml` — Encounter schema reference
- `Tasks/SHIPPED.T257.generate_expanded_encounter_test_data.md` — reference for Obsidian dialogue structure, actual windows, and no-show invariants
- **Out of scope:** Modifying schema or dictionaries; adding encounters for empty-state personas (`pat`, `helen`, `nora`, `donny`).

### Mentee Cohort Scheduling Distribution

For the 11 new mentees (`A...22` through `A...2c`), encounters are generated according to the following distribution:

| Mentee Profile `_id` | Persona | Mentor | Distribution Profile | Encounter Structure |
| --- | --- | --- | --- | --- |
| `A...22` | Jordan Persevere | Paula (`A...10`) | **Completed & Scheduled** | 6 completed (past), next at `now + random_days (<7)`, + 3 scheduled (future) |
| `A...23` | Taylor Persevere | Paula (`A...10`) | **Completed & Scheduled** | 4 completed (past), next at `now + random_days (<7)`, + 4 scheduled (future) |
| `A...24` | Casey SuperSoft | Danny (`A...14`) | **Completed & Scheduled** | 8 completed (past), next at `now + random_days (<7)`, + 2 scheduled (future) |
| `A...25` | Morgan SuperSoft | Danny (`A...14`) | **Completed & Scheduled** | 5 completed (past), next at `now + random_days (<7)`, + 3 scheduled (future) |
| `A...26` | Alex SuperSoft | Danny (`A...14`) | **Only Scheduled** | 0 completed, next at `now + random_days (<7)`, + 5 scheduled (future) |
| `A...27` | Sam Startup | Elon (`A...11`) | **Completed & Scheduled** | 6 completed (past), next at `now + random_days (<7)`, + 3 scheduled (future) |
| `A...28` | Riley Revenue | Elon (`A...11`) | **Completed & Scheduled** | 4 completed (past), next at `now + random_days (<7)`, + 4 scheduled (future) |
| `A...29` | Quinn Capital | Elon (`A...11`) | **Only Completed** | 8 completed (past), 0 scheduled (alumni / concluded program) |
| `A...2a` | Avery Design | Melinda (`A...15`) | **Completed & Scheduled** | 7 completed (past), next at `now + random_days (<7)`, + 3 scheduled (future) |
| `A...2b` | Devon Interface | Melinda (`A...15`) | **Completed & Scheduled** | 5 completed (past), next at `now + random_days (<7)`, + 3 scheduled (future) |
| `A...2c` | Harper Fullstack | Melinda (`A...15`) | **Only Scheduled** | 0 completed, next at `now + random_days (<7)`, + 4 scheduled (future) |

Summary:
- **Majority (8 of 11)** have a combination of completed and scheduled encounters.
- **2 of 11** have only scheduled encounters (new cohort entrants).
- **1 of 11** has only completed encounters (concluded coaching cycle).

### Scheduling and Timing Rules

1. **Relative Anchor (`now`)**:
   - Generator captures `now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)`.

2. **The "Next" Encounter (`now + random days (< 7)`)**:
   - For all mentees with scheduled sessions, the first upcoming encounter date `next_dt` is calculated as:
     `next_dt = now + timedelta(days=random_days, hours=random_hour_offset)`
     where `1 <= random_days <= 6` (strictly less than 7 days from `now`).
   - Subsequent scheduled encounters follow at weekly intervals: `next_dt + timedelta(days=7 * k)`.

3. **Past Completed Encounters**:
   - Scheduled times precede `now`: `next_dt - timedelta(days=7 * k)` (or relative to `now - timedelta(days=7 * k)`).
   - Completed encounters must be ordered chronologically.

4. **Plan and Agenda Checklist**:
   - **Encounter #1** for each mentee: uses `FirstEncounter` plan (`f00000000000000000000002`) with the 7-item onboarding checklist.
   - **Encounters #2+**: use `Standard` plan (`f00000000000000000000001`) with the 8-item standard coaching checklist.
   - All completed attended encounters have checklist items checked (`checked: true`).
   - Scheduled sessions have all checklist items unchecked (`checked: false`).

5. **Actual Windows and No-Show Invariants**:
   - Attended completed sessions: include `actual: {"from": ..., "to": ...}` with slight realistic variance (started 2–5 min late, ended 50–55 min later).
   - Flag 1–2 completed encounters across the new cohort as `"no_show": true`.
   - For `no_show: true` encounters: `transcript`, `summary`, `tldr`, and `actual` MUST BE OMITTED, and agenda items must be `checked: false`.
   - Scheduled encounters: omit `actual`, `transcript`, `summary`, and `tldr`.

6. **Transcripts, Summaries, and TLDRs**:
   - For attended completed sessions: generate realistic mentor/mentee dialogues tailored to the mentor's specialization and mentee's track.
   - `tldr`: single line, max 255 characters, no newlines/tabs (`sentence` type).
   - `summary`: markdown summary adhering to Obsidian format.

## Goals

- Extend `Tasks/scripts/generate_encounter_test_data.py` to generate encounters for all 11 new mentees alongside existing canonical encounters.
- Regenerate `configurator/test_data/Encounter.0.1.0.0.json`.
- Majority of new mentees (8/11) have both completed and scheduled encounters.
- Every new mentee with scheduled encounters has their next encounter scheduled within `now + random days (less than 7)`.
- Completed encounters have realistic Obsidian markdown summaries, transcripts, and TLDRs, with actual window timestamps.
- Configure-database succeeds with HTTP **200** and top-level **`status: SUCCESS`**.

## Testing Expectations

### Generator Execution

```sh
python3 Tasks/scripts/generate_encounter_test_data.py
```

- Generates clean, schema-valid EJSON records.

### Database Drop & Configure Test

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200** and top-level **`status: SUCCESS`**.
- `CFG-05-Encounter.yaml` imports all encounters cleanly without validation errors.

### MongoDB Spot Checks (`mongosh mentor_hub`)

```javascript
// Verify all 11 new mentees have encounters
const newMenteeIds = [
  "A00000000000000000000022", "A00000000000000000000023",
  "A00000000000000000000024", "A00000000000000000000025", "A00000000000000000000026",
  "A00000000000000000000027", "A00000000000000000000028", "A00000000000000000000029",
  "A0000000000000000000002a", "A0000000000000000000002b", "A0000000000000000000002c"
];

for (const id of newMenteeIds) {
  const count = db.Encounter.countDocuments({ mentee_id: ObjectId(id) });
  print(`Mentee ${id} encounter count: ${count}`);
}

// Verify next encounter is scheduled within 7 days from now
const now = new Date();
const in7Days = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000);

const nextEncounters = db.Encounter.find({
  status: "scheduled",
  "appointment.from": { $gte: now, $lt: in7Days }
}).count();
print(`Upcoming encounters in next 7 days: ${nextEncounters}`);

// Verify no-show invariants
db.Encounter.countDocuments({ no_show: true, actual: { $exists: true } }) // 0
db.Encounter.countDocuments({ no_show: true, summary: { $exists: true } }) // 0
```

### Packaging Verification

```sh
make down
make container
mh up mongodb
```

## Outputs

- `Tasks/scripts/generate_encounter_test_data.py` — extended encounter generation script
- `configurator/test_data/Encounter.0.1.0.0.json` — updated encounter test data
- `Tasks/PENDING.T259.generate_new_mentee_encounters.md` — this file (Execution Notes)

## Execution Notes

### Plan

1. Update `Tasks/scripts/generate_encounter_test_data.py` to import new mentee IDs from `persona_ids.json` and generate realistic encounter streams for all 11 new mentees.
2. Implement next-encounter scheduling logic relative to `now` with `random_days` strictly < 7 days.
3. Run the generator script to produce `configurator/test_data/Encounter.0.1.0.0.json`.
4. Start dev environment (`make dev`), drop database (`DELETE /api/database/`), and run configuration (`POST /api/configurations/`).
5. Execute MongoDB spot checks via `mongosh` to verify counts, distributions, next-encounter dates, and schema constraints.
6. Verify packaging (`make down`, `make container`, `mh up mongodb`).

### Completion Summary

*(To be filled by execution agent)*

### Test Results

*(To be filled by execution agent)*
