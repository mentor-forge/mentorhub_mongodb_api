# T202 – Remove Customer mentees Property

**Status**: Pending  
**Type**: Feature  
**Depends On**: none  
**Description**: Remove the `mentees[]` property from the Customer dictionary; sponsorship is expressed via Profile `customer_id` instead.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/dictionaries/`, `configurator/configurations/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `configurator/dictionaries/Customer.0.1.0.yaml` — includes `mentees` array of identifier references
- `configurator/configurations/Customer.yaml` — no index on `mentees` (only `name` and `saved.at_time`)
- `configurator/test_data/Customer.0.1.0.0.json` — all five records carry `mentees[]` today

### Design decision

Customer documents describe sponsoring organizations. Which users they sponsor is determined by **Profile.customer_id**, not a denormalized `mentees[]` on Customer. Removing `mentees` simplifies the model and aligns with JWT/Profile-centric identity.

## Goals

- Remove the `mentees` property block from `Customer.0.1.0.yaml`.
- Pre-release: edit existing **0.1.0** dictionary in place; no version bump.
- Leave Customer test data unchanged in this task (T203 migrates test data).

## Testing Expectations

```sh
make dev
make container
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- `make container` must succeed.
- Configure-database **Customer** step may fail until T203 strips `mentees` from test data (`additionalProperties` validation). That is expected; document the error in **Execution Notes**.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/dictionaries/Customer.0.1.0.yaml` — remove `mentees` property

## Execution Notes

_(Reserved for the task execution agent.)_
