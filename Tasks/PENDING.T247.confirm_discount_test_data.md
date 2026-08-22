# T247 – Confirm Discount Setting seeds and subscription grant coordination (F-D28)

**Status:** Pending  
**Type:** Feature  
**Depends On:** T246  
**Description:** Confirm F-D22 Discount **test data** covers active/inactive, trial, and partner codes, and that **Customer.subscriptions[]** grant fields match a real Setting `code`. Append **only** if a locked example is missing (e.g. unlimited `max_redemptions`). Do **not** create Discount test_data files. Prefer append over rewrite.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/customer_journey_issues.md` — E2 Discount seeds; `discount_code` / `free_encounters_*` on `subscriptions[]`
- GitHub: [F-D28 #54](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/54)
- `Tasks/SHIPPED.T230.seed_commerce_catalog_and_customer_subscriptions.md` — expected Discount seeds + persevere `TRIAL2WK`
- `Tasks/PENDING.T246.confirm_discount_setting_shape.md` — schema confirm
- `configurator/test_data/Setting.0.1.0.0.json` — T230: `TRIAL2WK` active trial, `OLDPROMO` inactive+expired, `PARTNER100` active partner (`f000…01`–`03`)
- `configurator/test_data/Customer.0.1.0.0.json` — persevere `discount_code: TRIAL2WK`, granted 4 / remaining 3; supersoft empty grant
- Unique Setting index `type` + `code` — new codes must not collide
- **Out of scope:** Product Setting rows unless a Discount edit accidentally requires it; Payment; Notification; `past_due` / `canceled`; Stripe coupons; Discount Mongo collection; rewriting T241/T244 Customer billing statuses

### Expected coverage (already seeded — confirm)

| `code` | `status` | Role |
| --- | --- | --- |
| `TRIAL2WK` | `active` | retail trial; modest `free_encounters` (4); persevere `subscriptions[]` uses this code |
| `OLDPROMO` | `inactive` | expired (`expires_at` in the past) negative path |
| `PARTNER100` | `active` | partner high grant (100) |

**Customer coordination:** at least one active `subscriptions[]` with `discount_code` equal to an active Setting Discount `code` and `free_encounters_granted` equal to that code’s `free_encounters`; at least one with `discount_code: ""` and grant 0. **Do not** retarget persevere/supersoft discount fields unless they no longer match Setting (then fix Customer grant fields only — list Customer JSON in Outputs if you must).

### Gap to fill if missing

Locked shape: omit `max_redemptions` = unlimited. T230 codes all set a cap. If no unlimited active code exists, **append** one Setting Discount (e.g. `code: OPENHOUSE`, `status: active`, **omit** `max_redemptions`, modest `free_encounters`, unused `f00000000000000000000004` if free). Do not apply it to a Customer unless needed for coordination.

Preserve existing Product Settings and Discount `_id`s.

## Goals

- Setting test data includes active trial, inactive/expired, and partner examples.
- `Customer.subscriptions[]` discount fields stay aligned with Setting `code` / `free_encounters`.
- No `test_data/Discount*` files.
- Configure-database **SUCCESS**. If T230 already satisfies coverage and you add unlimited-or-nothing, document in Execution Notes.

## Testing Expectations

```sh
make dev
# If host port 27017 is busy, use compose ports !override (e.g. host 27018) as in prior F-D tasks.
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- Spot-check:

```javascript
db.Setting.find({ type: "Discount" }).count()  // ≥3
db.Setting.distinct("status", { type: "Discount" })  // includes active and inactive
db.Customer.find({ "subscriptions.discount_code": "TRIAL2WK" }).count()  // ≥1
```

- Grep `configurator/` for `test_data/Discount` — expect none.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Setting.0.1.0.0.json` — append only if a coverage gap (unlimited code) remains
- Optional: `configurator/test_data/Customer.0.1.0.0.json` — **only** if grant fields are out of sync with Setting codes
- `Tasks/PENDING.T247.confirm_discount_test_data.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

_(Reserved for the task execution agent.)_
