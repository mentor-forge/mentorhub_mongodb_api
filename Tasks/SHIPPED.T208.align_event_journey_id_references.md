# T208 – Align Event journey_id References

**Status**: Shipped  
**Type**: Feature  
**Depends On**: T207  
**Description**: Update Event test data `context.journey_id` values to match the new Journey `_id` / Profile `_id` alignment and remove events tied to pruned journeys.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `configurator/test_data/Event.0.1.0.0.json` — `context.journey_id` references legacy `D000…` Journey ids
- `Tasks/PENDING.T207.align_journey_test_data_resource_ids.md` — new Journey `_id` mapping
- GitHub issue **#45** (F-D19)

### Journey id migration map

| Legacy Journey `_id` | New Journey `_id` |
| --- | --- |
| `D00000000000000000000001` | `A00000000000000000000002` |
| `D00000000000000000000002` | `A00000000000000000000003` |
| `D00000000000000000000003` | `A00000000000000000000004` |
| `D00000000000000000000004` | `A00000000000000000000005` |
| `D00000000000000000000005` | **remove** events (riley) |
| `D00000000000000000000006` | `A00000000000000000000014` |
| `D00000000000000000000007` | **remove** events (casey) |

## Goals

- Replace legacy `context.journey_id` values per the migration map above.
- Remove Event documents whose `context.journey_id` references pruned journeys (`D000…05`, `D000…07`).
- Confirm remaining `context.resource_id` values (if any) reference valid Resource `$oid`s.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect top-level **SUCCESS**.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Event.0.1.0.0.json`

## Execution Notes

- Updated `context.journey_id` from legacy `D000…` values to Profile-aligned Journey `$oid`s.
- Removed 54 Event documents tied to pruned riley/casey journeys (312 → 258). Configure-database SUCCESS.
