# T222 – Add Notification collection (F-D29)

**Status:** Pending  
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

*(Reserved for the execution agent.)*
