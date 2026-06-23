# T117 – Create Journey Template Document

**Status**: Shipped  
**Task Type**: Feature  
**Run Mode**: Sequential  

## User inputs (edit before running)

- **Dictionary file** `../configurator/dictionaries/Journey.0.1.0.yaml`
- **Enumerators file** `../configurator/enumerators/enumerations.0.yaml`
- **Target test-data file** `../configurator/test_data/Journey.0.1.0.0.json`
- **Template Journey `_id`**: `{ "$oid": "ffff00000000000000000001" }`

## Goal

Add the **template Journey** document used when the mentee API creates a new Journey for a profile that does not yet have one. The template has **no** `profile_id` and encodes the default **onboarding** roadmap in `now` and `next`, with full curriculum **Paths** queued in `later`. Uses **Paths** and **Resources** only — not Plans.

## Context / Input files

These files must be treated as **inputs** and read before implementation:

- [Data standards](../../mentorhub/DeveloperEdition/standards/data_standards.md)
- `../configurator/dictionaries/Journey.0.1.0.yaml` — `later` holds **Path** `$oid` references.
- `../configurator/test_data/Resource.0.1.0.0.json` — onboarding Resource `$oid` and `name` values (T116).
- `../configurator/test_data/Path.0.1.0.0.json` — EngineerKit and Odin for `later`.
- [SHIPPED.T116](./SHIPPED.T116.add_onboarding_journey_resources.md) — onboarding Resource ids.
- [mentorhub/Specifications/features.md](../../mentorhub/Specifications/features.md) — Journey API clones template `$oid` `ffff00000000000000000001`.

### Onboarding Resources → `now` and `next`

These are **standalone onboarding Resources** (not EngineerKit path resources):

| Scope | Resource | URL |
| --- | --- | --- |
| `now` | Agile Learning Institute homepage | `https://agile-learning.institute` |
| `next` | Initiatives blog | `https://agile-learning.institute/initiatives` |
| `next` | Agile Manifesto | `https://agilemanifesto.org` |
| `next` | Software Craftsmanship Manifesto | `https://manifesto.softwarecraftsmanship.org` |

### Path references for `later`

| Path | `_id` |
| --- | --- |
| EngineerKit | `C00000000000000000000006` |
| Odin | `C00000000000000000000008` |

`later` is an array of **Path** `$oid` values. Do **not** use Plan `$oid` values.

## Requirements

### Template document shape

Append **one** Journey document to `Journey.0.1.0.0.json` (file should be `[]` after T115):

| Field | Value |
| --- | --- |
| `_id` | `ffff00000000000000000001` |
| `profile_id` | **Omit** (clone source — no owner) |
| `status` | `active` |
| `library` | `[]` |
| `created` / `saved` | Breadcrumb objects consistent with other seed documents |

### `now` scope

Exactly **one** in-progress resource — Agile Learning Institute homepage:

```json
{
  "resource_id": "AgileLearningInstitute",
  "added": { "$date": "<ISO-8601>" },
  "used": 0
}
```

- `now.resource_id` is the Resource **`name`** (`word` type), not `$oid`.

### `next` scope

Onboarding content as **modules** with **topics** per `Journey.0.1.0.yaml`:

| Module `name` | Module `description` | Topics |
| --- | --- | --- |
| `Introduction` | Introduction to Agile Learning and mentorship context. | _(optional — may be empty if all content is under Mindset)_ |
| `Mindset` | Institute initiatives and engineering manifestos. | See below |

**Mindset topics** (each topic `resources` array holds `$oid` references):

| Topic `name` | Topic `description` | `resources` |
| --- | --- | --- |
| `AgileLearningInitiatives` | Review Agile Learning Institute initiatives and partnership programs. | Initiatives blog `$oid` |
| `AgileManifesto` | Review the Manifesto for Agile Software Development. | Agile Manifesto `$oid` |
| `SoftwareCraftsmanshipManifesto` | Review the Manifesto for Software Craftsmanship. | Craftsmanship Manifesto `$oid` |

### `later` scope

Array of **two Path** `$oid` references:

1. **EngineerKit** — `C00000000000000000000006`
2. **Odin** — `C00000000000000000000008`

New mentees start with onboarding in `now`/`next`; full **EngineerKit** and **Odin** paths are promoted from `later` when ready (T118 walks EngineerKit for active mentees).

### EJSON and schema rules

1. Resource references in `next` use `{ "$oid": "…" }`; Path references in `later` use `{ "$oid": "…" }`.
2. Dates use `{ "$date": "…" }`.
3. Do **not** add mentee journeys in this task — that is T118.

## Testing expectations

- **Processing test**
  - Drop and configure database on port **8385**; validate `SUCCESS`.
  - Confirm exactly **one** Journey document with `_id` `ffff00000000000000000001`.
- **Packaging test**
  - `make container` and `make process` succeed.

## Dependencies / Ordering

- Depends on [SHIPPED.T115](./SHIPPED.T115.clear_journey_test_data.md) and [SHIPPED.T116](./SHIPPED.T116.add_onboarding_journey_resources.md).
- Must complete before [SHIPPED.T118](./SHIPPED.T118.generate_mentee_journey_test_data.md).

## Change control checklist

- [x] Reviewed T116 Resource id notes.
- [x] Appended template Journey; `later` = EngineerKit + Odin Path ids.
- [x] `now` / `next` use onboarding Resources (not EngineerKit path content).
- [x] Ran `make container` and `make process` successfully.
- [x] Created a scoped commit referencing this task ID.

## Implementation notes (to be updated by the agent)

**Summary of changes**

Added template Journey `ffff00000000000000000001` with no `profile_id`.

| Scope | Content |
| --- | --- |
| `now` | `AgileLearningInstitute` (`B000…724`) |
| `next` → Mindset | Initiatives (`B000…725`), Agile Manifesto (`B000…297`), Craftsmanship Manifesto (`B000…676`) |
| `later` | EngineerKit (`C000…06`), Odin (`C000…08`) |

**Testing results**

- `make container` → SUCCESS.
- `POST /api/configurations/` on port 8385 → SUCCESS.
