# T247 – Confirm Discount Setting seeds and subscription grant coordination (F-D28)

**Status:** Shipped  
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

### Plan (append unlimited code only)

**Decision: append one Setting Discount; do not edit Customer.**

Confirm inventory (T246 + current JSON):

| `_id` | `code` | `status` | `free_encounters` | `max_redemptions` | Role |
| --- | --- | --- | --- | --- | --- |
| `f000…01` | `TRIAL2WK` | active | 4 | 1000 | retail trial; persevere uses this |
| `f000…02` | `OLDPROMO` | inactive | 10 | 50 | past `expires_at` |
| `f000…03` | `PARTNER100` | active | 100 | 100 | partner high grant |

All three **set** `max_redemptions`. Locked “omit = unlimited” example is missing. `f00000000000000000000004` is unused. No `test_data/Discount*` files.

Customer grants already aligned:

- persevere: `discount_code: TRIAL2WK`, granted 4 / remaining 3 (matches Setting `free_encounters: 4`)
- supersoft (and other subscribed orgs): `discount_code: ""`, grant 0

**Changes:**

1. Append Setting Discount `OPENHOUSE` on `f00000000000000000000004`: `status: active`, modest `free_encounters: 2`, **omit** `max_redemptions` and `expires_at`. Preserve existing Product Settings and Discount `_id`s.
2. Do **not** edit `Customer.0.1.0.0.json` (grants in sync; do not apply OPENHOUSE; do not rewrite T241/T244 billing statuses).
3. Do **not** create `test_data/Discount*`.

Testing: reuse already-running configurator `http://localhost:8385` (Mongo `:27017`). DELETE then POST `/api/configurations/`. Skip packaging. Spot-check Discount count ≥3 (expect 4), statuses include active + inactive, ≥1 Customer with `TRIAL2WK`. Grep `configurator/` for `test_data/Discount` — expect none.

### Confirm-vs-edit

**append** — T230 coverage (trial / inactive-expired / partner) already present and Customer grants already aligned. Added only the locked unlimited example (`OPENHOUSE` omit `max_redemptions`). No Customer JSON change.

### Files changed

- `configurator/test_data/Setting.0.1.0.0.json` — appended `OPENHOUSE` on `f00000000000000000000004` (`active`, `free_encounters: 2`, omit `max_redemptions` / `expires_at`)
- `Tasks/PENDING.T247.confirm_discount_test_data.md` — Execution Notes + in-file Status Running. Filename left `PENDING.` for orchestrator.

Not changed: `Customer.0.1.0.0.json` (persevere `TRIAL2WK` granted 4 / remaining 3; supersoft empty grant). No `test_data/Discount*` created.

### Test results (packaging skipped)

Reused running configurator on `:8385` (Mongo `:27017`); did not `make down` / `make container`.

| Check | Result |
| --- | --- |
| `DELETE /api/database/` | HTTP **200**, top-level `status: SUCCESS` (`DROP_DATABASE`) |
| `POST /api/configurations/` | HTTP **200**, top-level `status: SUCCESS` (`CFG-07-PROCESS_ALL`); `Setting.yaml` `PROCESS_VERSION-0.1.0.0` SUCCESS — **6** Setting docs loaded (`e000…01`–`02` Product + `f000…01`–`04` Discount, including `OPENHOUSE`) |
| `db.Setting.find({ type: "Discount" }).count()` | **4** (≥3) |
| `db.Setting.distinct("status", { type: "Discount" })` | `active`, `inactive` |
| `db.Customer.find({ "subscriptions.discount_code": "TRIAL2WK" }).count()` | **1** (persevere, granted 4 / remaining 3) |
| OPENHOUSE loaded | `f000…04`, `status: active`, `free_encounters: 2`, **no** `max_redemptions` |
| Grep `configurator/` for `test_data/Discount` | none |
| `find configurator` for `Discount*` | none |

**Orchestrator confirmation:** `DELETE`/`POST` on `:8385` re-ran SUCCESS (Setting + Customer CFG). Spot-check: Discount 4; statuses active+inactive; TRIAL2WK Customer 1; OPENHOUSE active omit max_redemptions; no `test_data/Discount`.
