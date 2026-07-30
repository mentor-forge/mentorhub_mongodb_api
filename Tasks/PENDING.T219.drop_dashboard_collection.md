# T219 – Drop Dashboard collection (F-D15 / E0)

**Status:** Pending  
**Type:** Feature  
**Depends On:** none  
**Description:** Delete the Dashboard Configuration, Dictionary, and Test Data so custom dashboards are no longer a MentorHub collection. Discovery SPA aggregation and Customer org home replace this surface. Prefer delete over rename.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/configurations/`, `configurator/dictionaries/`, `configurator/test_data/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/customer_journey_issues.md` — Experience **E0** cleanup (drop Dashboard; SPA aggregation replaces custom dashboards)
- GitHub: [F-D15 #36](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/36)
- Umbrella: **F-D-E0 (#62)** may supersede this issue when that ships — this task still implements the Dashboard drop if #36 remains open
- `configurator/configurations/Dashboard.yaml` — collection configuration (`test_data: Dashboard.0.1.0.0.json`)
- `configurator/dictionaries/Dashboard.0.1.0.yaml` — Dashboard schema (`customer_id` + stub fields)
- `configurator/test_data/Dashboard.0.1.0.0.json` — currently an empty array `[]`
- `Tasks/SHIPPED.T218.drop_top_level_subscription_collection.md` — prior delete-collection pattern (F-D14)
- `Tasks/SHIPPED.T200.remove_identity_collection.md` — earlier delete-collection pattern
- **Out of scope:** Building Discovery dashboard cards or Customer org home UX. Do **not** delete **Event** Configuration, Dictionary, or Test Data.
- **External:** Customer API / SPA may still expose Dashboard CRUD; that is **not** orchestrated from this repo (separate E0 API/SPA tickets F-CA04 / F-CS02).

## Goals

- Delete `configurator/configurations/Dashboard.yaml`.
- Delete `configurator/dictionaries/Dashboard.0.1.0.yaml` (and any other `dictionaries/Dashboard.*.yaml` if present).
- Delete `configurator/test_data/Dashboard.0.1.0.0.json` (and any other Dashboard test-data files if present).
- Prefer **delete** (not rename) of these artifacts.
- Confirm configure-database succeeds **without** a Dashboard collection and **with** Event still present.
- Leave Event Configuration / Dictionary / Test Data untouched.

## Testing Expectations

Run Dev configurator against this repo’s `configurator/` input folder, then drop and configure:

```sh
make dev
# If host port 27017 is busy, use a compose ports !override (e.g. host 27018) as in F-D16 Card drop / T218 verification.
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200** and top-level **`status: SUCCESS`**.
- `GET /api/configurations/` (or process result) must **not** list `Dashboard.yaml`.
- Confirm **`Event.yaml`** (or Event dictionary) is still present and configures successfully.
- Grep `configurator/` for leftover Dashboard collection paths (`configurations/Dashboard`, `dictionaries/Dashboard`, `test_data/Dashboard`) — expect none.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/configurations/Dashboard.yaml` — **delete**
- `configurator/dictionaries/Dashboard.0.1.0.yaml` — **delete**
- `configurator/test_data/Dashboard.0.1.0.0.json` — **delete**
- `Tasks/PENDING.T219.drop_dashboard_collection.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

*(Reserved for the execution agent.)*
