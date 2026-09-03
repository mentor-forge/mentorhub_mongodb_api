# T249 – Cover Encounter Detail statuses in seed data (F-D30)

**Status:** Shipped  
**Type:** Feature  
**Depends On:** T248  
**Description:** Update Encounter test data so Developer Edition seeds include every `encounter_status` value required by SPA Encounter Detail: Scheduled, Active, Complete, and Archived.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- GitHub: [F-D30 EncounterStatus #73](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/73)
- `Tasks/PENDING.T248.add_encounter_status_enumerator.md` — schema predecessor
- `Tasks/SHIPPED.T213.realign_encounter_test_data_for_personas.md` — persona mentor–mentee graph
- `Tasks/SHIPPED.T237.seed_roster_encounter_activity.md` — empty-activity rules (helen, pat, nora, donny, patha-owner)
- `configurator/test_data/Encounter.0.1.0.0.json` — eleven documents `E000…01`–`E000…0b`; ten `active`, Linda `E000…09` `archived`
- `configurator/test_data/Plan.0.1.0.0.json` — `basic` plan `f00000000000000000000001`
- **Out of scope:** enumerator / dictionary edits (T248); Profile schema (T250–T251); adding Encounters for empty-activity personas; rewriting the whole Encounter file

### Current vs target status coverage (prefer retarget existing rows)

| `_id` (illustrative) | Today | Target | Notes |
| --- | --- | --- | --- |
| `E000…09` Linda / Marti | `archived` | **keep `archived`** | Historical archived mentee |
| One past primary session (e.g. `E000…01`) | `active` | **`complete`** | Finished Encounter Detail |
| One later / upcoming session (e.g. `E000…0a` or `E000…0b`) | `active` (dates 2026-07 / 2026-08) | **`scheduled`** | Booked session; set `date` **in the future** relative to seed time if needed |
| Remaining persona sessions | `active` | keep **`active`** | In-progress Encounter Detail |

Do **not** invent new mentor/mentee pairs. Keep T213/T237 counts and `_id`s unless a new document is required to hit a missing status — then append with next unused `E000…` hex and the `basic` plan.

Empty-state rules from T237 still hold: **no** Encounters for helen, pat, nora, donny, or patha-owner.

## Goals

- At least one Encounter for each of `scheduled`, `active`, `complete`, `archived`.
- Prefer in-place status (and `date` if needed for `scheduled`) over rewrite.
- Preserve persona linkage, agendas, and narrative fields except where status/`date` must change.
- Configure-database Encounter step returns **SUCCESS**.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200** and top-level **`status: SUCCESS`**.

MongoDB spot checks:

```javascript
db.Encounter.distinct("status")  // scheduled, active, complete, archived
db.Encounter.countDocuments({ status: "scheduled" })  // >= 1
db.Encounter.countDocuments({ status: "complete" })   // >= 1
db.Encounter.countDocuments({ status: "archived" })   // >= 1 (Linda)
db.Encounter.countDocuments({ mentee_id: ObjectId("A00000000000000000000019") })  // 0 (pat)
```

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Encounter.0.1.0.0.json` — retarget statuses (and `date` if needed) for F-D30 coverage
- `Tasks/PENDING.T249.cover_encounter_status_test_data.md` — this file (Execution Notes)

## Execution Notes
**Plan:** Retarget existing Encounter seeds in place so Developer Edition explicitly covers every `encounter_status` value without changing persona counts or `_id`s. Keep Linda `E000...09` as `archived`, convert one past active session to `complete`, convert one future-dated 2026 session to `scheduled`, and leave the remaining Encounter documents `active`; then re-run local configure-database checks plus the requested MongoDB status spot checks.

**Completed:** Updated `configurator/test_data/Encounter.0.1.0.0.json` in place so `E00000000000000000000001` is now `complete`, `E0000000000000000000000b` is now `scheduled`, and its `date`/breadcrumbs moved to `2026-12-09T15:00:00.000Z`; `E00000000000000000000009` stayed `archived` and the remaining Encounter seeds stayed `active`. This preserves the existing 11-document persona graph while explicitly covering `scheduled`, `active`, `complete`, and `archived`.

**Testing results**

- `make dev` completed successfully.
- `DELETE /api/database/` on `http://localhost:8385` returned top-level `status: SUCCESS`.
- `POST /api/configurations/` on `http://localhost:8385` returned top-level `status: SUCCESS`; `CFG-05-Encounter.yaml` loaded **11** Encounter documents successfully.
- MongoDB spot check returned `db.Encounter.distinct("status")` = `active`, `archived`, `complete`, `scheduled`.
- MongoDB counts: `scheduled` = **1**, `complete` = **1**, `archived` = **1**, `db.Encounter.countDocuments({ mentee_id: ObjectId("A00000000000000000000019") })` = **0** for pat.
- Packaging verification passed: `make down && make container && mh up mongodb` exited **0**.

**Follow-on info for orchestrator:** T249 now leaves Encounter seed coverage ready for downstream SPA/detail tasks with one explicit `complete` fixture (`E...01`) and one explicit future `scheduled` fixture (`E...0b`, `2026-12-09T15:00:00.000Z`). No new `_id`s were introduced and no empty-activity personas gained Encounter rows.
