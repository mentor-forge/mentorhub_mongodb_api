# T211 – Rebuild Profile Test Data for Personas

**Status**: Shipped  
**Type**: Feature  
**Depends On**: T210  
**Description**: Rebuild Profile seed data for twelve persistent personas with correct `roles`, `customer_id`, `mentor_id`, and stable `_id` values.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/Profile.0.1.0.0.json`, `configurator/dictionaries/Profile.0.1.0.yaml`, `configurator/enumerators/enumerations.0.yaml`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `Tasks/PENDING.T209.audit_persona_test_data.md` — `_id` map and realignment plan
- `Tasks/PENDING.T210.update_customer_test_data_for_personas.md` — Customer `$oid` references
- `configurator/enumerators/enumerations.0.yaml` — `user_roles`, `profile_status`

### Target profiles (12 documents)

Use T209 **Execution Notes** for final `_id` assignments. Preserve existing `_id` values where the slug is retained to minimize downstream churn:

| `_id` (proposed) | `name` | Persona | `roles` | `customer_id` | `mentor_id` |
| --- | --- | --- | --- | --- | --- |
| `A000…01` | `mike` | Mike the Admin | all `user_roles` | ALI | — |
| `A000…02` | `daniel` | Daniel | mentee | Persevere | Special (`A000…??`) |
| `A000…03` | `lucky` | Lucky | mentee | SuperSoft | Sr. Dev (`A000…??`) |
| `A000…04` | `mary` | Mary the Super Mentee | customer, coordinator, mentee | Mary | Marti (`A000…06`) |
| `A000…06` | `marti` | Marti the Mentor | mentor | — | — |
| `A000…07` | `emma` | Emma the Coordinator | coordinator | Persevere | — |
| `A000…08` | `stacey` | Stacey the CEO | customer | Persevere | — |
| `A000…09` | `special` | Special Mentor | mentor | ALI | — |
| `A000…10` | `money` | Money Mentor | mentor | ALI | — |
| `A000…11` | `entrepreneur` | Entrepreneur | customer | SuperSoft | — |
| `A000…12` | `devlead` | Dev Lead | coordinator | SuperSoft | — |
| `A000…13` | `srdev` | Sr. Dev | coordinator, mentor | SuperSoft | — |

**Reuse note:** `A000…13` may replace former `sam`; `A000…07` replaces `carol` → `emma`. Assign new `_id` values for `special`, `money`, `entrepreneur`, `devlead` per T209.

### Profiles to remove

Delete documents for deprecated slugs: `luther`, `sam`, `carol`, `cat`, `taylor` (unless T209 audit retains any for enum coverage under a new persona name).

### Field rules

- `full_name` unique across all profiles.
- `email`: `{slug}@mentor-forge.dev` unless audit specifies otherwise.
- `roles`: must match persona matrix; every `user_roles` enum value appears at least once across the dataset.
- `customer_id`: required on customer, mentee, and coordinator profiles per sponsorship table.
- `mentor_id`: set on mentee profiles per mentor assignment matrix (T209).
- EJSON: `$oid` for identifiers, `$date` for date-times.
- Preserve believable `experience`, `goals`, and `interests` aligned with each persona story.

## Goals

- `Profile.0.1.0.0.json` contains exactly **twelve** persona documents (plus any audit-approved edge-case personas).
- All retained `_id` values documented in T209 plan are unchanged.
- Removed profiles no longer referenced by any seed collection after downstream tasks ship.
- Configure-database Profile step returns **SUCCESS**.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

MongoDB spot checks:

```javascript
db.Profile.countDocuments({})
db.Profile.countDocuments({ name: { $in: ["luther","sam","carol","cat","taylor"] } })  // 0
db.Profile.countDocuments({ roles: { $exists: true } })  // all profiles
```

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Profile.0.1.0.0.json`

## Execution Notes

_(Reserved for task execution agent.)_
