# T215 – Realign Event Test Data for Personas

**Status**: Pending  
**Type**: Feature  
**Depends On**: T213, T214  
**Description**: Regenerate Event seed data so activity trails exist for all persona mentees and key coordinator/customer personas.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/Event.0.1.0.0.json`, `configurator/dictionaries/Event.0.1.0.yaml`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `Tasks/PENDING.T209.audit_persona_test_data.md` — event density targets
- `Tasks/PENDING.T214.realign_journey_test_data_for_personas.md` — journey-driven events
- `Tasks/PENDING.T213.realign_encounter_test_data_for_personas.md` — encounter events
- `Tasks/SHIPPED.T119.generate_event_test_data.md` — generation patterns

### Event coverage requirements

**Mentees (required):** Daniel, Lucky, Mary

- `link`, `started`, `completed`, `advanced` derived from each mentee's Journey state
- `encounter` events aligned to T213 Encounter dates
- At least one `note` event per mentee

**Coordinators (recommended):** Emma, Dev Lead, Sr. Dev, Mary

- `login`, `arrived` events for coordinator SPA testing
- Emma / Sr. Dev: events implying matchmaking activity if schema supports context metadata

**Customers (recommended):** Stacey, Entrepreneur, Mary

- Sparse `login` / `arrived` events — busy executives checking dashboards

**Mentors (optional):** Marti, Special, Money

- `login` events for mentor SPA entry

**Enum coverage:** Every `event_types` value appears at least once (`fail` may be rare).

### Update rules

- Remove events whose `context.profile_id` references deprecated profiles.
- Regenerate deterministic `_id` prefix `F000…` if document count changes substantially.
- Spread `created.at_time` over last 6 months; Mary highest density, Daniel moderate, Lucky moderate.
- Do not invent resources not on a mentee's journey.

## Goals

- Event trails exist for all three persona mentees consistent with Journey and Encounter data.
- Coordinator and customer personas have enough events for dashboard / activity-feed testing.
- No events reference removed profile `_id` values.
- Configure-database Event step returns **SUCCESS**.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

MongoDB spot check:

```javascript
db.Event.distinct("context.profile_id")  // includes daniel, lucky, mary ObjectIds
```

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Event.0.1.0.0.json`

## Execution Notes

_(Reserved for task execution agent.)_
