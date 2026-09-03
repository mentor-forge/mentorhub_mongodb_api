# T252 – Replace Encounter `date` with `appointment.{from,to}` (F-D32)

**Status:** Pending  
**Type:** Feature  
**Depends On:** none  
**Description:** Replace Encounter `date` with an embedded `appointment` object containing `from` and `to` date-times. Schema only — existing Encounter JSON still uses `date` until T253.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/dictionaries/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- GitHub: [F-D32 EncounterAppointment #75](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/75)
- `configurator/dictionaries/Encounter.0.1.0.yaml` — currently uses top-level `date: date-time`
- `configurator/test_data/Encounter.0.1.0.0.json` — current seed documents still carry top-level `date`
- `Tasks/SHIPPED.T213.realign_encounter_test_data_for_personas.md` — current Encounter persona/story distribution to preserve when test data moves to `appointment`
- `Tasks/PENDING.T248.add_encounter_status_enumerator.md` and `Tasks/PENDING.T249.cover_encounter_status_test_data.md` — nearby Encounter work; do not couple this task to status changes unless already present on branch
- **Out of scope:** Encounter seed-data migration (T253); status enum work (T248–T249); version bumps / migrations; changing Encounter indexes unless required by an existing `date` index is discovered during execution

### Target shape

Use an embedded object on Encounter:

```yaml
appointment:
  type: object
  properties:
    - name: from
      type: date-time
    - name: to
      type: date-time
```

- Remove top-level `date`.
- Keep property names **snake case**? No: the issue explicitly requires `from` and `to`; use those exact keys.
- Prefer an inline object definition in `Encounter.0.1.0.yaml` unless execution uncovers an existing configurator convention that requires a shared type file.
- `appointment.from` should represent scheduled start; `appointment.to` scheduled end.

This is a **tightening / shape change** with `additional_properties: false`: configure-database is expected to fail on current Encounter seed data until T253 removes `date` and supplies `appointment`.

## Goals

- Remove Encounter top-level `date` from `configurator/dictionaries/Encounter.0.1.0.yaml`.
- Add top-level `appointment` object with `from` and `to` date-time properties.
- Update Encounter descriptions so they describe a scheduled appointment window rather than a single timestamp.
- Keep the rest of the Encounter schema unchanged.
- Pre-release: edit the existing **0.1.0** Encounter dictionary in place; no version bump.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Dictionary load must not fail on YAML syntax or object-shape configuration errors.
- Configure-database **may fail** on Encounter seed data because documents still contain `date` and do not yet contain `appointment.from` / `appointment.to`. Confirm failures are Encounter test-data related, not dictionary syntax related.
- `make container` must succeed.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/dictionaries/Encounter.0.1.0.yaml` — replace `date` with embedded `appointment.{from,to}`
- `Tasks/PENDING.T252.rename_encounter_date_to_appointment.md` — this file (Execution Notes)

## Execution Notes
