# Draft Discord message for Mike (review before executing tasks)

**Copy/paste to Discord:**

---

Hi Mike — I'm following the Build-a-Feature workflow for **Event test data** (next item in `mentorhub/Specifications/features.md` Data features, after Journey T115–T118).

**Feature branch:** `feature/event-test-data-tasks` on `mentorhub_mongodb_api`

**Cursor prompt I used to draft the task** (please review before I run orchestration):

```
Review @mentorhub/DeveloperEdition/standards/data_standards.md,
@mentorhub_mongodb_api/Tasks/README.md,
@mentorhub_mongodb_api/Tasks/AS_NEEDED.generate_test_data.md,
@mentorhub/Specifications/features.md (Data features → Event),
@mentorhub_mongodb_api/configurator/dictionaries/Event.0.1.0.yaml,
@mentorhub_mongodb_api/configurator/enumerators/enumerations.0.yaml,
@mentorhub_mongodb_api/configurator/test_data/Journey.0.1.0.0.json,
@mentorhub_mongodb_api/Tasks/SHIPPED.T118.generate_mentee_journey_test_data.md,
and create one PENDING task file following our Tasks conventions:

PENDING.T119.generate_event_test_data.md

Goal: generate Event test data driven by Journey progress (library/now/next),
related to resource engagement for aggregation downstream.

Requirements:
- Target Event.0.1.0.0.json (currently empty)
- Use event_types enum; ensure every type appears at least once where realistic
- Focus on started, completed, advanced, link, and encounter events tied to
  mentee profiles and EngineerKit resources from Journey test data
- Include a few login/logout/arrived events for realism
- EJSON encoding ($oid, $date, breadcrumbs)
- Do NOT execute the task yet — task definition only
- Reference T118 mentee journeys and Profile ids

Share the task file on branch feature/event-test-data-tasks for review.
Do not orchestrate or implement until I confirm with you.
```

**PR for task review:** https://github.com/mentor-forge/mentorhub_mongodb_api/pull/13

I've **not** run "Orchestrate all pending tasks" yet — waiting for your OK on the task definition first.

---
