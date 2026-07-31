# T229 – Add Payment collection (F-D22)

**Status:** Pending  
**Type:** Feature  
**Depends On:** T225  
**Description:** Create **Payment** Configuration and Dictionary for Stripe-backed payment records consumed after Admin ingress / Customer API event handling. Prefer create over rename. Derive fields from Stripe webhook payloads and F-D29 event types — confirm via **running configurator** and [Stripe API docs](https://docs.stripe.com/api).

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/configurations/`, `configurator/dictionaries/`, `configurator/test_data/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/customer_journey_issues.md` — E2 Payment persistence; Stripe webhooks on Admin ingress; F-D29 event types
- GitHub: [F-D22 #50](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/50)
- `Tasks/SHIPPED.T220.extend_event_types_and_lifecycle_enums.md` — `payment_recorded`, `subscription_changed`, etc.
- `Tasks/SHIPPED.T221.add_external_event_collection.md` — ExternalEvent append-only ingress
- `Tasks/PENDING.T225.add_commerce_enumerators.md` — `payment_status`
- Payment Card collection already dropped (F-D16) — Payment here is **financial record**, not PAN storage
- **Out of scope:** Writing Payments from Customer API (F-CA06); rich invoice fixtures for E5–E7 (later F-D25/F-D26); seeds beyond empty/minimal (T230 may add a couple of Payment docs).

### Property design (illustrative — finalize in implementation)

Derive from Stripe PaymentIntent / Invoice / Checkout Session objects as needed for idempotent sync, e.g.:

| Field | Notes |
| --- | --- |
| `_id` | identifier |
| `customer_id` | MentorHub Customer `_id` |
| `stripe_payment_intent_id` / `stripe_invoice_id` / `stripe_checkout_session_id` | provider ids (keep only those justified by webhook payloads) |
| `amount` / `currency` | settled amounts |
| `status` | enum `payment_status` |
| `product_id` / `subscription` / `quantity` | optional MentorHub context from checkout metadata |
| `created` | breadcrumb (append-oriented OK; `saved` only if updates expected) |

Indexes: unique on chosen Stripe id(s); `customer_id` + `created.at_time`.  
**Stable `_id` prefix for seeds:** e.g. `Y0…` — record in Execution Notes.

## Goals

- Create `configurator/dictionaries/Payment.0.1.0.yaml` with fields justified by Stripe + F-D29 (document mapping in Execution Notes).
- Create `configurator/configurations/Payment.yaml` version `0.1.0.0`.
- Create `configurator/test_data/Payment.0.1.0.0.json` as `[]` until T230 (or minimal).
- Prefer **create**. Confirm configure **SUCCESS**. Do not store card PANs.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- Configurations list includes `Payment.yaml`; no payment-Card collection.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/dictionaries/Payment.0.1.0.yaml` — **create**
- `configurator/configurations/Payment.yaml` — **create**
- `configurator/test_data/Payment.0.1.0.0.json` — **create** (`[]` acceptable)
- `Tasks/PENDING.T229.add_payment_collection.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

*(Reserved for the execution agent.)*
