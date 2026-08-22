# T244 – Seed canceled and cancel_at_period_end subscriptions (F-D27)

**Status:** Shipped  
**Type:** Feature  
**Depends On:** T241, T243  
**Description:** Seed **E7** `Customer.subscriptions[]` cancel scenarios: **scheduled cancel** (`status: active`, `cancel_at_period_end: true`) and **already canceled** (`status: canceled`). Do **not** flip persevere (E5) or supersoft (E6 failed invoice). Pre-release: edit `Customer.0.1.0.0.json` in place.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/customer_journey_issues.md` — E7: Portal cancel → `canceled`; Resubscribe CTA; gated routes honor `cancel_at_period_end`
- GitHub: [F-D27 #59](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/59)
- `Tasks/PENDING.T243.add_cancel_at_period_end.md` — schema
- `Tasks/PENDING.T241.seed_active_capacity_subscriptions.md` — persevere qty 8 **active**; supersoft qty 2 **active**; harbor qty 1 **active** (if T236)
- Unique sparse index `subscriptions.stripe_subscription_id` — new Stripe sub ids must not collide
- **Out of scope:** Notification / Event (T245); Payment rows unless a cancel invoice is required (default **no** new Payment); Profile; Setting; GDPR; Dashboard; `past_due`

### Target cancel mix (minimum)

Do **not** change persevere or supersoft `subscriptions[].status`.

| Customer | `subscriptions[].status` | `cancel_at_period_end` | `current_period_end` | Notes |
| --- | --- | --- | --- | --- |
| **harbor** `D…11` (T236) | **`active`** | **`true`** | **future** (still entitled) | Scheduled Portal cancel; keep starter qty / stripe ids from T236; bump `saved` |
| **scamsoft** `D…08` | **`canceled`** | `true` or omit | **past** | Period already ended; add one `subscriptions[]` entry (today `[]`); unique `stripe_subscription_id` / `stripe_customer_id` if adding billing ids; starter-shaped snapshot OK |

If harbor is missing after T236/T241, apply the scheduled-cancel shape to another **non-persevere, non-supersoft** subscribed org only if one exists; otherwise document the gap in Execution Notes and still seed scamsoft as `canceled`.

Preserve unsubscribed mary / ali / northstar / Path A stub (empty `[]`).

Stripe uniqueness: do not reuse `sub_test_persevere_growth` or `sub_test_supersoft_starter`.

## Goals

- ≥1 subscription with `cancel_at_period_end: true` and `status: active` (access until `current_period_end`).
- ≥1 subscription with `status: canceled`.
- Persevere remains E5 active capacity; supersoft remains E6 active-with-failed-invoice.
- Configure-database Customer **SUCCESS**.

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
db.Customer.findOne({ name: "harbor" }).subscriptions[0]
// status "active", cancel_at_period_end true
db.Customer.findOne({ name: "scamsoft" }).subscriptions[0].status  // "canceled"
db.Customer.findOne({ name: "persevere" }).subscriptions[0].status  // "active"
db.Customer.findOne({ name: "supersoft" }).subscriptions[0].status  // "active"
```

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Customer.0.1.0.0.json` — harbor scheduled cancel + scamsoft canceled
- `Tasks/PENDING.T244.seed_canceled_subscriptions.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

