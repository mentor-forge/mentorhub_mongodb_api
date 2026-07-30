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
- `Tasks/PENDING.T220.extend_event_types_and_lifecycle_enums.md` — `notification_scope` enum
- `Tasks/scripts/persona_ids.json` — Customer / Profile ids for later fixtures
- **Out of scope:** Discovery Card polymorphic schema (T223); Notification seed content (T224); Discovery dismiss API (external F-DA01).

### Target properties (refine against running configurator)

| Property | Notes |
| --- | --- |
| `_id` | identifier |
| `scope` | enum `notification_scope`: `all` \| `customer` \| `mentor` \| `profile` |
| Target ids | e.g. `customer_id`, `mentor_id`, `profile_id` as applicable to scope (optional identifiers) |
| `message` | user-facing text (`sentence` or equivalent) |
| `link_metadata` | object for cross-SPA routes (F-US09); allow structured fields Discovery/SPA map to links |
| Dismiss state | e.g. `dismissed` boolean and/or `dismissed_at` / breadcrumb — finalize in implementation |
| `created` | breadcrumb |
| `status` | soft-delete via `default_status` (`active` / `archived`) — distinct from dismiss UX state |
| `name` / `description` | include if required by data standards / configurator defaults; otherwise omit with rationale in Execution Notes |

Indexes: `created.at_time` descending; consider compound indexes on `scope` + target id for list queries.

**Stable `_id` prefix for later seeds (T224):** use `N0…` (e.g. `N00000000000000000000001`).

## Goals

- Create `configurator/dictionaries/Notification.0.1.0.yaml`.
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
