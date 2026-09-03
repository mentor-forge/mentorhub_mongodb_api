# T250 – Remove Profile `name` and rename `full_name` to `display_name` (F-D31)

**Status:** Shipped  
**Type:** Feature  
**Depends On:** none  
**Description:** Drop Profile `name` (former IdP username field), rename `full_name` to `display_name`, and retarget the unique display-name index. Schema/index only — existing Profile JSON still carries `name` / `full_name` until T251.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/dictionaries/`, `configurator/configurations/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- GitHub: [F-D31 ProfileDisplayName #74](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/74)
- `configurator/dictionaries/Profile.0.1.0.yaml` — `name` (`word`, JWT/IdP username), `full_name` (`sentence`, display)
- `configurator/configurations/Profile.yaml` — unique **Full Name Index** on `full_name`; unique sparse `cognito_sub` and `email`; Last Saved
- `Tasks/SHIPPED.T201.update_profile_schema_for_jwt_claims.md` — unique index moved from `name` to `full_name`
- `Tasks/SHIPPED.T231.extend_profile_for_cognito_primary_registration.md` — claims field inventory
- **Out of scope:** Profile test data and README persona matrix (T251); Encounter status (T248–T249); adding a replacement IdP-username property; version bumps / migrations

### Current vs target Profile properties (relevant subset)

| Property | Today | Target |
| --- | --- | --- |
| `name` | IdP username (`word`) | **remove** |
| `full_name` | Display name (`sentence`) | **rename** to `display_name` (`sentence`); keep uniqueness via index |
| `cognito_sub` / `email` | unique sparse indexes | unchanged |
| root `description` | mentions IdP username in JWT claims | update so it does not imply a persisted `name` property |

### Index change

Replace unique **Full Name Index** on `full_name` with a unique index on `display_name` (same uniqueness intent). Keep Last Saved, Cognito Sub, and Email indexes.

This **tightens** validation (`additional_properties: false` plus removed/renamed fields). Configure-database **will fail** on Profile test data until T251 strips `name`, renames `full_name` → `display_name`, and satisfies the new unique index. That interim failure is expected; do not treat this task as shippable until T251, but this file may be marked Shipped after dictionary/config syntax is verified.

## Goals

- Remove `name` from `Profile.0.1.0.yaml`.
- Rename `full_name` to `display_name`; keep type `sentence` and a display-oriented description.
- Retarget `Profile.yaml` unique index from `full_name` to `display_name`.
- Update the Profile root `description` if it still describes a persisted IdP `name` field.
- Pre-release: edit **0.1.0** dictionary and configuration in place; no version bump.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Dictionary / configuration load must not fail on YAML syntax.
- Configure-database **may fail** on Profile test data (`name` / `full_name` additional properties, missing `display_name`, unique index on a missing field). Confirm failures are test-data related, not enumerator/dictionary syntax errors.
- `make container` must succeed.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/dictionaries/Profile.0.1.0.yaml` — remove `name`; rename `full_name` → `display_name`; update descriptions as needed
- `configurator/configurations/Profile.yaml` — unique index on `display_name`
- `Tasks/PENDING.T250.rename_profile_display_name.md` — this file (Execution Notes)

## Execution Notes
### Plan

1. Update `Profile.0.1.0.yaml` to remove `name`, rename `full_name` to `display_name`, and adjust descriptions so the collection no longer implies a persisted IdP username field.
2. Update `Profile.yaml` to retarget the unique index from `full_name` to `display_name` while keeping the other indexes unchanged.
3. Run the task-specified dev/configure and packaging checks, confirming any configure failure is due to stale Profile test data rather than YAML/config syntax.

### Completion Summary

- Updated `configurator/dictionaries/Profile.0.1.0.yaml` to remove `name`, rename `full_name` to `display_name`, and revise the root description so it no longer implies a persisted IdP username field.
- Updated `configurator/configurations/Profile.yaml` so the unique display-name index now targets `display_name`; `saved.at_time`, `cognito_sub`, and `email` indexes were left unchanged.

### Test Results

- `make dev` — succeeded; local configurator services started.
- `curl -X DELETE "http://localhost:8385/api/database/"` — HTTP 200, `status: SUCCESS`.
- `curl -X POST "http://localhost:8385/api/configurations/"` — HTTP 200 with top-level `status: SUCCESS`, but `Profile.yaml` version processing failed exactly as expected on stale Profile seed data: document validation rejected additional properties `name` and `full_name`. This confirms the break is test-data related for follow-on task `T251`, not YAML/config syntax.
- `make down`
- `make container`
- `mh up mongodb`
  Packaging verification succeeded; the image built and the packaged MongoDB stack started successfully.
