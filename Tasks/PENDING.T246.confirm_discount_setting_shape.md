# T246 – Confirm Discount locked shape on Setting (not a Discount collection) (F-D28)

**Status:** Pending  
**Type:** Feature  
**Depends On:** none  
**Description:** Confirm the locked **Discount** dictionary is the **Setting** variant `type: Discount` from F-D22. Do **not** create `Discount.yaml` / a Discount Mongo collection. Add a field to the Setting Discount variant **only** if running configurator shows a locked-shape gap. Coordinate with existing `Customer.subscriptions[]` discount grant fields (do not rename them).

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/dictionaries/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/customer_journey_issues.md` — [Discount codes & free encounters (locked)](../mentorhub/Workshops/customer_journey_issues.md); not Stripe coupons
- GitHub: [F-D28 #54](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/54); F-D22 already shipped [F-D22 #50](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/50)
- `Tasks/SHIPPED.T227.add_setting_collection.md` — Setting `one_of` Product \| Discount
- `Tasks/SHIPPED.T225.add_commerce_enumerators.md` — `discount_status`: `active` \| `inactive`
- `Tasks/SHIPPED.T226.extend_customer_subscriptions_schema.md` — `discount_code`, `free_encounters_granted`, `free_encounters_remaining`
- `configurator/dictionaries/Setting.0.1.0.yaml` — Discount variant (expected present)
- `configurator/configurations/Setting.yaml` — unique sparse `type` + `code`
- **Out of scope:** Separate Discount collection; Stripe Coupon/Promotion codes; Customer API checkout validation (F-CA06); Admin SPA CRUD (`ISSUE.mentorhub_admin_spa.products_catalog_crud.md`); test-data edits (T247); GDPR; Dashboard

### Locked Discount fields (must exist on Setting Discount variant)

| Field | Role |
| --- | --- |
| `code` | unique redeemable code (API trim + uppercase) |
| `free_encounters` | integer ≥ 0 granted at checkout |
| `status` | `discount_status` `active` \| `inactive` |
| `description` | ops label; not shown on Stripe Checkout |
| `expires_at` | optional; reject if now > expiry |
| `max_redemptions` | optional; omit = unlimited |

**Do not add** `gdpr_*`. **Do not** store Stripe coupon ids. Optional `redemption_count` was considered in T227 — **do not add** unless configure/API cannot derive usage from `Customer.subscriptions[].discount_code` (default: derive, per Setting dictionary comments).

**Customer coordination (confirm names only — do not change in this task):**

| Customer.subscriptions[] | Discount |
| --- | --- |
| `discount_code` | copy of Setting Discount.`code` or `""` |
| `free_encounters_granted` | copy of `free_encounters` at checkout (0 if none) |
| `free_encounters_remaining` | starts at granted |

## Goals

- Locked Discount fields live on **Setting** `type: Discount`.
- No `configurations/Discount.yaml`, `dictionaries/Discount*`, or `test_data/Discount*`.
- Configure-database **SUCCESS**. If every field is already present, ship with Execution Notes only (no dictionary diff).

## Testing Expectations

```sh
make dev
# If host port 27017 is busy, use compose ports !override (e.g. host 27018) as in prior F-D tasks.
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- `GET /api/configurations/` lists `Setting.yaml`; does **not** list `Discount.yaml` or `Product.yaml`.
- Grep Setting Discount variant for `code`, `free_encounters`, `status`, `description`, `expires_at`, `max_redemptions`.
- Grep `configurator/` for `Discount.yaml` — expect none.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/dictionaries/Setting.0.1.0.yaml` — **only if** a locked field is missing
- `Tasks/PENDING.T246.confirm_discount_setting_shape.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

_(Reserved for the task execution agent. Record confirm-vs-edit.)_
