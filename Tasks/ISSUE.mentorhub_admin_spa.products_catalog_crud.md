# ISSUE — mentorhub_admin_spa: F-AS01 Setting catalog CRUD (Product / Discount) (F-D22 follow-on)

**Status:** Pending (human files GitHub issue; not orchestrated from mongodb_api)  
**Type:** Feature  
**Depends On:** F-D22 Setting dictionary (T227) shipped in `mentorhub_mongodb_api`  
**Description:** Copy-paste GitHub issue body for Admin SPA catalog UI over the polymorphic **Setting** collection (`type: Product` | `type: Discount`). Admin SPA owns list/create/edit; not Customer SPA.

## Path Anchoring

Sibling repo: `mentorhub_admin_spa` (when bootstrapped via F-W18). This file lives only in `mentorhub_mongodb_api/Tasks/` as an external follow-on prompt.

## Context

- `../mentorhub/Workshops/customer_journey_issues.md` — E2; catalog shared with Admin SPA
- GitHub data: [F-D22 #50](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/50)
- Cross-SPA linking: F-US09 (`mentorhub_spa_utils`)
- Data: single Mongo collection **Setting** (not separate Product/Discount collections)

## Issue body (paste into Admin SPA / mentorhub as appropriate)

```text
Title: F-AS01: Admin SPA Setting catalog CRUD — Product and Discount (E2 / F-D22)

Create @_PLANNING.md tasks to implement this issue. Only create tasks, do not execute tasks, do not edit any files outside of the @tasks folder.

Repository: mentor-forge/mentorhub_admin_spa

Description:
Admin SPA CRUD for MentorHub plan offerings and discount codes. Data lives in
mentorhub_mongodb_api F-D22 as a polymorphic Setting collection (type: Product |
type: Discount) — not separate Product/Discount Mongo collections.

Goals:
- List/create/edit Settings filtered by type (Product, Discount) wired to Admin API.
- Product fields: minimum_members, subscription, unit_price, stripe_price_id
  (+ name/description/status).
- Discount fields: code, free_encounters, status, description, expires_at,
  max_redemptions.
- Use universal nav / cross-repo links from F-US09 when available.
- No Customer SPA Product/Discount admin routes.

Depends on: F-D22 Setting dictionary (T227); F-W18 Admin SPA bootstrap; F-US09.
Context: Workshops/customer_journey_issues.md E2; F-D22 #50; Setting bag decision
```

## Execution Notes

*(Record filed issue URL here after a human creates it.)*
