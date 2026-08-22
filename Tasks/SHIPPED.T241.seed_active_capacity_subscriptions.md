# T241 – Seed active capacity-changed Customer.subscriptions[] (F-D25)

**Status:** Shipped  
**Type:** Feature  
**Depends On:** T236  
**Description:** Update **Customer.subscriptions[]** so E5 has **varied seat quantities**, all **`status: active`**. Represent a mid-lifecycle **capacity increase** on an existing paid org (quantity / `mentee_count` / `total_cost` in sync). Do **not** set `past_due` or `canceled` (F-D26 / F-D27). Pre-release: edit `Customer.0.1.0.0.json` in place.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/customer_journey_issues.md` — E5: capacity via Checkout and/or Portal; webhooks sync `subscriptions[]`
- GitHub: [F-D25 #57](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/57)
- Prerequisites (already on `main`): F-D22 Customer billing fields + catalog (`Tasks/SHIPPED.T226`, `T230`); F-D29 `subscription_changed` (`Tasks/SHIPPED.T220`)
- `Tasks/PENDING.T236.seed_customer_org_roster_profiles.md` — may add **harbor** (starter qty 1) and `subscriptions: []` on northstar; wait so Customer JSON does not collide
- `configurator/test_data/Customer.0.1.0.0.json` — today: persevere growth **qty 5** active; supersoft starter **qty 2** active; others unsubscribed / provisioned
- `configurator/test_data/Payment.0.1.0.0.json` — T230 checkout + T234 renewal: persevere qty **5** / supersoft qty **2**. Keep those Payment rows; T242 adds the capacity Payment.
- `configurator/dictionaries/Customer.0.1.0.yaml` — confirm-only; do not add fields
- **Out of scope:** Payment / ExternalEvent / Event (T242); Profile; Notification (E6/E7); Setting catalog; `past_due` / `canceled`; GDPR; Dashboard; Invite collection

### Locked E5 vs E6 / E7

| Experience | This task |
| --- | --- |
| E5 capacity / mid-lifecycle | **Yes** — `subscriptions[].status` stays **`active`**; vary `quantity` |
| E6 renewal / past_due | **No** — do not flip supersoft (T234 failed invoice) to `past_due` |
| E7 cancel | **No** — F-D27 |

### Target active quantity mix (after this task)

Leave **supersoft** at starter qty **2** so T234 failed Payment still matches. Use **persevere** for the capacity change (T234 paid renewal was qty 5; E5 is a later increase).

| Customer | Plan | `quantity` / `mentee_count` | `status` | Notes |
| --- | --- | --- | --- | --- |
| persevere `D…02` | growth | **8** (was 5) | **active** | Mid-lifecycle seat increase; `unit_cost` 9900; `total_cost` **79200** (8 × 9900); keep `stripe_subscription_id` / `stripe_price_id` / discount fields; bump `saved` |
| supersoft `D…07` | starter | **2** | **active** | Unchanged (small active) |
| harbor `D…11` (if T236 shipped) | starter | **1** | **active** | Unchanged small-capacity org |
| mary, ali, northstar, scamsoft, Path A stub | — | empty `[]` | n/a | Do **not** subscribe them here |

If T236 did not add harbor, the mix is still valid (persevere 8 vs supersoft 2). Do not invent a new Customer unless Execution Notes need a third active quantity and harbor is absent.

Preserve persona `_id`s, names, and unsubscribed orgs.

## Goals

- At least two **active** `subscriptions[]` with **different `quantity`** values; at least one differs from its original T230 Checkout quantity (persevere 5 → 8).
- No `past_due` or `canceled` on `subscriptions[].status`.
- Configure-database Customer step **SUCCESS**. No dictionary changes unless running configurator proves a gap (stop and document).

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
db.Customer.findOne({ name: "persevere" }).subscriptions[0]
// quantity 8, mentee_count 8, total_cost 79200, status "active"
db.Customer.findOne({ name: "supersoft" }).subscriptions[0].quantity  // 2
db.Customer.find({ "subscriptions.status": { $in: ["past_due", "canceled"] } }).count()  // 0
```

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Customer.0.1.0.0.json` — persevere capacity increase only (plus preserve T236 harbor/northstar if present)
- `Tasks/PENDING.T241.seed_active_capacity_subscriptions.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

