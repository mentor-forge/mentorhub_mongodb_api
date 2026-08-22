# T238 – Seed Event activity trails for Customer org roster (F-D23)

**Status:** Shipped  
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

**Plan:** Append roster Event trails in place (no rewrite of `F…0001`–`F…0197`; no Notification / Dashboard / Encounter / Profile edits). Confirm next unused Event hex after `F…0197` — `F00000000000000000000198` onward (Event seeds increment as decimal-looking hex: `198`, `199`, `200`… not `19a`). (1) `type: encounter` for Daniel `A…02` / `E…0a` / persevere `D…02` at `2026-07-14T15:00:00.000Z`; (2) `type: encounter` for Lucky `A…03` / `E…0b` / supersoft `D…07` at `2026-08-11T15:00:00.000Z`; both include `profile_id`, `encounter_id`, and `customer_id`. (3) Sparse non-encounter for empty-state orgs: helen `A…18` `arrived` + `login` (harbor `D…11`); nora `A…17` `login` (northstar `D…10`); pat `A…19` single `arrived` without encounter/journey types (persevere `D…02`). Do **not** add `encounter` / `started` / `completed` / `note` / `notification_created` for pat, helen, nora, or donny. Do **not** backfill `customer_id` on existing Events. Reuse already-running configurator `:8385`; skip packaging so later sequential tasks can reuse it.

**IDs used** (confirmed unused in Event before write; last prior seed remains `F…0197`)

| Kind | `_id` | Notes |
| --- | --- | --- |
| Event (Daniel 2026 encounter) | `F00000000000000000000198` | `type: encounter`; Daniel `A…02`; `E…0a`; persevere `D…02`; `created.at_time` 2026-07-14 |
| Event (Lucky 2026 encounter) | `F00000000000000000000199` | `type: encounter`; Lucky `A…03`; `E…0b`; supersoft `D…07`; `created.at_time` 2026-08-11 |
| Event (helen arrived) | `F00000000000000000000200` | `type: arrived`; helen `A…18`; harbor `D…11` |
| Event (helen login) | `F00000000000000000000201` | `type: login`; helen `A…18`; harbor `D…11` |
| Event (nora login) | `F00000000000000000000202` | `type: login`; nora `A…17`; northstar `D…10` |
| Event (pat arrived) | `F00000000000000000000203` | `type: arrived` only (no encounter/journey); pat `A…19`; persevere `D…02` |

**Preserved:** `F000…01`–`F000…0197` unchanged. Notification seeds unchanged (still `C…01`–`C…06`). No Dashboard collection.

**Testing results**

- Reused already-running local configurator `:8385` (compose on host `:27017`; no `make dev`, no port override). Packaging skipped (`make down` / `make container` / `mh up mongodb`) so later sequential tasks can reuse `:8385`.
- `DELETE /api/database/` → HTTP 200, `status: SUCCESS`.
- `POST /api/configurations/` → HTTP 200, top-level `status: SUCCESS` (`CFG-07-PROCESS_ALL`); zero FAILURE events.
- `CFG-05-Event.yaml` SUCCESS (203 docs: prior 197 + 6 new).
- `CFG-05-Notification.yaml` SUCCESS (6 docs; no new Notification documents).
- Spot-check (mongosh `mentor_hub`):
  - `type: encounter` + `context.customer_id` persevere `D…02`: **1** (`F…0198` / `E…0a`).
  - `type: encounter` + `context.customer_id` supersoft `D…07`: **1** (`F…0199` / `E…0b`).
  - `type: encounter` + pat `A…19` / helen `A…18` / nora `A…17` / donny `A…13` / harbor `D…11`: **0**.
  - helen `A…18` `type: login`: **1**; nora `A…17` `type: login`: **1**; pat `A…19` `arrived` only.
  - `F…0197` retained; Notification count **6**; no `notification_created` after `F…0197`; no `Dashboard` collection.
- Grep `configurator/` for Dashboard collection paths: none (only Resource name `Project: Admin Dashboard`).

**Orchestrator confirmation:** `DELETE`/`POST` on `:8385` re-ran SUCCESS (Event + Notification CFG). Spot-check: Event 203; Notification 6; encounter+customer persevere 1 / supersoft 1; pat/harbor encounter 0; helen login 1.

**Follow-ups**

- T240 / T242: next free Event `_id` is `F00000000000000000000204`.
