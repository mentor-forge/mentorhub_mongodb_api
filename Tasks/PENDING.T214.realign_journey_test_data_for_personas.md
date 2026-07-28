# T214 – Realign Journey Test Data for Personas

**Status**: Pending  
**Type**: Feature  
**Depends On**: T211, T212  
**Description**: Reassign mentee Journey documents to persona mentees and adjust progress stories for Daniel, Lucky, and Mary.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/Journey.0.1.0.0.json`, `configurator/test_data/Path.0.1.0.0.json`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `Tasks/PENDING.T209.audit_persona_test_data.md` — journey ownership plan
- `Tasks/PENDING.T211.rebuild_profile_test_data_for_personas.md`
- `Tasks/PENDING.T212.update_mentee_test_data_for_personas.md`
- `Tasks/SHIPPED.T117.create_journey_template.md` — template journey
- `Tasks/SHIPPED.T118.generate_mentee_journey_test_data.md` — mentee progress model

### Target journey ownership

| Mentee persona | Profile | Progress depth | Path focus |
| --- | --- | --- | --- |
| Daniel | `daniel` | Moderate — mid `library`, active `now` | Frontend / Vue practitioner path |
| Lucky | `lucky` | Moderate — mid `library`, active `now` | Backend / SRE practitioner path |
| Mary | `mary` | Deep — extensive `library`, rich `now` | Full-stack / platform path |

### Migration rules

- Remove journey documents owned by deprecated profiles (`luther`, `taylor`, etc.).
- Reassign or regenerate journeys so exactly **three** mentee journeys exist (one per persona mentee).
- Preserve journey `_id` values tied to unchanged `profile_id` where possible.
- Journey `library` / `now` / `next` resource references must exist in `Resource.0.1.0.0.json`.
- Progress depth should correlate with planned Event density (Mary > Lucky ≈ Daniel).

## Goals

- Three mentee journeys aligned to Daniel, Lucky, and Mary personas.
- No journey references removed profile `_id` values.
- Configure-database Journey step returns **SUCCESS**.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Journey.0.1.0.0.json`

## Execution Notes

_(Reserved for task execution agent.)_
