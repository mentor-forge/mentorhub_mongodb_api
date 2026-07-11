# T205 – Prune Mentee Test Data

**Status**: Shipped  
**Type**: Feature  
**Depends On**: T204  
**Description**: Remove Mentee seed documents for pruned profiles (riley, casey) so Mentee `profile_id` references remain valid.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `configurator/test_data/Mentee.0.1.0.0.json` — seven Mentee dossiers today
- `Tasks/PENDING.T204.update_profile_test_data.md` — removes Profile `A000…10` (riley) and `A000…15` (casey)
- `Tasks/SHIPPED.T106.mentee_collection_and_profile_schema.md` — Mentee keyed by `profile_id`

### Mentee records today

| `_id` | `profile_id` | Profile `name` | Action |
| --- | --- | --- | --- |
| `CC0000000000000000000001` | `A000…02` | daniel | **keep** |
| `CC0000000000000000000002` | `A000…03` | lucky | **keep** |
| `CC0000000000000000000003` | `A000…04` | mary | **keep** |
| `CC0000000000000000000004` | `A000…05` | luther | **keep** |
| `CC0000000000000000000005` | `A000…10` | riley | **remove** |
| `CC0000000000000000000006` | `A000…14` | taylor | **keep** |
| `CC0000000000000000000007` | `A000…15` | casey | **remove** |

This task addresses orphaned Mentee references after Profile pruning. It is **not** removing the Mentee collection — only seed documents tied to deleted profiles.

## Goals

- Reduce `Mentee.0.1.0.0.json` from seven to **five** documents.
- Remove Mentee records `CC…05` (riley) and `CC…07` (casey).
- Leave five active mentee dossiers (daniel, lucky, mary, luther, taylor) unchanged except as needed for schema conformance.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect top-level **SUCCESS**.

MongoDB spot check:

```javascript
db.Mentee.countDocuments({})  // 5
db.Mentee.find({ profile_id: { $in: [
  ObjectId("A00000000000000000000010"),
  ObjectId("A00000000000000000000015")
]}}).count()  // 0
```

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Mentee.0.1.0.0.json` — five Mentee documents per goals

## Execution Notes

**Summary of changes**

- Pruned `configurator/test_data/Mentee.0.1.0.0.json` from seven records to five.
- Removed Mentee records for pruned Profile IDs `A00000000000000000000010` (riley) and `A00000000000000000000015` (casey).

**Testing results**

- `curl -X DELETE http://localhost:8385/api/database/` -> HTTP 200, SUCCESS.
- `curl -X POST http://localhost:8385/api/configurations/` -> HTTP 200, SUCCESS.
- MongoDB spot checks: `Mentee` count = 5; removed profile references = 0.
- `make down && make container && mh up mongodb` -> SUCCESS.
