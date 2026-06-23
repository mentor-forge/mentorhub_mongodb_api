# Discord message for Mike — copy/paste below the line

---

Hi Mike,

I'm working through the **Build-a-Feature** workflow for the next **Data** item in `Specifications/features.md`:

**Event test data** — *"Create a series of events related to resource aggregation, driven by journey test data"* (depends on Journey T115–T118, which is shipped).

**Branch:** `feature/event-test-data-tasks` on `mentorhub_mongodb_api`  
**PR (task review only — no test data generated yet):** https://github.com/mentor-forge/mentorhub_mongodb_api/pull/13

### What I need from you

Please review the **Cursor prompt** below and the task file **`Tasks/PENDING.T119.generate_event_test_data.md`** on that branch **before** I run orchestration.

I have **not** run *"Orchestrate all pending tasks"* yet.

### Cursor prompt (for your review)

```
Review @mentorhub/DeveloperEdition/standards/data_standards.md,
@mentorhub_mongodb_api/Tasks/README.md,
@mentorhub_mongodb_api/Tasks/AS_NEEDED.generate_test_data.md,
@mentorhub/Specifications/features.md (Data features → Event),
@mentorhub_mongodb_api/configurator/dictionaries/Event.0.1.0.yaml,
@mentorhub_mongodb_api/configurator/enumerators/enumerations.0.yaml,
@mentorhub_mongodb_api/configurator/test_data/Journey.0.1.0.0.json,
@mentorhub_mongodb_api/Tasks/SHIPPED.T118.generate_mentee_journey_test_data.md,
and create PENDING.T119.generate_event_test_data.md following our Tasks conventions.

Goal: Event test data driven by Journey library/now/next progress.
Target: Event.0.1.0.0.json. EJSON. event_types enum coverage.
Task definition only — do not execute until I confirm with you.
```

(Full prompt also in `Tasks/DRAFT.cursor_prompt_T119.md` on the branch.)

### After you OK it

I'll run orchestration, test with `make container` / configure database, then open an implementation PR.

Thanks,  
Mary

---
