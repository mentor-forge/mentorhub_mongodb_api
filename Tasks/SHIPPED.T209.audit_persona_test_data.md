# T209 – Audit Test Data for Persona Alignment

**Status**: Shipped  
**Type**: Feature  
**Depends On**: none  
**Description**: Audit all MongoDB seed data and Developer Edition auth mappings against the target persona matrix; produce a concrete test-data realignment plan for T210–T217.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`, `README.md`
- External (read-only for audit): `../mentorhub/login.html`, `../mentorhub/welcome-auth.js`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./Tasks/_ORCHESTRATE.md`
- `./README.md`
- `configurator/test_data/*.json` — all current seed collections
- `configurator/enumerators/enumerations.0.yaml` — `user_roles`, `event_types`, etc.
- `Tasks/SHIPPED.T203.update_customer_test_data.md` — current three-customer model
- `Tasks/SHIPPED.T204.update_profile_test_data.md` — current ten-profile model
- `../mentorhub/welcome-auth.js` — static JWT persona map (must stay in sync with Profile seed data)

### Pre-release

This pipeline is **test-data and documentation only**. Do not plan dictionary version bumps, new configuration versions, or configurator migration pipelines. Edit existing **0.1.0** artifacts in place only if a schema gap blocks seed data (unlikely for this feature). See `README.md` **Pre-release**.

### Target persona matrix (starting point)

| Persona | `name` (slug) | Roles | Explanation | Customer |
| --- | --- | --- | --- | --- |
| Mary the Super Mentee | `mary` | customer, coordinator, mentee | Self-funded apprentice; owns her sponsorship | Mary |
| Stacey the CEO | `stacey` | customer | Big-time CEO; may check on mentees; super busy | Persevere |
| Margaret the Coordinator | coordinator | Suspended Status | Persevere | 
| Emma the Coordinator | `emma` | coordinator | Matches mentees with mentors | Persevere |
| Daniel the Mentee | `daniel` | mentee | Mentee from Persevere | Persevere |
| Marti the Mentor | `marti` | mentor | Any Mentee | ALI |
| Mike the Admin | `mike` | admin | Platform SRE / super-user | ALI |
| Paula the Persevere Mentor | `paula` | mentor | Mentors **only** Persevere mentees (Daniel) | ALI |
| Elon the Money Mentor | `elon` | mentor | Compensated encounters only | ALI |
| Eddy the Entrepreneur | `eddy` | customer | Startup CEO for SuperSoft | SuperSoft |
| Danny the Dev Lead | `danny` | coordinator, mentor | Watches mentees for SuperSoft; mentors for SuperSoft only | SuperSoft |
| Lucky the Mentee | `lucky` | mentee | Mentee from SuperSoft | SuperSoft |
| Donny the Deadbeat | `danny` | customer | Past Due Subscription Customer | ScamSoft |
| Melinda the Multi Customer Mentor | `melinda` | Mentor | Mentors for Compensated and Persevere only | ALI |
| Linda the Archived Mentee | `linda` | Mentee |  Linda left, and is archived status | ALI | 

### Customers (target)

| Customer slug | Display name | Sponsored personas |
| --- | --- | --- |
| `mary` | Mary | Mary (self) |
| `persevere` | Persevere Now | Stacey, Emma, Daniel |
| `ali` | Agile Learning Institute | Mike, Marti, Special, Money |
| `supersoft` | SuperSoft | Entrepreneur, Dev Lead, Sr. Dev, Lucky |
| `scamsoft` | ScamSoft | Overdue Subscription Customer | 

### Current seed snapshot (baseline)

**Customers (3):** `cat`, `Persevere Now`, `Agile Learning Institute`  
**Profiles (10):** `mike`, `daniel`, `lucky`, `mary`, `luther`, `marti`, `carol`, `cat`, `sam`, `taylor`

**Likely removals / renames (confirm in audit):**

| Current | Disposition |
| --- | --- |
| `luther` | Remove unless audit finds a unique role combo not covered elsewhere |
| `sam` | Rename -> `donny`; past due CEO |
| `carol` | Rename → `emma`; reassign customer to Persevere |
| `cat` | Remove — replaced by Mary customer + Entrepreneur |
| `taylor` | Remove — replaced by `donny` (coordinator + mentor) |

### Role-combination coverage checklist

Audit must confirm every meaningful `user_roles` combination appears at least once:

