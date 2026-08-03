# T232 – Confirm Customer for primary org provisioning (F-D21)

**Status:** Pending  
**Type:** Feature  
**Depends On:** none  
**Description:** Confirm **Customer (Organization)** dictionary supports Admin-ingress minimal create + Customer API enrich for Path A: `customer_status` includes `provisioned` → `active` (F-D29). Extend only where the **running configurator** shows a real E1 gap. Do **not** add `subscriptions[]` / `stripe_customer_id` (F-D22), Card, or GDPR fields. Prefer add over rename; pre-release edit `Customer.0.1.0` in place.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/dictionaries/`, `configurator/configurations/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/customer_journey_issues.md` — E1; Customer vs Organization naming; Admin ingress provisions minimal Customer
- `../mentorhub/Research/cognito.md` — Path A creates new Customer org + owner Profile
- `../mentorhub/Research/squarespace_sheet/squarespace_sheet_research.md` — company → Customer `name` / optional `description` (no new columns required for those mappings alone)
- GitHub: [F-D21 #53](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/53)
- Prerequisites: `Tasks/SHIPPED.T220.extend_event_types_and_lifecycle_enums.md` — `customer_status` (`provisioned`, `active`, `archived`) already on Customer.`status`
- `configurator/dictionaries/Customer.0.1.0.yaml` — `_id`, `name`, `description`, `created`, `saved`, `status`
- `configurator/configurations/Customer.yaml` — unique `name`; Last Saved
- Parallel: `Tasks/PENDING.T231.extend_profile_for_cognito_primary_registration.md`
- **Out of scope:** Profile `cognito_sub` (T231); seeds (T233); F-D22 billing fields; Card; `gdpr_*`; renaming collection Customer → Organization

### Confirm present (document in Execution Notes)

| Field | Role for E1 |
| --- | --- |
| `_id` | New org id → Profile.`customer_id` / JWT claim |
| `name` | Org / company name (unique index — provisioned stubs need distinct names) |
| `description` | Optional org blurb (often empty until enrich) |
| `status` | `provisioned` at ingress; `active` after enrich |
| `created` / `saved` | Breadcrumbs |

### Allowed dictionary/config updates in this task

- Clarify root **description** (Customer = Organization / paying sponsor org for Path A).
- Index tweaks only if justified for ingress/enrich lookups (document choices).
- **Do not** add billing or GDPR properties. If running configurator reveals no property gaps, record “confirm-only” and still ship after SUCCESS configure.

## Goals

- Confirm Customer supports provisioned → active lifecycle for ingress-created orgs (F-D29 enums already wired).
- Apply only additive/clarifying dictionary or index updates required for E1 (none for subscriptions/stripe).
- Existing Customer test data still configures **SUCCESS**.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- Customer CFG SUCCESS; `customer_status` / `provisioned` still valid.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/dictionaries/Customer.0.1.0.yaml` — confirm / clarify description; additive E1 fields only if justified
- `configurator/configurations/Customer.yaml` — only if indexes change
- `Tasks/PENDING.T232.confirm_customer_for_primary_org_provisioning.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

*(Reserved for the execution agent.)*
