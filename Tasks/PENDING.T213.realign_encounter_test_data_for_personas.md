# T213 – Realign Encounter Test Data for Personas

**Status**: Pending  
**Type**: Feature  
**Depends On**: T211, T212  
**Description**: Rebuild Encounter seed data so sessions reflect persona mentor–mentee relationships, including compensated encounters for Money Mentor.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/Encounter.0.1.0.0.json`, `configurator/dictionaries/Encounter.0.1.0.yaml`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `Tasks/PENDING.T209.audit_persona_test_data.md` — encounter distribution plan
- `Tasks/PENDING.T211.rebuild_profile_test_data_for_personas.md` — mentor/mentee `$oid` values
- `Tasks/PENDING.T212.update_mentee_test_data_for_personas.md` — schedule alignment
- `Tasks/SHIPPED.T107.generate_encounter_test_data.md` — agenda/plan conventions
- `configurator/test_data/Plan.0.1.0.0.json` — `basic` plan (`f00000000000000000000001`)

### Target encounter distribution

| Mentee | Primary mentor | Session count (min) | Notes |
| --- | --- | --- | --- |
| Daniel | Special | 2 | Persevere-exclusive mentoring |
| Lucky | Sr. Dev | 2 | SuperSoft technical mentoring |
| Mary | Marti | 2 | Self-funded apprentice sessions |

| Mentor | Mentee | Session count (min) | Notes |
| --- | --- | --- | --- |
| Money | Daniel | 1 | **Compensated** encounter |
| Money | Lucky | 1 | **Compensated** encounter |
| Marti | Mary | (included above) | Standard ALI mentoring |

Optional: one historical Marti → Daniel encounter if product needs cross-mentor history; default is Special-only for Daniel.

### Field rules

- Use `basic` plan for `plan_id`; copy checklist into `agenda` per T107.
- Deterministic Encounter `_id` prefix `E000…` (renumber if document count changes).
- Remove encounters referencing deprecated profile `_id` values (luther, taylor, etc.).
- Set `mentor_id` / `mentee_id` to persona Profile `$oid` values.
- If Encounter schema supports compensation/billing fields, set them on Money Mentor sessions using **existing** dictionary fields only (pre-release: do not add schema versions or migrations).
- Realistic `transcript`, `summary`, `tldr` referencing persona names and journey progress.
- Spread `date` over last 6 months; align with Mentee `schedule` / `next_appointment`.
- Cover `default_status` enum (`active`, `archived`) — use archived session for audit-approved archived mentee if present.

## Goals

- Every active persona mentee has at least **two** encounters with their assigned primary mentor.
- Money Mentor has at least **two** compensated encounters (Daniel + Lucky).
- No encounters reference removed profiles.
- Configure-database Encounter step returns **SUCCESS**.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

MongoDB spot checks:

```javascript
db.Encounter.countDocuments({ mentee_id: ObjectId("...daniel...") })
db.Encounter.countDocuments({ mentor_id: ObjectId("...money...") })  // >= 2
```

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Encounter.0.1.0.0.json`

## Execution Notes

_(Reserved for task execution agent.)_
