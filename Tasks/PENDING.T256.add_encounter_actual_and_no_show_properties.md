# T256 – Add Encounter actual and no_show properties (F-D33)

**Status:** Pending  
**Type:** Feature  
**Depends On:** none  
**Description:** Add `actual` (type: `appointment`) and `no_show` (type: `boolean`) properties to Encounter dictionary in `Encounter.0.1.0.yaml`. Schema update only — existing Encounter test data remains valid since new properties are optional.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/dictionaries/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- GitHub: [F-D33 Encounter Test Data #79](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/79)
- `configurator/dictionaries/Encounter.0.1.0.yaml` — current Encounter dictionary definition
- `configurator/types/appointment.yaml` — existing reusable appointment type (`from`, `to` date-times)
- `configurator/types/boolean.yaml` — existing reusable boolean type
- `configurator/test_data/Encounter.0.1.0.0.json` — current Encounter seed documents
- `Tasks/SHIPPED.T252.rename_encounter_date_to_appointment.md` — prior Encounter schema work
- `Tasks/SHIPPED.T253.update_encounter_test_data_for_appointment_window.md` — prior Encounter test data work
- **Out of scope:** Encounter test data regeneration and expansion (deferred to dependent task T257); modifying other dictionaries or enumerators; version bumps (pre-release in-place edits).

### Target schema shape

Add two properties to `configurator/dictionaries/Encounter.0.1.0.yaml`:

```yaml
  - description: When the encounter actually happened
    name: actual
    required: false
    type: appointment
  - description: Flag indicating whether the encounter was a no-show
    name: no_show
    required: false
    type: boolean
```

- `actual` uses the existing reusable type `appointment` defined in `configurator/types/appointment.yaml` (which specifies `{ from, to }` date-time properties).
- `no_show` uses the existing reusable type `boolean` defined in `configurator/types/boolean.yaml`.
- Place `actual` adjacent to the scheduled `appointment` property to keep scheduling fields grouped.
- Maintain `root.additional_properties: false`.

### Compatibility note

This is a schema relaxation/extension adding two optional properties to Encounter. Because `required: false` is used, existing Encounter documents in `configurator/test_data/Encounter.0.1.0.0.json` remain valid and will pass schema validation during this task. Unlike tightening changes, `POST /api/configurations/` must return HTTP 200 with top-level `status: SUCCESS`.

## Goals

- Add `actual` (type: `appointment`, description: `"When the encounter actually happened"`, `required: false`) to `configurator/dictionaries/Encounter.0.1.0.yaml`.
- Add `no_show` (type: `boolean`, description: `"Flag indicating whether the encounter was a no-show"`, `required: false`) to `configurator/dictionaries/Encounter.0.1.0.yaml`.
- Ensure `root.additional_properties` remains `false`.
- Keep all existing properties, descriptions, types, and enumerators unchanged.
- Pre-release: edit the existing **0.1.0** Encounter dictionary in place; no version bump.
- Verify dictionary loads cleanly and existing Encounter test data continues to validate with HTTP 200 SUCCESS.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Dictionary load must succeed with no YAML syntax or type-resolution errors.
- Both curl commands must return HTTP **200** and top-level **`status: SUCCESS`**.
- Existing Encounter seed data (`Encounter.0.1.0.0.json`) must pass validation without write errors.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

- Verify container builds cleanly and packaged stack starts with healthy MongoDB status.

## Outputs

- `configurator/dictionaries/Encounter.0.1.0.yaml` — add `actual` and `no_show`
- `Tasks/PENDING.T256.add_encounter_actual_and_no_show_properties.md` — this file (Execution Notes)

## Execution Notes

*Reserved for the task execution agent to record plan, commands run, test results, and follow-ups.*
