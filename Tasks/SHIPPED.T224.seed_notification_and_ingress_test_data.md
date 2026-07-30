# T224 – Seed Notification, ingress Event chains, and card samples (F-D29)

**Status:** Shipped  
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

| Fixture | `scope_id` one_of (typical) | Persona hint |
| --- | --- | --- |
| Invite | `profile_id` or `customer_id` | e.g. invite toward a Persevere / ALI member |
| Payment reminder | `customer_id` | e.g. Stacey / Persevere (`stacey`, `persevere`) |
| Past due | `customer_id` | e.g. Donny / ScamSoft (`donny`, `scamsoft`) |

Include `name`, `message` (no `description`), `link_metadata`, `dismissed` / `cancelled` breadcrumbs where relevant (at least one dismissed + one active), and `created`.

### Ingress / Event chains

- At least one **ExternalEvent** + related **Event** document for representative new types (need not exhaust every enum value if volume is high — cover ingress, subscription/payment, invite, notification, and GDPR/`profile_redacted` at minimum).
- Reuse ExternalEvent `_id` / `external_id` consistently in Event `context`.

### Card chain samples

- Card is non-persisted (`0.0.0.0` per T223). Store illustrative JSON samples that validate against the Card dictionary (path from T223 Execution Notes).
- Cover **three** samples only: one **Customer**, one **Profile**, one **Notification** card (no Mine/Other/role splits).
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
- Spot-check seeded Notification `scope_id` variants and Event `type` values against new enums / one_of shapes.

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

**Plan:** Seed Notification / ExternalEvent fixtures, append Event chains for new `event_types`, and add non-persisted Card samples under `configurator/samples/`. Leave Customer/Profile statuses unchanged (F-D21). Verify local configure-database then package via `make container` + `mh up mongodb`.

**Notification `_id` prefix:** T222 planned `N0…`, but `N` is not valid ObjectId hex. Seeds use **`C0…`** (`C00000000000000000000001` … `C00000000000000000000005`), distinct from Mentee `CC…` ids. ExternalEvent keeps **`E0…`** (same hex family as Encounter; uniqueness is per-collection). New Events continue **`F0…`** from `F…0175`.

**Notification fixtures (5):**

| `_id` | `name` | `scope_id` | Notes |
| --- | --- | --- | --- |
| C…001 | InviteMember | `profile_id` → daniel | active invite |
| C…002 | PaymentReminder | `customer_id` → persevere | active |
| C…003 | PastDue | `customer_id` → scamsoft | **dismissed** |
| C…004 | MentorDigest | `mentor_id` → paula | **cancelled** |
| C…005 | PlatformNotice | `global` breadcrumb | active |

`name` is type `word` (no spaces, ≤40). Breadcrumb `correlation_id` also ≤40.

**ExternalEvent fixtures (5):** cognito provision, stripe past_due, stripe checkout, cognito invite, cognito GDPR redact — sources `stripe` \| `cognito`.

**Event append (17 docs, F…0175–F…0191):** preserves prior 174 activity/login events. Covers `external_received`, `identity_provisioned`, `organization_enriched`, `subscription_changed`, `payment_recorded`, `invite_created`, `invite_accepted`, `notification_created`, `notification_dismissed`, `profile_redacted`. `identity_provisioned` is illustrative only — no Customer/Profile flipped to `provisioned`.

**Card samples:** `configurator/samples/Card.chain.json` — three one_of payloads (Customer / Profile / Notification). `Card.yaml` `test_data` remains `null`; samples are **not** loaded into Mongo. Dockerfile does not COPY `samples/` (repo-local illustrative artifacts).

**Changes**

- Populated `Notification.0.1.0.0.json` (5 docs).
- Populated `ExternalEvent.0.1.0.0.json` (5 docs).
- Appended 17 Events to `Event.0.1.0.0.json` (191 total).
- Created `configurator/samples/Card.chain.json`.
- Did not modify Customer/Profile provisioned status.

**Testing results**

- Local configurator (Mongo host `:27018` override): `DELETE /api/database/` → HTTP 200 SUCCESS; `POST /api/configurations/` → HTTP 200, top-level `status: SUCCESS`; `CFG-05-Notification.yaml`, `CFG-05-ExternalEvent.yaml`, `CFG-05-Event.yaml`, `CFG-05-Card.yaml` SUCCESS.
- Spot-check: Notification=5 (scope keys profile/customer/mentor/global; dismissed+cancelled present); ExternalEvent=5 (stripe+cognito); Event=191; `HAS_Card=false`.
- `make container` → image includes Notification/ExternalEvent test_data under `/input`.
- `mh up mongodb` → API :8383 lists Notification/ExternalEvent/Card/Event; packaged mongo `HAS_Card=false`, Notification=5, ExternalEvent=5, Event=191; packaged DROP → 403 as expected.
