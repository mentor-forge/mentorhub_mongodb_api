# T220 – Extend event types and provisioned lifecycle enums (F-D29)

**Status:** Shipped  
**Type:** Feature  
**Depends On:** T219  
**Description:** Extend shared enumerators for Admin ingress and Discovery: new `event_types`, Notification scope, ExternalEvent source, and `provisioned` → `active` lifecycle values on Profile and Customer status enums. Schema/enum work only — no new collections in this task.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/enumerators/`, `configurator/dictionaries/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/discovery_journey_issues.md` — F-D29 / Discovery data
- `../mentorhub/Workshops/customer_journey_issues.md` — Phase 0 / E0 coordination; provisioned lifecycle
- `../mentorhub/Workshops/customer_journey_issues_adjustments.md` — illustrative `event_types` list
- GitHub: [F-D29 #61](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/61); supersedes F-W14 **F-SD01** naming ([mentorhub#38](https://github.com/mentor-forge/mentorhub/issues/38))
- Prerequisite in-repo: `Tasks/PENDING.T219.drop_dashboard_collection.md` (remaining E0 drop; Card/Subscription already shipped)
- `configurator/enumerators/enumerations.0.yaml` — current `event_types`, `profile_status`, `default_status`
- `configurator/dictionaries/Profile.0.1.0.yaml` — uses `profile_status`
- `configurator/dictionaries/Customer.0.1.0.yaml` — uses `default_status`
- **Out of scope:** ExternalEvent / Notification / Card dictionaries (T221–T223); test-data seeds (T224); F-D21 provisioned seed pairs beyond enum support.

### Enum design (finalize names in implementation; keep snake_case values)

**`event_types` — add** (retain existing mentee/mentor activity values):

| Value (illustrative) | Intent |
| --- | --- |
| `external_received` | Raw normalized external payload reference |
| `identity_provisioned` | Profile and/or Customer created by Admin ingress |
| `organization_enriched` | Customer domain filled business fields |
| `subscription_changed` | Checkout, invoice, cancel, past_due |
| `invite_created` / `invite_accepted` | Member invite lifecycle |
| `notification_created` / `notification_dismissed` | Notification write / dismiss |
| `payment_recorded` | Payment persistence |
| `profile_redacted` | GDPR redact |

**New enumerators:**

- `external_event_source`: `stripe`, `cognito`
- **Do not** add `notification_scope` — Notification targeting is a `scope_id` **`one_of`** (`profile_id` | `customer_id` | `mentor_id` | global breadcrumb) per T222

**Lifecycle:**

- Add `provisioned` to `profile_status` (keep `active`, `archived`, `suspended`).
- Introduce `customer_status` with `provisioned`, `active`, `archived` — switch Customer dictionary `status` from `default_status` to `customer_status` (do **not** pollute `default_status` used by other collections). Prefer add over rename of existing values.

## Goals

- Extend `event_types` for ingress, subscription, invite, notification, and GDPR (Admin) use cases; keep existing activity types.
- Add `external_event_source` enumerator (Notification scope is `scope_id` one_of in T222, not an enum).
- Support Profile / Customer `provisioned` → `active` lifecycle via status enums + Customer dictionary enum retarget.
- Pre-release: edit enumerators / 0.1.0 dictionaries in place; no version bumps.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200** and top-level **`status: SUCCESS`** (enum/dictionary changes must not break existing test data: existing Profile/Customer statuses remain valid values).
- Confirm new enumerator names appear in configurator output / loaded enums.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/enumerators/enumerations.0.yaml` — extend `event_types`, `profile_status`; add `external_event_source`, `customer_status`
- `configurator/dictionaries/Customer.0.1.0.yaml` — `status.enums: customer_status`
- `Tasks/SHIPPED.T220.extend_event_types_and_lifecycle_enums.md` — this file (Execution Notes)

## Execution Notes

**Plan:** Extend `enumerations.0.yaml` in place (keep existing `event_types`; add provisioned to `profile_status`; add `external_event_source` and `customer_status`; do not add `notification_scope` or touch `default_status`). Point Customer `status` at `customer_status`. Verify via local configurator (Mongo host port 27018 `ports: !override` if 27017 busy) then `make container` + `mh up mongodb`.

**Changes**

- `enumerations.0.yaml`: added `provisioned` to `profile_status`; extended `event_types` with ingress/subscription/invite/notification/GDPR values; added `external_event_source` (`stripe`, `cognito`) and `customer_status` (`provisioned`, `active`, `archived`). Left `default_status` unchanged; did not add `notification_scope`.
- `Customer.0.1.0.yaml`: `status.enums` retargeted from `default_status` to `customer_status` (in place, no version bump).

**Testing results**

- Local configurator (INPUT_FOLDER mount, Mongo host port 27018 via `ports: !override`): `DELETE /api/database/` → HTTP 200, `status: SUCCESS`.
- `POST /api/configurations/` → HTTP 200, top-level `status: SUCCESS`; `ENU-01-enumerations.0.yaml`, `CFG-05-Customer.yaml`, `CFG-05-Profile.yaml`, `CFG-05-Event.yaml` SUCCESS; process result mentions `customer_status`, `external_event_source`, `provisioned`, `identity_provisioned`.
- `make container` → image `ghcr.io/mentor-forge/mentorhub_mongodb_api:latest` built successfully; image `/input` contains new enums and Customer `customer_status`.
- `mh up mongodb` → API on :8383 lists configs including `Customer.yaml` / `Event.yaml` (packaged DROP disabled → 403 as expected).
