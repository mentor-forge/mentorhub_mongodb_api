# T235 – Seed past_due Notification for failed invoice (F-D26)

**Status:** Pending  
**Type:** Feature  
**Depends On:** T234  
**Description:** Add an **active** Discovery **past_due** Notification for the E6 `invoice.payment_failed` Customer (supersoft), plus a `notification_created` Event. Keep the existing dismissed PastDue seed (T224 / scamsoft). Do **not** edit Customer.`subscriptions[]` (F-D25 / F-D27). Pre-release: extend `Notification.0.1.0.0.json` in place.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`, `Tasks/`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./README.md`
- `../mentorhub/Workshops/customer_journey_issues.md` — E6: failed renewal → past_due Notification for Discovery
- `../mentorhub/Workshops/discovery_journey_issues.md` — Notification presentation / dismiss
- GitHub: [F-D26 #58](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/58)
- `Tasks/PENDING.T234.seed_invoice_paid_and_payment_failed_payments.md` — failed Payment + ExternalEvent for supersoft
- `Tasks/SHIPPED.T224.seed_notification_and_ingress_test_data.md` — existing Notifications (`C…001`–`C…005`); `C…003` PastDue is **dismissed** on scamsoft (`D…08`)
- `configurator/dictionaries/Notification.0.1.0.yaml` — `name` (word), `message` (sentence), optional `customer_id`, `link_metadata`, `dismissed` / `cancelled`, `created`, `status`
- `configurator/test_data/Notification.0.1.0.0.json` — append; do not replace
- `Tasks/scripts/persona_ids.json` — `supersoft` Customer `D00000000000000000000007`
- **Out of scope:** Payment / ExternalEvent files (T234); Customer or Profile JSON (F-D21 / F-D25 / F-D27); Setting catalog; Card samples; GDPR fields

### Seed expectations (minimum)

**Notification — active past_due (E6 Discovery banner)**

| Field | Expectation |
| --- | --- |
| `_id` | Next free `C0…` hex (e.g. `C00000000000000000000006` — confirm unused) |
| `name` | `word` (no spaces) e.g. `PastDue` or `InvoicePastDue` |
| `message` | sentence: billing failed / update payment (Discovery copy) |
| `customer_id` | supersoft `D00000000000000000000007` (same Customer as T234 failed Payment) |
| `link_metadata` | Customer SPA billing route (same pattern as T224 PaymentReminder / PastDue) |
| `dismissed` / `cancelled` | **omit** — this fixture must remain undismissed for Discovery |
| `status` | `active` |
| `created` | breadcrumb; `correlation_id` ≤40 chars; align timestamps after T234 failed Payment `created` |

Keep **all** existing Notifications, including dismissed scamsoft PastDue (`C…003`).

**Event (optional but expected)**

- Append one `notification_created` Event referencing the new Notification `_id` and supersoft `customer_id`.
- Continue `F0…` after T234’s last Event `_id`. Preserve **all** existing Events.

## Goals

- Append ≥1 **active** (not dismissed) past_due Notification scoped to the failed-invoice Customer.
- Preserve T224 Notification fixtures.
- Configure-database **SUCCESS**.
- Do not flip Customer subscription status to `past_due` in this ticket.

## Testing Expectations

```sh
make dev
# If host port 27017 is busy, use compose ports !override (e.g. host 27018) as in prior F-D tasks.
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect HTTP **200**, top-level **`status: SUCCESS`**.
- Notification (and Event if updated) CFG SUCCESS.
- Spot-check: ≥1 Notification with `customer_id` → supersoft, past-due copy, **no** `dismissed`; T224 `C…003` still present and dismissed.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `configurator/test_data/Notification.0.1.0.0.json` — append active past_due Notification
- `configurator/test_data/Event.0.1.0.0.json` — append `notification_created` if added; preserve existing
- `Tasks/PENDING.T235.seed_past_due_notification_for_failed_invoice.md` — this file (Execution Notes; rename to `SHIPPED.` when done)

## Execution Notes

*(Reserved for the execution agent.)*
