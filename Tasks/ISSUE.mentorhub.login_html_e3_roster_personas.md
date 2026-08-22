# ISSUE — mentorhub: Developer Edition login personas for E3 roster fixtures (F-D23 follow-on)

**Status:** Pending (human files GitHub issue; not orchestrated from mongodb_api)  
**Type:** Feature  
**Depends On:** T236 shipped in `mentorhub_mongodb_api`  
**Description:** Copy-paste GitHub issue body so Developer Edition `login.html` / `welcome-auth.js` mint JWT claims for E3 org-home personas (harbor/helen empty roster, pat empty activity, plus Path A nora if still missing).

## Path Anchoring

Sibling repo: `mentorhub`. This file lives only in `mentorhub_mongodb_api/Tasks/` as an external follow-on prompt.

- Target files (external): `login.html`, `welcome-auth.js`
- Source of truth (this repo): `configurator/test_data/Profile.0.1.0.0.json`, `README.md` Test Personas, `Tasks/scripts/persona_ids.json`

## Context

- `../mentorhub/Workshops/customer_journey_issues.md` — E3 Customer org home via universal nav
- GitHub data: [F-D23 #55](https://github.com/mentor-forge/mentorhub_mongodb_api/issues/55)
- `Tasks/PENDING.T236.seed_customer_org_roster_profiles.md` — harbor / helen / pat `_id`s (use Execution Notes after ship)
- Existing prompt: `Tasks/ISSUE.mentorhub.login_html_persona_alignment.md` — original T211 matrix; this issue **adds** E1/E3 personas rather than replacing that work

## Issue body (paste into mentorhub)

```text
Title: Align login.html personas with E3 Customer org roster seeds (F-D23)

Create @_PLANNING.md tasks to implement this issue. Only create tasks, do not execute tasks, do not edit any files outside of the @tasks folder.

Repository: mentor-forge/mentorhub

Description:
Developer Edition JWT minting must include Customer org-home fixtures from
mentorhub_mongodb_api F-D23 so Cat-the-Customer can demo roster vs empty states.

Goals:
- Add welcome-auth.js PROFILES entries matching mongodb_api README Test Personas
  after T236: helen (harbor owner, customer role, active subscription, empty
  mentee roster), pat (persevere mentee, no encounters).
- Include nora / northstar and patha-owner if those Profile seeds are still
  missing from PROFILES (F-D21 Path A pairs).
- Claims must match Profile seed data: profile_id, customer_id, mentor_id, roles.
- Group or label Customer SPA demo logins (Stacey/Eddy/Helen subscribed vs
  Mary/Nora unsubscribed) if the picker is crowded.
- Do not add Dashboard or Discovery-card fixtures in mentorhub.

Depends on: mentorhub_mongodb_api T236 (and T233 if nora is included) merged.
Context: Workshops/customer_journey_issues.md E3; F-D23 #55
```

## Testing Expectations

N/A — external issue only. Record the filed GitHub URL in Execution Notes after a human creates it.

## Outputs

- None in this repository (issue filed manually in `mentorhub`).

## Execution Notes

_(Record filed issue URL here after a human creates it.)_
