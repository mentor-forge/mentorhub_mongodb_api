# T238 – Seed Event activity trails for Customer org roster (F-D23)

**Status:** Pending  
**Type:** Feature  
**Depends On:** T237  
**Description:** Append **Event** trails for E3 roster activity (encounter + sparse login/arrived), including `context.customer_id` on **new** Events so org-home aggregates can filter without a Dashboard collection. Do **not** seed Discovery Notification cards. Prefer append over rewrite. Pre-release: edit `Event.0.1.0.0.json` in place.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/customer_journey_issues.md` — E3; Event trails for mentee activity; platform “what needs attention” is Discovery (out of scope)
- `../mentorhub/Workshops/customer_journey_issues_adjustments.md` — F-D23 is **not** Discovery notification/dashboard cards
- GitHub: [F-D23 #55](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/55)
- `Tasks/PENDING.T236.seed_customer_org_roster_profiles.md` — harbor / helen / pat / northstar conventions
- `Tasks/PENDING.T237.seed_roster_encounter_activity.md` — **Execution Notes** new Encounter `_id`s
- `configurator/dictionaries/Event.0.1.0.yaml` — `type` (`event_types`), `context` with `profile_id` and **`additional_properties: true`** (may add `customer_id`, `encounter_id`)
- `configurator/test_data/Event.0.1.0.0.json` — last seed `_id` `F00000000000000000000197` (T235); **append** from `F…0198`
- **Out of scope:** Notification / ExternalEvent documents; Discovery card samples; Dashboard; Customer / Profile / Encounter JSON (T236 / T237); `notification_created` / past_due / invite Events (those are Discovery / E4 / E6)

### Event coverage (minimum)

Continue `_id` prefix `F000…` from `F00000000000000000000198`. Preserve **all** existing Events.

**New T237 Encounters** — one `type: encounter` Event per new Encounter:

| `context` | Value |
| --- | --- |
| `profile_id` | mentee Profile (Daniel or Lucky) |
| `encounter_id` | matching new Encounter `_id` from T237 |
| `customer_id` | persevere `D…02` or supersoft `D…07` |

Align `created.at_time` with the Encounter `date`.

**Empty-state orgs** — sparse **non-encounter** Events only (so login/home still has a trail, roster activity stays empty):

| Persona | `type` | `context.profile_id` | `context.customer_id` |
| --- | --- | --- | --- |
| helen | `login` (and optional `arrived`) | helen `A…18` | harbor `D…11` |
| nora | `login` | nora `A…17` | northstar `D…10` |
| pat | **none**, or a single `arrived` **without** `encounter` / journey types | pat `A…19` | persevere `D…02` |

Do **not** add `type: encounter` (or `started` / `completed` / `note`) for pat, helen, nora, or donny.

Do **not** rewrite existing encounter Events to backfill `customer_id` (prefer add). New Events must include `customer_id` so F-CA07 can demo org-scoped reads.

Do **not** add Notification documents or `notification_created` Events in this task.

## Goals

- New encounter Events exist for T237 sessions, each with `profile_id`, `encounter_id`, and `customer_id`.
- Harbor / northstar / pat have no encounter Events (empty activity).
- Existing Event documents retained; last `_id` before this task remains `F…0197` plus any T237-independent rows.
- Configure-database Event step **SUCCESS**.
- Dashboard collection still absent; Notification test data unchanged.

## Testing Expectations

```sh
make dev
# If host port 27017 is busy, use compose ports !override (e.g. host 27018) as in prior F-D tasks.
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- Event CFG SUCCESS; Notification CFG still SUCCESS with **no** new Notification docs.
- Spot-check:

```javascript
db.Event.countDocuments({ type: "encounter", "context.customer_id": ObjectId("D00000000000000000000002") })  // ≥1 (new)
db.Event.countDocuments({ type: "encounter", "context.customer_id": ObjectId("D00000000000000000000007") })  // ≥1 (new)
db.Event.countDocuments({ type: "encounter", "context.profile_id": ObjectId("<pat>") })  // 0
db.Event.countDocuments({ type: "encounter", "context.customer_id": ObjectId("<harbor>") })  // 0
db.Event.countDocuments({ "context.profile_id": ObjectId("<helen>"), type: "login" })  // ≥1
```

- Grep `configurator/` for Dashboard collection paths — expect none.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Event.0.1.0.0.json` — append roster activity Events only
- `Tasks/PENDING.T238.seed_roster_event_activity.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

_(Reserved for the task execution agent.)_
