# T116 – Add Onboarding Journey Resources

**Status**: Shipped  
**Task Type**: Feature  
**Run Mode**: Sequential  

## User inputs (edit before running)

- **Dictionary file** `../configurator/dictionaries/Resource.0.1.0.yaml`
- **Enumerators file** `../configurator/enumerators/enumerations.0.yaml`
- **Target test-data file** `../configurator/test_data/Resource.0.1.0.0.json`
- **Special requirements** — Append only the Resource documents listed below **if no existing Resource already uses the same URL** (normalize `http` vs `https` and trailing slashes when comparing).

## Goal

Ensure Resource test data contains the onboarding URLs required by the Journey template (T117). Confirm **EngineerKit** and **Odin** paths already exist in `Path.0.1.0.0.json` for T117 `later` references. Journey test data uses **Paths** and **Resources** — not Plans.

## Context / Input files

These files must be treated as **inputs** and read before implementation:

- [Data standards](../../mentorhub/DeveloperEdition/standards/data_standards.md)
- Resource dictionary, enumerators, and [type files](../configurator/types/) — especially `word.yaml` (`name` must match `^[^\s]{1,40}$`).
- `../configurator/test_data/Resource.0.1.0.0.json` — append new documents; do not replace existing harvest.
- `../configurator/test_data/Path.0.1.0.0.json` — **read only**; confirm:
  - **EngineerKit** — `C00000000000000000000006` (primary curriculum path for T118 `library`/`now`/`next`)
  - **Odin** — `C00000000000000000000008` (template T117 `later`)
- Do **not** create or modify Path documents in this task.

### URL inventory (check before creating)

| URL | Used in | Likely existing Resource |
| --- | --- | --- |
| `https://agile-learning.institute` | T117 template `now` | **Missing** — create if absent |
| `https://agile-learning.institute/initiatives` | T117 template `next` | **Missing** — create if absent |
| `https://agilemanifesto.org` | T117 template `next` | Likely `ManifestoforAgileSoftwareDevelopment` (`B00000000000000000000675`) or `AgileManifesto` (`B00000000000000000000297`) — **reuse** |
| `https://manifesto.softwarecraftsmanship.org` | T117 template `next` | Likely `ManifestoforSoftwareCraftsmanship` (`B00000000000000000000676`) — **reuse** |

## Requirements

### 1. Agile Learning Institute (homepage)

Create **only if** no Resource matches `https://agile-learning.institute`:

| Field | Value |
| --- | --- |
| `_id` | Next available `B000…` |
| `name` | `AgileLearningInstitute` |
| `url` | `https://agile-learning.institute` |
| `type` | `article` |
| `cost` | `free` |
| `skill_level` | `Apprentice` |
| `interests` | `["api"]` |
| `technologies` | `["Other"]` |
| `status` | `active` |
| `description` | Agile Learning Institute — a 501(c)(3) educational nonprofit providing free mentorship and one-on-one coaching for software engineers. |

### 2. Agile Learning Initiatives (blog)

Create **only if** no Resource matches `https://agile-learning.institute/initiatives`:

| Field | Value |
| --- | --- |
| `_id` | Next sequential `B000…` |
| `name` | `AgileLearningInitiatives` |
| `url` | `https://agile-learning.institute/initiatives` |
| `type` | `article` |
| `cost` | `free` |
| `skill_level` | `Apprentice` |
| `interests` | `["api"]` |
| `technologies` | `["Other"]` |
| `status` | `active` |
| `description` | Agile Learning Institute initiatives — partnership programs and articles including Persevere Partnership, Building T-Shaped Engineers, and The Power of Agile Mentorship. |

### 3. Manifesto resources

- **Do not** duplicate manifesto Resources if URLs already exist.
- Record all `$oid` values (new and reused) in implementation notes for T117.

### 4. General rules

1. **EJSON encoding** — `_id` as `{ "$oid": "…" }`; dates as `{ "$date": "…" }`.
2. Include `created`, `saved`, and `last_verified` breadcrumbs consistent with T111/T113 resources.
3. Do **not** modify Journey or Path test data.
4. Confirm EngineerKit and Odin paths exist; if either is missing, stop and report an error.

## Testing expectations

- **Processing test**
  - `curl -X DELETE "http://localhost:8385/api/database/"` then `curl -X POST "http://localhost:8385/api/configurations/"` on port **8385**.
  - Validate configure result reports `SUCCESS`.
- **Packaging test**
  - Run `make container` and `make process` successfully.

## Dependencies / Ordering

- Depends on [SHIPPED.T115](./SHIPPED.T115.clear_journey_test_data.md).
- Must complete before [SHIPPED.T117](./SHIPPED.T117.create_journey_template.md).
- T111–T114 should already be shipped (EngineerKit path from T112).

## Change control checklist

- [x] Reviewed Resource file for existing URLs before appending.
- [x] Appended 0–2 new Resource documents as needed.
- [x] Confirmed EngineerKit (`C000…06`) and Odin (`C000…08`) paths exist.
- [x] Documented Resource `$oid` table for T117.
- [x] Ran `make container` and `make process` successfully.
- [x] Created a scoped commit referencing this task ID.

## Implementation notes (to be updated by the agent)

**Summary of changes**

Appended **2** onboarding Resource documents. Confirmed EngineerKit (`C00000000000000000000006`) and Odin (`C00000000000000000000008`) paths exist.

| Resource | `$oid` | Action |
| --- | --- | --- |
| `AgileLearningInstitute` | `B00000000000000000000724` | Created |
| `AgileLearningInitiatives` | `B00000000000000000000725` | Created |
| `AgileManifesto` | `B00000000000000000000297` | Reused (T117 template) |
| `ManifestoforSoftwareCraftsmanship` | `B00000000000000000000676` | Reused (T117 template) |

**Testing results**

- `make container` → SUCCESS.
- `POST /api/configurations/` on port 8385 → SUCCESS.
