# T230 – Seed Products, Discounts, and Customer subscription fixtures (F-D22)

**Status:** Pending  
**Type:** Feature  
**Depends On:** T226, T227, T228, T229  
**Description:** Seed Product catalog, Discount codes, and Customer fixtures covering **unsubscribed** and **active** (with `subscriptions[]`) orgs for E2 Checkout. Optional minimal Payment samples. Align `_id`s with persona Customer map.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/customer_journey_issues.md` — E2 locked shapes; Checkout contract
- GitHub: [F-D22 #50](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/50)
- `Tasks/PENDING.T226.extend_customer_subscriptions_schema.md` — Customer billing fields
- `Tasks/PENDING.T227.add_product_collection.md` — Product schema + `_id` prefix
- `Tasks/PENDING.T228.add_discount_collection.md` — Discount schema + `_id` prefix
- `Tasks/PENDING.T229.add_payment_collection.md` — Payment schema + `_id` prefix
- `Tasks/scripts/persona_ids.json` — Customer ObjectIds (`mary`, `persevere`, `ali`, `supersoft`, `scamsoft`)
- `configurator/test_data/Customer.0.1.0.0.json` — extend in place (pre-release)
- **Out of scope:** E5–E7 past_due/canceled dense fixtures (later F-D tickets); Admin SPA Product UI; Customer API Checkout.

### Seed expectations (minimum)

**Products** — at least two catalog rows (e.g. starter vs growth) with distinct `subscription`, `minimum_members`, `unit_price`, `stripe_price_id` (test/placeholder Stripe price ids OK for local).

**Discounts** — at least:
- one `active` retail/trial-style code with modest `free_encounters`
- one `inactive` or expired code for negative-path demos
- optional partner high-grant code

**Customers** — using existing persona `_id`s:
- **Unsubscribed:** empty `subscriptions[]` (and optional empty/`null` `stripe_customer_id`) — e.g. prospect org
- **Active:** at least one Customer with `stripe_customer_id` and one `subscriptions[]` entry (`status: active`, business + sync + discount fields populated)
- Prefer not destroying persona display names; only add billing fields

**Payments** — optional 1–2 documents tied to an active Customer / Product for consumer demos; otherwise leave `[]` and note follow-on F-D26.

## Goals

- Populate `Product.0.1.0.0.json` and `Discount.0.1.0.0.json`.
- Update `Customer.0.1.0.0.json` with unsubscribed + active subscription examples.
- Optionally seed `Payment.0.1.0.0.json`.
- Configure-database **SUCCESS** with all collections.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- Spot-check Product/Discount counts; Customer docs with and without `subscriptions[]`.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Product.0.1.0.0.json` — catalog seeds
- `configurator/test_data/Discount.0.1.0.0.json` — discount seeds
- `configurator/test_data/Customer.0.1.0.0.json` — billing / subscriptions fixtures
- Optional: `configurator/test_data/Payment.0.1.0.0.json` — minimal payment samples
- `Tasks/PENDING.T230.seed_commerce_catalog_and_customer_subscriptions.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

*(Reserved for the execution agent.)*
