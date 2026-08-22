# T233 – Seed provisioned + enriched primary-owner Customer/Profile pairs (F-D21)

**Status:** Shipped  
**Type:** Feature  
**Depends On:** T231, T232  
**Description:** Seed **provisioned** (minimal Admin-ingress) and **enriched** (post–Customer API) primary-owner **Customer + Profile** pairs for E1 / F-CA05 integration tests. Align `_id`s with `persona_ids.json` style (valid 24-hex ObjectIds). No Card fixtures; no GDPR fields.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/customer_journey_issues.md` — E1 Actions; Path A outcome
- `../mentorhub/Research/cognito.md` — Path A: roles `["customer"]`, `mentor_id` empty; idempotent on sub/email
- GitHub: [F-D21 #53](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/53)
- `Tasks/PENDING.T231.extend_profile_for_cognito_primary_registration.md` — `cognito_sub` + indexes
- `Tasks/PENDING.T232.confirm_customer_for_primary_org_provisioning.md` — Customer confirm
- `Tasks/SHIPPED.T224.seed_notification_and_ingress_test_data.md` — deferred full provisioned seeds to F-D21
- `Tasks/scripts/persona_ids.json` — existing Customer/Profile ObjectIds (do not reuse collisions)
- `configurator/test_data/Customer.0.1.0.0.json` / `Profile.0.1.0.0.json` — extend in place (pre-release)
- **Out of scope:** Dense billing/subscription seeds (F-D22); invite Path B members (F-D24); Notification/ExternalEvent beyond existing F-D29; Admin/Customer API code

### Seed expectations (minimum)

**Pair A — provisioned (ingress stub)**

| Collection | Expectations |
| --- | --- |
| Customer | `status: provisioned`; minimal/placeholder `name` (must remain unique); optional empty `description`; breadcrumbs |
| Profile (owner) | `status: provisioned`; `customer_id` → that Customer; `roles: ["customer"]`; `mentor_id` omitted or null-safe empty per schema; `email` + `cognito_sub` set (fake test sub); `email_verified` as appropriate for post-confirm; `full_name` unique; IdP `name` set |

**Pair B — enriched (post F-CA05)**

| Collection | Expectations |
| --- | --- |
| Customer | `status: active`; org `name` / `description` filled as enriched company |
| Profile (owner) | `status: active`; same linkage pattern; `full_name` / `email` enriched; `cognito_sub` present; claims fields populated for JWT demos |

Prefer **new** Customer + Profile `_id`s (unused hex — e.g. next free `D0…` / `A0…` slots) over mutating mary/persevere personas. Record chosen ids in Execution Notes and optionally extend `Tasks/scripts/persona_ids.json` if that file is listed in Outputs.

Respect Profile unique `full_name` (and any new unique `email` / `cognito_sub` indexes from T231).

## Goals

- Append provisioned + enriched primary-owner pairs to Customer and Profile test data.
- Configure-database **SUCCESS**.
- Do not introduce Card or GDPR documents/fields.

## Testing Expectations

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- Spot-check: ≥1 Customer + Profile with `status: provisioned` linked by `customer_id`; ≥1 enriched `active` owner pair with `cognito_sub`.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Customer.0.1.0.0.json` — provisioned + enriched Customer docs
- `configurator/test_data/Profile.0.1.0.0.json` — matching owner Profiles
- Optional: `Tasks/scripts/persona_ids.json` — only if new ids are registered there
- `Tasks/PENDING.T233.seed_provisioned_and_enriched_primary_owner_pairs.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

### Chosen ObjectIds

Verified unused as Customer/Profile `_id`s (Rating already reuses `D0…09`/`D0…10` as Rating `_id`s — same cross-collection pattern as scamsoft `D0…08`). Profiles `A0…16` / `A0…17` free.

| Pair | Role | Customer `_id` | Profile `_id` | Customer `name` | Profile IdP `name` |
| --- | --- | --- | --- | --- | --- |
| A (provisioned) | Admin ingress stub | `D00000000000000000000009` | `A00000000000000000000016` | `provisioned-org-path-a` | `patha-owner` |
| B (enriched) | post F-CA05 | `D00000000000000000000010` | `A00000000000000000000017` | `northstar` | `nora` |

Registered in `Tasks/scripts/persona_ids.json`. Did **not** mutate mary/persevere.

### Seed contents

- **Pair A:** Customer `status: provisioned`, no description; Profile `status: provisioned`, `roles: ["customer"]`, `mentor_id` omitted, `email` + `cognito_sub` (UUID-like word) + `email_verified: true`, unique `full_name` `Path A Owner`.
- **Pair B:** Customer `status: active` with org name/description; Profile `status: active`, linked `customer_id`, claims fields (`name`, `full_name`, `email`, `email_verified`, `cognito_sub`, `roles`), plus enrichment (`description`, `goals`, `interests`, `experience`).
- No Card, GDPR fields, or F-D22 billing seeds.

### Verification

- Local configurator (`docker compose` + `/tmp/mh-mongo-port-override.yaml` host **27018**; INPUT_FOLDER mount): `DELETE /api/database/` → HTTP 200, `status: SUCCESS`.
- `POST /api/configurations/` → HTTP 200, top-level `status: SUCCESS`; Customer/Profile CFG SUCCESS; fail_count 0.
- Spot-check: provisioned Customer `D0…09` ↔ Profile `A0…16` (`customer_id`, `cognito_sub`); enriched active Customer `D0…10` ↔ Profile `A0…17` with `cognito_sub`.
- `make container` → image `ghcr.io/mentor-forge/mentorhub_mongodb_api:latest` (test_data layer rebuilt).
- `mh up mongodb` → packaged API + SPA healthy.
