# T246 – Confirm Discount locked shape on Setting (not a Discount collection) (F-D28)

**Status:** Shipped  
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

### Plan (confirm-vs-edit)

**Decision: confirm (no dictionary edit).** After reading `configurator/dictionaries/Setting.0.1.0.yaml` Discount variant and locked F-D28 / workshop fields, every locked field is already present. No `Setting.0.1.0.yaml` diff.

Locked-field inventory (Setting `type: Discount`):

| Locked field | Present | Notes |
| --- | --- | --- |
| `code` | yes | `word`; API trim + uppercase documented |
| `free_encounters` | yes | `count` |
| `status` | yes | `enums: discount_status` |
| `description` | yes | ops label; not Stripe Checkout |
| `expires_at` | yes | optional `date-time` |
| `max_redemptions` | yes | optional `count`; omit = unlimited |

Not added (by design): `gdpr_*`, Stripe coupon ids, `redemption_count`. Dictionary comments already say usage is derived from `Customer.subscriptions[].discount_code` (or Admin ingress), so configure/API can derive without a stored counter.

Customer coordination (names only, unchanged): `discount_code`, `free_encounters_granted`, `free_encounters_remaining` on `Customer.subscriptions[]`.

No `Discount.yaml` / `Discount*` dictionary or test-data files exist under `configurator/`. `Setting.yaml` already has unique sparse `type` + `code`.

Testing: reuse already-running configurator `http://localhost:8385` (Mongo `:27017`). Skip packaging.

### Confirm-vs-edit

**confirm** — no `Setting.0.1.0.yaml` (or any dictionary) change. Locked Discount shape already lives on Setting `type: Discount` from F-D22 / T227.

### Files changed

- `Tasks/PENDING.T246.confirm_discount_setting_shape.md` only (Execution Notes + in-file Status Running). Filename left `PENDING.` for orchestrator.

### Test results (packaging skipped)

Reused running configurator on `:8385` (Mongo `:27017`); did not `make down` / `make container`.

| Check | Result |
| --- | --- |
| `DELETE /api/database/` | HTTP **200**, top-level `status: SUCCESS` (`DROP_DATABASE`) |
| `POST /api/configurations/` | HTTP **200**, top-level `status: SUCCESS` (`CFG-07-PROCESS_ALL`); `Setting.yaml` `PROCESS_VERSION-0.1.0.0` SUCCESS (indexes Type Subscription / Type Code / Type Stripe Price Id / Created; 5 Setting docs loaded) |
| `GET /api/configurations/` | HTTP **200**; lists `Setting.yaml`; does **not** list `Discount.yaml` or `Product.yaml` |
| Grep Setting Discount variant | `code`, `free_encounters`, `status` (`discount_status`), `description`, `expires_at`, `max_redemptions` all present |
| Grep `configurator/` for `Discount.yaml` | none |
| `find configurator` for `Discount*` / `Product.yaml` | none |

Customer coordination names (read-only): `Customer.subscriptions[]` already has `discount_code`, `free_encounters_granted`, `free_encounters_remaining`.

### Notes for T247

- Schema is confirmed; T247 should only touch `Setting.0.1.0.0.json` (append) and optionally Customer JSON if grants drift — never create `test_data/Discount*`.
- Current Discount seeds (`f000…01`–`03`): `TRIAL2WK` (active, 4 encounters, `max_redemptions: 1000`), `OLDPROMO` (inactive + past `expires_at`, cap 50), `PARTNER100` (active, 100, cap 100). All three **set** `max_redemptions`; locked “omit = unlimited” example is still missing — T247’s planned append (`OPENHOUSE` on unused `f00000000000000000000004`, omit `max_redemptions`) is the expected gap fill.
- Do **not** add `redemption_count` on Setting; derive usage from `Customer.subscriptions[].discount_code`.
- Unique sparse Setting index is `type` + `code`; new seed codes must not collide.
- Configure already SUCCESS with current 5 Setting docs (2 Product + 3 Discount); after any append, re-run DELETE+POST on `:8385`.

**Orchestrator confirmation:** `DELETE`/`POST` on `:8385` re-ran SUCCESS (`CFG-05-Setting.yaml`). `GET /api/configurations/` lists `Setting.yaml`, not `Discount.yaml` or `Product.yaml`. Confirm-only (no dictionary diff).
