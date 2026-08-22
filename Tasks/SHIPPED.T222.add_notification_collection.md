# T222 – Add Notification collection (F-D29)

**Status:** Shipped  
**Type:** Feature  
**Depends On:** T220  
**Description:** Create **Notification** Configuration and Dictionary for cross-domain producer writes and Discovery dismiss/presentation. Prefer create over rename. Fixture documents land in T224.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/configurations/`, `configurator/dictionaries/`, `configurator/test_data/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/discovery_journey_issues.md` — Notification contract; scope → card mapping
- `../mentorhub/Workshops/customer_journey_issues.md` — producers write Notifications; Discovery dismisses
- GitHub: [F-D29 #61](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/61)
- `Tasks/PENDING.T220.extend_event_types_and_lifecycle_enums.md` — shared enums; **scope is encoded via `scope_id` one_of below** (do not rely on a separate `notification_scope` enum unless still useful elsewhere)
- `Tasks/scripts/persona_ids.json` — Customer / Profile ids for later fixtures
- **Out of scope:** Discovery Card polymorphic schema (T223); Notification seed content (T224); Discovery dismiss API (external F-DA01).

### Target properties (locked design notes)

Use configurator **`one_of`** for optional / alternate shapes. Keep **`name`**; use **`message`** for body text — **do not** add `description`.

| Property | Notes |
| --- | --- |
| `_id` | identifier |
| `name` | keep — searchable / display title (`word` or equivalent) |
| `message` | user-facing body (`sentence` or equivalent) — **prefer over `description`**; omit `description` |
| `scope_id` | **`one_of`**: `profile_id` \| `customer_id` \| `mentor_id` \| **global** (breadcrumb) — encodes scope target; global uses a breadcrumb rather than an id |
| `link_metadata` | optional object for cross-SPA routes (F-US09); model optional fields with `one_of` / optional as appropriate |
| `dismissed` | **breadcrumb** (set when the user dismisses) |
| `cancelled` | **breadcrumb** (set when the notification is cancelled / superseded) |
| `created` | breadcrumb |
| `status` | soft-delete via `default_status` (`active` / `archived`) — distinct from `dismissed` / `cancelled` breadcrumbs |

Indexes: `created.at_time` descending; consider indexes useful for listing by `scope_id` variant (document chosen keys in Execution Notes).

**Stable `_id` prefix for later seeds (T224):** use `N0…` (e.g. `N00000000000000000000001`).

## Goals

- Create `configurator/dictionaries/Notification.0.1.0.yaml` with `name`, `message` (no `description`), `scope_id` as `one_of` (`profile_id` | `customer_id` | `mentor_id` | global breadcrumb), and `dismissed` / `cancelled` breadcrumbs; use `one_of` for other optional alternates as needed.
- Create `configurator/configurations/Notification.yaml` version `0.1.0.0`.
- Create `configurator/test_data/Notification.0.1.0.0.json` as `[]` until T224.
- Confirm configure-database succeeds with Notification present.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- Configurations list includes `Notification.yaml`.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/dictionaries/Notification.0.1.0.yaml` — **create**
- `configurator/configurations/Notification.yaml` — **create**
- `configurator/test_data/Notification.0.1.0.0.json` — **create** (`[]` acceptable)
- `Tasks/PENDING.T222.add_notification_collection.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

**Plan:** Create Notification dictionary/configuration/test_data with `scope_id` as configurator `one_of`. Empty test data `[]`. Verify via local configurator then `make container` + `mh up mongodb`.

**`scope_id` / `one_of` modeling:** Configurator `one_of` emits JSON Schema `oneOf` from each child property's schema. Bare `identifier` alternates would be identical (ObjectId string) and fail `oneOf` (exactly one match). Each alternate is therefore a **single-key object**:

- `scope_id: { profile_id: <identifier> }`
- `scope_id: { customer_id: <identifier> }`
- `scope_id: { mentor_id: <identifier> }`
- `scope_id: { global: <breadcrumb> }`

Document shape for T224 seeds matches those wrappers. `link_metadata` is an optional object (`required: false`, `additional_properties: true`, empty property list) rather than a present/absent `one_of`.

**Indexes:**

- `Created` — `created.at_time: -1`
- `Scope Profile Id` — `scope_id.profile_id: 1` (sparse)
- `Scope Customer Id` — `scope_id.customer_id: 1` (sparse)
- `Scope Mentor Id` — `scope_id.mentor_id: 1` (sparse)

No index on `scope_id.global` (breadcrumb object; listing globals uses `created` / status filters).

**_id prefix for T224 seeds:** `N0…` hex ObjectIds (e.g. `N00000000000000000000001`).

**Changes**

- Created `Notification.0.1.0.yaml`: `_id`, `name` (word), `message` (sentence), `scope_id` (`one_of` of four single-key objects), `link_metadata`, `dismissed` / `cancelled` / `created` breadcrumbs, `status` (`default_status`); no `description` / `saved`.
- Created `Notification.yaml` version `0.1.0.0` with Created + three sparse scope indexes; `test_data` → `Notification.0.1.0.0.json`.
- Created `Notification.0.1.0.0.json` as `[]` (fixtures deferred to T224).
- Did not touch Card / ExternalEvent.

**Testing results**

- Local configurator (`docker compose` / INPUT_FOLDER mount; Mongo on :27017 after `mh down`): `DELETE /api/database/` → HTTP 200, `status: SUCCESS`.
- `POST /api/configurations/` → HTTP 200, top-level `status: SUCCESS`; `CFG-05-Notification.yaml` SUCCESS; sparse scope indexes `PRO-04-Scope Profile/Customer/Mentor Id` SUCCESS.
- `GET /api/configurations/` lists `Notification.yaml`.
- `make container` → image `ghcr.io/mentor-forge/mentorhub_mongodb_api:latest` includes Notification under `/input`.
- `mh up mongodb` → API on :8383 lists `Notification.yaml` (packaged DROP disabled → 403 as expected).
