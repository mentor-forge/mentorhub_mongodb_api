# T234 – Seed invoice.paid and invoice.payment_failed Payment fixtures (F-D26)

**Status:** Pending  
**Type:** Feature  
**Depends On:** none  
**Description:** Append **Payment** test data for E6 renewal webhooks: one **`invoice.paid`** (succeeded) and one **`invoice.payment_failed`** (failed) record, plus matching Stripe **ExternalEvent** + **Event** chains. Prefer add over rewrite. Do **not** mutate Customer / Profile documents (F-D21 / F-D25 / F-D27 own those). Pre-release: edit `Payment.0.1.0.0.json` (and Event / ExternalEvent test data) in place.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`, `configurator/dictionaries/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/customer_journey_issues.md` — E6 recurring charge; `invoice.paid` / `invoice.payment_failed` → Payment + past_due Notification
- `../mentorhub/Research/stripe_research.md` — webhook table: `invoice.paid` persist payment; `invoice.payment_failed` persist failure
- GitHub: [F-D26 #58](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/58)
- Prerequisites (already on `main`): F-D22 Payment collection + catalog seeds (`Tasks/SHIPPED.T229`, `Tasks/SHIPPED.T230`); F-D29 Event types + ExternalEvent (`Tasks/SHIPPED.T220`, `Tasks/SHIPPED.T221`, `Tasks/SHIPPED.T224`)
- `configurator/dictionaries/Payment.0.1.0.yaml` — already has `stripe_invoice_id`, `stripe_payment_intent_id`, `payment_status` (`pending` \| `succeeded` \| `failed` \| `canceled`)
- `configurator/test_data/Payment.0.1.0.0.json` — two Checkout-originated **succeeded** Payments (`b…01` persevere, `b…02` supersoft); append, do not replace
- `configurator/test_data/ExternalEvent.0.1.0.0.json` — `E…02` is a thin `invoice.payment_failed` for scamsoft (`D…08`); keep it; add **richer** invoice.paid / invoice.payment_failed events tied to Payment ids
- `configurator/test_data/Event.0.1.0.0.json` — last seed `_id` `F00000000000000000000191`; append
- `Tasks/scripts/persona_ids.json` — Customer ids (`persevere` `D…02`, `supersoft` `D…07`)
- **External:** Admin ingress receives Stripe webhooks; Customer API consumer writes Payment (not this repo)
- **Out of scope:** Payment dictionary changes unless running configurator proves a gap (document in Execution Notes; do not invent fields); Customer.`subscriptions[]` `past_due` / `canceled` (F-D25 / F-D27); Profile / Customer seed files (F-D21); Notification fixtures (T235); PAN storage; new collections
- **Numbering note:** Task ids start at **T234** so they do not collide with F-D21 `T231`–`T233` on branch `F-D21/E1-extend-customer-profile-self-registration`

### Seed expectations (minimum)

Reuse existing **active-subscription** persona Customers from T230 (do **not** edit Customer JSON):

| Fixture | Customer | Payment `status` | Stripe mapping |
| --- | --- | --- | --- |
| Renewal **paid** | persevere `D00000000000000000000002` | `succeeded` | `invoice.paid` — require `stripe_invoice_id` (`in_…`) + `stripe_payment_intent_id` (`pi_…`); omit or leave empty checkout session |
| Renewal **failed** | supersoft `D00000000000000000000007` | `failed` | `invoice.payment_failed` — require `stripe_invoice_id` + `stripe_payment_intent_id`; unique vs T230 ids |

Suggested unused Payment `_id`s (valid 24-hex; confirm unused before write):

- `b00000000000000000000003` — invoice.paid
- `b00000000000000000000004` — invoice.payment_failed

Amounts / `product_id` / `subscription` / `quantity` should match T230 catalog snapshots (persevere growth `e…02` qty 5 amount 49500; supersoft starter `e…01` qty 2 amount 9800) unless Execution Notes justify otherwise.

**Unique indexes:** `stripe_payment_intent_id` is unique — new `pi_test_…` values must not collide with T230.

### Ingress / Event chains (minimum)

Append (do not rewrite existing T224 rows):

| Collection | Expectations |
| --- | --- |
| ExternalEvent | Two `source: stripe` docs: `normalized_body.type` `invoice.paid` and `invoice.payment_failed`; `external_id` Stripe-like `evt_…`; include MentorHub `customer_id`, `stripe_invoice_id`, and Payment `_id` or PI id in `normalized_body` |
| Event | At least one `payment_recorded` per Payment; optional `external_received` / `subscription_changed` for the failed invoice. Continue `F0…` from `F…0192`. Preserve **all** existing Events |

Suggested unused ExternalEvent `_id`s: `E00000000000000000000006`, `E00000000000000000000007` (skip if taken).

## Goals

- Append invoice.paid (succeeded) and invoice.payment_failed (failed) Payments with `stripe_invoice_id` populated.
- Append matching Stripe ExternalEvent + Event chains; keep existing Checkout Payments and T224 ingress fixtures.
- Confirm existing Payment schema is enough for those shapes (confirm-only unless a real gap is found via running configurator).
- Do **not** edit Customer, Profile, Setting, or Notification files in this task.
- Configure-database **SUCCESS**.

## Testing Expectations

```sh
make dev
# If host port 27017 is busy, use compose ports !override (e.g. host 27018) as in prior F-D tasks.
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- Payment / ExternalEvent / Event CFG SUCCESS.
- Spot-check: ≥1 Payment `status: succeeded` with `stripe_invoice_id` and no requirement on checkout session; ≥1 Payment `status: failed` with `stripe_invoice_id`; unique `stripe_payment_intent_id`s.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Payment.0.1.0.0.json` — append invoice.paid + invoice.payment_failed docs
- `configurator/test_data/ExternalEvent.0.1.0.0.json` — append stripe invoice webhook samples
- `configurator/test_data/Event.0.1.0.0.json` — append `payment_recorded` (and related) Events; preserve existing
- `Tasks/PENDING.T234.seed_invoice_paid_and_payment_failed_payments.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

*(Reserved for the execution agent.)*
