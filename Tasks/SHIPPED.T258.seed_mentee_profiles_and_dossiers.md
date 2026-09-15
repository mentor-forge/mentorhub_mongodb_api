# T258 – Seed Mentee profiles and dossiers for active mentors

**Status:** Shipped  
**Type:** Feature  
**Depends On:** T257  
**Description:** Add 11 new mentee Profile documents in `Profile.0.1.0.0.json` and corresponding Mentee dossier documents in `Mentee.0.1.0.0.json`, ensuring every active Mentor other than Marti (Paula, Danny, Elon, Melinda) has 3 to 5 mentees assigned. Update `Tasks/scripts/persona_ids.json`.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`, `Tasks/scripts/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `configurator/test_data/Profile.0.1.0.0.json` — existing Profile test data
- `configurator/test_data/Mentee.0.1.0.0.json` — existing Mentee test data
- `configurator/test_data/Customer.0.1.0.0.json` — customer organization IDs (`persevere`: `D...02`, `supersoft`: `D...07`, `ali`: `D...06`)
- `Tasks/scripts/persona_ids.json` — persona ObjectId map
- `Tasks/SHIPPED.T255.update_mentee_test_data.md` — Mentee schema reference (`summary`, `notes`, `status`, `created`, `saved`)
- `Tasks/SHIPPED.T257.generate_expanded_encounter_test_data.md` — predecessor task
- **Out of scope:** Modifying dictionary schemas; modifying Marti's mentee roster (Marti remains with Mary and Linda); creating encounters (deferred to T259).

### Active Mentor Allocation and Target Counts

| Mentor | Mentor `_id` | Organization | Existing Mentees | New Mentees to Add | Total Mentee Count |
| --- | --- | --- | --- | --- | --- |
| **Marti Lombardi** | `A00000000000000000000006` | ALI | 2 (Mary, Linda) | **0** (excluded) | 2 (unchanged) |
| **Paula Persevere** | `A00000000000000000000010` | Persevere | 2 (Daniel `A...02`, Pat `A...19`) | **2** (`A...22`, `A...23`) | **4** |
| **Danny Dev Lead** | `A00000000000000000000014` | SuperSoft | 1 (Lucky `A...03`) | **3** (`A...24`, `A...25`, `A...26`) | **4** |
| **Elon Money** | `A00000000000000000000011` | ALI / Startup | 0 | **3** (`A...27`, `A...28`, `A...29`) | **3** |
| **Melinda Multi** | `A00000000000000000000015` | ALI / Full-Stack | 0 | **3** (`A...2a`, `A...2b`, `A...2c`) | **3** |

### New Mentee Inventory

| Mentee `_id` | Display Name | Mentor | Customer | Email |
| --- | --- | --- | --- | --- |
| `A00000000000000000000022` | Jordan Persevere | Paula (`A...10`) | Persevere (`D...02`) | `jordan.persevere@mentor-forge.dev` |
| `A00000000000000000000023` | Taylor Persevere | Paula (`A...10`) | Persevere (`D...02`) | `taylor.persevere@mentor-forge.dev` |
| `A00000000000000000000024` | Casey SuperSoft | Danny (`A...14`) | SuperSoft (`D...07`) | `casey.supersoft@mentor-forge.dev` |
| `A00000000000000000000025` | Morgan SuperSoft | Danny (`A...14`) | SuperSoft (`D...07`) | `morgan.supersoft@mentor-forge.dev` |
| `A00000000000000000000026` | Alex SuperSoft | Danny (`A...14`) | SuperSoft (`D...07`) | `alex.supersoft@mentor-forge.dev` |
| `A00000000000000000000027` | Sam Startup | Elon (`A...11`) | ALI (`D...06`) | `sam.startup@mentor-forge.dev` |
| `A00000000000000000000028` | Riley Revenue | Elon (`A...11`) | ALI (`D...06`) | `riley.revenue@mentor-forge.dev` |
| `A00000000000000000000029` | Quinn Capital | Elon (`A...11`) | ALI (`D...06`) | `quinn.capital@mentor-forge.dev` |
| `A0000000000000000000002a` | Avery Design | Melinda (`A...15`) | ALI (`D...06`) | `avery.design@mentor-forge.dev` |
| `A0000000000000000000002b` | Devon Interface | Melinda (`A...15`) | ALI (`D...06`) | `devon.interface@mentor-forge.dev` |
| `A0000000000000000000002c` | Harper Fullstack | Melinda (`A...15`) | ALI (`D...06`) | `harper.fullstack@mentor-forge.dev` |

### Field Rules

1. **Profile Documents (`Profile.0.1.0.0.json`)**:
   - `_id`: deterministic ObjectId (`A00000000000000000000022` through `A0000000000000000000002c`).
   - `status`: `"active"`.
   - `roles`: `["mentee"]`.
   - `mentor_id`: `{"$oid": "<mentor_id>"}`.
   - `customer_id`: `{"$oid": "<customer_id>"}`.
   - `display_name`: unique string adhering to Full Name unique index.
   - `email`: unique `@mentor-forge.dev` address adhering to Email unique index.
   - `email_verified`: `true`.
   - `goals`, `interests`, `description`, and `experience`: populated with realistic data aligned with the mentee's learning track.
   - `created` and `saved`: valid breadcrumb objects.

