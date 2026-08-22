# ISSUE mentorhub – Align login.html Personas with MongoDB Seed Data

**Status**: Run as needed  
**Type**: Feature  
**Depends On**: T211 (external prerequisite — Profile seed data must be shipped first)  
**Description**: GitHub issue prompt for updating Developer Edition sign-in personas in the `mentorhub` repository. **Do not execute in this API repo.**

## Path Anchoring

This task is **documentation only**. Implementation happens in the **`mentorhub`** sibling repository.

- Target files (external): `login.html`, `welcome-auth.js`
- Source of truth (this repo): `configurator/test_data/Profile.0.1.0.0.json`, `README.md` Test Personas section (T217)

## Context

- `./Tasks/PENDING.T211.rebuild_profile_test_data_for_personas.md` — shipped Profile personas
- `./Tasks/PENDING.T217.document_personas_in_readme.md` — README persona tables
- `../mentorhub/login.html` — Developer Edition sign-in UI
- `../mentorhub/welcome-auth.js` — static `PROFILES` map minting JWT claims

Today `welcome-auth.js` mirrors the **old** ten-profile seed (includes `luther`, `sam`, `carol`, `cat`, `taylor`). After T211 ships, the PROFILES map must match the new twelve-persona matrix.

## Goals

- Provide a copy-paste **GitHub issue** body for a human to file in `mentorhub`.
- Issue should be filed **after T211 and T217 ship** so claims and README tables are final.

---

## GitHub issue (copy below)

**Title:** Align Developer Edition login personas with MongoDB test data (T211 persona matrix)

**Repository:** `mentor-forge/mentorhub`

### Summary

Update `welcome-auth.js` (and `login.html` if persona grouping or labels need UX improvement) so Developer Edition JWT minting matches the persistent persona matrix shipped in `mentorhub_mongodb_api` Profile seed data.

### Background

MongoDB configure-database seed data now defines **twelve stable personas** across four customers (Mary, Persevere, ALI, SuperSoft). Journey SPAs, domain API E2E tests, and manual QA depend on `login.html` emitting JWT claims (`profile_id`, `customer_id`, `mentor_id`, `roles`) that match Profile documents exactly.

Reference: `mentorhub_mongodb_api` README **Test Personas** section (T217) and `configurator/test_data/Profile.0.1.0.0.json`.

### Required changes

1. **Replace `PROFILES` in `welcome-auth.js`**
   - Remove deprecated entries: `luther`, `sam`, `carol`, `cat`, `taylor`.
   - Add personas: `stacey`, `emma`, `special`, `money`, `entrepreneur`, `devlead`, `srdev`.
   - Update existing entries so `roles`, `customer_id`, and `mentor_id` match Profile seed data:
     - **mary** — roles: `customer`, `coordinator`, `mentee`; customer: Mary; mentor: Marti
     - **daniel** — mentee; customer: Persevere; mentor: Special
     - **lucky** — mentee; customer: SuperSoft; mentor: Sr. Dev
     - **mike** — all roles; customer: ALI

2. **Labels**
   - Use persona display names from README (e.g. "Emma the Coordinator", "Stacey the CEO", "Money Mentor").

3. **Optional `login.html` UX**
   - Group `<select>` options by customer (Mary / Persevere / ALI / SuperSoft) if the list exceeds ~8 entries.
   - Add a one-line persona hint under the select showing roles + customer.

4. **Downstream test updates**
   - Search `mentorhub`, `mentorhub_*_api`, and `mentorhub_spa_utils` for hard-coded old profile slugs or `_id` values in E2E auth helpers (`e2e_auth.py`, etc.) and update to match.

### Acceptance criteria

- [ ] Every Profile in `Profile.0.1.0.0.json` has a matching `PROFILES` entry in `welcome-auth.js`.
- [ ] No orphaned `PROFILES` entries for removed seed profiles.
- [ ] Signing in as each persona produces JWT claims that pass domain API auth middleware.
- [ ] Spot-check: Mary (customer+coordinator+mentee), Mike (all roles), Daniel (Persevere mentee + Special mentor), Lucky (SuperSoft mentee + Sr. Dev mentor), Money (mentor only).
- [ ] Cypress / E2E specs referencing old persona names updated or confirmed green.

### Dependencies

- **Blocked until** `mentorhub_mongodb_api` tasks T211 (Profile seed) and T217 (README) are merged.

### Test plan

1. `mh up` Developer Edition stack.
2. Drop + configure MongoDB from Admin UI or `make process` in mongodb_api repo.
3. Open `http://127.0.0.1:8080/login.html?return_to=http://127.0.0.1:8388/` (adjust port per SPA).
4. Sign in as each persona; confirm SPA loads and API calls succeed.
5. Run affected E2E suites in domain API repos.

---

## Testing Expectations

N/A — external issue only.

## Outputs

- None in this repository (issue filed manually in `mentorhub`).

## Execution Notes

_(Record issue URL here after a human creates it.)_
