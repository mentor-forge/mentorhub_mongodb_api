# T255 – Update Mentee test data for simplified schema

**Status:** Shipped  
**Type:** Feature  
**Depends On:** T254  
**Description:** Update Mentee seed data in `Mentee.0.1.0.0.json` to match the simplified schema: rename `description` to `summary`, and remove `focus`, `homework`, `schedule`, and `next_appointment` across all Mentee documents, preserving persona relationships, notes, and statuses.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `Tasks/SHIPPED.T254.modify_mentee_schema.md` — schema predecessor (configure fails until this task ships)
- `configurator/test_data/Mentee.0.1.0.0.json` — 4 mentee seed documents (Daniel, Lucky, Mary, Linda)
- `Tasks/SHIPPED.T212.update_mentee_test_data_for_personas.md` — persona Mentee seed alignment
- `Tasks/scripts/persona_ids.json` — mentee IDs map
- **Out of scope:** Schema edits (completed in T254); changing persona IDs or mentor relationships; modifying other test data collections.

### Document transformation rules

For every document in `configurator/test_data/Mentee.0.1.0.0.json`:

1. Rename property `"description"` to `"summary"`, keeping the existing string value unchanged.
2. Remove property `"focus"`.
3. Remove property `"homework"`.
4. Remove property `"schedule"`.
5. Remove property `"next_appointment"`.
6. Retain `_id`, `summary`, `notes`, `status`, `created`, and `saved` intact.

### Document inventory

| Mentee `_id` | Persona | Target `summary` |
| --- | --- | --- |
| `A00000000000000000000002` | Daniel Dissler | `"Daniel is a Persevere graduate deepening frontend and Vue skills with Paula."` |
| `A00000000000000000000003` | Lucky Minyard | `"Lucky is a SuperSoft engineering apprentice building SRE and backend depth with Danny."` |
| `A00000000000000000000004` | Mary Anderson | `"Mary is a self-funded apprentice deepening full-stack skills with bi-weekly Marti sessions."` |
| `A00000000000000000000005` | Linda Left | `"Linda completed her ALI mentee program and left active learning; dossier retained for archive."` |

### Compatibility note

This task closes the interim configure failure introduced by T254. After this task ships, all Mentee documents validate against `Mentee.0.1.0.yaml` with `additional_properties: false`.

## Goals

- Every Mentee document in `configurator/test_data/Mentee.0.1.0.0.json` contains `summary` and no longer contains `description`.
- No Mentee document contains `focus`, `homework`, `schedule`, or `next_appointment`.
- All 4 persona documents retain unchanged `_id`, `notes`, `status`, `created`, and `saved` data.
- Configure-database succeeds with HTTP 200 and top-level `status: SUCCESS`.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200** and top-level **`status: SUCCESS`**.
- `CFG-05-Mentee.yaml` (or Mentee configuration step) imports all 4 documents cleanly without validation errors.

MongoDB spot checks:

```javascript
db.Mentee.countDocuments({ description: { $exists: true } })      // 0
db.Mentee.countDocuments({ focus: { $exists: true } })            // 0
db.Mentee.countDocuments({ homework: { $exists: true } })         // 0
db.Mentee.countDocuments({ schedule: { $exists: true } })         // 0
db.Mentee.countDocuments({ next_appointment: { $exists: true } }) // 0
db.Mentee.countDocuments({ summary: { $exists: true } })          // 4
db.Mentee.countDocuments({})                                      // 4
```

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Mentee.0.1.0.0.json` — rename `description` to `summary`, remove deprecated fields across all 4 documents
- `Tasks/SHIPPED.T255.update_mentee_test_data.md` — this file (Execution Notes)

## Execution Notes

### Plan

1. Update `configurator/test_data/Mentee.0.1.0.0.json` across all 4 documents to rename `"description"` to `"summary"` and remove `"focus"`, `"homework"`, `"schedule"`, and `"next_appointment"`.
2. Start dev services via `make dev`, drop the database with `DELETE /api/database/`, and apply configuration via `POST /api/configurations/`. Verify HTTP 200 and top-level `status: SUCCESS`.
3. Perform MongoDB spot checks via `mongosh` against `mentor_hub` database to ensure counts for legacy fields are 0 and `summary` is 4.
4. Verify packaging via `make down`, `make container`, and `mh up mongodb`.

### Completion Summary

- Updated all 4 Mentee seed documents in `configurator/test_data/Mentee.0.1.0.0.json`:
  - `A00000000000000000000002` (Daniel): renamed `description` to `summary`; removed `focus`, `homework`, `schedule`, `next_appointment`.
  - `A00000000000000000000003` (Lucky): renamed `description` to `summary`; removed `focus`, `homework`, `schedule`, `next_appointment`.
  - `A00000000000000000000004` (Mary): renamed `description` to `summary`; removed `focus`, `homework`, `schedule`, `next_appointment`.
  - `A00000000000000000000005` (Linda): renamed `description` to `summary`; removed `focus`, `homework`, `schedule`, `next_appointment`.
- Retained persona IDs, `notes`, `status`, `created`, and `saved` breadcrumbs intact.

### Test Results

- `make dev` — started local configurator dev services successfully.
- `curl -X DELETE "http://localhost:8385/api/database/"` — returned HTTP 200, `{"status": "SUCCESS", "type": "DROP_DATABASE"}`.
- `curl -X POST "http://localhost:8385/api/configurations/"` — returned HTTP 200 with top-level `status: SUCCESS`. `CFG-05-Mentee.yaml` loaded all 4 Mentee documents with `status: SUCCESS`.
- MongoDB spot checks:
  - `total`: 4
  - `description`: 0
  - `focus`: 0
  - `homework`: 0
  - `schedule`: 0
  - `next_appointment`: 0
  - `summary`: 4
- `make down` — local containers stopped cleanly.
- `make container` — successfully built Docker container image `ghcr.io/mentor-forge/mentorhub_mongodb_api:latest`.
- `mh up mongodb` — packaged container stack initialized and reached healthy state.
