# T245 – Seed Discovery Notification for subscription cancel (F-D27)

**Status:** Pending  
**Type:** Feature  
**Depends On:** T244, T240  
**Description:** Append Discovery **Notification** (and Event / optional ExternalEvent) for E7 **cancel** — scheduled cancel on harbor and/or fully canceled scamsoft. Prefer append over rewrite. Do **not** replace T235 past_due. Pre-release: edit Notification / Event test data in place.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/customer_journey_issues.md` — E7 cancel Notification; Resubscribe CTA; Discovery is the attention surface
- `../mentorhub/Workshops/customer_journey_issues_adjustments.md` — F-D-E5E7 include Notification fixtures for cancel
- GitHub: [F-D27 #59](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/59)
- `Tasks/PENDING.T244.seed_canceled_subscriptions.md` — harbor `cancel_at_period_end`; scamsoft `canceled`
- `Tasks/PENDING.T240.seed_invite_notification.md` — wait so Notification/Event appends do not collide (T240 may use `C…007`)
- `Tasks/SHIPPED.T235.seed_past_due_notification_for_failed_invoice.md` — keep `C…006` InvoicePastDue
- `configurator/dictionaries/Notification.0.1.0.yaml` — `name` (word), `message` (sentence), `customer_id`, `link_metadata`
- **Out of scope:** Customer JSON (T244); Profile; Payment; GDPR; Dashboard; Invite collection

### Notification (minimum)

Append **≥1 active** cancel Notification (undismissed):

| Field | Expectation |
| --- | --- |
| `_id` | Next free `C0…` after T240 (likely `C00000000000000000000008`) |
| `name` | word e.g. `PlanCanceled` or `CancelScheduled` |
| `message` | sentence: plan ends at period / resubscribe (Discovery copy) |
| `customer_id` | **harbor** (scheduled cancel — still in period) **or** scamsoft (already `canceled`) — prefer harbor if T244 seeded it; document choice |
| `link_metadata` | Customer SPA billing / resubscribe route |
| `dismissed` | **omit** |
| `status` | `active` |

Optional second Notification for the other cancel org. Keep all existing Notifications (invite, past_due, T224).

Do **not** put `cancel_at_period_end` on Notification — Customer.subscriptions[] is source of truth.

### Events / ingress (append only)

Continue `F0…` after T240 / T242. Minimum:

- `notification_created` for the new Notification
- `subscription_changed` with `context.customer_id` and a cancel reason (`cancel_at_period_end` or `canceled`)

Optional ExternalEvent `source: stripe`, `normalized_body.type` `customer.subscription.updated` (or `customer.subscription.deleted`) for the canceled Customer — next free `E…` after T242 (`E…08`+). Unique `external_id`.

Preserve **all** existing Events.

## Goals

- Discovery can show a cancel / scheduled-cancel card for an E7 Customer.
- T235 past_due Notification unchanged.
- Configure-database Notification (and Event / ExternalEvent if updated) **SUCCESS**.

## Testing Expectations

```sh
make dev
# If host port 27017 is busy, use compose ports !override (e.g. host 27018) as in prior F-D tasks.
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- Spot-check: ≥1 active Notification with cancel copy and `customer_id` → harbor or scamsoft; `C…006` still present; ≥1 `subscription_changed` Event for that Customer.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Notification.0.1.0.0.json` — append cancel Notification
- `configurator/test_data/Event.0.1.0.0.json` — append `notification_created` + `subscription_changed`
- Optional: `configurator/test_data/ExternalEvent.0.1.0.0.json` — Stripe cancel webhook sample
- `Tasks/PENDING.T245.seed_cancel_notification.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

_(Reserved for the task execution agent.)_
