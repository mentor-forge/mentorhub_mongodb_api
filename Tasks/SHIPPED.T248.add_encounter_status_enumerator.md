# T248 – Add `encounter_status` enumerator for Encounter Detail (F-D30)

**Status:** Shipped  
**Type:** Feature  
**Depends On:** none  
**Description:** Introduce a dedicated Encounter lifecycle enumerator (`scheduled`, `active`, `complete`, `archived`) and retarget Encounter `status` off `default_status` so SPA Encounter Detail can represent scheduled, in-progress, finished, and soft-deleted sessions.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/enumerators/`, `configurator/dictionaries/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- GitHub: [F-D30 EncounterStatus #73](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/73)
- `configurator/enumerators/enumerations.0.yaml` — `default_status` is only `active` / `archived`
- `configurator/dictionaries/Encounter.0.1.0.yaml` — `status.enums: default_status`
- `Tasks/SHIPPED.T220.extend_event_types_and_lifecycle_enums.md` — pattern: dedicated status enum (do **not** pollute `default_status`)
- `Tasks/SHIPPED.T213.realign_encounter_test_data_for_personas.md` — current seeds use `active` / `archived` only
- **Out of scope:** Encounter test-data status coverage (T249); Profile `name` / `display_name` (T250–T251); new Encounter properties; version bumps

### Enumerator (snake_case values; keep labels aligned with issue #73)

| Value | Intent |
| --- | --- |
| `scheduled` | Session is booked / not yet started (SPA: Scheduled) |
| `active` | Session in progress (SPA: Active) |
| `complete` | Session finished (SPA: Complete) — use `complete`, not `completed` |
| `archived` | Soft delete (SPA: Archived) |

Do **not** add these values to `default_status` (used by other collections). Prefer add of `encounter_status` over renaming existing enumerators.

Existing Encounter test documents use only `active` and `archived`, which remain valid after this widening. Configure-database must still **SUCCESS** in this task.

## Goals

- Add `encounter_status` to `enumerations.0.yaml` with the four values above and short descriptions.
- Point Encounter dictionary `status` at `encounter_status`.
- Leave `default_status` unchanged.
- Pre-release: edit enumerators / **0.1.0** dictionary in place; no version bump.

## Testing Expectations

```sh
make dev
# If host port 27017 is busy, use compose ports !override (e.g. host 27018) as in prior F-D tasks.
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200** and top-level **`status: SUCCESS`**. Existing Encounter seeds remain valid (`active` / `archived`).
- Confirm `encounter_status` appears in configurator output / loaded enums and Encounter config uses it.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/enumerators/enumerations.0.yaml` — add `encounter_status`
- `configurator/dictionaries/Encounter.0.1.0.yaml` — `status.enums: encounter_status`
- `Tasks/PENDING.T248.add_encounter_status_enumerator.md` — this file (Execution Notes)

## Execution Notes
**Plan:** Add a dedicated `encounter_status` enumerator to `configurator/enumerators/enumerations.0.yaml` with `scheduled`, `active`, `complete`, and `archived`, then retarget `configurator/dictionaries/Encounter.0.1.0.yaml` `status.enums` from `default_status` to `encounter_status`. Run the local configure-database flow to confirm existing Encounter seeds still load successfully and then perform the packaging verification commands required by this task.

**Completion:** Added `encounter_status` to `configurator/enumerators/enumerations.0.yaml` with the required four lifecycle values and left `default_status` unchanged. Retargeted `configurator/dictionaries/Encounter.0.1.0.yaml` `status.enums` to `encounter_status` in place with no version bump and no seed-data changes.

**Testing results**

- `make dev` completed successfully and started the local configurator stack.
- `DELETE http://localhost:8385/api/database/` returned top-level `status: SUCCESS`.
- `POST http://localhost:8385/api/configurations/` returned top-level `status: SUCCESS`; configurator output included `encounter_status`, and `CFG-05-Encounter.yaml` / `PRO-06-LOAD_TEST_DATA` for `Encounter.0.1.0.0.json` both succeeded with existing `active` / `archived` seed data.
- `make down`
- `make container`
- `mh up mongodb`

**Follow-on note:** Existing Encounter seed data still only exercises `active` and `archived`; dependent task T249 should add explicit `scheduled` and `complete` coverage.
