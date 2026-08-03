# T230 – Seed Setting (Product/Discount) and Customer subscription fixtures (F-D22)

**Status:** Shipped  
**Type:** Feature  
**Depends On:** T226, T227, T229  
**Description:** Seed **Setting** documents (`type: Product` and `type: Discount`), plus Customer fixtures covering **unsubscribed** and **active** (with `subscriptions[]`) orgs for E2 Checkout. Optional minimal Payment samples. Align `_id`s with persona Customer map.

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
- `Tasks/PENDING.T227.add_setting_collection.md` — Setting polymorphic schema + `_id` prefixes
- `Tasks/PENDING.T229.add_payment_collection.md` — Payment schema + `_id` prefix
- `Tasks/scripts/persona_ids.json` — Customer ObjectIds (`mary`, `persevere`, `ali`, `supersoft`, `scamsoft`)
- `configurator/test_data/Customer.0.1.0.0.json` — extend in place (pre-release)
- **Out of scope:** E5–E7 past_due/canceled dense fixtures (later F-D tickets); Admin SPA Setting UI; Customer API Checkout.

### Seed expectations (minimum)

**Setting / Product** (`type: Product`) — at least two catalog rows (e.g. starter vs growth) with distinct `subscription`, `minimum_members`, `unit_price`, `stripe_price_id` (test/placeholder Stripe price ids OK for local).

**Setting / Discount** (`type: Discount`) — at least:
- one `active` retail/trial-style code with modest `free_encounters`
- one `inactive` or expired code for negative-path demos
- optional partner high-grant code

**Customers** — using existing persona `_id`s:
- **Unsubscribed:** empty `subscriptions[]` (and optional empty/`null` `stripe_customer_id`) — e.g. prospect org
- **Active:** at least one Customer with `stripe_customer_id` and one `subscriptions[]` entry (`status: active`, business + sync + discount fields populated)
- Prefer not destroying persona display names; only add billing fields

**Payments** — optional 1–2 documents tied to an active Customer / Product Setting for consumer demos; otherwise leave `[]` and note follow-on F-D26.

## Goals

- Populate `Setting.0.1.0.0.json` with Product and Discount variant documents.
- Update `Customer.0.1.0.0.json` with unsubscribed + active subscription examples.
- Optionally seed `Payment.0.1.0.0.json`.
- Do **not** create Product.* or Discount.* test_data files.
- Configure-database **SUCCESS**.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- Spot-check Setting counts by `type`; Customer docs with and without `subscriptions[]`.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Setting.0.1.0.0.json` — Product + Discount Setting seeds
- `configurator/test_data/Customer.0.1.0.0.json` — billing / subscriptions fixtures
- Optional: `configurator/test_data/Payment.0.1.0.0.json` — minimal payment samples
- `Tasks/PENDING.T230.seed_commerce_catalog_and_customer_subscriptions.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

**Plan:** Seed Product/Discount Settings, Customer billing fields (unsubscribed + active), and 1–2 Payments. Use **valid 24-hex ObjectIds only** (letters outside `a-f` are invalid). Verified against orchestrator configurator on `:8385` (Mongo `:27018`) then packaged via `make container` / `mh up mongodb`.

**ObjectId prefix mapping** (T227/T229 placeholders `P0…` / `K0…` / `Y0…` are **not** valid hex — `P`, `K`, `Y` are outside `0-9a-f`):

| Kind | Invalid placeholder | Valid prefix used |
| --- | --- | --- |
| Product Setting | `P0…` | `e0000000000000000000000N` |
| Discount Setting | `K0…` | `f0000000000000000000000N` |
| Payment | `Y0…` | `b0000000000000000000000N` |

**Seed inventory**

**Setting / Product (2)**

| `_id` | name | subscription | minimum_members | unit_price | stripe_price_id | status |
| --- | --- | --- | --- | --- | --- | --- |
| `e00000000000000000000001` | Starter | `starter` | 1 | 4900 | `price_test_starter` | active |
| `e00000000000000000000002` | Growth | `growth` | 5 | 9900 | `price_test_growth` | active |

**Setting / Discount (3)**

| `_id` | code | free_encounters | status | notes |
| --- | --- | --- | --- | --- |
| `f00000000000000000000001` | `TRIAL2WK` | 4 | active | retail trial |
| `f00000000000000000000002` | `OLDPROMO` | 10 | inactive | `expires_at` 2025-01-01 (past) |
| `f00000000000000000000003` | `PARTNER100` | 100 | active | partner high-grant |

**Customers** (persona `_id`s unchanged)

| Persona | `_id` | Billing | Notes |
| --- | --- | --- | --- |
| mary | `D…01` | **unsubscribed** | `subscriptions: []`; no `stripe_customer_id` |
| persevere | `D…02` | **active** | `cus_test_persevere`; growth qty 5; `TRIAL2WK`; total_cost 49500 |
| ali | `D…06` | **unsubscribed** | platform operator; `subscriptions: []` |
| supersoft | `D…07` | **active** | `cus_test_supersoft`; starter qty 2; no discount |
| scamsoft | `D…08` | **unsubscribed** | empty `subscriptions[]` (past_due dense fixtures deferred) |

**Payments (2)**

| `_id` | customer | product_id | amount | stripe_payment_intent_id | status |
| --- | --- | --- | --- | --- | --- |
| `b00000000000000000000001` | persevere (`D…02`) | growth (`e…02`) | 49500 | `pi_test_persevere_growth_01` | succeeded |
| `b00000000000000000000002` | supersoft (`D…07`) | starter (`e…01`) | 9800 | `pi_test_supersoft_starter_01` | succeeded |

**Changes**

- Replaced `Setting.0.1.0.0.json` `[]` with 2 Product + 3 Discount documents.
- Extended `Customer.0.1.0.0.json` in place with billing fields only (personas preserved).
- Seeded `Payment.0.1.0.0.json` with 2 succeeded payments tied to active customers.

**Testing results**

- Orchestrator `:8385`: `DELETE /api/database/` → HTTP 200 SUCCESS; `POST /api/configurations/` → HTTP 200, top-level `status: SUCCESS`; `CFG-05-Setting.yaml` SUCCESS (5 docs); `CFG-05-Customer.yaml` SUCCESS (5 docs); `CFG-05-Payment.yaml` SUCCESS (2 docs); zero FAILURE events.
- Packaging: `make down && make container && mh up mongodb` OK. Packaged API `:8383` `GET /api/configurations/` lists `Setting.yaml` + `Payment.yaml` (no `Product.yaml` / `Discount.yaml`). `DELETE /api/database/` → HTTP 403 (expected non-Local BUILT_AT).
