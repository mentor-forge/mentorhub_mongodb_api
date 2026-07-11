# T201 – Update Profile Schema for JWT Claims

**Status**: Shipped  
**Type**: Feature  
**Depends On**: T200  
**Description**: Add `roles` to Profile, retarget the unique search index to `full_name`, and update the collection description for the Identity-free model.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/dictionaries/`, `configurator/configurations/`, `configurator/enumerators/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `configurator/dictionaries/Profile.0.1.0.yaml` — current schema; `customer_id` already present; no `roles` yet
- `configurator/configurations/Profile.yaml` — unique index on `name` today
- `configurator/enumerators/enumerations.0.yaml` — `user_roles` enum (`mentor`, `mentee`, `customer`, `coordinator`, `admin`)
- `configurator/test_data/Identity.0.1.0.0.json` — **removed in T200**; role values for test data are documented in T204
- `Tasks/SHIPPED.T106.mentee_collection_and_profile_schema.md` — prior Profile schema work

### Current vs target Profile properties (relevant subset)

| Property | Today | Target |
| --- | --- | --- |
| `name` | IdP username (JWT claim) | unchanged |
| `full_name` | display name (`sentence`) | unchanged; becomes indexed field |
| `customer_id` | `identifier` (optional) | unchanged (already in dictionary) |
| `roles` | — | **add** `enum_array` of `user_roles` |
| `description` (root) | "associated with one **Identity**" | JWT-claims / sponsorship model |

### Index change

Replace the unique **Name Index** on `name` with a unique index on `full_name`. Keep the `saved.at_time` descending index.

## Goals

- Add `roles` to `Profile.0.1.0.yaml` as `type: enum_array` with `enums: user_roles`.
- Update the Profile root `description` to reflect that Profile is the authoritative person record (IdP `name` in JWT claims, roles and sponsorship on Profile).
- Update `Profile.yaml` version `0.1.0.0` indexes: unique `full_name`, remove unique `name` index.
- Pre-release: edit **0.1.0** dictionary and configuration in place; no version bump.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- `make container` must succeed.
- Configure-database may **fail** until T204 updates Profile test data (missing `roles`, duplicate `full_name` risk after index change, etc.) — acceptable for this schema-only task. Confirm failures are test-data related, not dictionary/config syntax errors.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/dictionaries/Profile.0.1.0.yaml` — add `roles`; update root description
- `configurator/configurations/Profile.yaml` — replace `name` unique index with `full_name` unique index

## Execution Notes

**Summary of changes**

- Updated `configurator/dictionaries/Profile.0.1.0.yaml` description for the Identity-free Profile model.
- Added Profile `roles` as `enum_array` using `user_roles`.
- Updated `configurator/configurations/Profile.yaml` to use a unique `full_name` index instead of the unique `name` index.

**Testing results**

- `curl -X DELETE http://localhost:8385/api/database/` -> HTTP 200, SUCCESS.
- `curl -X POST http://localhost:8385/api/configurations/` -> HTTP 200, SUCCESS after T204 Profile test data updates.
- `make down && make container && mh up mongodb` -> SUCCESS.
