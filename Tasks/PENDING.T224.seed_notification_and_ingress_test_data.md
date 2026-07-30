# T224 – Seed Notification, ingress Event chains, and card samples (F-D29)

**Status:** Pending  
**Type:** Feature  
**Depends On:** T221, T222, T223  
**Description:** Add test data and sample payloads for F-D29: Notification fixtures (invite, payment reminder, past_due), ExternalEvent + Event chains for new `event_types`, and non-persisted Discovery card chain samples. Align `_id`s with persona maps.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`, `configurator/dictionaries/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/discovery_journey_issues.md` — Notification + card catalog
- `../mentorhub/Workshops/customer_journey_issues_adjustments.md` — at least one ExternalEvent + Event chain per new type; Notifications for invite and past_due
- GitHub: [F-D29 #61](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/61)
- `Tasks/PENDING.T221.add_external_event_collection.md` — ExternalEvent schema + `_id` prefix
- `Tasks/PENDING.T222.add_notification_collection.md` — Notification schema + `_id` prefix
- `Tasks/PENDING.T223.add_discovery_card_polymorphic_schema.md` — Card polymorphism (non-persisted)
- `Tasks/scripts/persona_ids.json` — Customer / Profile ObjectIds
- `configurator/test_data/Event.0.1.0.0.json` — append new-type samples without breaking existing activity events
- `configurator/test_data/Customer.0.1.0.0.json` / `Profile.0.1.0.0.json` — optional one `provisioned` pair only if needed for `identity_provisioned` chain; full provisioned seeds are **F-D21**
- **Out of scope:** F-D21/F-D22/F-D24/F-D25 journey-specific seeds beyond F-D29 minimums; Admin/Discovery API code.

### Notification fixtures (minimum)

| Fixture | Scope (typical) | Persona hint |
| --- | --- | --- |
| Invite | `profile` or `customer` | e.g. invite toward a Persevere / ALI member |
| Payment reminder | `customer` | e.g. Stacey / Persevere (`stacey`, `persevere`) |
| Past due | `customer` | e.g. Donny / ScamSoft (`donny`, `scamsoft`) |

Include `message`, `link_metadata`, dismiss state (at least one dismissed + one active), and `created` breadcrumbs.

### Ingress / Event chains

- At least one **ExternalEvent** + related **Event** document for representative new types (need not exhaust every enum value if volume is high — cover ingress, subscription/payment, invite, notification, and GDPR/`profile_redacted` at minimum).
- Reuse ExternalEvent `_id` / `external_id` consistently in Event `context`.

### Card chain samples

- Because Card is **non-persisted**, store illustrative JSON samples that validate against the Card dictionary (path agreed in T223 Execution Notes — e.g. `configurator/samples/` or a non-loaded fixture file). Cover one sample per MVP card type **except** Coordinator.
- Samples should reference real persona Customer/Profile/Notification `_id`s where applicable so Discovery can demo end-to-end locally.

## Goals

- Populate `Notification.0.1.0.0.json` with invite, payment-reminder, and past_due fixtures.
- Populate `ExternalEvent.0.1.0.0.json` and extend `Event.0.1.0.0.json` with ingress-oriented chains.
- Add Discovery card chain sample artifacts (non-persisted) for the MVP catalog.
- Optionally set one Customer/Profile to `provisioned` only if required for an `identity_provisioned` Event — otherwise leave F-D21 to own provisioned seeds.
- Configure-database **SUCCESS** with all of the above.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- Notification / ExternalEvent / Event sub-events SUCCESS; no Card collection created from samples.
- Spot-check seeded Notification scopes and Event `type` values against new enums.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Notification.0.1.0.0.json` — invite, payment reminder, past_due (+ dismiss variants)
- `configurator/test_data/ExternalEvent.0.1.0.0.json` — ingress samples
- `configurator/test_data/Event.0.1.0.0.json` — append new-type Events (preserve existing activity events)
- Card chain sample file(s) under path chosen in T223 (list exact paths in Execution Notes)
- Optional: `configurator/test_data/Customer.0.1.0.0.json` / `Profile.0.1.0.0.json` — only if a provisioned fixture is required here
- `Tasks/PENDING.T224.seed_notification_and_ingress_test_data.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

*(Reserved for the execution agent.)*