2. **Mentee Documents (`Mentee.0.1.0.0.json`)**:
   - `_id`: matching Profile ObjectId.
   - `summary`: concise single-sentence summary of the mentoring relationship.
   - `notes`: markdown mentor observations and learning goals.
   - `status`: `"active"`.
   - `created` and `saved`: valid breadcrumb objects.

3. **Persona IDs Map (`Tasks/scripts/persona_ids.json`)**:
   - Add new profiles to `profiles` and `mentees` sections.

## Goals

- Add 11 new mentee Profile documents to `configurator/test_data/Profile.0.1.0.0.json`.
- Add 11 corresponding Mentee dossier documents to `configurator/test_data/Mentee.0.1.0.0.json`.
- Update `Tasks/scripts/persona_ids.json` to register the new personas and mentees.
- Every active mentor other than Marti has 3 to 5 mentees (Paula: 4, Danny: 4, Elon: 3, Melinda: 3).
- Marti's mentee roster remains unchanged.
- Configure-database succeeds with HTTP 200 and top-level `status: SUCCESS`.

## Testing Expectations

### Database Drop & Configure Test

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200** and top-level **`status: SUCCESS`**.
- `CFG-05-Profile.yaml` and `CFG-05-Mentee.yaml` import cleanly without schema or unique index violations.

### MongoDB Spot Checks (`mongosh mentor_hub`)

```javascript
// Total profile counts
db.Profile.countDocuments({}) // >= 32 (21 existing + 11 new)
db.Profile.countDocuments({ roles: "mentee" }) // 16 (5 existing + 11 new)

// Per-mentor mentee counts in Profile
db.Profile.countDocuments({ mentor_id: ObjectId("A00000000000000000000010") }) // Paula == 4
db.Profile.countDocuments({ mentor_id: ObjectId("A00000000000000000000014") }) // Danny == 4
db.Profile.countDocuments({ mentor_id: ObjectId("A00000000000000000000011") }) // Elon == 3
db.Profile.countDocuments({ mentor_id: ObjectId("A00000000000000000000015") }) // Melinda == 3
db.Profile.countDocuments({ mentor_id: ObjectId("A00000000000000000000006") }) // Marti == 2

// Mentee collection counts
db.Mentee.countDocuments({}) // >= 15 (4 existing + 11 new)
db.Mentee.countDocuments({ summary: { $exists: true } }) // matches total
```

### Packaging Verification

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Profile.0.1.0.0.json` — append 11 new mentee Profile documents
- `configurator/test_data/Mentee.0.1.0.0.json` — append 11 new Mentee dossier documents
- `Tasks/scripts/persona_ids.json` — register new persona IDs
- `Tasks/PENDING.T258.seed_mentee_profiles_and_dossiers.md` — this file (Execution Notes)

## Execution Notes

### Plan

1. Edit `configurator/test_data/Profile.0.1.0.0.json` to append 11 new mentee documents (`A...22` through `A...2c`) with required fields, unique display names, and email addresses.
2. Edit `configurator/test_data/Mentee.0.1.0.0.json` to append 11 new dossier documents with `summary`, `notes`, and breadcrumbs.
3. Update `Tasks/scripts/persona_ids.json` with the new profiles and mentees.
4. Run `make dev`, drop database with `DELETE /api/database/`, and configure via `POST /api/configurations/`.
5. Verify spot check queries in `mongosh`.
6. Run packaging verification (`make down`, `make container`, `mh up mongodb`).

### Completion Summary

- Created and ran `Tasks/scripts/seed_mentee_test_data.py` to deterministically append 11 new mentee documents across `Profile.0.1.0.0.json`, `Mentee.0.1.0.0.json`, and `Tasks/scripts/persona_ids.json`.
- Mentees added:
  - Paula (`A...10`): Jordan Persevere (`A...22`), Taylor Persevere (`A...23`) -> Total Paula mentees = 4.
  - Danny (`A...14`): Casey SuperSoft (`A...24`), Morgan SuperSoft (`A...25`), Alex SuperSoft (`A...26`) -> Total Danny mentees = 4.
  - Elon (`A...11`): Sam Startup (`A...27`), Riley Revenue (`A...28`), Quinn Capital (`A...29`) -> Total Elon mentees = 3.
  - Melinda (`A...15`): Avery Design (`A...2a`), Devon Interface (`A...2b`), Harper Fullstack (`A...2c`) -> Total Melinda mentees = 3.
  - Marti (`A...06`): Unchanged with 2 mentees (Mary, Linda).
- All profiles satisfy unique indexes on `display_name` and `email`. All mentee dossiers contain valid `summary`, `notes`, and breadcrumbs.

### Test Results

- Local dev services started cleanly with `INPUT_FOLDER=$(pwd)/configurator docker compose up -d`.
- `curl -X DELETE "http://localhost:8385/api/database/"` returned HTTP 200 with status SUCCESS (`DROP_DATABASE`).
- `curl -X POST "http://localhost:8385/api/configurations/"` returned HTTP 200 with status SUCCESS (`PROCESS`), 18 sub-events with 0 failures.
- `mongosh` spot checks:
  - `Total profiles`: 32
  - `Total mentees in Profile`: 16
  - `Paula mentees`: 4
  - `Danny mentees`: 4
  - `Elon mentees`: 3
  - `Melinda mentees`: 3
  - `Marti mentees`: 2
  - `Total Mentee collection docs`: 15
  - `Mentee docs with summary`: 15

