# T237 – Seed Encounter activity for Customer org roster (F-D23)

**Status:** Pending  
**Type:** Feature  
**Depends On:** T236  
**Description:** Ensure **Encounter** seeds support E3 roster **activity** vs **empty** rows: recent sessions for populated subscribed orgs; **no** Encounters for harbor (empty roster) or pat (empty activity). Prefer append over rewrite. Pre-release: edit `Encounter.0.1.0.0.json` in place.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/customer_journey_issues.md` — E3; Encounter is session activity under a Customer org (join `mentee_id` → `Profile.customer_id`)
- GitHub: [F-D23 #55](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/55)
- `Tasks/PENDING.T236.seed_customer_org_roster_profiles.md` — roster graph + stable ids (harbor / helen / pat); **Execution Notes** after T236 ships
- `Tasks/SHIPPED.T213.realign_encounter_test_data_for_personas.md` — existing E01–E09 (Daniel, Lucky, Mary, Linda)
- `configurator/dictionaries/Encounter.0.1.0.yaml` — `mentor_id`, `mentee_id`, `date`, `plan_id`, `agenda`, `status`, narrative fields; **no** `customer_id` (do not add schema)
- `configurator/test_data/Encounter.0.1.0.0.json` — nine documents `E000…01`–`E000…09`; last is Linda archived
- `configurator/test_data/Plan.0.1.0.0.json` — `basic` plan `f00000000000000000000001` (same hex as Discount Setting `f…01` — different collection; reuse this **plan** `_id` for new Encounters)
- **Out of scope:** Event files (T238); Profile / Customer edits (T236); Notification / Dashboard; Mentee / Journey / Note / Rating for pat; dictionary changes unless running configurator proves a gap (document only; do not invent fields)

### Empty-state rules (must hold after this task)

| Profile | Customer | Encounters |
| --- | --- | --- |
| helen `A…18` | harbor (subscribed, no mentees) | **none** (helen is not a mentee) |
| pat `A…19` | persevere | **none** — empty activity row on populated roster |
| nora `A…17` | northstar (unsubscribed) | **none** |
| donny `A…13` | scamsoft | **none** |

Do **not** add Encounters whose `mentee_id` is helen, pat, nora, donny, or patha-owner.

### Populated roster (keep + refresh)

Existing E01–E09 already cover Daniel (persevere), Lucky (supersoft), Mary (unsubscribed self-funded), Linda (archived ALI). **Preserve all nine.**

Append **at least two** new **active** Encounters with `date` in **2026** (org-home “recent activity”; existing sessions are 2024–2025):

| Suggested Encounter `_id` | Mentor | Mentee | Customer via Profile |
| --- | --- | --- | --- |
| `E0000000000000000000000a` or next free `E0…` in **Encounter** collection | Paula `A…10` | Daniel `A…02` | persevere |
| next free `E0…` | Danny `A…14` | Lucky `A…03` | supersoft |

Confirm unused in `Encounter.0.1.0.0.json` (Note documents may already use `E000…10` — cross-collection reuse is OK; within Encounter the hex must be unique). Prefer sequential unused 24-hex after `E…09` (e.g. `E0000000000000000000000a` / `E…0b` **or** `E…10` / `E…11` if those Encounter ids are free).

Field rules: copy T213/`basic` `plan_id` + checklist `agenda`; realistic `transcript` / `summary` / `tldr`; `status: active`; breadcrumbs. Encounter schema has no `customer_id` — join remains `mentee_id` → Profile.

## Goals

- Populated subscribed orgs (persevere, supersoft) have Encounter activity including ≥1 session dated 2026 per demo mentee (Daniel, Lucky).
- pat / harbor / northstar / scamsoft remain Encounter-empty for E3 empty states.
- Existing E01–E09 unchanged.
- Configure-database Encounter step **SUCCESS**.

## Testing Expectations

```sh
make dev
# If host port 27017 is busy, use compose ports !override (e.g. host 27018) as in prior F-D tasks.
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- Spot-check (use T236 Execution Notes ids):

```javascript
db.Encounter.countDocuments({ mentee_id: ObjectId("A00000000000000000000002") })  // Daniel: prior + new
db.Encounter.countDocuments({ mentee_id: ObjectId("A00000000000000000000003") })  // Lucky: prior + new
db.Encounter.countDocuments({ mentee_id: ObjectId("<pat>") })  // 0
db.Encounter.countDocuments({ mentee_id: ObjectId("<helen>") })  // 0
db.Encounter.countDocuments({ mentee_id: ObjectId("A00000000000000000000017") })  // nora: 0
```

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Encounter.0.1.0.0.json` — append recent Daniel + Lucky sessions; do not rewrite E01–E09
- `Tasks/PENDING.T237.seed_roster_encounter_activity.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

_(Reserved for the task execution agent. Record new Encounter `_id`s for T238.)_
