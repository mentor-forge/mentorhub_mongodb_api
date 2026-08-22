# T243 – Add cancel_at_period_end on Customer.subscriptions[] (F-D27)

**Status:** Shipped  
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

**Plan:** Edit `Customer.0.1.0.yaml` in place. Add optional `cancel_at_period_end` (`type: boolean`, `required: false`) on embedded `subscriptions[]` items, after `current_period_end` (Stripe sync group). Matches `configurator/types/boolean.yaml` and existing boolean usage (`Profile.email_verified`, `Encounter.steps[].checked`). Relaxing change — omit = not canceling; existing Customer docs (T241 Persevere qty 8, Harbor qty 1) keep configuring. No enumerator. No version bump. No Customer.yaml index: boolean is not a lookup key; existing sparse unique indexes on `stripe_customer_id` / `subscriptions.stripe_subscription_id` remain sufficient. No test-data value changes (T244). Skip packaging — prefer already-running configurator :8385 / Mongo :27017.

**Property types (Customer.0.1.0 `subscriptions[]` addition):**

| Field | Type |
| --- | --- |
| `cancel_at_period_end` | boolean (optional) |

**Indexes (`Customer.yaml`):** none added.

**Test data:** No change to `Customer.0.1.0.0.json` (optional field omitted = not canceling).

**Testing results**

- `DELETE /api/database/` → HTTP 200, `status: SUCCESS` (localhost:8385 / Mongo :27017).
- `POST /api/configurations/` → HTTP 200, top-level `status: SUCCESS`; `CFG-05-Customer.yaml` SUCCESS (PRO-05 schema, PRO-06 test data including T241 Persevere qty 8 / Harbor qty 1 without `cancel_at_period_end`); indexes `PRO-04-Name Index`, `PRO-04-Last Saved`, `PRO-04-Stripe Customer Id`, `PRO-04-Stripe Subscription Id` SUCCESS. No new index.
- Packaging verification skipped (orchestrator owns stack).

**Orchestrator confirmation:** `DELETE`/`POST` on `:8385` re-ran SUCCESS (`CFG-05-Customer.yaml`). Field is optional boolean after `current_period_end`; no index.
