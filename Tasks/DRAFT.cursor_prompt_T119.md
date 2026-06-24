# Cursor prompt — T119 Event test data (review before running)

**Do not run this until Mike approves.** After approval, paste into Cursor on branch `feature/event-test-data-tasks` in `mentorhub_mongodb_api`.

---

Review @mentorhub/DeveloperEdition/standards/data_standards.md,
@mentorhub_mongodb_api/Tasks/README.md,
@mentorhub_mongodb_api/Tasks/AS_NEEDED.generate_test_data.md,
@mentorhub/Specifications/features.md (Data features → Event, line ~182),
@mentorhub_mongodb_api/configurator/dictionaries/Event.0.1.0.yaml,
@mentorhub_mongodb_api/configurator/enumerators/enumerations.0.yaml,
@mentorhub_mongodb_api/configurator/test_data/Journey.0.1.0.0.json,
@mentorhub_mongodb_api/Tasks/SHIPPED.T118.generate_mentee_journey_test_data.md,
and create one PENDING task file following our Tasks conventions:

**PENDING.T119.generate_event_test_data.md**

**Goal:** Generate Event test data driven by Journey progress (`library` / `now` / `next`), related to resource engagement for downstream Aggregation test data.

**Requirements:**
- Target `configurator/test_data/Event.0.1.0.0.json` (currently empty)
- Use `event_types` enum; every type should appear at least once where realistic
- Focus on `started`, `completed`, `advanced`, `link`, and `encounter` events tied to mentee Profile `$oid` values and EngineerKit resources from Journey test data (T118)
- Include a few `login`, `logout`, `arrived`, `fail`, and `note` events for realism
- EJSON encoding (`$oid`, `$date`, breadcrumbs)
- Deterministic Event `_id` values starting at `F00000000000000000000001`
- **Task definition only** — do not execute the task or generate JSON yet

Commit the task file to branch `feature/event-test-data-tasks` and open a PR for review.

---

**After Mike approves the task definition**, run:

```
Orchestrate all pending tasks using the tasks/README.md process
```
