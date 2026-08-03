# T231 – Extend Profile for Cognito primary self-registration (F-D21)

**Status:** Pending  
**Type:** Feature  
**Depends On:** none  
**Description:** Confirm Profile already carries JWT/Cognito claim homes (`name`, `customer_id`, `mentor_id`, `roles`, `email`, `full_name`, `email_verified`) and add **`cognito_sub`** plus indexes so Admin ingress / Customer API can idempotently provision Path A owners. Prefer add over rename. No Card; no GDPR request fields. Pre-release: edit `Profile.0.1.0` in place.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/dictionaries/`, `configurator/configurations/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/customer_journey_issues.md` — E1 Path A; F-D21 issue text
- `../mentorhub/Research/cognito.md` — Path A; idempotent on Cognito `sub` / email; Hosted UI → claims
- GitHub: [F-D21 #53](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/53)
- Prerequisites (already on `main`): F-D-E0 drops; F-D29 `profile_status.provisioned` (`Tasks/SHIPPED.T220`)
- `configurator/dictionaries/Profile.0.1.0.yaml` — current Profile
- `configurator/configurations/Profile.yaml` — unique `full_name`; Last Saved
- `Tasks/SHIPPED.T201.update_profile_schema_for_jwt_claims.md` — `roles` / JWT model
- **External:** Cognito pool custom attributes `custom:profile_id|customer_id|mentor_id|roles` are F-S01 (not this repo); claim *values* come from Profile/`_id` fields
- **Out of scope:** Customer dictionary (T232); seeds (T233); Card collection; `gdpr_*` properties; phone; F-D22 `subscriptions[]`; F-CA05 API code
- **Numbering note:** Task ids start at **T231** so they do not collide with F-D22 `T225`–`T230` on branch `F-D22/E2-product-payment-subscriptions`

### Confirm present (document in Execution Notes; do not remove)

| Field | Role for E1 / F-S01 |
| --- | --- |
| `_id` | → JWT / `custom:profile_id` |
| `name` | IdP username |
| `full_name` | Hosted UI / intake display name |
| `email` / `email_verified` | Sign-up email; verification flag |
| `customer_id` | → `custom:customer_id` (new org for Path A owner) |
| `mentor_id` | → `custom:mentor_id` (empty / unset for primary owner) |
| `roles` | → `custom:roles` (owner: `["customer"]`) |
| `status` | `provisioned` → `active` via `profile_status` (F-D29) |

### Add

| Field | Notes |
| --- | --- |
| `cognito_sub` | Cognito user `sub` (immutable); Path A idempotency key — type per **running configurator** (prefer `sentence` / `word`) |

### Indexes (finalize in Execution Notes)

- Unique **sparse** on `cognito_sub` (when present)
- Unique **sparse** on `email` (idempotency / duplicate sign-up guard) if supported alongside existing unique `full_name`
- Keep Last Saved; do not reintroduce unique `name` unless configurator evidence requires it

Existing Profile test data must still configure (new fields optional) until T233 adds provisioned/enriched fixtures.

## Goals

- Add optional `cognito_sub` to `Profile.0.1.0.yaml`.
- Update `Profile.yaml` indexes for Cognito/`email` idempotency as above.
- Confirm claim-related Profile fields and `provisioned` status already support F-S01 / Path A (record any gaps found via running configurator — do not invent properties beyond `cognito_sub` without Execution Notes justification).
- Do **not** add Card, GDPR, or phone fields.
- Configure-database **SUCCESS** with current Profile test data (schema relaxes).

## Testing Expectations

```sh
make dev
# If host port 27017 is busy, use compose ports !override (e.g. host 27018) as in prior F-D tasks.
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- Profile CFG SUCCESS; new property / indexes appear in process output.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/dictionaries/Profile.0.1.0.yaml` — add `cognito_sub`; confirm claim fields
- `configurator/configurations/Profile.yaml` — indexes if changed
- `Tasks/PENDING.T231.extend_profile_for_cognito_primary_registration.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

*(Reserved for the execution agent.)*
