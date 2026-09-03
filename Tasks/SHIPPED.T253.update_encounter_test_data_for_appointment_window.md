# T253 – Replace Encounter seed `date` with `appointment.{from,to}` (F-D32)

**Status:** Shipped  
**Type:** Feature  
**Depends On:** T252  
**Description:** Update Encounter seed data so every document uses the new `appointment` object with `from` and `to` date-times instead of top-level `date`, while preserving existing persona pairings and status coverage.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- GitHub: [F-D32 EncounterAppointment #75](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/75)
- `Tasks/PENDING.T252.rename_encounter_date_to_appointment.md` — schema predecessor; configure may fail until this task ships
- `configurator/test_data/Encounter.0.1.0.0.json` — current Encounter seeds use top-level `date`
- `Tasks/SHIPPED.T213.realign_encounter_test_data_for_personas.md` — preserve mentor/mentee storyline and deterministic Encounter `_id`s
- `Tasks/PENDING.T249.cover_encounter_status_test_data.md` — if already shipped first, preserve whatever status distribution it established while moving to `appointment`
- `configurator/test_data/Plan.0.1.0.0.json` — `basic` plan reference remains unchanged
- **Out of scope:** dictionary edits (T252); changing plan references / agenda content; adding or removing Encounter documents unless required to preserve current status coverage already planned elsewhere

### Migration rules

- For every Encounter, delete top-level `date`.
- Add:

```json
"appointment": {
  "from": { "$date": "..." },
  "to": { "$date": "..." }
}
```

- Preserve the existing meeting start timestamp by moving it to `appointment.from`.
- Set `appointment.to` to a realistic end time after `from` for every document. Default to a one-hour mentoring window unless existing session narrative clearly supports a different duration; keep the rule consistent across the file.
- Keep `_id`, `mentor_id`, `mentee_id`, `plan_id`, `agenda`, `status`, `transcript`, `summary`, `tldr`, `created`, and `saved` unchanged unless a minimal timestamp adjustment is needed to keep chronology sensible.
- Breadcrumb `created.at_time` / `saved.at_time` may stay at the original encounter start time unless execution discovers a schema rule requiring alignment to `appointment.from`.

### Compatibility note

This task closes the expected interim configure failure introduced by T252. After this task, Encounter documents should validate with **no** top-level `date` properties remaining.

## Goals

- Every Encounter document uses `appointment.from` and `appointment.to`.
- No Encounter document retains top-level `date`.
- Existing persona relationships, narratives, and deterministic `_id` assignments remain intact.
- Configure-database returns **SUCCESS**.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200** and top-level **`status: SUCCESS`**.

MongoDB spot checks:

```javascript
db.Encounter.countDocuments({ date: { $exists: true } })  // 0
db.Encounter.countDocuments({ "appointment.from": { $exists: true } })  // == Encounter count
db.Encounter.countDocuments({ "appointment.to": { $exists: true } })    // == Encounter count
db.Encounter.countDocuments({ $expr: { $gte: ["$appointment.from", "$appointment.to"] } })  // 0
```

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Encounter.0.1.0.0.json` — replace top-level `date` with `appointment.{from,to}` on every document
- `Tasks/PENDING.T253.update_encounter_test_data_for_appointment_window.md` — this file (Execution Notes)

## Execution Notes
**2026-09-03 Plan**

- Update `configurator/test_data/Encounter.0.1.0.0.json` in place so each Encounter replaces top-level `date` with `appointment.from` and `appointment.to`.
- Preserve the current 11-document persona graph and status coverage established by prior tasks: `E00000000000000000000001` stays `complete`, `E0000000000000000000000b` stays `scheduled`, `E00000000000000000000009` stays `archived`, and the rest stay `active`.
- Use the existing timestamp as `appointment.from` and set `appointment.to` to one hour later for every document, leaving breadcrumbs and narrative fields unchanged unless validation requires otherwise.
- Verify locally with the configure-database flow and the task's MongoDB spot checks, then record results here.

**2026-09-03 Completion**

- Updated all 11 Encounter seed documents in `configurator/test_data/Encounter.0.1.0.0.json` to replace top-level `date` with `appointment.from` and `appointment.to`.
- Preserved the existing persona pairings, deterministic Encounter `_id`s, agendas, narrative fields, and the shipped status coverage: `E...01` remains `complete`, `E...0b` remains `scheduled`, `E...09` remains `archived`, and all other Encounter rows remain `active`.
- Kept each original meeting start time as `appointment.from` and set `appointment.to` to one hour later for a consistent mentoring window; breadcrumb timestamps stayed unchanged.

**Testing results**

- `make dev` succeeded locally.
- `DELETE /api/database/` on `http://localhost:8385` returned top-level `status: SUCCESS`.
- `POST /api/configurations/` on `http://localhost:8385` returned top-level `status: SUCCESS`; `CFG-05-Encounter.yaml` loaded **11** Encounter documents successfully.
- MongoDB spot checks passed: total Encounter count = **11**, `date` exists count = **0**, `appointment.from` exists count = **11**, `appointment.to` exists count = **11**, and invalid appointment windows (`from >= to`) = **0**.
- Packaging verification passed: `make down && make container && mh up mongodb` exited **0**.