- [ ] `customer` only — Stacey, Entrepreneur
- [ ] `coordinator` only — Emma, Dev Lead
- [ ] `mentee` only — Daniel, Lucky
- [ ] `mentor` only — Marti, Special, Money
- [ ] `customer` + `coordinator` + `mentee` — Mary
- [ ] `admin` only — Mike
- [ ] `coordinator` + `mentor` — Sr. Dev

### Collections to audit

For each file under `configurator/test_data/`, record:

1. Documents referencing profiles or customers slated for removal
2. Mentor–mentee pairings that conflict with the target matrix
3. Encounter compensation flags (Money Mentor)
4. Event density and `context.profile_id` coverage per persona
5. Journey ownership (which mentees have progress stories)
6. Note and Rating author/subject references

| Collection file | Primary persona fields |
| --- | --- |
| `Customer.0.1.0.0.json` | `_id`, `name` |
| `Profile.0.1.0.0.json` | `_id`, `name`, `roles`, `customer_id`, `mentor_id` |
| `Mentee.0.1.0.0.json` | `profile_id`, `mentor_id` (if present) |
| `Encounter.0.1.0.0.json` | `mentor_id`, `mentee_id`, compensation-related fields |
| `Journey.0.1.0.0.json` | mentee journey ownership |
| `Event.0.1.0.0.json` | `context.profile_id` |
| `Note.0.1.0.0.json` | profile references |
| `Rating.0.1.0.0.json` | rater/ratee profile references |

### Mentor assignment matrix (target)

| Mentor | Mentees | Notes |
| --- | --- | --- |
| Marti | Mary | ALI volunteer mentor |
| Paula | Daniel only | Persevere-exclusive |
| Elon | Daniel, Lucky | At least one compensated encounter each with Daniel and Lucky |
| Danny | Lucky | SuperSoft coordinator-mentor |

## Goals

- Produce a **Persona Realignment Plan** in **Execution Notes** with:
  - Final persona count and stable `_id` assignment table (Profile `A000…`, Customer `D000…`, Mentee `CC…` where applicable)
  - Per-collection change summary (add / update / remove counts)
  - Explicit list of deprecated slugs (`luther`, `sam`, `carol`, `cat`, `taylor`) and replacement mapping
  - Encounter and event realignment outline (which mentees get sessions, event density targets)
  - Confirmation that no dictionary version bumps or configurator migrations are required
- Confirm configure-database **baseline** passes before realignment (`make process` → SUCCESS with current data).
- Do **not** modify seed JSON files in this task — audit and plan only.

## Testing Expectations

Baseline (current seed data must pass before planning changes):

```sh
make dev
curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"
```

- Expect top-level **SUCCESS** on baseline audit.
- Record baseline document counts per collection in **Execution Notes**.

**Packaging verification** (no code changes expected):

```sh
make down
make container
mh up mongodb
```

## Outputs

- `./Tasks/PENDING.T209.audit_persona_test_data.md` — **Execution Notes** only (realignment plan)

## Execution Notes

**Baseline configure (2026-07-28):** `DELETE` + `POST` → **SUCCESS**

| Collection | Baseline count |
| --- | --- |
| Customer | 3 |
| Profile | 10 |
| Mentee | 5 |
| Journey | 6 |
| Encounter | 15 |
| Event | 258 |
| Note | 35 |
| Rating | 88 |

**Pre-release:** No dictionary version bumps or configurator migrations required.

**Deprecated slugs → replacement:**

| Old | New |
| --- | --- |
| `luther` (A05) | `linda` (archived mentee, same `_id`) |
| `carol` (A07) | `emma` |
| `cat` (A08) | `stacey` (profile); customer slot → `mary` (D01) |
| `sam` (A13) | `donny` |
| `taylor` (A14) | `danny` |

**Final counts:** 5 customers, 15 profiles, 4 mentee dossiers, 5 journeys (1 template + 4 mentees).

**Stable `_id` map:** see `Tasks/scripts/persona_ids.json` for handoff to T210–T217.

**Encounter plan:** Daniel→Paula×2, Lucky→Danny×2, Mary→Marti×2, Elon→Daniel+Lucky×1 each (compensated noted in narrative), Linda→Marti×1 archived.

**Event density:** mary > daniel ≈ lucky > linda; coordinator/customer login events for emma, danny, margaret, stacey, eddy.

**Role coverage:** all `user_roles` values covered; `suspended` via margaret; `archived` profile via linda.
