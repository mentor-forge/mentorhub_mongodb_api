# T244 – Seed canceled and cancel_at_period_end subscriptions (F-D27)

**Status:** Pending  
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

_(Reserved for the task execution agent.)_
