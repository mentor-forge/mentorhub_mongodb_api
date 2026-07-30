# T218 – Drop top-level Subscription collection (F-D14 / E0)

**Status:** Pending  
**Type:** Feature  
**Depends On:** none  
**Description:** Delete the top-level Subscription Configuration, Dictionary, and Test Data so subscriptions are no longer a standalone MentorHub collection. Billing state will live on `Customer.subscriptions[]` under **F-D22** (do **not** implement F-D22 in this task). Prefer delete over rename.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/configurations/`, `configurator/dictionaries/`, `configurator/test_data/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/customer_journey_issues.md` — Experience **E0** cleanup (drop top-level Subscription; embed later on Customer)
- GitHub: [F-D14 #35](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/35)
- Umbrella: **F-D-E0 (#62)** may supersede this issue when that ships — this task still implements the Subscription drop if #35 remains open
- `configurator/configurations/Subscription.yaml` — collection configuration (`test_data: Subscription.0.1.0.0.json`)
- `configurator/dictionaries/Subscription.0.1.0.yaml` — top-level Subscription schema
- `configurator/test_data/Subscription.0.1.0.0.json` — currently an empty array `[]`
- `Tasks/SHIPPED.T200.remove_identity_collection.md` — prior delete-collection pattern
- **Out of scope:** Creating or extending `Customer.subscriptions[]` (**F-D22**). Do **not** delete **Event** Configuration, Dictionary, or Test Data. Do **not** remove subscription-related **enumerators** (cost-tier labels) unless a later ticket says so — they are not the Subscription collection.
- **External:** Customer API / SPA still may expose standalone Subscription CRUD; that is **not** orchestrated from this repo (separate E0 API/SPA tickets).

## Goals

- Delete `configurator/configurations/Subscription.yaml`.
- Delete `configurator/dictionaries/Subscription.0.1.0.yaml` (and any other `dictionaries/Subscription.*.yaml` if present).
- Delete `configurator/test_data/Subscription.0.1.0.0.json` (and any other Subscription test-data files if present).
- Prefer **delete** (not rename) of these artifacts.
- Confirm configure-database succeeds **without** a Subscription collection and **with** Event still present.
- Leave Event Configuration / Dictionary / Test Data untouched.
- Do not add `Customer.subscriptions[]` in this task (F-D22).

## Testing Expectations

Run Dev configurator against this repo’s `configurator/` input folder, then drop and configure:

```sh
make dev
# If host port 27017 is busy, use a compose ports !override (e.g. host 27018) as in F-D16 Card drop verification.
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200** and top-level **`status: SUCCESS`**.
- `GET /api/configurations/` (or process result) must **not** list `Subscription.yaml`.
- Confirm **`Event.yaml`** (or Event dictionary) is still present and configures successfully.
- Grep `configurator/` for leftover Subscription collection paths (`configurations/Subscription`, `dictionaries/Subscription`, `test_data/Subscription`) — expect none.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/configurations/Subscription.yaml` — **delete**
- `configurator/dictionaries/Subscription.0.1.0.yaml` — **delete**
- `configurator/test_data/Subscription.0.1.0.0.json` — **delete**
- `Tasks/PENDING.T218.drop_top_level_subscription_collection.md` — this file (Execution Notes only when run)

## Execution Notes

(Reserved for the execution agent.)
