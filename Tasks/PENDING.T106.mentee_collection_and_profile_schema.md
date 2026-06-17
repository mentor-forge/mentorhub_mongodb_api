# T106 – Mentee Collection and Profile Schema Update

**Status**: Pending  
**Task Type**: Feature  
**Run Mode**: Sequential (main pipeline — not “Run as needed”)

This task is the implementation plan for introducing a **Mentee** collection, moving appointment scheduling off **Profile**, and adding **`full_name`** to Profile. A human or orchestrator should set `Status` to `Running` before execution and rename the file prefix when complete (`SHIPPED.T106...`).

## User inputs (edit before running)

- **Branch name**: `mentee_collection` (mongodb_api) and `mentee-collection` (mentorhub specs)
- **Mentee dictionary (new)**: `../configurator/dictionaries/Mentee.0.1.0.yaml`
- **Mentee configuration (new)**: `../configurator/configurations/Mentee.yaml`
- **Profile dictionary (source)**: `../configurator/dictionaries/Profile.0.1.0.yaml`
- **Profile dictionary (0.2.0 bump)**: `../configurator/dictionaries/Profile.0.2.0.yaml`
- **Profile dictionary (0.3.0 bump)**: `../configurator/dictionaries/Profile.0.3.0.yaml`
- **Enumerators file**: `../configurator/enumerators/enumerations.0.yaml`
- **Profile test data (baseline)**: `../configurator/test_data/Profile.0.1.0.0.json`
- **Mentee test data (target)**: `../configurator/test_data/Mentee.0.1.0.0.json`
- **Profile migrations (0.2.0 / 0.3.0)**: `../configurator/migrations/Profile.0.2.0.0.json`, `../configurator/migrations/Profile.0.3.0.0.json`
- **Mentorhub specs repo**: `../../mentorhub/Specifications/catalog.yaml`, `../../mentorhub/Specifications/architecture.yaml`

## Goal

1. Add a **Mentee** collection — “Mentor notes about a Mentee” — linked to Profile via `profile_id`.
2. Move **`schedule`** and related appointment fields from Profile to Mentee.
3. Add **`full_name`** to Profile for display names from intake (distinct from IdP `name`).
4. Generate linked test data, verify configure-database succeeds, commit, and open PR(s) for review.

## Design decisions

| Concept | Decision |
|--------|----------|
| **Mentee vs Profile** | Profile remains the person’s preferences and intake data. Mentee is the mentor’s working dossier for a assigned mentee (notes, homework, schedule). |
| **`profile_id`** | Required link from Mentee → Profile `_id`. One Mentee document per mentee profile (unique index on `profile_id`). |
| **`mentor_id`** | Keep on Profile for coordinator matching; copy onto Mentee for mentor-scoped queries. |
| **`schedule`** | Remove from Profile at 0.3.0; live on Mentee only. |
| **`full_name`** | Use dictionary type **`sentence`** (not `word`) so values like `Mike Storey` validate. |
| **Version test data** | `Profile.0.2.0.0.json` and `Profile.0.3.0.0.json` must be **empty arrays** (`[]`). The configurator **inserts** per version; duplicating all 15 Profile `_id`s causes E11000 duplicate-key errors. Use **migrations** for field adds/removals instead. |

## Context / Input files

Read before implementation:

- [Tasks/README.md](./README.md) — task workflow and change control
- [SHIPPED.T102.generate_profile_test_data.md](./SHIPPED.T102.generate_profile_test_data.md) — Profile test-data conventions and EJSON rules
- `../configurator/dictionaries/Profile.0.1.0.yaml` — current Profile schema (`schedule` on lines 106–118)
- `../configurator/configurations/Profile.yaml` — currently only version 0.1.0.0
- `../configurator/test_data/Profile.0.1.0.0.json` — 15 profiles; mentees with `mentor_id` + `schedule`: daniel, lucky, mary, luther, riley, taylor, casey
- `../configurator/types/` — type fragments for dictionary fields
- `erd.drawio` / `erd.svg` — branch already proposes Mentee in ERD (commit `6eb04db`)
- `../../mentorhub/Specifications/catalog.yaml` — register Mentee in product catalog

