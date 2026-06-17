# T106 – Mentee Collection and Profile Schema Update

**Status**: Pending  
**Task Type**: Feature  
**Run Mode**: Sequential (main pipeline — not “Run as needed”)

This task introduces a **Mentee** collection, moves appointment scheduling off **Profile**, and adds **`full_name`** to Profile. We are **pre-release**, so edit the existing **0.1.0** dictionaries and test data directly — **no version bumps and no migrations**.

A human or orchestrator should set `Status` to `Running` before execution and rename the file prefix when complete (`SHIPPED.T106...`).

## User inputs (edit before running)

- **Branch name**: `mentee_collection`
- **Profile dictionary**: `../configurator/dictionaries/Profile.0.1.0.yaml`
- **Mentee dictionary (new)**: `../configurator/dictionaries/Mentee.0.1.0.yaml`
- **Profile configuration**: `../configurator/configurations/Profile.yaml` (stays at version 0.1.0.0)
- **Mentee configuration (new)**: `../configurator/configurations/Mentee.yaml` (version 0.1.0.0)
- **Enumerators file**: `../configurator/enumerators/enumerations.0.yaml`
- **Profile test data**: `../configurator/test_data/Profile.0.1.0.0.json`
- **Mentee test data (new)**: `../configurator/test_data/Mentee.0.1.0.0.json`

## Goal

1. Add a **Mentee** collection — “Mentor notes about a Mentee” — linked to Profile via `profile_id`.
2. Move **`schedule`** and **`next_appointment`** from Profile to Mentee.
3. Add **`full_name`** to Profile for display names (distinct from IdP `name`).
4. Update **0.1.0 test data** to match the revised schemas and verify configure-database succeeds.

## Design decisions

| Concept | Decision |
|--------|----------|
| **Pre-release** | Edit `Profile.0.1.0.yaml` and `Profile.0.1.0.0.json` in place. Do **not** add Profile 0.2.0/0.3.0 versions or migration pipelines. |
| **Mentee vs Profile** | Profile holds person preferences and the **current** `mentor_id` assignment. Mentee is the shared dossier for that person (notes, homework, schedule) — not tied to one mentor. |
| **`profile_id`** | Links Mentee → Profile `_id`. One Mentee per mentee profile (unique index). |
| **Shared notes** | Mentee `notes` (and related fields) accumulate for the **mentee Profile**, not a specific mentor. Do **not** store `mentor_id` on Mentee — when a mentee gets a new mentor (updated on Profile), the new mentor reads the same Mentee document and prior notes remain visible. |
| **`mentor_id` on Profile only** | Keep `mentor_id` on Profile for coordinator matching and current assignment. It does not belong on Mentee. |
| **`full_name`** | Dictionary type **`sentence`** (not `word`) so values like `Mike Storey` validate. |

## Context / Input files

- [Tasks/README.md](./README.md)
- [SHIPPED.T102.generate_profile_test_data.md](./SHIPPED.T102.generate_profile_test_data.md) — EJSON and test-data conventions
- `../configurator/dictionaries/Profile.0.1.0.yaml`
- `../configurator/test_data/Profile.0.1.0.0.json` — 15 profiles; 7 mentees currently carry `mentor_id` + `schedule`
- `../configurator/test_data/Identity.0.1.0.0.json` — source for display names
- `../configurator/types/`
- `erd.drawio` / `erd.svg` — Mentee proposed on branch (`6eb04db`)

## Implementation plan

### Step 1 — Update Profile.0.1.0.yaml

In **`Profile.0.1.0.yaml`**:

- **Add** after `description`:
  ```yaml
  - description: Display name from intake (distinct from IdP username)
    name: full_name
    required: false
    type: sentence
  ```
- **Remove** the `schedule` property block entirely.

`Profile.yaml` configuration stays at **0.1.0.0** pointing at `Profile.0.1.0.0.json`.

### Step 2 — Create Mentee.0.1.0.yaml and configuration

Create **`Mentee.0.1.0.yaml`**. Name: **Mentee**. Description: **Mentor notes about a Mentee**.

