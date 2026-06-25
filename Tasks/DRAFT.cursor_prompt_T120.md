# Cursor prompt — T120 Rating test data (review before running)

**Do not run this until Mike approves.** After approval, paste into Cursor on branch `feature/rating-test-data-tasks` in `mentorhub_mongodb_api`.

---

Review @mentorhub/DeveloperEdition/standards/data_standards.md,
@mentorhub_mongodb_api/Tasks/README.md,
@mentorhub_mongodb_api/Tasks/AS_NEEDED.generate_test_data.md,
@mentorhub/Specifications/features.md (Data features → Rating, line ~186),
@mentorhub_mongodb_api/configurator/dictionaries/Rating.0.1.0.yaml,
@mentorhub_mongodb_api/configurator/types/rating.yaml,
@mentorhub_mongodb_api/configurator/enumerators/enumerations.0.yaml,
@mentorhub_mongodb_api/configurator/test_data/Journey.0.1.0.0.json,
@mentorhub_mongodb_api/configurator/test_data/Resource.0.1.0.0.json,
@mentorhub_mongodb_api/configurator/test_data/Profile.0.1.0.0.json,
@mentorhub_mongodb_api/Tasks/SHIPPED.T118.generate_mentee_journey_test_data.md,
and create one PENDING task file following our Tasks conventions:

**PENDING.T120.generate_rating_test_data.md**

**Goal:** Generate Rating test data based on resources each mentee has **completed** in their Journey `library` (from T118), as input for downstream Aggregation test data.

**Requirements:**
- Target `configurator/test_data/Rating.0.1.0.0.json` (currently empty `[]`)
- One Rating per completed library resource where realistic; tie `profile_id` to the journey owner and `resource_id` to the Resource `$oid` for that library entry
- `rating` values 1–4 (star scale per `rating.yaml`); vary scores by mentee progress and resource difficulty
- Include `default_status` enum coverage (`active` and at least one `archived` if realistic)
- EJSON encoding (`$oid`, `$date`, breadcrumbs)
- Deterministic `_id` values starting at `G00000000000000000000001` (24-char hex ObjectIds throughout)
- Do not invent library resources — only rate resources already in each mentee's Journey `library`
- **Task definition only** — do not execute the task or generate JSON yet

Commit the task file to branch `feature/rating-test-data-tasks` and open a PR for review.

---

**After Mike approves the task definition**, run:

```
Orchestrate all pending tasks using the tasks/README.md process
```
