# T209 – Audit Test Data for Persona Alignment

**Status**: Pending  
**Type**: Feature  
**Depends On**: none  
**Description**: Audit all MongoDB seed data and Developer Edition auth mappings against the target persona matrix; produce a concrete migration plan for T210–T217.

## Path Anchoring

All paths are relative to **this API repository root** (the directory that contains `Pipfile`).

- Standards: `../mentorhub/DeveloperEdition/standards/data_standards.md`
- In-repo: `configurator/test_data/`, `README.md`
- External (read-only for audit): `../mentorhub/login.html`, `../mentorhub/welcome-auth.js`

## Context

- `../mentorhub/DeveloperEdition/standards/data_standards.md`
- `./Tasks/_PLANNING.md`
- `./Tasks/_ORCHESTRATION.md`
- `./README.md`
- `configurator/test_data/*.json` — all current seed collections
- `configurator/enumerators/enumerations.0.yaml` — `user_roles`, `event_types`, etc.
- `Tasks/SHIPPED.T203.update_customer_test_data.md` — current three-customer model
- `Tasks/SHIPPED.T204.update_profile_test_data.md` — current ten-profile model
- `../mentorhub/welcome-auth.js` — static JWT persona map (must stay in sync with Profile seed data)

### Target persona matrix (starting point)

| Persona | `name` (slug) | Roles | Explanation | Customer |
| --- | --- | --- | --- | --- |
| Mary the Super Mentee | `mary` | customer, coordinator, mentee | Self-funded apprentice; owns her sponsorship | Mary |
| Stacey the CEO | `stacey` | customer | Big-time CEO; may check on mentees; super busy | Persevere |
| Emma the Coordinator | `emma` | coordinator | Matches mentees with mentors | Persevere |
| Daniel | `daniel` | mentee | Mentee from Persevere | Persevere |
| Marti the Mentor | `marti` | mentor | Primary ALI mentor | ALI |
| Mike the Admin | `mike` | admin, customer, coordinator, mentor, mentee | Platform SRE / super-user | ALI |
| Special Mentor | `special` | mentor | Mentors **only** Persevere mentees (Daniel) | ALI |
| Money Mentor | `money` | mentor | Compensated encounters only | ALI |
| Entrepreneur | `entrepreneur` | customer | Startup CEO for SuperSoft | SuperSoft |
| Dev Lead | `devlead` | coordinator | Watches mentees for SuperSoft; does not mentor | SuperSoft |
| Sr. Dev | `srdev` | coordinator, mentor | Matches and mentors SuperSoft mentees | SuperSoft |
| Lucky | `lucky` | mentee | Mentee from SuperSoft | SuperSoft |

### Customers (target)

| Customer slug | Display name | Sponsored personas |
| --- | --- | --- |
| `mary` | Mary | Mary (self) |
| `persevere` | Persevere Now | Stacey, Emma, Daniel |
| `ali` | Agile Learning Institute | Mike, Marti, Special, Money |
| `supersoft` | SuperSoft | Entrepreneur, Dev Lead, Sr. Dev, Lucky |

### Current seed snapshot (pre-migration)

**Customers (3):** `cat`, `Persevere Now`, `Agile Learning Institute`  
**Profiles (10):** `mike`, `daniel`, `lucky`, `mary`, `luther`, `marti`, `carol`, `cat`, `sam`, `taylor`

**Likely removals / renames (confirm in audit):**

| Current | Disposition |
| --- | --- |
| `luther` | Remove unless audit finds a unique role combo not covered elsewhere |
| `sam` | Remove — duplicate all-role admin; Mike covers super-user |
| `carol` | Rename → `emma`; reassign customer to Persevere |
| `cat` | Remove — replaced by Mary customer + Entrepreneur |
| `taylor` | Remove — replaced by `srdev` (coordinator + mentor) |

### Suggested additional personas (audit should confirm or reject)

| Persona | Roles | Rationale |
| --- | --- | --- |
| **Archived Mentee** (`archived`) | mentee (archived status) | Preserve `archived` profile/encounter enum coverage if Luther is removed |
| **Suspended Coordinator** (`suspended_coord`) | coordinator (suspended) | Cover `suspended` profile_status if no other persona uses it |

### Role-combination coverage checklist

Audit must confirm every meaningful `user_roles` combination appears at least once:

- [ ] `customer` only — Stacey, Entrepreneur
- [ ] `coordinator` only — Emma, Dev Lead
- [ ] `mentee` only — Daniel, Lucky
- [ ] `mentor` only — Marti, Special, Money
- [ ] `customer` + `coordinator` + `mentee` — Mary
- [ ] `customer` + `coordinator` + `mentor` + `mentee` + `admin` — Mike
- [ ] `coordinator` + `mentor` — Sr. Dev
- [ ] `mentor` + `mentee` (no coordinator) — **gap**; accept as covered by Mike or propose a lightweight persona
- [ ] `admin` without all other roles — **gap**; Mike covers; document decision

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

| Mentee | Primary mentor | Alternate / special |
| --- | --- | --- |
| Daniel | Special (`special`) | Marti for historical encounters optional |
| Lucky | Sr. Dev (`srdev`) | Marti optional for cross-customer edge case |
| Mary | Marti (`marti`) | Self-coordinated |

| Mentor | Mentees | Notes |
| --- | --- | --- |
| Marti | Mary | ALI platform mentor |
| Special | Daniel only | Persevere-exclusive |
| Money | Any (paid sessions) | At least one compensated encounter each with Daniel and Lucky |
| Sr. Dev | Lucky | SuperSoft coordinator-mentor |

## Goals

- Produce a **Persona Migration Plan** in **Execution Notes** with:
  - Final persona count and stable `_id` assignment table (Profile `A000…`, Customer `D000…`, Mentee `CC…` where applicable)
  - Per-collection change summary (add / update / remove counts)
  - Explicit list of deprecated slugs (`luther`, `sam`, `carol`, `cat`, `taylor`) and replacement mapping
  - Encounter and event realignment outline (which mentees get sessions, event density targets)
  - Decision on suggested additional personas (archived mentee, suspended coordinator)
- Confirm configure-database **baseline** passes before migration (`make process` → SUCCESS with current data).
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

- `./Tasks/PENDING.T209.audit_persona_test_data.md` — **Execution Notes** only (migration plan)

## Execution Notes

_(Reserved for audit agent: baseline counts, gap analysis, final `_id` map, and per-task handoff notes for T210–T217.)_
