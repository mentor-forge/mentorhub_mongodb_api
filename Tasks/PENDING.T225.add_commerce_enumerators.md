# T225 – Add F-D22 commerce enumerators (subscription / discount / payment status)

**Status:** Pending  
**Type:** Feature  
**Depends On:** none  
**Description:** Add shared enumerators needed by Customer `subscriptions[]`, Discount, and Payment for E2 Checkout (F-D22). Enum-only — no collection schemas in this task.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/enumerators/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/customer_journey_issues.md` — E2 locked Product / Subscription / Discount shapes; Stripe sync fields
- GitHub: [F-D22 #50](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/50)
- Prerequisites (already shipped): F-D-E0 drops; F-D29 event types (`Tasks/SHIPPED.T220`–`T224`)
- `configurator/enumerators/enumerations.0.yaml` — extend in place (pre-release; no version bump)
- **Out of scope:** Customer / Setting / Payment dictionaries (T226–T229); seeds (T230); Admin SPA Setting UI (external ISSUE).

### Enumerators to add (snake_case values; refine descriptions in implementation)

| Enumerator | Values | Used by |
| --- | --- | --- |
| `subscription_status` | `active`, `past_due`, `canceled` | `Customer.subscriptions[].status` |
| `discount_status` | `active`, `inactive` | Setting Discount variant.`status` |
| `payment_status` | derive from Stripe PaymentIntent / Invoice lifecycle during T229 (e.g. `succeeded`, `failed`, `pending` / equivalents) — finalize against Stripe docs + F-D29 `payment_recorded` / `subscription_changed` event context | Payment.`status` |

Do **not** revive a top-level Subscription collection enum; subscriptions are embedded on Customer.

## Goals

- Add `subscription_status`, `discount_status`, and `payment_status` (or equivalent names) to `enumerations.0.yaml`.
- Keep existing enumerators unchanged except additive inserts.
- Confirm configure-database still **SUCCESS** (enum additions are relaxing).

## Testing Expectations

```sh
make dev
# If host port 27017 is busy, use compose ports !override (e.g. host 27018) as in prior F-D tasks.
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- New enumerator names appear in configurator / process output.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/enumerators/enumerations.0.yaml` — add F-D22 commerce status enums
- `Tasks/PENDING.T225.add_commerce_enumerators.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

*(Reserved for the execution agent.)*
