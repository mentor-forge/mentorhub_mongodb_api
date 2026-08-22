# ISSUE — mentorhub_customer_api: E5 capacity-change Checkout / subscription.updated (F-D25 follow-on)

**Status:** Pending (human files GitHub issue; not orchestrated from mongodb_api)  
**Type:** Feature  
**Depends On:** F-D25 capacity seeds (T241–T242) shipped in `mentorhub_mongodb_api`  
**Description:** Copy-paste GitHub issue fragment for Customer API E5 capacity: update `subscriptions[]` quantity from Checkout/Portal webhooks. Full E5–E7 API surface may already live in F-CA09 — file only if that issue is not scoped for capacity.

## Path Anchoring

Sibling repo: `mentorhub_customer_api`. This file lives only in `mentorhub_mongodb_api/Tasks/` as an external follow-on prompt.

## Context

- `../mentorhub/Workshops/customer_journey_issues.md` — E5; F-CA09
- GitHub data: [F-D25 #57](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/57)
- Seeds: persevere growth qty 5 → 8 still `active`; Payment + `customer.subscription.updated`

## Issue body (paste into Customer API if F-CA09 does not already cover E5)

```text
Title: F-CA09 (E5 slice): Capacity-change Checkout and subscription.updated consumer

Create @_PLANNING.md tasks to implement this issue. Only create tasks, do not execute tasks, do not edit any files outside of the @tasks folder.

Repository: mentor-forge/mentorhub_customer_api

Description:
E5 mid-lifecycle seat changes. Admin ingress receives Stripe webhooks; this
service consumes normalized events and updates Customer.subscriptions[]
quantity / mentee_count / total_cost. Status stays active (past_due / canceled
are E6 / E7).

Use mongodb_api F-D25 seeds: persevere growth quantity 8 after a capacity
Payment; original T230 qty 5 Payments remain history.

Goals:
- Capacity Checkout session (quantity >= Product.minimum_members) and/or Portal.
- Event consumer: customer.subscription.updated (+ checkout.session.completed /
  invoice.paid proration) → sync subscriptions[] ; persist Payment.
- Never trust success URL as paid; no production webhook verify on Customer API.
- Do not implement past_due / cancel in this slice if those are separate F-CA09 tasks.

Depends on: F-D25 (#57); F-CA06; F-AA01.
Context: Workshops/customer_journey_issues.md E5
```

## Testing Expectations

N/A — external issue only. Record the filed GitHub URL in Execution Notes after a human creates it.

## Outputs

- None in this repository (issue filed manually in `mentorhub_customer_api`).

## Execution Notes

_(Record filed issue URL here after a human creates it.)_
