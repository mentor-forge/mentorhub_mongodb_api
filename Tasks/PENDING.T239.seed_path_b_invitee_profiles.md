# T239 – Seed Path B invitee Profiles using profile_status (F-D24)

**Status:** Pending  
**Type:** Feature  
**Depends On:** T238  
**Description:** Seed Path B member **Profiles** under the inviter’s `customer_id`. Invitation state is **existing `profile_status` only** — `provisioned` (pending), `active` (accepted), `archived` (revoked). Reorder Profile dictionary properties so JWT/claim fields sit together after `_id` (no new fields). Do **not** add an Invite collection, `invite_status`, or any invite-state field. No GDPR property. Pre-release: edit `Profile.0.1.0.yaml` / `Profile.0.1.0.0.json` in place.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/dictionaries/`, `configurator/enumerators/`, `configurator/test_data/`, `README.md`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/customer_journey_issues.md` — E4: API creates Profile then Cognito `AdminCreateUser`; list pending/accepted/revoked
- `../mentorhub/Research/cognito.md` — Path B: Profile under inviter `customer_id`, `roles: ["customer"]`, `mentor_id` omitted; idempotent on email; JWT claims from Profile
- GitHub: [F-D24 #56](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/56)
- Prerequisites (already on `main`): F-D21 `cognito_sub` + unique `email` (`Tasks/SHIPPED.T231`); `profile_status` includes `provisioned` / `active` / `archived` (`Tasks/SHIPPED.T220`); F-D29 Notification schema (`Tasks/SHIPPED.T222`)
- `Tasks/PENDING.T238.seed_roster_event_activity.md` — wait so T236 Profile edits (helen/pat) land first
- `Tasks/PENDING.T236.seed_customer_org_roster_profiles.md` — do **not** reuse helen `A…18` / pat `A…19`; next free Profile ids expected `A00000000000000000000020` / `A…21` (confirm unused)
- `configurator/dictionaries/Profile.0.1.0.yaml` — **reorder only** (see below); no new properties
- `configurator/enumerators/enumerations.0.yaml` — **do not** add `invite_status`; wrap the long `payment_status` `pending` description if still one overlong line
- Unique Profile indexes: `email`, `cognito_sub`, `full_name`
- **Locked design:** The pending member **is** the Profile. UI/API writes Profile, then Cognito with `custom:profile_id`, `custom:customer_id`, `custom:roles`. Org invite list = Profiles with that `customer_id`, filtered by `status`.
- **Out of scope:** Invite collection / `Customer.invites[]`; Notification / Event files (T240); Dashboard; GDPR fields; new Profile/enumerator values

### Profile dictionary property order (no new fields)

HEAD today interleaves `status` after `name` and leaves `customer_id` / `mentor_id` / `roles` / `cognito_sub` at the bottom. Reorder `Profile.0.1.0.yaml` `root.properties` to:

1. `_id`
2. `customer_id`, `mentor_id`, `roles`, `cognito_sub` (JWT / Path A–B claim homes)
3. `name`, `full_name`, `description`, `email`, `email_verified`
4. `goals`, `interests`, `experience` (unchanged nested shapes)
5. `status` (`profile_status`)
6. `created`, `saved`

Keep existing descriptions and types. Fold the root `description` string if the YAML line is overlong. Do **not** add `invited_by` or `invite_status`.

### Invitation state → Profile.status (do not track separately)

| Invite list | `profile_status` | Seed |
| --- | --- | --- |
| pending | `provisioned` | **create** Path B invitee (slug `riley`) under **persevere** (`D…02`) |
| accepted | `active` | **reuse emma** (`A…07`) — already active org member; do not rewrite |
| revoked | `archived` | **create** Path B invitee (slug `quinn`) under persevere, `status: archived` |

Do **not** confuse Path B `riley` with Path A `patha-owner` (`A…16` / Customer `D…09`). Path A provisioned creates a **new** Customer; Path B provisioned joins an **existing** Customer.

Workshop inviter: **Stacey** (`A…08`) / persevere. Record that in README prose if useful; do **not** add `invited_by` on Profile.

### Seed expectations (minimum)

**Riley (`A…20` if free)** — pending invite:

- `status: provisioned`
- `customer_id` → persevere `D00000000000000000000002`
- `roles: ["customer"]`
- `mentor_id` omitted (identifier type; do not use `""`)
- unique `name` / `full_name` / `email` (`riley@mentor-forge.dev`) / `cognito_sub` (fake test sub as if AdminCreateUser already ran)
- `email_verified` as appropriate for invited-not-yet-logged-in (typically `false`)

**Quinn (`A…21` if free)** — revoked invite:

- same Path B shape as riley
- `status: archived`
- unique email / `cognito_sub` / `full_name`

Preserve all existing Profiles. Do not add Mentee / Journey / Encounter documents for riley or quinn.

## Goals

- Persevere has Profiles that demo pending (`provisioned`), accepted (`active` emma), and revoked (`archived`) without an Invite collection or invite-status field.
- Profile dictionary lists claim fields (`customer_id`, `mentor_id`, `roles`, `cognito_sub`) immediately after `_id`, and `status` immediately before breadcrumbs — same properties as today.
- No `Invite.yaml` / `dictionaries/Invite*` / `test_data/Invite*` created.
- Register riley / quinn in `persona_ids.json`; note them on `README.md` Test Personas as Path B invite fixtures (not Sign-in personas until accepted).
- Configure-database **SUCCESS**. No GDPR fields.

## Testing Expectations

```sh
make dev
# If host port 27017 is busy, use compose ports !override (e.g. host 27018) as in prior F-D tasks.
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- Profile CFG SUCCESS.
- Spot-check:

```javascript
db.Profile.find({ customer_id: ObjectId("D00000000000000000000002"), roles: "customer" })
// includes stacey (active), emma (active), riley (provisioned), quinn (archived)
db.Profile.findOne({ name: "riley" }).status  // provisioned
db.Profile.findOne({ name: "quinn" }).status  // archived
```

- Grep `configurator/` for `Invite.yaml`, `dictionaries/Invite`, `invite_status` — expect **none**.
- Grep Customer / Profile dictionaries for `gdpr` — expect none.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/dictionaries/Profile.0.1.0.yaml` — reorder properties as specified (no new fields)
- `configurator/enumerators/enumerations.0.yaml` — wrap `payment_status` `pending` description only (no new enum values)
- `configurator/test_data/Profile.0.1.0.0.json` — append riley + quinn
- `Tasks/scripts/persona_ids.json` — riley / quinn ids
- `README.md` — Test Personas note for Path B invite fixtures
- `Tasks/PENDING.T239.seed_path_b_invitee_profiles.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

_(Reserved for the task execution agent.)_
