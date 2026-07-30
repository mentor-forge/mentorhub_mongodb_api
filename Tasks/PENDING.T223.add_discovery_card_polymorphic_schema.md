# T223 – Add Discovery Card polymorphic schema (F-D29)

**Status:** Pending  
**Type:** Feature  
**Depends On:** T220  
**Description:** Add a **configurator-only, non-persisted** polymorphic Card schema for Discovery dashboard card payloads (version `-1` / orphan pattern). **Do not** create a MongoDB Card collection. Omit Coordinator card type. This is **not** the dropped payment-Card collection (F-D16 / #37).

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/dictionaries/`, `configurator/configurations/` (only if required for orphan registration), `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/discovery_journey_issues.md` — [Polymorphic card types (MVP catalog)](../mentorhub/Workshops/discovery_journey_issues.md); omit `Profile (Coordinator)`
- GitHub: [F-D29 #61](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/61); F-W14 originally F-SD01
- Payment **Card** already removed ([F-D16 #37](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/37)) — reclaiming the `Card` dictionary name for Discovery UI types is OK if clearly described; alternatively use `Discovery_Card` if configurator naming conflicts — document choice in Execution Notes
- **Out of scope:** Persisted card documents; Notification fixtures (T224); Discovery API aggregate (external F-DA01).

### MVP card type catalog (must cover; no Coordinator)

| Card type | Source data |
| --- | --- |
| Customer (Mine) | JWT `customer_id` org |
| Customer (Other) | Customer visible via RBAC |
| Profile (Me) | Caller’s Profile |
| Profile (Mentor) | Profiles linked via `mentor_id` |
| Profile (Mentee) | Mentee profiles visible to mentor/customer |
| Profile (Customer) | Profiles with `customer` role in org |
| Notification (Global) | Scope `all` |
| Notification (Customer) | Scope `customer` + id |
| Notification (Mentor) | Scope `mentor` + id |
| Notification (Profile) | Scope `profile` + id |

Use configurator `one_of` (or equivalent) polymorphism discriminated by card type. Include fields Discovery needs for title, summary, and link/target metadata aligned with F-US09 templates (link shapes may be stubs until spa_utils ships).

### Version `-1` / non-persisted pattern

- Confirm via **running configurator** how to register a dictionary **without** creating a Mongo collection (orphan dictionary and/or configuration version `-1`).
- Prefer: dictionary present for API/OpenAPI consumers; **no** `test_data` load into Mongo; configure-database must **not** create a `Card` collection.
- Prefer delete+create of any mistaken Configuration that would persist cards.

## Goals

- Create polymorphic Card (or `Discovery_Card`) dictionary covering the MVP catalog; omit Coordinator.
- Register as non-persisted / version `-1` orphan so configure-database does **not** create a collection.
- Document the chosen configurator pattern in Execution Notes for F-DA01 / F-DS01 consumers.
- Leave Notification / ExternalEvent / Event collections untouched except as schema refs if needed.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- After configure, confirm **no** persisted `Card` / `Discovery_Card` collection in Mongo (e.g. list collections / configurator process result).
- Dictionary (or orphan config) is visible to the configurator for schema inspection.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/dictionaries/Card.0.1.0.yaml` or `Discovery_Card.0.1.0.yaml` — **create** (name per Execution Notes)
- Optional orphan configuration only if required by configurator for version `-1` — list exact path in Execution Notes
- `Tasks/PENDING.T223.add_discovery_card_polymorphic_schema.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

*(Reserved for the execution agent.)*
