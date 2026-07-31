# ISSUE — mentorhub_admin_spa: F-AS01 Product catalog CRUD (F-D22 follow-on)

**Status:** Pending (human files GitHub issue; not orchestrated from mongodb_api)  
**Type:** Feature  
**Depends On:** F-D22 Product dictionary (T227) shipped in `mentorhub_mongodb_api`  
**Description:** Copy-paste GitHub issue body for Admin SPA Product catalog UI. Product CRUD is **Admin SPA** (F-AS01 ProductsListPage per F-US09), not Customer SPA.

## Path Anchoring

Sibling repo: `mentorhub_admin_spa` (when bootstrapped via F-W18). This file lives only in `mentorhub_mongodb_api/Tasks/` as an external follow-on prompt.

## Context

- `../mentorhub/Workshops/customer_journey_issues.md` — E2; Product catalog shared with Admin SPA
- GitHub data: [F-D22 #50](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/50)
- Cross-SPA linking: F-US09 (`mentorhub_spa_utils`)
- Admin SPA product admin when catalog UI needed (journey implementation order)

## Issue body (paste into Admin SPA / mentorhub as appropriate)

```text
Title: F-AS01: Admin SPA Product catalog CRUD (E2 / F-D22)

Create @_PLANNING.md tasks to implement this issue. Only create tasks, do not execute tasks, do not edit any files outside of the @tasks folder.

Repository: mentor-forge/mentorhub_admin_spa

Description:
Product catalog CRUD for MentorHub plan offerings. Data dictionary ships in
mentorhub_mongodb_api F-D22 (Product collection). Admin SPA owns list/create/edit UI
(ProductsListPage). Customer SPA must not host Product admin CRUD.

Goals:
- Products list / new / edit pages wired to Admin API Product endpoints (when filed).
- Fields align with locked Product shape: minimum_members, subscription, unit_price,
  stripe_price_id (+ standard name/description/status).
- Use universal nav / cross-repo links from F-US09 when available.
- No Customer SPA Product admin routes.

Depends on: F-D22 Product dictionary; F-W18 Admin SPA bootstrap; F-US09.
Context: Workshops/customer_journey_issues.md E2; F-D22 #50
```

## Execution Notes

*(Record filed issue URL here after a human creates it.)*
