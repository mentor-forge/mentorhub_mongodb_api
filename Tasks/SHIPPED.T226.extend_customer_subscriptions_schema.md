# T226 – Extend Customer with stripe_customer_id and subscriptions[] (F-D22)

**Status:** Shipped  
**Type:** Feature  
**Depends On:** T225  
**Description:** Extend **Customer** dictionary with Stripe customer id and embedded `subscriptions[]` (business + Stripe sync + discount grant fields) per locked E2 shapes. Prefer add over rename. Existing Customer test data must still configure after this task (new fields optional) or be updated here if required.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/dictionaries/`, `configurator/configurations/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/customer_journey_issues.md` — [Product & Subscription data shape (locked)](../mentorhub/Workshops/customer_journey_issues.md); Discount grant fields on `subscriptions[]`
- GitHub: [F-D22 #50](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/50)
- `Tasks/PENDING.T225.add_commerce_enumerators.md` — `subscription_status`
- `configurator/dictionaries/Customer.0.1.0.yaml` — current Customer (no billing fields)
- `configurator/configurations/Customer.yaml` — indexes; consider sparse index on `stripe_customer_id` / `subscriptions.stripe_subscription_id` if useful
- Top-level Subscription collection already dropped (F-D14 / T218) — do **not** recreate it
- **Out of scope:** Setting (Product/Discount variants) / Payment collections; full Customer seed rewrite (T230 may add unsubscribed vs active subscription fixtures); Customer API Checkout (external F-CA06).

### Locked Customer additions

| Field | Notes |
| --- | --- |
| `stripe_customer_id` | Stripe Customer id (word/sentence as appropriate) |
| `subscriptions[]` | array of embedded subscription objects |

**Each `subscriptions[]` element — business fields:**

| Field | Notes |
| --- | --- |
| `mentee_count` | Entitled mentee seats |
| `encounters_mo` | Encounters-per-month entitlement |
| `subscription` | Plan identifier (matches Setting Product.`subscription`) |
| `quantity` | Purchased seat quantity |
| `unit_cost` | Snapshot of Setting Product.`unit_price` at purchase |
| `total_cost` | `quantity × unit_cost` (or Stripe-reconciled) |
| `discount_code` | Redeemed code or `""` |
| `free_encounters_granted` | From Discount at checkout (0 if none) |
| `free_encounters_remaining` | Starts at granted; decremented later by Encounter domain |

**Each element — Stripe sync fields:**

| Field | Notes |
| --- | --- |
| `status` | enum `subscription_status`: `active` \| `past_due` \| `canceled` |
| `stripe_subscription_id` | Stripe Subscription id |
| `stripe_price_id` | Stripe Price id |
| `current_period_end` | period end (date-time) |

Confirm property types against **running configurator** (prefer delete+create of nested object definitions over rename). Pre-release: edit `Customer.0.1.0` in place.

## Goals

- Add `stripe_customer_id` and `subscriptions[]` to `Customer.0.1.0.yaml` per locked shape.
- Update `Customer.yaml` indexes as needed (document choices in Execution Notes).
- Prefer optional new fields so existing Customer documents still validate until T230 seeds richer fixtures.
- Configure-database **SUCCESS** with current Customer test data (or update test data in this task if required — list any Customer test-data files in Outputs).

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- Customer CFG SUCCESS; no top-level Subscription collection reintroduced.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/dictionaries/Customer.0.1.0.yaml` — add `stripe_customer_id`, `subscriptions[]`
- `configurator/configurations/Customer.yaml` — indexes if changed
- Optional: `configurator/test_data/Customer.0.1.0.0.json` — only if schema tightening requires it in this task
- `Tasks/SHIPPED.T226.extend_customer_subscriptions_schema.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

**Plan:** Edit `Customer.0.1.0.yaml` in place; all new fields `required: false` so existing Customer seeds keep validating. Types: Stripe ids as `sentence` (same pattern as `ExternalEvent.external_id`); plan `subscription` as `word`; money amounts as `count` (integer cents, matching ExternalEvent test `amount_total: 9900`); `status` → enum `subscription_status` from T225. Add sparse unique indexes on `stripe_customer_id` and `subscriptions.stripe_subscription_id` (configurator supports `sparse` + `unique` together, as used for Notification scope indexes). Do not change Customer test data unless configure fails. Skip packaging (`make down` / container / `mh up`) — orchestrator owns :8385 / Mongo :27018.

**Property types (Customer.0.1.0):**

| Field | Type |
| --- | --- |
| `stripe_customer_id` | sentence (optional) |
| `subscriptions[]` | array of object (optional); nested fields all optional |
| `mentee_count`, `encounters_mo`, `quantity`, `unit_cost`, `total_cost`, `free_encounters_granted`, `free_encounters_remaining` | count |
| `subscription` | word |
| `discount_code` | sentence (empty string allowed) |
| `status` | enum `subscription_status` |
| `stripe_subscription_id`, `stripe_price_id` | sentence |
| `current_period_end` | date-time |

**Indexes (`Customer.yaml`):**

| Name | Key | Options | Rationale |
| --- | --- | --- | --- |
| Name Index | `name: 1` | unique | unchanged |
| Last Saved | `saved.at_time: -1` | — | unchanged |
| Stripe Customer Id | `stripe_customer_id: 1` | unique + sparse | one Stripe Customer per org; sparse so docs without billing id do not collide |
| Stripe Subscription Id | `subscriptions.stripe_subscription_id: 1` | unique + sparse | multikey uniqueness for Stripe sub ids; sparse for empty/`subscriptions` absent |

Configurator accepted both sparse unique indexes (PRO-04 SUCCESS). No need for application-enforced uniqueness for these keys.

**Test data:** No change to `Customer.0.1.0.0.json` (optional fields only).

**Testing results**

- `DELETE /api/database/` → HTTP 200, `status: SUCCESS` (localhost:8385).
- `POST /api/configurations/` → HTTP 200, top-level `status: SUCCESS`; `CFG-05-Customer.yaml` SUCCESS; indexes `PRO-04-Name Index`, `PRO-04-Last Saved`, `PRO-04-Stripe Customer Id`, `PRO-04-Stripe Subscription Id` SUCCESS.
- Packaging verification skipped (orchestrator owns stack).
