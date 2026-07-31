# T228 – Add Discount collection (F-D22)

**Status:** Pending  
**Type:** Feature  
**Depends On:** T225  
**Description:** Create **Discount** Configuration, Dictionary, and empty/minimal test data for MentorHub free-encounter discount codes (not Stripe Coupons). Prefer create over rename.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/configurations/`, `configurator/dictionaries/`, `configurator/test_data/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/customer_journey_issues.md` — [Discount codes & free encounters (locked)](../mentorhub/Workshops/customer_journey_issues.md)
- GitHub: [F-D22 #50](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/50)
- `Tasks/PENDING.T225.add_commerce_enumerators.md` — `discount_status`
- **Out of scope:** Redemption counter increment logic (F-CA06); Product / Payment / Customer seeds (T227/T229/T230).

### Locked Discount fields

| Field | Notes |
| --- | --- |
| Standard metadata | `_id`, `name` (optional ops label), `created`, `saved` as needed — prefer delete+create; do not invent Stripe coupon fields |
| `code` | unique string (API normalizes trim + uppercase on lookup) |
| `free_encounters` | integer ≥ 0 |
| `status` | enum `discount_status`: `active` \| `inactive` |
| `description` | ops label |
| `expires_at` | optional date-time |
| `max_redemptions` | optional integer (null/omit = unlimited) |
| Optional | `redemption_count` integer if stored on document (F-CA06 may own increments) — include only if needed for seed realism; document choice |

Indexes: unique on `code`.  
**Stable `_id` prefix for seeds (T230):** e.g. `DC…` or `K0…` — record in Execution Notes (valid hex ObjectId prefix).

## Goals

- Create `configurator/dictionaries/Discount.0.1.0.yaml`.
- Create `configurator/configurations/Discount.yaml` version `0.1.0.0`.
- Create `configurator/test_data/Discount.0.1.0.0.json` as `[]` until T230.
- Confirm configure **SUCCESS**.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- Configurations list includes `Discount.yaml`.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/dictionaries/Discount.0.1.0.yaml` — **create**
- `configurator/configurations/Discount.yaml` — **create**
- `configurator/test_data/Discount.0.1.0.0.json` — **create** (`[]` acceptable)
- `Tasks/PENDING.T228.add_discount_collection.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

*(Reserved for the execution agent.)*
