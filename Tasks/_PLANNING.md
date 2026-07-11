# API Task Automation Framework - Planning

This folder contains coding tasks that an orchestration agent can execute, based on the context and instructions in each task file. This file is a guide for an agent that is helping to plan changes by creating task files to achieve a goal. Create tasks following the [naming conventions](#naming-conventions) and guides below.

- **Context** Before creating any task files you should review the following files for context:
- ../mentorhub/DeveloperEdition/standards/data_standards.md
- ./README.md
- ./Tasks/_ORCHESTRATION.md
- ./Tasks/_PLANNING.md (this file)

## Task File Layout

Each task file must contain the following sections under H1 and H2 headings.

- Under the top H1 task header:
  - Each task file should declare `Status:` **inside the file**, and also encode the status in the **filename prefix** so tasks are visually grouped in the IDE.
  - **Lifecycle statuses (in‑file)**:
    - `Pending`: Not yet started.
    - `Running`: Work is currently being done in the active session.
    - `Blocked`: Waiting on some external dependency or decision.
    - `Shipped`: Implemented, tested, and committed as per the change control process.
    - `Run as needed`: Not part of the main long‑running sequence; to be run manually or opportunistically.
  - **Filename status prefixes (for grouping)**:
    - `AS_NEEDED.` – Tasks that should **not** be part of the main long‑running sequence.
    - `BLOCKED.` – Tasks currently blocked.
    - `PENDING.` – Tasks that are ready to be picked up when their turn comes.
    - `RUNNING.` – (Optional) Tasks currently being executed in this session.
    - `SHIPPED.` – Tasks that are fully implemented and completed.
  - **Type**: `Feature` | `Defect` to describe why we are running this task
  - **Depends On**: `L010_update_profile_openapi` the required predecessor task **in this repo**, or `none` for parallel tasks
  - **Description**: A brief human description of the task.

Under a **Path Anchoring** H2 header:
  - All paths in task files are relative to **this API repository root** (the directory that contains `Pipfile`).
  - Sibling repos must all be sibling folders under a common parent.
  - Standards: `../mentorhub/DeveloperEdition/standards/api_standards.md`
  - In-repo: `README.md`, `docs/openapi.yaml`, `src/...`, `test/...`, `tasks/...`
- Under a **Context** H2 header:
  - A list of context files. This list should always include:
    - `../mentorhub/DeveloperEdition/standards/data_standards.md`
    - `./Tasks/_PLANNING.md`
    - `./README.md`
  - Any other input files for the execution of the task.
  - `AS_NEEDED` tasks may include a **Parameters (edit before running)** subsection here for values to customize before promoting to `Pending`.

- Under a **Goals** H2 header:
  - A list of desired outcomes for the task.
  - Each item should describe the outcome (Add test data for new use cases).

- Under a **Testing Expectations** H2 header:
  - Should always include a description of the tests that should be used to verify completion.
  - In this repo, that typically means some combination of:
    - Run in Dev mode, and Drop and configure the database with these two curl commands
```sh
make dev
curl -X DELETE "http://localhost:8081/api/database/" -H "accept: application/json"
curl -X POST "http://localhost:8081/api/configurations/" -H "accept: application/json"
```
    - Make sure both return a 200. If there are errors in the configure return value they can help diagnose the problem.
  - Should always include the **Packaging verification** step:
```sh
make down
make container
mh up mongodb
```

- Under an **Outputs** H2 header:
  - A list of the files that will be created/updated/moved/renamed/etc.
  - `file_name.json` will be updated to support `<Goal>`
  - List all files including new files to be created.
  - The agent will not update files not listed.

- Under an **Execution Notes** H2 header:
  - Reserved for the task execution agent to record plan, commands run, test results, and follow-ups.

## Schema and test data

Dictionary schema tasks and test-data tasks are often **separate**, but plan them together.

- **Schema-only tasks without test-data changes** are appropriate only when the schema update **relaxes** constraints — for example adding an optional property, widening an enum, or loosening validation so existing documents still pass.
- **Tightening constraints** — removing a property, changing a type, setting `additional_properties: false` on a field that test data still carries, or making a field required — almost always requires **test data updates in the same pipeline** before the work can be marked complete.
- **Removing a property** from a dictionary is a common case: existing EJSON in `configurator/test_data/` will fail configure-database until that property is stripped from every document. Do not treat “dictionary change only” as shippable when `make process` / `POST /api/configurations/` will fail; either include test-data files in **Outputs** or add a dependent test-data task and document the expected configure failure only as an interim state between tasks.
- When splitting schema and test data across tasks, use serial **Depends On** ordering (schema task blocks test-data task) and state clearly in **Testing Expectations** whether configure-database must pass in that task or may fail until the follow-on task ships.

## Naming Conventions
- **Recommended filename pattern**:
  - `STATUS.LNNN.short_task_name.md`
  - Examples:
    - `AS_NEEDED.generate_test_data`
    - `PENDING.T010.update_profile_schema.md`
    - `RUNNING.T021.update_profile_test_data.md`
    - `SHIPPED.T020.update_profile_indexes.md`

## External repository boundaries

Task planning and execution in **this API repo** (`mentorhub_mongodb_api`) must not read or depend on other sibling repositories for input context, except:

- **`../mentorhub`** — platform standards and shared documentation (e.g. `DeveloperEdition/standards/data_standards.md`).
- **`../mentorhub_api_utils`** — shared Python MongoIO utilities used by domain APIs

Do **not** reference paths under any domain API repos, SPAs, or CloudFormation repos in task **Context** or **Goals**. If work in another repository is a prerequisite, describe it as an **external prerequisite** in prose (e.g. “MongoDB dictionary must include field X”) and set **Status** to `Blocked` until a human confirms it — do not link to or read files in that repo.
