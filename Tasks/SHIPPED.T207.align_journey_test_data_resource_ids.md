# T207 – Align Journey Test Data resource_id Values

**Status**: Shipped  
**Type**: Feature  
**Depends On**: T206  
**Description**: Audit Journey test data `resource_id` values, convert `now` entries to Resource `$oid`s, align Journey `_id` with Profile `_id` (1-to-1), and prune journeys for removed profiles.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `configurator/dictionaries/Journey.0.1.0.yaml` — T206 sets `now.resource_id` to `identifier`
- `configurator/test_data/Profile.0.1.0.0.json` — ten active profiles; mentees with `mentor_id`: daniel, lucky, mary, luther, taylor
- `configurator/test_data/Resource.0.1.0.0.json` — Resource `$oid` lookup by `name`
- `configurator/test_data/Journey.0.1.0.0.json` — eight documents today (template + seven mentee journeys)
- `Tasks/SHIPPED.T118.generate_mentee_journey_test_data.md` — prior Journey `_id` scheme (`D000…`)
- `Tasks/SHIPPED.T204.update_profile_test_data.md` — removed riley (`A000…10`) and casey (`A000…15`) profiles
- GitHub issue **#45** (F-D19)

### Target mentee Journey mapping (1-to-1 `_id` = `profile_id`)

| Profile `name` | Journey `_id` / `profile_id` | Action |
| --- | --- | --- |
| daniel | `A00000000000000000000002` | migrate from `D000…01` |
| lucky | `A00000000000000000000003` | migrate from `D000…02` |
| mary | `A00000000000000000000004` | migrate from `D000…03` |
| luther | `A00000000000000000000005` | migrate from `D000…04` |
| taylor | `A00000000000000000000014` | migrate from `D000…06` |
| riley | `A00000000000000000000010` | **remove** journey |
| casey | `A00000000000000000000015` | **remove** journey |

Keep the T117 template Journey (`ffff00000000000000000001`) unchanged.

## Goals

- Convert every `now[].resource_id` string (Resource `name`) to a valid Resource `$oid` from `Resource.0.1.0.0.json`.
- Confirm `library[].resource_id` and `next[].topics[].resources[]` already reference valid Resource `$oid` values.
- Set each mentee Journey `_id` equal to its `profile_id` (same `$oid` value).
- Remove Journey documents for pruned profiles (riley, casey).
- Final count: **6** Journey documents (1 template + 5 mentees).

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect top-level **SUCCESS**.

MongoDB spot check:

```javascript
db.Journey.countDocuments({})  // 6
db.Journey.find({ profile_id: { $exists: true }, $expr: { $ne: ["$_id", "$profile_id"] } }).count()  // 0
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

- Ran `Tasks/scripts/align_f_d19_resource_ids.py` to convert `now.resource_id` names to Resource `$oid`s.
- Migrated mentee Journey `_id` values to match `profile_id`; removed riley and casey journeys.
- Final Journey count: 6 (template + 5 mentees). Configure-database SUCCESS.
