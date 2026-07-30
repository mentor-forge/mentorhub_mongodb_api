# T221 – Add ExternalEvent collection (F-D29)

**Status:** Shipped  
**Type:** Feature  
**Depends On:** T220  
**Description:** Create append-only **ExternalEvent** Configuration and Dictionary for Admin ingress (Stripe / Cognito). Prefer delete+create of new artifacts over rename. Empty or minimal test data only if configure requires a file; full ingress chains land in T224.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/configurations/`, `configurator/dictionaries/`, `configurator/test_data/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/customer_journey_issues_adjustments.md` — ExternalEvent shape
- `../mentorhub/Workshops/admin_journey_issues.md` — Admin ingress consumes this collection
- GitHub: [F-D29 #61](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/61)
- `Tasks/PENDING.T220.extend_event_types_and_lifecycle_enums.md` — `external_event_source` enum
- `configurator/configurations/Event.yaml` / `dictionaries/Event.0.1.0.yaml` — sibling append-oriented pattern (`created` only; no `saved`)
- `configurator/api_config/templates/default_new_dictionary.yaml` / `default_new_configuration.yaml` — starters (adapt; ExternalEvent is **not** a full CRUD stub)
- **Out of scope:** Notification / Card schemas; rich test fixtures (T224); Admin API write paths (external F-AA02).

### Target properties (refine against running configurator)

| Property | Notes |
| --- | --- |
| `_id` | identifier |
| `source` | enum `external_event_source` (`stripe` \| `cognito`) |
| `external_id` | provider event / message id (idempotency) |
| `payload_hash` | hash of verified raw payload |
| `normalized_body` or body reference | normalized payload object or ref — finalize field name in implementation |
| `created` | breadcrumb only (append-only — **no** `saved`) |

Indexes: unique compound on `source` + `external_id` (ingress idempotency). Prefer `created.at_time` descending index like Event.

**Stable `_id` prefix for later seeds (T224):** use `E0…` hex ObjectIds (e.g. `E00000000000000000000001`) — document chosen prefix in Execution Notes.

## Goals

- Create `configurator/dictionaries/ExternalEvent.0.1.0.yaml` (append-only; no `saved`).
- Create `configurator/configurations/ExternalEvent.yaml` version `0.1.0.0` with indexes and `test_data` pointer.
- Create `configurator/test_data/ExternalEvent.0.1.0.0.json` as `[]` or a single placeholder only if needed for configure — full chains in T224.
- Prefer **create** new files (do not revive payment-Card naming or rename unrelated collections).
- Confirm configure-database succeeds with ExternalEvent present and Event still present.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- `GET /api/configurations/` lists `ExternalEvent.yaml`; `Event.yaml` still present.
- No accidental creation of a payment-Card collection.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/dictionaries/ExternalEvent.0.1.0.yaml` — **create**
- `configurator/configurations/ExternalEvent.yaml` — **create**
- `configurator/test_data/ExternalEvent.0.1.0.0.json` — **create** (empty or minimal)
- `Tasks/PENDING.T221.add_external_event_collection.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

**Plan:** Create append-only ExternalEvent dictionary/configuration/test_data matching Event style (`created` only; no `saved`). Unique compound index on `source`+`external_id`; `created.at_time:-1` like Event. Empty test data `[]`. Verify via local configurator (Mongo host port 27018 `ports: !override`) then `make container` + `mh up mongodb`.

**_id prefix for T224 seeds:** `E0…` hex ObjectIds (e.g. `E00000000000000000000001`). Same hex prefix family as Encounter seeds; uniqueness is per-collection, so ExternalEvent seeds can reuse the `E0…` pattern.

**Changes**

- Created `ExternalEvent.0.1.0.yaml`: `_id`, `source` (`external_event_source`), `external_id`, `payload_hash`, `normalized_body` (object, `additional_properties: true`), `created` breadcrumb; no `saved`.
- Created `ExternalEvent.yaml` version `0.1.0.0` with unique `Source External Id` index (`source`+`external_id`) and `Created` index (`created.at_time:-1`).
- Created `ExternalEvent.0.1.0.0.json` as `[]` (full ingress fixtures deferred to T224).
- Did not touch Notification or Card.

**Testing results**

- Local configurator (INPUT_FOLDER mount, Mongo host port 27018 via `ports: !override`): `DELETE /api/database/` → HTTP 200, `status: SUCCESS`.
- `POST /api/configurations/` → HTTP 200, top-level `status: SUCCESS`; `CFG-05-ExternalEvent.yaml` SUCCESS; `CFG-05-Event.yaml` SUCCESS; unique index `PRO-04-Source External Id` SUCCESS.
- `GET /api/configurations/` lists `ExternalEvent.yaml` and `Event.yaml`; no `Card.yaml` / `Notification.yaml`.
- `make container` → image `ghcr.io/mentor-forge/mentorhub_mongodb_api:latest` includes ExternalEvent configuration/dictionary/test_data under `/input`.
- `mh up mongodb` → API on :8383 lists `ExternalEvent.yaml` and `Event.yaml` (packaged DROP disabled → 403 as expected).
