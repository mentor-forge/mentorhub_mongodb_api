# Cursor prompt — T121 Note test data (review before running)

**Do not run this until Mike approves.** After approval, paste into Cursor on branch `feature/note-test-data-tasks` in `mentorhub_mongodb_api`.

---

Review @mentorhub/DeveloperEdition/standards/data_standards.md,
@mentorhub_mongodb_api/Tasks/README.md,
@mentorhub_mongodb_api/Tasks/AS_NEEDED.generate_test_data.md,
@mentorhub/Specifications/features.md (Data features → Note, line ~190),
@mentorhub_mongodb_api/configurator/dictionaries/Note.0.1.0.yaml,
@mentorhub_mongodb_api/configurator/types/markdown.yaml,
@mentorhub_mongodb_api/configurator/enumerators/enumerations.0.yaml,
@mentorhub_mongodb_api/configurator/test_data/Journey.0.1.0.0.json,
@mentorhub_mongodb_api/configurator/test_data/Resource.0.1.0.0.json,
@mentorhub_mongodb_api/configurator/test_data/Profile.0.1.0.0.json,
@mentorhub_mongodb_api/configurator/test_data/Rating.0.1.0.0.json,
@mentorhub_mongodb_api/Tasks/SHIPPED.T118.generate_mentee_journey_test_data.md,
@mentorhub_mongodb_api/Tasks/SHIPPED.T120.generate_rating_test_data.md,
and create one PENDING task file following our Tasks conventions:

**PENDING.T121.generate_note_test_data.md**

**Goal:** Generate Note test data related to Journey `library` and `now` resources (from T118), aligned with T120 ratings where applicable, as input for downstream Aggregation test data.

**Requirements:**
- Target `configurator/test_data/Note.0.1.0.0.json` (currently empty `[]`)
- At least 35 notes across seven mentees; more for higher-progress mentees (luther, mary)
- Tie `profile_id` to journey owner and `resource_id` to library/now Resource `$oid`
- Markdown note text; vary length and style; align tone with T120 ratings where both exist
- Include `default_status` enum coverage (`active` and at least one `archived` for casey)
- EJSON encoding (`$oid`, `$date`, breadcrumbs); include both `created` and `saved`
- Deterministic `_id` values starting at `H00000000000000000000001`
- Do not invent resources — only note resources on each mentee's Journey `library` or `now`
- **Task definition only** — do not execute the task or generate JSON yet

Commit the task file to branch `feature/note-test-data-tasks` and open a PR for review.

---

**After Mike approves the task definition**, run:

```
Orchestrate all pending tasks using the tasks/README.md process
```