**Plan:** Edit `Customer.0.1.0.0.json` in place only. Mid-lifecycle E5 capacity increase is **persevere** `D00000000000000000000002` growth subscription: keep `status: active`, `stripe_customer_id`, `stripe_subscription_id` / `stripe_price_id`, `unit_cost` 9900, discount fields (`TRIAL2WK` / free encounters), and `encounters_mo`. Change `quantity` / `mentee_count` 5 → **8** and `total_cost` 49500 → **79200** (8 × 9900). Bump `saved` to after T234 persevere `invoice.paid` (`2026-08-05`). Leave **harbor** `D…11` starter qty 1 active unchanged. Leave **northstar** `D…10` as `subscriptions: []` (no `stripe_customer_id`). Leave **supersoft** starter qty 2 active unchanged. Do **not** set `past_due` or `canceled`. Do **not** subscribe mary / ali / scamsoft / Path A stub. No Payment / ExternalEvent / Event / dictionary / Profile edits (T242 owns the capacity Payment). Configure-database SUCCESS on already-running `:8385`; skip packaging.

**Previous vs new quantity (for T242)**

| Customer | Field | Previous | New |
| --- | --- | --- | --- |
| persevere `D00000000000000000000002` | `quantity` | 5 | **8** |
| persevere | `mentee_count` | 5 | **8** |
| persevere | `total_cost` | 49500 (5 × 9900) | **79200** (8 × 9900) |
| persevere | `status` | active | active (unchanged) |
| supersoft `D…07` | `quantity` | 2 | 2 (unchanged) |
| harbor `D…11` | `quantity` | 1 | 1 (unchanged) |

**Implemented:** persevere `subscriptions[0]` quantity / mentee_count 8, `total_cost` 79200; `saved.at_time` `2026-08-18T16:00:00.000Z` (`save-customer-002-capacity`). Stripe ids and discount fields unchanged. Harbor / northstar / supersoft / unsubscribed orgs untouched.

**Testing results**

- Reused already-running local configurator `:8385` (Mongo host `:27017`; no `make dev`, no port override). Packaging skipped (`make down` / `make container` / `mh up mongodb`) so later sequential tasks can reuse `:8385`.
- `DELETE /api/database/` → HTTP 200, `status: SUCCESS`.
- `POST /api/configurations/` → HTTP 200, top-level `status: SUCCESS` (`CFG-07-PROCESS_ALL`); zero FAILURE events.
- `CFG-05-Customer.yaml` SUCCESS (8 docs, includes `D…02` / `D…07` / `D…10` / `D…11`).
- Spot-check (mongosh `mentor_hub`):
  - persevere `D…02`: `quantity` 8, `mentee_count` 8, `total_cost` 79200, `status: active`, `unit_cost` 9900, `stripe_subscription_id: sub_test_persevere_growth`, `stripe_price_id: price_test_growth`, `discount_code: TRIAL2WK`.
  - supersoft `D…07`: quantity 2, `status: active`.
  - harbor `D…11`: quantity 1, `status: active`.
  - northstar `D…10`: `subscriptions: []` (no `stripe_customer_id`).
  - `db.Customer.find({ "subscriptions.status": { $in: ["past_due", "canceled"] } }).count()` → **0**.

**Orchestrator confirmation:** `DELETE`/`POST` on `:8385` re-ran SUCCESS. Spot-check: persevere 8/8/79200 active; supersoft qty 2; 0 past_due/canceled.

**Follow-ups**

- T242: append capacity Payment for persevere at **quantity 8** (previous 5). Amount may be proration 29700 (3 × 9900) or new period total 79200. Timestamps after T234 `invoice.paid` (`2026-08-05`); this seed’s `saved` is `2026-08-18T16:00:00.000Z`.
