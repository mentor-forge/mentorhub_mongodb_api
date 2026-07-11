# T204 – Update Profile Test Data

**Status**: Pending  
**Type**: Feature  
**Depends On**: T201, T203  
**Description**: Prune Profile seed data to ten personas, add `roles` and `customer_id`, and align with the JWT-claims identity model.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`, `configurator/dictionaries/`, `configurator/enumerators/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `configurator/dictionaries/Profile.0.1.0.yaml` — `roles` and `customer_id` (T201)
- `configurator/enumerators/enumerations.0.yaml` — `user_roles`
- `configurator/test_data/Profile.0.1.0.0.json` — 15 profiles today
- `configurator/test_data/Customer.0.1.0.0.json` — three customers (T203)
- `Tasks/SHIPPED.T102.generate_profile_test_data.md` — EJSON and deterministic `_id` conventions
- Former `Identity.0.1.0.0.json` role mappings (reference for migration):

| `name` | Former Identity `roles` |
| --- | --- |
| mike | `admin`, `mentor` |
| daniel | `mentee` |
| lucky | `mentee` |
| mary | `mentee` |
| luther | `mentee`, `admin` |
| marti | `mentor` |
| carol | `coordinator` |
| cat | `customer` |
| sam | `admin` |
| taylor | `mentor`, `mentee` |

### Profiles to **keep** (10 documents)

Retain these `name` values and **preserve existing `_id` values** so downstream test data (Journey, Encounter, Event, Note, Rating, Mentee) continues to resolve:

| `_id` | `name` | `full_name` |
| --- | --- | --- |
| `A00000000000000000000001` | mike | Mike Storey |
| `A00000000000000000000002` | daniel | Daniel Dissler |
| `A00000000000000000000003` | lucky | Lucky Minyard |
| `A00000000000000000000004` | mary | Mary Anderson |
| `A00000000000000000000005` | luther | Luther Still |
| `A00000000000000000000006` | marti | Marti Lombardi |
| `A00000000000000000000007` | carol | Carol Coordinator |
| `A00000000000000000000008` | cat | Cat Customer |
| `A00000000000000000000013` | sam | Sam Admin |
| `A00000000000000000000014` | taylor | Taylor Dual |

### Profiles to **remove**

Delete documents for: `jordan`, `riley`, `morgan`, `alex`, `casey` (`_id` `09`–`12`, `15`).

### `roles` assignment rules

1. **Default**: Populate `roles` from the former Identity mapping table above, inferred from each profile's `description` where helpful.
2. **mike** and **sam**: Assign **all** `user_roles` values: `admin`, `coordinator`, `customer`, `mentee`, `mentor`.
3. Ensure every `user_roles` enum value appears at least once across the ten profiles.

### `customer_id` assignment rules

Apply `customer_id` on **customer**, **mentee**, and **coordinator** profiles (and any profile that previously had `customer_id`):

| Customer `_id` | Customer `name` | Profiles |
| --- | --- | --- |
| `D00000000000000000000006` | Agile Learning Institute | **mike**, **sam**, **carol** (admin/coordinator sponsorship) |
| `D00000000000000000000002` | Persevere Now | **daniel**, **lucky**, **mary**, **luther** |
| `D00000000000000000000001` | cat | **cat**, **taylor** (family / dual-role mentee sponsorship) |

- **marti** (mentor only): omit `customer_id` unless business rules require it.
- Replace any stale `customer_id` references to removed customers (`D000…03`–`05`).

### Other field rules

- Keep `full_name` unique across all retained profiles (required by new index).
- Preserve `mentor_id` on mentee profiles where already set (daniel, lucky, mary, luther, taylor → marti `A000…06`).
- EJSON: `$oid` for identifiers, `$date` for date-times.

## Goals

- Reduce `Profile.0.1.0.0.json` to exactly **ten** documents listed above.
- Add `roles` to every retained profile per assignment rules.
- Set `customer_id` on customer, mentee, and coordinator profiles per sponsorship table.
- Ensure all retained documents validate against Profile 0.1.0 schema (including `roles`, no forbidden extra properties).

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect top-level **SUCCESS** for Profile (and overall configure once T203 Customer data is present).

MongoDB spot checks:

```javascript
db.Profile.countDocuments({})                                    // 10
db.Profile.countDocuments({ name: { $in: ["jordan","riley","morgan","alex","casey"] } }) // 0
db.Profile.countDocuments({ roles: { $exists: true } })          // 10
db.Profile.countDocuments({ full_name: { $exists: true } })      // 10
```

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Profile.0.1.0.0.json` — ten Profile documents per goals

## Execution Notes

_(Reserved for the task execution agent.)_
