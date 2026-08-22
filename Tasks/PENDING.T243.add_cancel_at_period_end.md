# T243 – Add cancel_at_period_end on Customer.subscriptions[] (F-D27)

**Status:** Pending  
**Type:** Feature  
**Depends On:** none  
**Description:** Add optional **`cancel_at_period_end`** (boolean) on embedded **Customer.subscriptions[]** so E7 Portal cancel can be seeded as “cancels at period end” vs already **`canceled`**. Pre-release: edit `Customer.0.1.0.yaml` in place. Relaxing change — existing Customer documents must still configure.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/dictionaries/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/customer_journey_issues.md` — E7 Portal cancel; F-CA09 **honor `cancel_at_period_end`**
- GitHub: [F-D27 #59](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/59)
- `Tasks/SHIPPED.T226.extend_customer_subscriptions_schema.md` — current `subscriptions[]` (no cancel-at-period-end)
- `configurator/dictionaries/Customer.0.1.0.yaml` — `subscriptions[].status` already uses `subscription_status` (`active` \| `past_due` \| `canceled`)
- `configurator/types/boolean.yaml` — type for the new field
- **Out of scope:** Customer test-data values (T244); Notification (T245); `past_due` seeds; Payment dictionary; GDPR; Dashboard

### Field to add (optional)

| Field | Type | Role |
| --- | --- | --- |
| `cancel_at_period_end` | `boolean`, `required: false` | Stripe `cancel_at_period_end`: entitlement continues until `current_period_end` when `status` is still `active` |

Prefer add over rename. Do **not** add a separate invite/cancel collection. Customer document `status` (`customer_status`) stays independent of `subscriptions[].status`.

No new enumerator. No version bump.

## Goals

- `subscriptions[]` items may include `cancel_at_period_end`.
- Existing Customer EJSON still validates (field omitted = not canceling).
- Configure-database **SUCCESS** with current test data (T244 has not run yet).

## Testing Expectations

```sh
make dev
# If host port 27017 is busy, use compose ports !override (e.g. host 27018) as in prior F-D tasks.
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- Customer CFG SUCCESS without requiring the new field on existing docs.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/dictionaries/Customer.0.1.0.yaml` — add optional `cancel_at_period_end`
- Optional: `configurator/configurations/Customer.yaml` — only if an index is justified (document in Execution Notes; default none)
- `Tasks/PENDING.T243.add_cancel_at_period_end.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

_(Reserved for the task execution agent.)_