Mentee notes are contributed by **any** mentor associated with the mentee over time. The document is keyed by `profile_id`, not by mentor — do **not** include `mentor_id`.

| Property | Type |
|----------|------|
| `_id` | identifier |
| `name` | word |
| `description` | sentence |
| `profile_id` | identifier |
| `notes` | markdown |
| `focus` | sentence |
| `homework` | markdown |
| `schedule` | object (`starting` date-time, `repeats` count) |
| `next_appointment` | date-time |
| `status` | enum (`default_status`) |
| `created`, `saved` | breadcrumb |

Create **`configurator/configurations/Mentee.yaml`** version **0.1.0.0** with indexes: unique `name`, unique `profile_id`, `saved.at_time` (desc). No `mentor_id` index.

### Step 3 — Update Profile.0.1.0.0.json

Edit **`Profile.0.1.0.0.json`** in place:

- **Add** `full_name` to all 15 profiles (derive from Identity email / role, e.g. `mike` → `Mike Storey`, `carol` → `Carol Coordinator`).
- **Remove** `schedule` from every profile.
- **Keep** `mentor_id` on mentee profiles unchanged.

### Step 4 — Create Mentee.0.1.0.0.json

Generate **7** EJSON documents for profiles that had both `mentor_id` and `schedule`: daniel, lucky, mary, luther, riley, taylor, casey.

| Rule | Value |
|------|-------|
| `_id` | `C00000000000000000000001` … `07` |
| `profile_id` | mentee Profile `_id` |
| `schedule` | moved from Profile |
| `name` | `{profile.name}-mentoring` |
| `notes`, `focus`, `homework` | realistic mentor content (markdown where applicable); `notes` may read as a running log visible to any future mentor |
| `next_appointment` | derived from `schedule.starting` + N × `repeats` weeks |
| `status` | `active`, except casey → `archived` |

Do **not** set `mentor_id` on Mentee documents. Current mentor assignment lives on Profile only.

## Requirements

1. **EJSON encoding** — `$oid` for identifiers, `$date` for date-times (see T102).
2. **Schema conformance** — test data matches the 0.1.0 dictionaries.
3. **Relationship integrity** — every Mentee `profile_id` references a real mentee Profile `_id`. Profile `mentor_id` references the currently assigned mentor and may change independently of Mentee notes.
4. **No version bumps** — do not add Profile 0.2.0/0.3.0 or migration files for this task.

## Testing expectations

```bash
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

Expect top-level **SUCCESS** for Profile and Mentee 0.1.0.0.

MongoDB spot checks:

```javascript
db.Profile.countDocuments({ full_name: { $exists: true } })  // 15
db.Profile.countDocuments({ schedule: { $exists: true } })     // 0
db.Mentee.countDocuments({})                                    // 7
```

## Dependencies / Ordering

- Requires existing **Identity** and **Profile 0.1.0** test data.
- Mentee configuration loads after Profile (references Profile `_id`s).

## Out of scope

- Schema version bumps and migrations (pre-release)
- Mentorhub `catalog.yaml` / `architecture.yaml` (separate PR if needed)
- Mentor API CRUD and Mentor SPA UI

## Change control checklist

- [x] Reviewed all **Context / Input files**
- [x] Updated Profile.0.1.0.yaml (`full_name` added, `schedule` removed)
- [x] Created Mentee.0.1.0.yaml and Mentee.yaml configuration
- [x] Updated Profile.0.1.0.0.json (full_name on all 15; schedule removed)
- [x] Created Mentee.0.1.0.0.json (7 documents)
- [ ] Configure database SUCCESS verified
- [x] Commit pushed referencing T106

## Implementation notes

**Summary of changes**

- Edited **Profile.0.1.0** in place: added `full_name`, removed `schedule`.
- Added **Mentee.0.1.0** dictionary and configuration.
- Updated **Profile.0.1.0.0.json** and created **Mentee.0.1.0.0.json** with schedule moved to Mentee records.

**Testing results**

_(run configure database and record results here before marking Shipped)_
