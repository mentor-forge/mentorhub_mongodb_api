# T212 – Update Mentee Test Data for Personas

**Status**: Pending  
**Type**: Feature  
**Depends On**: T211  
**Description**: Align Mentee dossiers to persona mentees (Daniel, Lucky, Mary) and remove dossiers for deprecated profiles.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/Mentee.0.1.0.0.json`, `configurator/dictionaries/Mentee.0.1.0.yaml`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `Tasks/PENDING.T209.audit_persona_test_data.md` — mentee `_id` / `profile_id` map
- `Tasks/PENDING.T211.rebuild_profile_test_data_for_personas.md` — Profile references
- `Tasks/SHIPPED.T205.prune_mentee_test_data.md` — prior prune pattern

### Target Mentee dossiers

Only profiles with the **mentee** role need Mentee collection documents:

| Persona | Profile `name` | Mentor (Profile) | Customer | Notes |
| --- | --- | --- | --- | --- |
| Daniel | `daniel` | Special (`special`) | Persevere | Persevere graduate story |
| Lucky | `lucky` | Sr. Dev (`srdev`) | SuperSoft | SuperSoft engineering apprentice |
| Mary | `mary` | Marti (`marti`) | Mary | Self-funded; bi-weekly sessions |

### Remove

- Mentee records for removed profiles: `luther`, `taylor`, and any other deprecated `profile_id` from T209.
- Preserve deterministic Mentee `_id` values where `profile_id` is unchanged (daniel, lucky, mary) to reduce Journey churn.

### Content guidelines

- Update `description`, `schedule`, `next_appointment`, and mentoring notes to reflect persona stories.
- Daniel: frontend/Vue focus, Persevere program context.
- Lucky: backend/system-design focus, SuperSoft startup context.
- Mary: career pivot / self-funded apprentice narrative.

## Goals

- `Mentee.0.1.0.0.json` contains exactly **three** mentee dossiers (unless T209 adds archived mentee).
- Every `profile_id` references a valid Profile with the mentee role.
- No orphaned references to removed profiles.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

MongoDB spot check:

```javascript
db.Mentee.countDocuments({})  // 3 (or audit count)
db.Mentee.distinct("profile_id")  // daniel, lucky, mary profile ObjectIds only
```

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Mentee.0.1.0.0.json`

## Execution Notes

_(Reserved for task execution agent.)_
