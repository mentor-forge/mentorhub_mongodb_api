# T251 – Update Profile seeds and README for `display_name` (F-D31)

**Status:** Shipped  
**Type:** Feature  
**Depends On:** T250  
**Description:** Align all Profile test documents with the F-D31 schema: remove `name`, rename `full_name` to `display_name`, keep uniqueness, and retitle the README persona matrix column.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`, `README.md`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md` — Test Personas matrix currently has a `full_name` column; Slug documents login.html / JWT persona keys (not a Profile field after T250)
- GitHub: [F-D31 ProfileDisplayName #74](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/74)
- `Tasks/PENDING.T250.rename_profile_display_name.md` — schema predecessor (configure may fail until this task)
- `configurator/test_data/Profile.0.1.0.0.json` — every document has `name` (slug) and `full_name` (display)
- `Tasks/scripts/persona_ids.json` — slug → `_id` map only (no `full_name`); do not invent fields
- `Tasks/SHIPPED.T217.document_personas_in_readme.md` — persona matrix layout
- **Out of scope:** Encounter status (T248–T249); changing Profile `_id`s or login slugs; editing `welcome-auth.js` (external `mentorhub` repo); rewriting experience / goals / roles

### Field rules

- Delete top-level Profile `name` from **every** document. Do not move the slug onto another Profile property.
- Rename `full_name` → `display_name`; keep the same string values (they remain unique).
- Do **not** change `email`, `cognito_sub`, `roles`, `customer_id`, `mentor_id`, `status`, breadcrumbs, or `_id`.
- Breadcrumb `by_user` values (e.g. `mike`, `paula`) may stay as-is — they are not the removed Profile `name` property.
- Other collections’ `name` fields (Customer, Resource, Plan, Notification, etc.) are unrelated — do not edit those files.

README: change the persona matrix column header from `` `full_name` `` to `` `display_name` ``. Keep the **Slug** column as Developer Edition sign-in / JWT persona keys. Update any prose that says Profile stores IdP `name` or `full_name`.

## Goals

- Every Profile document validates against T250 (`display_name` present; no `name` or `full_name`).
- Unique `display_name` index still holds (same uniqueness set as today’s `full_name`).
- README Test Personas section matches the new field name.
- Configure-database returns **SUCCESS** (this task closes the T250 interim failure).

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200** and top-level **`status: SUCCESS`**.

MongoDB spot checks:

```javascript
db.Profile.countDocuments({ name: { $exists: true } })          // 0
db.Profile.countDocuments({ full_name: { $exists: true } })     // 0
db.Profile.countDocuments({ display_name: { $exists: true } })  // == Profile.countDocuments()
db.Profile.aggregate([{ $group: { _id: "$display_name", n: { $sum: 1 } } }, { $match: { n: { $gt: 1 } } }])  // empty
```

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Profile.0.1.0.0.json` — strip `name`; rename `full_name` → `display_name` on every document
- `README.md` — persona matrix / prose: `full_name` → `display_name`
- `Tasks/PENDING.T251.update_profile_display_name_test_data.md` — this file (Execution Notes)

## Execution Notes
Plan:
- Update `configurator/test_data/Profile.0.1.0.0.json` so every Profile document removes `name` and uses `display_name` instead of `full_name`.
- Update `README.md` persona matrix/prose to refer to `display_name` while keeping the separate slug/sign-in column unchanged.
- Run the configure/package verification commands from this task if the local environment supports them, then record results here.

Completed:
- Updated all 21 Profile seed documents to remove top-level `name` and rename `full_name` to `display_name`.
- Updated the README persona matrix header from `full_name` to `display_name`; the Slug column remains the Developer Edition sign-in / JWT persona key.

Tests:
- `make dev` followed by `curl -X DELETE http://localhost:8385/api/database/` returned HTTP 200 with `status: SUCCESS`.
- `curl -X POST http://localhost:8385/api/configurations/` returned HTTP 200 with top-level `status: SUCCESS`.
- MongoDB spot checks passed against database `mentor_hub`: `name` count = 0, `full_name` count = 0, `display_name` count = 21, total Profile count = 21, duplicate `display_name` aggregate = `[]`.
- Packaging verification passed: `make down`, `make container`, and `mh up mongodb` all completed successfully.

Follow-up:
- No additional in-repo follow-up identified for T251. Dependent tasks can assume Profile seed data now matches the T250 `display_name` schema.
