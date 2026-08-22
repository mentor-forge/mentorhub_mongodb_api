# T240 – Seed Discovery Notification for Path B invite (F-D24)

**Status:** Shipped  
**Type:** Feature  
**Depends On:** T239  
**Description:** Append an optional Discovery **Notification** (and `invite_created` / `notification_created` Events) for the Path B **pending** Profile (`provisioned` riley). Do **not** persist invite state on Notification or Event — Profile.status remains source of truth. Prefer append over rewrite. No GDPR property.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/customer_journey_issues.md` — E4; Notification on invite for Discovery F-DS01
- `../mentorhub/Workshops/customer_journey_issues_adjustments.md` — F-D24 optional Notification seed
- GitHub: [F-D24 #56](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/56)
- `Tasks/PENDING.T239.seed_path_b_invitee_profiles.md` — riley / quinn `_id`s (Execution Notes after T239)
- `Tasks/PENDING.T238.seed_roster_event_activity.md` — last Event `_id` after F-D23; continue `F0…` from the next free id (before T238 the last id is `F00000000000000000000197`)
- `configurator/test_data/Notification.0.1.0.0.json` — keep T224 `C…001` InviteMember (daniel) and T235 `C…006`; **append** (`C00000000000000000000007` if free)
- `configurator/dictionaries/Notification.0.1.0.yaml` — `name` (word), `message` (sentence), `profile_id` and/or `customer_id`, `link_metadata`
- Existing `event_types`: `invite_created`, `invite_accepted`, `notification_created` — **do not** add `invite_revoked` or `invite_status`
- **Out of scope:** Invite collection; Profile JSON (T239); enumerators; Dashboard; GDPR fields; rewriting T224 Events that reference daniel

### Notification (minimum)

Append **one active** Notification for **riley** (pending / `provisioned`):

| Field | Expectation |
| --- | --- |
| `_id` | Next free `C0…` (e.g. `C…007`) |
| `name` | word e.g. `MemberInvite` |
| `message` | sentence: invited to join Persevere |
| `profile_id` | riley **or** `customer_id` → persevere — pick one; document in Execution Notes |
| `link_metadata` | Customer SPA members/invite route (same pattern as T224 InviteMember) |
| `status` | `active`; do not set `dismissed` |

Do **not** replace `C…001`. Do **not** add invite-status fields on Notification.

### Events (append only)

Continue `F0…` after T238 / any later appends. Minimum:

- one `invite_created` with `context.profile_id` → riley, `context.customer_id` → persevere, `invited_by` → Stacey `A…08` (context only; not a Profile field)
- one `notification_created` for the new Notification `_id`

Do **not** add `invite_revoked`. Do **not** add ExternalEvent rows (T224 already has a cognito invite sample).

## Goals

- Discovery can render an invite card for the pending Path B Profile.
- Invite lifecycle is still only `Profile.status` — Notification is presentation, not state.
- Existing Notification / Event documents retained.
- Configure-database **SUCCESS**. No Invite collection. No GDPR fields.

## Testing Expectations

```sh
make dev
# If host port 27017 is busy, use compose ports !override (e.g. host 27018) as in prior F-D tasks.
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- Notification / Event CFG SUCCESS.
- Spot-check: ≥1 active Notification targeting riley or persevere with invite copy; ≥1 `invite_created` Event for riley; T224 `C…001` still present.
- Grep `configurator/` for Invite collection / `invite_status` — expect none.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Notification.0.1.0.0.json` — append pending-invite Notification
- `configurator/test_data/Event.0.1.0.0.json` — append `invite_created` + `notification_created`
- `Tasks/PENDING.T240.seed_invite_notification.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

**Plan:** Confirm unused Notification hex after T235 `C…006` — `C00000000000000000000007` is free in Notification JSON (keep T224 `C…001` InviteMember / daniel). Confirm unused Event hex after T238 `F…0203` — append `F00000000000000000000204` / `F…0205`. Append one **active** Notification (`name: MemberInvite`, no `dismissed`) targeting **riley** via `profile_id` `A00000000000000000000020` (not `customer_id`; Discovery card is for the pending Path B Profile). Message: invited to join Persevere. `link_metadata` follows T224 InviteMember (`spa: customer`, `route: /invites/accept`, riley invite token). Append Events only: `invite_created` (`context.profile_id` riley, `context.customer_id` persevere `D…02`, `invited_by` Stacey `A…08` in context only) and `notification_created` for `C…007`. Do **not** add `invite_revoked`, Invite collection, ExternalEvent, GDPR, or rewrite T224 daniel Events. Reuse already-running configurator `:8385`; skip packaging so later sequential tasks can reuse it.

**IDs used** (confirmed unused in Notification / Event before write)

| Kind | `_id` | Notes |
| --- | --- | --- |
| Notification MemberInvite | `C00000000000000000000007` | active; `profile_id` → riley `A…20`; no `customer_id` / `dismissed`; T224 `C…001` InviteMember (daniel) retained |
| Event invite_created | `F00000000000000000000204` | riley `A…20`; persevere `D…02`; `invited_by` Stacey `A…08` (context only) |
| Event notification_created | `F00000000000000000000205` | `notification_id` `C…007`; riley + persevere; `reason: invite` |

**Target choice:** `profile_id` → riley (pending Path B Profile). Invite lifecycle remains `Profile.status` only.

**Preserved:** Notification `C…001`–`C…006` unchanged. Event `F…0001`–`F…0203` unchanged. No Invite collection / `invite_status` / `invite_revoked`. No ExternalEvent. No GDPR.

**Testing results**

- Reused already-running local configurator `:8385` (compose on host `:27017`; no `make dev`, no port override). Packaging skipped (`make down` / `make container` / `mh up mongodb`) so later sequential tasks can reuse `:8385`.
- `DELETE /api/database/` → HTTP 200, `status: SUCCESS`.
- `POST /api/configurations/` → HTTP 200, top-level `status: SUCCESS` (`CFG-07-PROCESS_ALL`); zero FAILURE events.
- `CFG-05-Notification.yaml` SUCCESS (7 docs: prior 6 + riley MemberInvite).
- `CFG-05-Event.yaml` SUCCESS (205 docs: prior 203 + invite_created + notification_created).
- Spot-check (mongosh `mentor_hub`):
  - ≥1 active Notification for riley with invite copy (`C…007` MemberInvite, `status: active`, no `dismissed`).
  - ≥1 `invite_created` Event for riley (`F…0204`; `invited_by` Stacey `A…08`).
  - T224 `C…001` InviteMember (daniel `A…02`) still present.
  - `invite_revoked` count 0; no Invite collection.
- Grep `configurator/` for `Invite.yaml` / `dictionaries/Invite` / `invite_status` / `invite_revoked` — **none**.

**Orchestrator confirmation:** `DELETE`/`POST` on `:8385` re-ran SUCCESS. Spot-check: Notification 7; Event 205; `C…007` MemberInvite riley active; `C…001` InviteMember present; `invite_created` for riley 1.

**Follow-ups**

- T242 / T245: last Event `_id` is `F00000000000000000000205`. Next free Event `_id` is `F00000000000000000000206`.
- T245: next free Notification `_id` is `C00000000000000000000008`.