## Implementation plan

### Phase 1 — Mentee dictionary and configuration

Create **`Mentee.0.1.0.yaml`** via configurator UI or by hand. Name: **Mentee**. Description: **Mentor notes about a Mentee**.

Properties (minimum):

| Property | Type | Notes |
|----------|------|-------|
| `_id` | identifier | |
| `name` | word | Searchable record name, e.g. `daniel-mentoring` |
| `description` | sentence | Short summary of the mentoring relationship |
| `profile_id` | identifier | `_id` of the related **Profile** (mentee) |
| `mentor_id` | identifier | Assigned mentor’s Profile `_id` |
| `notes` | markdown | Mentor notes (progress, observations, next steps) |
| `focus` | sentence | Current session focus |
| `homework` | markdown | Follow-up items for the mentee |
| `schedule` | object | Move from Profile: `starting` (date-time), `repeats` (count, weeks) |
| `next_appointment` | date-time | Next scheduled meeting |
| `status` | enum | `default_status` |
| `created`, `saved` | breadcrumb | |

Create **`configurator/configurations/Mentee.yaml`** version **0.1.0.0** with indexes:

- unique on `name`
- unique on `profile_id`
- index on `mentor_id`
- index on `saved.at_time` (descending)

### Phase 2 — Profile 0.2.0 (`full_name`)

Copy `Profile.0.1.0.yaml` → **`Profile.0.2.0.yaml`**. Add:

```yaml
- description: Display name from intake (distinct from IdP username)
  name: full_name
  required: false
  type: sentence
```

Add version **0.2.0.0** to `configurator/configurations/Profile.yaml`:

- `test_data: Profile.0.2.0.0.json` → file content **`[]`**
- `migrations: [Profile.0.2.0.0.json]` → aggregation pipeline that `$set`s `full_name` (and any other 0.2.0 fields) on all 15 existing profiles by `_id`

### Phase 3 — Profile 0.3.0 (remove `schedule`)

Copy `Profile.0.2.0.yaml` → **`Profile.0.3.0.yaml`**. **Remove** the `schedule` property block.

Add version **0.3.0.0** to `Profile.yaml`:

- `test_data: Profile.0.3.0.0.json` → **`[]`**
- `migrations: [Profile.0.3.0.0.json]` → pipeline that `$unset`s `schedule` on all Profile documents

### Phase 4 — Mentee test data

Generate **`Mentee.0.1.0.0.json`** (EJSON). Rules:

- **Count**: 7 documents — one per mentee Profile in `Profile.0.1.0.0.json` that has both `mentor_id` and `schedule` (daniel, lucky, mary, luther, riley, taylor, casey).
- **Deterministic `_id`**: `C00000000000000000000001` … `C00000000000000000000007`.
- **Per document**:
  - `profile_id` → mentee Profile `_id`
  - `mentor_id` → copied from that Profile
  - `schedule` → copied from that Profile (before 0.3.0 migration removes it)
  - `name` → `{profile.name}-mentoring`
  - `description` → one sentence summarizing the relationship
  - `notes` → markdown with `## Progress`, `## Observations`
  - `focus` → one-line current focus
  - `homework` → markdown bullet list
  - `next_appointment` → derived from `schedule.starting` + N × `schedule.repeats` weeks (one upcoming date)
  - `status` → `active` (use `archived` when related Profile is archived — casey)
  - `created` / `saved` → breadcrumbs consistent with Profile style

### Phase 5 — Profile `full_name` migration content

The 0.2.0 migration must set **`full_name`** on all 15 profiles. Derive display names from `name` (title case + role suffix where helpful), e.g.:

| `name` | `full_name` |
|--------|-------------|
| mike | Mike Storey |
| carol | Carol Coordinator |
| daniel | Daniel Dissler |
| … | (all 15 profiles) |

