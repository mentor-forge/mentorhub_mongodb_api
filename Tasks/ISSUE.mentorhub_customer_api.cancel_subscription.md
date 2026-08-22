# ISSUE — mentorhub_customer_api: E7 Portal cancel and cancel_at_period_end (F-D27 follow-on)

**Status:** Pending (human files GitHub issue; not orchestrated from mongodb_api)  
**Type:** Feature  
**Depends On:** F-D27 cancel seeds (T243–T245) shipped in `mentorhub_mongodb_api`  
**Description:** Copy-paste GitHub issue fragment for Customer API E7: Portal cancel consumer, `cancel_at_period_end`, gated routes, cancel Notification. File only if F-CA09 is not already scoped for cancel.

## Path Anchoring

Sibling repo: `mentorhub_customer_api`. This file lives only in `mentorhub_mongodb_api/Tasks/` as an external follow-on prompt.

## Context

- `../mentorhub/Workshops/customer_journey_issues.md` — E7; F-CA09 honor `cancel_at_period_end`
- GitHub data: [F-D27 #59](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/59)
- Seeds: harbor `active` + `cancel_at_period_end`; scamsoft `subscriptions[].status: canceled`; Discovery cancel Notification

## Issue body (paste into Customer API if F-CA09 does not already cover E7)

```text
Title: F-CA09 (E7 slice): Portal cancel, cancel_at_period_end, and access gate

Create @_PLANNING.md tasks to implement this issue. Only create tasks, do not execute tasks, do not edit any files outside of the @tasks folder.

Repository: mentor-forge/mentorhub_customer_api

Description:
E7 cancel via Customer Portal. Admin ingress receives Stripe webhooks; this
service consumes normalized events. mongodb_api F-D27 adds
subscriptions[].cancel_at_period_end and seeds harbor (scheduled cancel,
status still active until current_period_end) and scamsoft (status canceled).

Goals:
- Portal session for cancel; consumer for customer.subscription.updated / deleted.
- Persist cancel_at_period_end; keep status active until period end when Stripe does.
- After canceled: require_active_subscription 403 on gated routes; Resubscribe CTA data.
- Write Notification on cancel for Discovery; do not treat success URL as canceled.
- No production webhook signature verification on Customer API.

Depends on: F-D27 (#59); F-CA06; F-AA01; F-D29.
Context: Workshops/customer_journey_issues.md E7
```

## Testing Expectations

N/A — external issue only. Record the filed GitHub URL in Execution Notes after a human creates it.

## Outputs

- None in this repository (issue filed manually in `mentorhub_customer_api`).

## Execution Notes

_(Record filed issue URL here after a human creates it.)_
