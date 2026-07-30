# T223 – Add Discovery Card polymorphic schema (F-D29)

**Status:** Shipped  
**Type:** Feature  
**Depends On:** T220  
**Description:** Add a **configurator-only, non-persisted** polymorphic Card schema for Discovery dashboard card payloads. Prevent collection creation by manually setting configuration **and** dictionary version/name to **`0.0.0.0`**. MVP: **one** Customer card, **one** Profile card, **one** Notification card (no Mine/Other/role splits; no Coordinator). This is **not** the dropped payment-Card collection (F-D16 / #37).

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/dictionaries/`, `configurator/configurations/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/discovery_journey_issues.md` — Discovery card concept (simplify catalog per this task)
- GitHub: [F-D29 #61](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/61); F-W14 originally F-SD01
- Payment **Card** already removed ([F-D16 #37](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/37)) — reclaiming the `Card` dictionary name for Discovery UI types is OK if clearly described
- `Tasks/PENDING.T222.add_notification_collection.md` — Notification shape cards may reference
- **Out of scope:** Persisted card documents; Notification fixtures (T224); Discovery API aggregate (external F-DA01); fine-grained Mine/Other/Mentor/Mentee card variants (defer).

### MVP card types (simplified)

Root polymorphism via configurator **`one_of`** — **three** variants only:

| Card type | Intent |
| --- | --- |
| **Customer** | Single Customer card shape (mine vs other is API/RBAC, not separate schemas) |
| **Profile** | Single Profile card shape (role/context is API/RBAC, not separate schemas) |
| **Notification** | Single Notification card shape (scope comes from Notification `scope_id`) |

Omit Coordinator. Do **not** create separate Customer (Mine)/(Other) or Profile (Me)/(Mentor)/(Mentee)/(Customer) dictionary variants for now.

Include fields Discovery needs for title, summary, and link/target metadata aligned with F-US09 templates (link shapes may be stubs until spa_utils ships).

### Non-persisted pattern — version `0.0.0.0`

- Create both a **Configuration** and a **Dictionary**.
- Manually set the configuration version to **`0.0.0.0`** and align the dictionary name/version to **`0.0.0.0`** (e.g. `Card.0.0.0.yaml` / config version `0.0.0.0`) — this **prevents the collection from being created**.
- Do **not** attach loadable Mongo test data that would create documents; configure-database must **not** create a `Card` collection.
- Confirm via **running configurator** that `0.0.0.0` behaves as expected; document any nuances in Execution Notes.
- Prefer delete+create of any mistaken Configuration that would persist cards at `0.1.0.0`.

## Goals

- Create Card dictionary + configuration with version/name **`0.0.0.0`** so no Mongo collection is created.
- Polymorphic root `one_of` with **exactly three** card types: Customer, Profile, Notification.
- Document the `0.0.0.0` non-persist pattern in Execution Notes for F-DA01 / F-DS01 consumers.
- Leave Notification / ExternalEvent / Event collections untouched except as schema refs if needed.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- After configure, confirm **no** persisted `Card` collection in Mongo (list collections / configurator process result).
- Card configuration/dictionary at `0.0.0.0` is visible for schema inspection.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/dictionaries/Card.0.0.0.yaml` — **create** (name/version `0.0.0.0`; adjust filename if configurator requires a different pattern — document in Execution Notes)
- `configurator/configurations/Card.yaml` — **create** with version **`0.0.0.0`** (no collection creation)
- `Tasks/PENDING.T223.add_discovery_card_polymorphic_schema.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

**Plan:** Create non-persisted Card dictionary/configuration at `0.0.0.0` with root `one_of` + `constant` discriminators for Customer / Profile / Notification. No test_data file. Verify via local configurator then `make container` + `mh up mongodb`.

### `0.0.0.0` non-persist pattern (for F-DA01 / F-DS01)

Configurator `VersionManager.get_current_version` returns `{Collection}.0.0.0.0` when no `CollectionVersions` row exists. `Version.process` **skips** any target version when `current_version >= target_version`. Therefore a configuration whose only version is **`0.0.0.0`** is always skipped on a fresh DB: no collection create, no schema validation, no indexes, no test-data load, no `CollectionVersions` upsert.

- Dictionary filename aligns via `VersionNumber.get_schema_filename()` → **`Card.0.0.0.yaml`** (four-part name + three version digits; enumerator omitted).
- Configuration version string is **`0.0.0.0`** (four parts including enumerator `0`).
- Observed process event: `CFG-05-Card.yaml` SUCCESS with nested skip `skip_reason: "Version already implemented"`, `current_version: "Card.0.0.0.yaml"`, `target_version: "0.0.0.0"`.
- Schema remains inspectable: `GET /api/configurations/Card.yaml/`, `GET /api/dictionaries/Card.0.0.0.yaml/`, `GET /api/configurations/json_schema/Card.yaml/0.0.0.0/`.

**Do not** bump Card to `0.1.0.0` unless intentionally creating a Mongo collection.

### `one_of` + `constant` modeling

Per mongodb_configurator_spa WelcomePage Dictionary guidance: root **`one_of`** of three **object** variants; each variant has a required **`type`** field with **`constant`** discriminator (`Customer` | `Profile` | `Notification`). JSON Schema emits `oneOf` with `const` on `type` so exactly one alternate matches.

Shared Discovery fields on each variant (stubs OK for F-US09):

- `title` (`sentence`), `summary` (`sentence`)
- entity id: `customer_id` | `profile_id` | `notification_id` (`identifier`)
- `link_metadata` optional object (`additional_properties: true`, empty property list) — same stub pattern as Notification

No Coordinator; no Mine/Other/role-split card types.

### Changes

- Created `Card.0.0.0.yaml` — root `one_of` of Customer / Profile / Notification objects with `constant` `type` discriminators + title/summary/id/link_metadata.
- Created `Card.yaml` version `0.0.0.0`, empty indexes/migrations, `test_data: null` (no loadable Card documents).
- Did not touch Notification / ExternalEvent / Event collections.

### Testing results

- Local configurator (`docker compose` + `/tmp/mh-mongo-port-override.yaml` host **27018**; INPUT_FOLDER mount): `DELETE /api/database/` → HTTP 200, `status: SUCCESS`.
- `POST /api/configurations/` → HTTP 200, top-level `status: SUCCESS`; `CFG-05-Card.yaml` SUCCESS with version skip as above.
- Mongo `db.getCollectionNames()` — **no `Card`**; `CollectionVersions` count for Card = **0**.
- `GET` Card config/dictionary/`json_schema/.../0.0.0.0/` — three `oneOf` variants with consts `Customer`, `Profile`, `Notification`.
- `make container` → image includes Card under `/input`.
- `mh up mongodb` → API :8383 lists `Card.yaml` + `Card.0.0.0.yaml`; packaged mongo **HAS_Card=false**.
