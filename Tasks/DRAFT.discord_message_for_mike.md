# Discord message for Mike — copy/paste below the line

---

Hi Mike,

T120 (**Rating test data**) is shipped on `feature/rating-test-data-tasks`. Next up from `Specifications/features.md`:

**Note test data** — *"Create a series of Notes related to Journey test data, library resources."*

**Branch:** `feature/note-test-data-tasks` on `mentorhub_mongodb_api`

### What I need from you

Please review the **Cursor prompt** below **before** I run it. I have **not** created the T121 task file or generated test data yet.

### Cursor prompt (for your review)

```
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

**Goal:** Generate Note test data for Journey library/now resources, aligned with T120 ratings where applicable.

**Requirements:**
- Target configurator/test_data/Note.0.1.0.0.json (currently empty)
- At least 35 notes across seven mentees
- Markdown note text; vary length and style
- default_status enum coverage
- EJSON encoding; deterministic _id values starting at H00000000000000000000001
- Task definition only — do not execute yet
```

(Full prompt also in `Tasks/DRAFT.cursor_prompt_T121.md` on the branch.)

### After you OK it

I'll run the prompt in Cursor, push the task file for your review, then orchestrate after you approve the tasks.

Thanks,  
Mary

---
