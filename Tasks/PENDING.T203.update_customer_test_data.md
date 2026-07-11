# T203 – Update Customer Test Data

**Status**: Pending  
**Type**: Feature  
**Depends On**: T202  
**Description**: Rebuild Customer seed data for the sponsorship model — add Agile Learning Institute, rename morgan to Persevere Now, remove `mentees[]`, and drop obsolete customer records.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`, `configurator/dictionaries/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `configurator/dictionaries/Customer.0.1.0.yaml` — `mentees` removed in T202
- `configurator/test_data/Customer.0.1.0.0.json` — five records today (`cat`, `morgan`, `greenfield-dev`, `acme-startup`, `legacy-corp`)
- `Tasks/PENDING.T204.update_profile_test_data.md` — consumes these Customer `_id` values for Profile `customer_id`

### Target Customer records (3 documents)

| `_id` | `name` | `description` | Notes |
| --- | --- | --- | --- |
| `D00000000000000000000001` | `cat` | Cat Customer sponsoring mentorship for a family member learning to code. | **Keep** existing record; remove `mentees[]` |
| `D00000000000000000000002` | `Persevere Now` | Persevere Now - sponsoring mentorship for just involved graduates of their programs. | **Replace** former `morgan` record (same `_id`) |
| `D00000000000000000000006` | `Agile Learning Institute` | Agile Learning Institute — platform operator sponsoring admin and coordinator users. | **New** record |

### Records to remove

- `D00000000000000000000003` (`greenfield-dev`)
- `D00000000000000000000004` (`acme-startup`)
- `D00000000000000000000005` (`legacy-corp`)

These existed only to back `mentees[]` entries for pruned profiles.

### EJSON conventions

- `$oid` for `_id`; `$date` for breadcrumb `at_time` fields.
- Preserve realistic `created` / `saved` breadcrumbs consistent with existing seed style.

## Goals

- Reduce `Customer.0.1.0.0.json` to **three** documents per the table above.
- Remove `mentees` from every Customer document.
- Add **Agile Learning Institute** with `_id` `D00000000000000000000006`.
- Update the `morgan` slot (`D00000000000000000000002`) to **Persevere Now** with the new description.
- Keep `cat` (`D00000000000000000000001`) with updated content only as needed (no `mentees`).

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Customer configure step returns **SUCCESS**.
- Full configure may still fail on Profile until T204 ships — document if so.

MongoDB spot check after full pipeline:

```javascript
db.Customer.countDocuments({})                              // 3
db.Customer.countDocuments({ mentees: { $exists: true } }) // 0
```

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Customer.0.1.0.0.json` — three Customer documents per goals

## Execution Notes

_(Reserved for the task execution agent.)_
