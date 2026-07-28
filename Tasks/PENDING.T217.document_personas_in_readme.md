# T217 – Document Personas in README

**Status**: Pending  
**Type**: Feature  
**Depends On**: T211  
**Description**: Add a persistent **Test Personas** section to `README.md` documenting the Developer Edition persona matrix, customers, and mentor relationships. Preserve the existing **Pre-release** section.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- In-repo: `README.md`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `Tasks/PENDING.T209.audit_persona_test_data.md` — final `_id` map (authoritative after audit ships)
- `Tasks/PENDING.T211.rebuild_profile_test_data_for_personas.md` — shipped profile data
- External sync target: `../mentorhub/login.html` + `../mentorhub/welcome-auth.js` (document cross-reference; updated via separate issue — see `ISSUE.mentorhub.login_html_persona_alignment.md`)

## Goals

Add a **Test Personas** section to `README.md` that includes:

0. **Pre-release** — keep the existing section; do not add version-bump or migration guidance to persona docs.
1. **Purpose** — personas are stable fixtures for configure-database seed data, manual SPA testing, and JWT claims on the Developer Edition sign-in page.
2. **Customer organizations** — table with `_id`, slug, display name, and sponsored personas.
3. **Persona matrix** — table with columns: Persona label, Profile `name` slug, `full_name`, Profile `_id`, Roles, Customer, Primary mentor (if mentee), Explanation.
4. **Mentor–mentee relationships** — concise matrix for encounters and scheduling.
5. **Sign-in** — note that `welcome-auth.js` must list the same profiles; link to external issue task for login page updates.
6. **Stable ID policy** — warn that changing Profile `_id` values requires updating Journey, Encounter, Event, and sibling-repo auth mappings.

Use the T209 audit **Execution Notes** and shipped test data as the source of truth — do not document stale slugs (`cat`, `carol`, `luther`, etc.).

### Example table shape (populate with final values)

| Persona | Slug | Roles | Customer | Mentor |
| --- | --- | --- | --- | --- |
| Mary the Super Mentee | `mary` | customer, coordinator, mentee | Mary | Marti |
| … | … | … | … | … |

## Testing Expectations

- Review-only task: no configure-database requirement.
- Verify README renders correctly (tables, links).
- Cross-check documented `_id` values against `Profile.0.1.0.0.json` and `Customer.0.1.0.0.json`.

**Packaging verification:**

```sh
make down
make container
mh up mongodb
```

## Outputs

- `README.md`

## Execution Notes

_(Reserved for task execution agent.)_
