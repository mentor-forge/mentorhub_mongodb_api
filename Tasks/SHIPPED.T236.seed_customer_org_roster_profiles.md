# T236 – Seed Customer/Profile roster fixtures for org home (F-D23)

**Status:** Shipped  
**Type:** Feature  
**Depends On:** none  
**Description:** Seed **Customer org roster** fixtures joined only by **`Profile.customer_id`**: populated subscribed orgs, unsubscribed Choose-a-plan orgs, a **subscribed empty mentee roster**, and a **mentee with no Encounter activity**. No Dashboard collection; not Discovery notification/dashboard cards. Pre-release: edit `Customer.0.1.0.0.json` / `Profile.0.1.0.0.json` in place.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`, `README.md`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/customer_journey_issues.md` — Experience **E3** (Customer org home, not platform landing); F-D23 issue text
- `../mentorhub/Workshops/customer_journey_issues_adjustments.md` — F-D23: Customer SPA roster/commerce views; Encounter/Event activity for mentee list; **not** Discovery notification cards
- GitHub: [F-D23 #55](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/55)
- Prerequisites (already on `main`): Dashboard dropped (`Tasks/SHIPPED.T219`); Customer `subscriptions[]` (`Tasks/SHIPPED.T230`); personas + Path A pairs (`Tasks/SHIPPED.T211`, `Tasks/SHIPPED.T233`)
- `Tasks/scripts/persona_ids.json` — register any new Customer/Profile `_id`s
- `configurator/test_data/Customer.0.1.0.0.json` — extend in place; **do not** flip existing `subscriptions[].status` (past_due/canceled belong to later F-D tickets)
- `configurator/test_data/Profile.0.1.0.0.json` — extend in place; unique `full_name` / `email` / `cognito_sub`
- **Out of scope:** Encounter / Event files (T237 / T238); Notification / ExternalEvent / Discovery card samples; Dashboard Configuration/Dictionary/Test Data (must stay **deleted**); invite persistence (F-D24); Payment / Setting catalog edits; GDPR fields

### Cross-task conventions (T236–T238)

Roster for Customer org home is **`Profile` where `customer_id` = JWT Customer `_id`**. Encounter activity joins `Encounter.mentee_id` → Profile. Event activity uses `Event.context.profile_id` (and may include `customer_id` on **new** Events in T238). Do **not** reintroduce a Dashboard collection.

Suggested unused ids (valid 24-hex; **confirm unused in the target collection** before write — Rating/Note may reuse the same hex in other collections):

| Kind | Suggested `_id` | Slug |
| --- | --- | --- |
| Customer | `D00000000000000000000011` | `harbor` |
| Profile (owner) | `A00000000000000000000018` | `helen` |
| Profile (empty-activity mentee) | `A00000000000000000000019` | `pat` |

### Existing coverage to **keep** (do not strip)

| Customer | `_id` | Commerce | Roster today | E3 use |
| --- | --- | --- | --- | --- |
| persevere | `D…02` | **active** sub (growth qty 5) | Stacey, Emma, Margaret, Daniel | Populated subscribed roster |
| supersoft | `D…07` | **active** sub (starter qty 2) | Eddy, Lucky, Danny | Populated subscribed roster |
| mary | `D…01` | **unsubscribed** `[]` | Mary (customer+mentee) | Choose a plan **with** mentee history |
| northstar | `D…10` | no `subscriptions` field | Nora (owner only) | Choose a plan + empty mentee list |
| scamsoft | `D…08` | **unsubscribed** `[]` | Donny only | Unsubscribed empty mentee list |
| ali | `D…06` | **unsubscribed** `[]` | operators + archived Linda | Not the primary E3 demo org |
| provisioned-org-path-a | `D…09` | none | patha-owner | Leave as E1 stub |

### Gaps this task fills

1. **Subscribed + empty mentee roster** — no current active-sub Customer has zero mentee-role Profiles. Add **harbor** + **helen** (customer role only).
2. **Mentee row with empty activity** — Daniel / Lucky / Mary / Linda all have Encounters. Add **pat** under persevere (`roles: ["mentee"]`, `mentor_id` → Paula `A…10`) with **no** Encounter (T237 must not add one).
3. **Commerce empty `subscriptions[]`** — add `subscriptions: []` on **northstar** (and provisioned-org if still omitted) so Choose-a-plan is an empty array, not a missing field. Do **not** add `stripe_customer_id` or a paid `subscriptions[]` entry on northstar (E1 unsubscribed enriched owner).

### Seed expectations (minimum)

**Harbor Customer (`D…11`)** — copy T230 **supersoft starter** shape (Setting Product `e00000000000000000000001`): `status: active`, `stripe_customer_id` like `cus_test_harbor`, one `subscriptions[]` entry `status: active`, `subscription: starter`, `quantity` / `mentee_count` ≥ Product `minimum_members` (1), unique `stripe_subscription_id`. Unique `name` (`harbor`).

**Helen Profile (`A…18`)** — `roles: ["customer"]` only; `customer_id` → harbor; `status: active`; unique `full_name` / `email` (`helen@mentor-forge.dev`); `cognito_sub` present; `mentor_id` omitted. **No** mentee role.

**Pat Profile (`A…19`)** — `roles: ["mentee"]`; `customer_id` → persevere `D…02`; `mentor_id` → Paula `A00000000000000000000010`; `status: active`; unique `full_name` / `email`. **Do not** add Mentee / Journey / Note / Rating documents (roster member who has not started mentoring).

Preserve all existing Customer and Profile documents and `_id`s.

## Goals

- Customer → Profile graph supports E3 **roster list** and **empty states** via `Profile.customer_id` only.
- Harbor is subscribed with **zero** mentee-role Profiles; Pat is a persevere mentee with **zero** Encounters after T237.
- Northstar remains unsubscribed (`subscriptions: []`) for Choose-a-plan + empty mentee list.
- Register new ids in `persona_ids.json`; document harbor / helen / pat on `README.md` Test Personas (do not invent version bumps).
- Configure-database **SUCCESS**. No Dashboard artifacts. No Notification seeds.

## Testing Expectations

```sh
make dev
# If host port 27017 is busy, use compose ports !override (e.g. host 27018) as in prior F-D tasks.
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- Customer / Profile CFG SUCCESS.
- Spot-check:
  - harbor Customer has `subscriptions[0].status: active`; **no** Profile with `roles` containing `mentee` and `customer_id` → harbor.
  - pat Profile `customer_id` → persevere; `roles` includes `mentee`.
  - northstar `subscriptions` is `[]`.
  - persevere / supersoft still have mentee-role Profiles (Daniel, Lucky).
- Grep `configurator/` for `configurations/Dashboard`, `dictionaries/Dashboard`, `test_data/Dashboard` — expect **none**.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Customer.0.1.0.0.json` — harbor + `subscriptions: []` on northstar (and provisioned-org if needed)
- `configurator/test_data/Profile.0.1.0.0.json` — helen + pat
- `Tasks/scripts/persona_ids.json` — harbor / helen / pat ids
- `README.md` — Test Personas tables (customers + persona matrix only)
- `Tasks/PENDING.T236.seed_customer_org_roster_profiles.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

**Plan:** Extend Customer/Profile seeds in place (no version bumps). Confirm suggested `_id`s unused in the **target** collection, then: (1) append **harbor** Customer `D…11` with T230 supersoft starter shape (`stripe_customer_id: cus_test_harbor`, one `subscriptions[]` entry `status: active`, Product `e…01` starter, `quantity`/`mentee_count` = 1 ≥ `minimum_members`); (2) set `subscriptions: []` on **northstar** and **provisioned-org-path-a** (empty array, not missing; no `stripe_customer_id`); (3) append **helen** Profile `A…18` (`roles: ["customer"]` only, `customer_id` → harbor, unique `full_name`/`email`/`cognito_sub`, no `mentor_id`); (4) append **pat** Profile `A…19` (`roles: ["mentee"]`, `customer_id` → persevere `D…02`, `mentor_id` → Paula `A…10`, no Mentee/Journey/Note/Rating/Encounter docs). Preserve every existing Customer/Profile document and `_id`. Do **not** flip existing `subscriptions[].status`. Register ids in `persona_ids.json`; document harbor/helen/pat on README Test Personas (customers + persona matrix only). No Dashboard/Notification seeds. Configure-database SUCCESS; skip packaging (`make down` / `make container` / `mh up mongodb`) so later tasks can reuse `:8385`.

**IDs used** (confirmed unused in Customer / Profile before write; Rating may reuse `D…11` in another collection)

| Kind | `_id` | Notes |
| --- | --- | --- |
| Customer harbor | `D00000000000000000000011` | starter `active`; `cus_test_harbor`; `sub_test_harbor_starter`; qty/mentee_count 1 |
| Profile helen | `A00000000000000000000018` | harbor owner; `roles: ["customer"]`; no mentee; no `mentor_id` |
| Profile pat | `A00000000000000000000019` | persevere mentee; Paula `A…10`; **zero** Encounters (T237 must keep this) |

**Preserved:** all existing Customers (`D…01`–`D…10`) and Profiles (`A…01`–`A…17`); persevere growth `active` / supersoft starter `active` statuses unchanged.

**Testing results**

- Reused already-running local configurator `:8385` (compose `mentorhub_mongodb_api-mongodb-1` on host `:27017`; no `make dev`, no port override). Packaging skipped (`make down` / `make container` / `mh up mongodb`) so later sequential tasks can reuse `:8385`.
- `DELETE /api/database/` → HTTP 200, `status: SUCCESS`.
- `POST /api/configurations/` → HTTP 200, top-level `status: SUCCESS` (`CFG-07-PROCESS_ALL`); zero FAILURE events.
- `CFG-05-Customer.yaml` SUCCESS (8 docs, includes `D…11`); `CFG-05-Profile.yaml` SUCCESS (19 docs, includes `A…18` / `A…19`).
- Spot-check (mongosh `mentor_hub`):
  - harbor `D…11`: `subscriptions[0].status: active`, starter, `cus_test_harbor`, `sub_test_harbor_starter`, qty/mentee_count 1.
  - **no** Profile with `roles` containing `mentee` and `customer_id` → harbor (helen only, `roles: ["customer"]`).
  - pat `A…19`: `customer_id` → persevere `D…02`; `roles: ["mentee"]`; `mentor_id` → Paula `A…10`; **0** Encounters.
  - northstar `D…10` `subscriptions: []` (no `stripe_customer_id`); provisioned-org-path-a also `[]`.
  - persevere still has Daniel mentee; supersoft still has Lucky mentee.
- Grep `configurator/` for `configurations/Dashboard`, `dictionaries/Dashboard`, `test_data/Dashboard` — **none**. No Dashboard collections in Mongo.

**Orchestrator confirmation:** `DELETE`/`POST` on `:8385` re-ran SUCCESS. Spot-check: harbor active qty 1, 0 harbor mentees, pat 0 Encounters, northstar `[]`, Daniel/Lucky mentees present, Customer 8 / Profile 19.

**Follow-ups**

- T237: do **not** add any Encounter with `mentee_id` → pat `A00000000000000000000019`. Pat must remain zero-activity after T237.
- T238: Event activity for roster list; harbor has no mentee-role Profiles; pat has no Encounter to hang Events on.
- T241: northstar `D00000000000000000000010` already has `subscriptions: []` (Choose-a-plan); do not add `stripe_customer_id` or a paid entry.
