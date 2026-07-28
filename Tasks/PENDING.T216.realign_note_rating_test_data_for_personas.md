# T216 – Realign Note and Rating Test Data for Personas

**Status**: Pending  
**Type**: Feature  
**Depends On**: T211  
**Description**: Update Note and Rating seed data so authors and subjects reference persona profiles only.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/Note.0.1.0.0.json`, `configurator/test_data/Rating.0.1.0.0.json`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `Tasks/PENDING.T209.audit_persona_test_data.md`
- `Tasks/PENDING.T211.rebuild_profile_test_data_for_personas.md`
- `Tasks/SHIPPED.T121.generate_note_test_data.md`
- `Tasks/SHIPPED.T120.generate_rating_test_data.md`

### Update rules

- Replace profile references to deprecated slugs (`luther`, `sam`, `carol`, `cat`, `taylor`) with appropriate persona profiles.
- Notes authored by mentors should use Marti, Special, Sr. Dev, or Money as appropriate.
- Notes about mentees should target Daniel, Lucky, or Mary.
- Ratings should include journey-library ratings tied to mentee progress (Mary deep, others moderate).
- Preserve deterministic `_id` conventions where documents remain valid after profile swap.

## Goals

- No Note or Rating documents reference removed profile `_id` values.
- At least one Note per persona mentee; ratings reflect journey library usage.
- Configure-database Note and Rating steps return **SUCCESS**.

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

- `configurator/test_data/Note.0.1.0.0.json`
- `configurator/test_data/Rating.0.1.0.0.json`

## Execution Notes

_(Reserved for task execution agent.)_
