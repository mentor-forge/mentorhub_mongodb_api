# T210 – Update Customer Test Data for Personas

**Status**: Pending  
**Type**: Feature  
**Depends On**: T209  
**Description**: Rebuild Customer seed data for four sponsorship organizations aligned with the persona matrix (Mary, Persevere, ALI, SuperSoft).

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/Customer.0.1.0.0.json`, `configurator/dictionaries/Customer.0.1.0.yaml`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `Tasks/PENDING.T209.audit_persona_test_data.md` — **Execution Notes** persona migration plan (source of truth for `_id` values)
- `Tasks/SHIPPED.T203.update_customer_test_data.md` — prior three-customer migration

### Target Customer records (4 documents)

Apply `_id` values from T209 audit. Proposed defaults (adjust if audit reassigns):

| `_id` | `name` slug | Display / description |
| --- | --- | --- |
| `D00000000000000000000001` | `mary` | Mary Anderson — self-funded apprenticeship sponsorship |
| `D00000000000000000000002` | `persevere` | Persevere Now — graduate mentorship programs |
| `D00000000000000000000006` | `ali` | Agile Learning Institute — platform operator |
| `D00000000000000000000007` | `supersoft` | SuperSoft — startup engineering mentorship (**new** `_id`) |

### Migration rules

- **Replace** former `cat` record (`D000…01`) with **Mary** customer (same or new `_id` per T209).
- **Keep** Persevere slot (`D000…02`); update slug to `persevere` and refresh description/breadcrumbs.
- **Keep** ALI (`D000…06`); update slug to `ali` if needed for consistency.
- **Add** SuperSoft (`D000…07` or audit-assigned `_id`).
- **Remove** any obsolete customer records not in the target four.
- No `mentees[]` property (removed in T202).

## Goals

- `Customer.0.1.0.0.json` contains exactly **four** documents matching the persona customer model.
- Every target customer has realistic `created` / `saved` breadcrumbs.
- Customer configure step returns **SUCCESS** (Profile configure may fail until T211 ships — document if so).

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

MongoDB spot check:

```javascript
db.Customer.countDocuments({})  // 4
db.Customer.distinct("name")    // mary, persevere, ali, supersoft (or audit-final slugs)
```

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Customer.0.1.0.0.json`

## Execution Notes

_(Reserved for task execution agent.)_
