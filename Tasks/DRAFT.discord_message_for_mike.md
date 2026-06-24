# Discord message for Mike — copy/paste below the line

---

Hi Mike,

I'm starting the next **Data** feature from `Specifications/features.md`:

**Rating test data** — *"Create a series of Ratings based on Journey Completed tasks."*

**Branch:** `feature/rating-test-data-tasks` on `mentorhub_mongodb_api`

### What I need from you

Please review the **Cursor prompt** below **before** I run it. I have **not** created task files or generated test data yet.

### Cursor prompt (for your review)

```
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

**Goal:** Generate Rating test data based on resources each mentee has completed in their Journey library (from T118), as input for downstream Aggregation test data.

**Requirements:**
- Target configurator/test_data/Rating.0.1.0.0.json (currently empty)
- One Rating per completed library resource where realistic
- rating values 1–4; vary by mentee progress
- default_status enum coverage
- EJSON encoding; deterministic _id values starting at G00000000000000000000001
- Task definition only — do not execute yet
```

(Full prompt also in `Tasks/DRAFT.cursor_prompt_T120.md` on the branch.)

### After you OK it

I'll run the prompt in Cursor, push the task file for your review, then orchestrate after you approve the tasks.

Thanks,  
Mary

---
