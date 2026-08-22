# T242 – Seed capacity-change Payment and webhook fixtures (F-D25)

**Status:** Pending  
**Type:** Feature  
**Depends On:** T241  
**Description:** Append **Payment** plus Stripe **ExternalEvent** / **Event** chains for an E5 **capacity change** (Checkout and/or `customer.subscription.updated`). New Payment `quantity` must match T241 persevere `subscriptions[].quantity`. Prefer append over rewrite. Keep `status: succeeded` — not E6 `invoice.payment_failed`. Pre-release: edit test_data in place.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/customer_journey_issues.md` — E5 capacity Checkout/Portal; webhooks sync seats; never trust success URL as paid
- `../mentorhub/Research/stripe_research.md` — Checkout `line_items[].quantity`; `customer.subscription.updated` for manage/capacity
- GitHub: [F-D25 #57](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/57)
- `Tasks/PENDING.T241.seed_active_capacity_subscriptions.md` — persevere growth **qty 8** (from 5)
- `Tasks/SHIPPED.T234.seed_invoice_paid_and_payment_failed_payments.md` — do **not** replace `b…01`–`b…04`
- `configurator/dictionaries/Payment.0.1.0.yaml` — `quantity`, `amount`, `stripe_invoice_id`, `stripe_payment_intent_id`, optional `stripe_checkout_session_id`; confirm-only
- Unique index: `stripe_payment_intent_id` — new `pi_test_…` must not collide
- `configurator/test_data/ExternalEvent.0.1.0.0.json` — last ids `E…06` / `E…07` (T234); next `E00000000000000000000008`+
- `configurator/test_data/Event.0.1.0.0.json` — continue `F0…` after T238 / T240 last id (before those tasks: `F…0197`)
- **Out of scope:** Customer JSON (T241); Profile; Notification; Setting; `past_due` / `canceled` Customer status; PAN storage; Payment dictionary changes unless configurator proves a gap

### Payment (minimum)

Append **one** succeeded Payment for **persevere** capacity increase:

| Field | Expectation |
| --- | --- |
| `_id` | `b00000000000000000000005` if unused |
| `customer_id` | persevere `D…02` |
| `subscription` / `product_id` | growth / Setting `e00000000000000000000002` |
| `quantity` | **8** (new seat count, matches T241) |
| `amount` | Proration for **added** seats (3 × 9900 = **29700**) **or** new period total 79200 — pick one Stripe-shaped value and document in Execution Notes |
| `status` | `succeeded` |
| `stripe_payment_intent_id` | unique `pi_test_persevere_capacity_01` (or similar) |
| `stripe_invoice_id` | unique `in_test_…` (capacity invoice / proration) |
| `stripe_checkout_session_id` | set if modeling capacity **Checkout**; omit if Portal-only `subscription.updated` |

Timestamps after T234 persevere `invoice.paid` (`2026-08-05`).

Preserve `b…01`–`b…04` (original qty 5 checkout, qty 5 renewal, supersoft qty 2).

### Ingress / Event chains (minimum)

Append (do not rewrite T224 / T234 rows):

| Collection | Expectations |
| --- | --- |
| ExternalEvent | ≥1 `source: stripe`: `normalized_body.type` **`customer.subscription.updated`** with `quantity` 8 (and previous 5 if you record it), MentorHub `customer_id`, Payment / PI / invoice ids. Optional second event `checkout.session.completed` if the Payment has a checkout session id. `_id` `E…08`+; unique `external_id` `evt_…` |
| Event | `subscription_changed` (capacity) + `payment_recorded` for the new Payment; optional `external_received`. Continue `F0…`. Preserve **all** existing Events |

Do **not** add past_due or cancel Notifications.

## Goals

- Payment + webhook fixtures exist for an E5 capacity change whose `quantity` matches persevere’s active `subscriptions[]`.
- Existing Checkout and E6 invoice Payments unchanged.
- Configure-database Payment / ExternalEvent / Event **SUCCESS**.
- No Customer edits in this task.

## Testing Expectations

```sh
make dev
# If host port 27017 is busy, use compose ports !override (e.g. host 27018) as in prior F-D tasks.
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- Spot-check: Payment `b…05` (or recorded id) `quantity` 8, `status` succeeded, unique `stripe_payment_intent_id`; ExternalEvent `customer.subscription.updated`; Event `subscription_changed` / `payment_recorded`; T234 `b…03` / `b…04` still present.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Payment.0.1.0.0.json` — append capacity Payment
- `configurator/test_data/ExternalEvent.0.1.0.0.json` — append Stripe capacity webhook(s)
- `configurator/test_data/Event.0.1.0.0.json` — append `subscription_changed` + `payment_recorded`
- `Tasks/PENDING.T242.seed_capacity_change_payments.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

_(Reserved for the task execution agent.)_
