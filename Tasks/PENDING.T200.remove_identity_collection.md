# T200 – Remove Identity Collection

**Status**: Pending  
**Type**: Feature  
**Depends On**: none  
**Description**: Remove the Identity dictionary, configuration, and test data now that JWT claims and user roles live on Profile.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/dictionaries/`, `configurator/configurations/`, `configurator/test_data/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `configurator/dictionaries/Identity.0.1.0.yaml` — IdP identity schema with `roles` (moving to Profile)
- `configurator/configurations/Identity.yaml` — collection configuration for version 0.1.0.0
- `configurator/test_data/Identity.0.1.0.0.json` — 15 seed identities whose `roles` will migrate to Profile in T204
- `Tasks/SHIPPED.T101.generate_identity_test_data.md` — prior Identity test-data conventions
- `Tasks/AS_NEEDED.generate_test_data.md` — still references Identity; update that file's **User inputs** in a follow-up human edit (out of scope for this task's **Outputs**)

### Design decision

Identity was a parallel record keyed by IdP username. The platform now treats **Profile** as the single person document: JWT `name` claim maps to Profile `name`, display uses `full_name`, and `roles` + `customer_id` support authorization and sponsorship. The Identity collection is obsolete.

## Goals

- Delete the Identity dictionary (`Identity.0.1.0.yaml`).
- Delete the Identity configuration (`Identity.yaml`).
- Delete Identity test data (`Identity.0.1.0.0.json`).
- Ensure no remaining in-repo references require the Identity collection for configure-database to load other collections (Profile, Customer, etc.).

## Testing Expectations

- Run in Dev mode and configure the database:

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect top-level **SUCCESS** — Identity is removed; remaining collections still configure.
- Profile configure may fail until T201/T204 ship if Profile schema or test data is inconsistent; document any interim failure in **Execution Notes**.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/dictionaries/Identity.0.1.0.yaml` — **delete**
- `configurator/configurations/Identity.yaml` — **delete**
- `configurator/test_data/Identity.0.1.0.0.json` — **delete**

## Execution Notes

_(Reserved for the task execution agent.)_
