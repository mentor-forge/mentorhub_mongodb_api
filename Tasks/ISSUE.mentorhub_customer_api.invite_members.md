# ISSUE — mentorhub_customer_api: F-CA08 Invite members (F-D24 follow-on)

**Status:** Pending (human files GitHub issue; not orchestrated from mongodb_api)  
**Type:** Feature  
**Depends On:** F-D24 Path B Profile seeds (T239) shipped in `mentorhub_mongodb_api`  
**Description:** Copy-paste GitHub issue body for Customer API Path B invites: create Profile under inviter `customer_id`, then Cognito AdminCreateUser with JWT claim attributes. Invitation state is `Profile.status` only.

## Path Anchoring

Sibling repo: `mentorhub_customer_api`. This file lives only in `mentorhub_mongodb_api/Tasks/` as an external follow-on prompt.

## Context

- `../mentorhub/Workshops/customer_journey_issues.md` — E4; F-CA08 issue text
- `../mentorhub/Research/cognito.md` — Path B
- GitHub data: [F-D24 #56](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/56)
- Data: **Profile** (`profile_status`: `provisioned` pending, `active` accepted, `archived` revoked) + **Notification** (F-D29). No Invite collection.

## Issue body (paste into Customer API)

```text
Title: F-CA08: E4 Invite members — Cognito AdminCreateUser under inviter customer_id

Create @_PLANNING.md tasks to implement this issue. Only create tasks, do not execute tasks, do not edit any files outside of the @tasks folder.

Repository: mentor-forge/mentorhub_customer_api

Description:
Primary user invites org members by name + email. The Profile is the invite
record (mentorhub_mongodb_api F-D24). Create Profile under inviter customer_id,
then AdminCreateUser with custom:profile_id, custom:customer_id, custom:roles.
Dev path per local_dev_mocks.md when COGNITO_ENABLED=false.

Invitation state is existing Profile.status only — do not add an Invite
collection or invite_status field:
- pending → provisioned (created, invitee has not completed Hosted UI)
- accepted → active (first login / password set)
- revoked → archived (and disable Cognito user)

Goals:
- POST invite: create Profile (customer_id from JWT, never from body alone;
  roles ["customer"]; mentor_id unset) then AdminCreateUser.
- GET list: Profiles for JWT customer_id, filterable by status
  (provisioned / active / archived).
- Optional revoke: set Profile.status archived; disable Cognito user.
- Idempotent re-invite on same email + customer_id (unique Profile.email);
  resend Cognito invite, no duplicate Profile.
- Reject emails already bound to another customer; optional seat check vs
  Customer.subscriptions[].
- Write Notification on invite (profile or customer scope) for Discovery F-DS01.
- Emit invite_created (and invite_accepted when the Profile becomes active).
- Cognito AdminCreateUser remains Customer API; Admin ingress only for Path A
  external signup provisioning.
- No GDPR request property; no Dashboard APIs; no Invite collection.

Depends on: F-D24 (#56); F-CA05; F-S01; F-UA12; F-D29.
Context: Workshops/customer_journey_issues.md E4; Research/cognito.md Path B
```

## Testing Expectations

N/A — external issue only. Record the filed GitHub URL in Execution Notes after a human creates it.

## Outputs

- None in this repository (issue filed manually in `mentorhub_customer_api`).

## Execution Notes

_(Record filed issue URL here after a human creates it.)_