Reference: existing Identity / Profile naming in `Identity.0.1.0.0.json` and `Profile.0.1.0.0.json`.

### Phase 6 — Mentorhub specifications (companion repo)

In **`mentorhub`**:

- Add to `Specifications/catalog.yaml`:
  ```yaml
  - name: Mentee
    description: Mentor notes about a Mentee
  ```
- Add **Mentee** to mentor journey `controls` in `Specifications/architecture.yaml`.

Commit on branch `mentee-collection`; open a companion PR linked to the mongodb_api PR.

### Phase 7 — Verify, commit, PR

1. `make dev` or ensure configurator API is running on port **8385**.
2. `DELETE /api/database/` → must return SUCCESS (drop fails if collections exceed safety limit — restart compose for a fresh MongoDB if needed).
3. `POST /api/configurations/` → top-level **SUCCESS**; Profile 0.1.0 → 0.2.0 (migration) → 0.3.0 (migration) and Mentee 0.1.0 all SUCCESS.
4. Verify in MongoDB:
   - 15 Profiles with `full_name`, **no** `schedule`
   - 7 Mentees with `schedule`, `notes`, valid `profile_id` / `mentor_id`
5. `make container` — packaging gate.
6. Commit mongodb_api changes referencing **T106**; push branch; open PR.
7. Commit mentorhub spec changes; open companion PR.

## Requirements

1. **EJSON encoding** — `$oid` for identifiers, `$date` for date-times (see T102).
2. **Schema conformance** — all test data validates against effective dictionary versions.
3. **Relationship integrity** — every Mentee `profile_id` and `mentor_id` references a real Profile `_id`.
4. **No duplicate version inserts** — Profile 0.2.0 / 0.3.0 test-data files stay `[]`; use migrations only.
5. **Incremental commits** — one scoped commit per repo; do not commit `artifacts/` or stray workflow files.

## Testing expectations

- **Configure database**
  ```bash
  curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
  curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
  ```
  Inspect `artifacts/process_all_configurations.json` on failure.

- **`make process`** — optional; may need API warmup after `docker compose up`.

- **MongoDB spot checks** (via `mongosh` or docker exec):
  ```javascript
  db.Profile.countDocuments({ full_name: { $exists: true } })  // 15
  db.Profile.countDocuments({ schedule: { $exists: true } })  // 0
  db.Mentee.countDocuments({})                                 // 7
  ```

## Dependencies / Ordering

- Requires existing **Identity** and **Profile 0.1.0** test data.
- Mentee configuration must be processed **after** Profile reaches 0.3.0 (Mentee references Profile `_id`s that no longer carry `schedule`).
- Mentorhub spec PR depends on mongodb_api dictionary being finalized (can ship in parallel for review).

## Out of scope (follow-up tasks)

- Mentor API CRUD endpoints for Mentee
- Mentor SPA UI for mentee notes / scheduling
- Coordinator API tag derivation for Profile intake fields
- Customer 0.2.0 / intake enumerators (separate intake work if needed)

## Change control checklist

- [ ] Reviewed all **Context / Input files**
- [ ] Phase 1 — Mentee dictionary + configuration
- [ ] Phase 2 — Profile 0.2.0 + migration + empty test data
- [ ] Phase 3 — Profile 0.3.0 + migration + empty test data
- [ ] Phase 4 — Mentee test data (7 documents)
- [ ] Phase 5 — Profile `full_name` on all 15 profiles via migration
- [ ] Phase 6 — mentorhub catalog + architecture
- [ ] Phase 7 — configure database SUCCESS; `make container` SUCCESS
- [ ] Commits pushed; PR(s) opened for review
- [ ] Renamed task file to `SHIPPED.T106...` and filled **Implementation notes**

## Implementation notes (to be updated by the agent)

**Summary of changes**

_(fill in after execution)_

**Testing results**

_(fill in after execution)_