**Plan:** Edit `Customer.0.1.0.0.json` in place only. E7 scheduled cancel is **harbor** `D00000000000000000000011`: keep starter qty 1, `cus_test_harbor`, `sub_test_harbor_starter`, `price_test_starter`, `status: active`, and existing future `current_period_end` `2026-09-15T12:00:00.000Z` (still entitled as of 2026-08-22). Add `cancel_at_period_end: true`. Bump `saved` after T241 (`2026-08-18`). E7 already-canceled is **scamsoft** `D00000000000000000000008` (today `subscriptions: []`): add `stripe_customer_id: cus_test_scamsoft` and one starter-shaped `subscriptions[]` entry (`qty`/`mentee_count` 1, `unit_cost` 4900, `total_cost` 4900, `price_test_starter`) with `status: canceled`, `cancel_at_period_end: true`, `current_period_end` in the past, unique `stripe_subscription_id: sub_test_scamsoft_starter`. Do **not** reuse `sub_test_persevere_growth` or `sub_test_supersoft_starter`. Do **not** change persevere or supersoft `subscriptions[].status` (remain `active`). Preserve unsubscribed mary / ali / northstar / Path A stub (`[]`). No Payment / Notification / Event / dictionary edits. Configure-database SUCCESS on already-running `:8385`; skip packaging. T245 should prefer harbor for the cancel Notification (`customer_id` → `D…11`).

**Implemented**

| Customer | Field | Value |
| --- | --- | --- |
| harbor `D00000000000000000000011` | `subscriptions[0].status` | `active` |
| harbor | `cancel_at_period_end` | `true` |
| harbor | `current_period_end` | `2026-09-15T12:00:00.000Z` (future; still entitled) |
| harbor | qty / stripe ids | starter qty 1; `cus_test_harbor`; `sub_test_harbor_starter`; `price_test_starter` (T236 unchanged) |
| harbor | `saved` | `2026-08-20T18:00:00.000Z` (`save-customer-011-cancel`) |
| scamsoft `D00000000000000000000008` | `stripe_customer_id` | `cus_test_scamsoft` (new) |
| scamsoft | `subscriptions[0].status` | `canceled` |
| scamsoft | `cancel_at_period_end` | `true` |
| scamsoft | `current_period_end` | `2026-07-15T08:00:00.000Z` (past; period ended) |
| scamsoft | qty / stripe ids | starter qty 1; `sub_test_scamsoft_starter`; `price_test_starter` |
| scamsoft | `saved` | `2026-07-15T08:05:00.000Z` (`save-customer-008-canceled`) |
| persevere / supersoft | `subscriptions[].status` | `active` (unchanged) |
| mary / ali / northstar / Path A stub | `subscriptions` | `[]` (unchanged) |

**Testing results**

- Reused already-running local configurator `:8385` (Mongo host `:27017`; no `make dev`, no port override). Packaging skipped (`make down` / `make container` / `mh up mongodb`) so later sequential tasks can reuse `:8385`.
- `DELETE /api/database/` → HTTP 200, `status: SUCCESS`.
- `POST /api/configurations/` → HTTP 200, top-level `status: SUCCESS` (`CFG-07-PROCESS_ALL`); zero FAILURE events.
- `CFG-05-Customer.yaml` SUCCESS.
- Spot-check (mongosh `mentor_hub`):
  - harbor `D…11`: `status: active`, `cancel_at_period_end: true`, `current_period_end` `2026-09-15T12:00:00.000Z`, qty 1, `sub_test_harbor_starter`.
  - scamsoft `D…08`: `status: canceled`, `cancel_at_period_end: true`, `current_period_end` `2026-07-15T08:00:00.000Z`, `cus_test_scamsoft` / `sub_test_scamsoft_starter`.
  - persevere `D…02`: `status: active`.
  - supersoft `D…07`: `status: active`.
  - mary / ali / northstar / provisioned-org-path-a: `subscriptions: []`.
  - Distinct `stripe_subscription_id`s: `sub_test_harbor_starter`, `sub_test_persevere_growth`, `sub_test_scamsoft_starter`, `sub_test_supersoft_starter` (no collisions).

**Orchestrator confirmation:** `DELETE`/`POST` on `:8385` re-ran SUCCESS. Spot-check: harbor active+cancel_at_period_end true; scamsoft canceled; persevere/supersoft active.

**T245 handoff:** Prefer **harbor** `D00000000000000000000011` for the cancel Notification (`CancelScheduled` / still-entitled Portal cancel). Scamsoft is the already-`canceled` org if a second card is needed.
