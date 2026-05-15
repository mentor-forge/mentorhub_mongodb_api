This folder contains coding tasks that an agent can execute, based on the context and instructions in each task file.

### Execution model: Orchestration agent (recommended)

For multi-task pipelines, use an **orchestration agent** that spawns a **fresh agent per task**:

1. **Orchestrator** discovers all tasks, respects dependencies, and determines execution order.
2. **For each task**, the orchestrator launches a new agent with:
   - The task file path
   - Paths to input/context files listed in the task
   - Any outputs from prior tasks (e.g. "R160 complete; template_service.py updated")
3. **Sub-agent** executes only that task: read context, implement, test, update task notes, commit.
4. **Orchestrator** moves to the next task. On failure, it can retry or skip and continue.

**Benefits**: Fresh context per task (no drift), clear boundaries, easier retries, dependency-aware ordering. Independent tasks (e.g. R100, R150, R160) can be run in parallel if the orchestrator supports it.

**Handoff**: Each sub-agent receives the task file and its input files. Task files should be self-contained so a new agent can pick up without prior session memory.

### Task execution workflow

The steps below apply to the agent that executes a task (whether a sub-agent launched by an orchestrator or a single long-running agent).

1. **Review all tasks** (or the current task, if orchestrated)
   - Each task is a markdown file in this folder (e.g., `T001_add_healthcheck.md`).
   - The agent should first **list all tasks**, then determine the **execution order** (see **Task ordering** below)—or, under orchestration, receive the current task from the orchestrator.
   - For each task, read the entire file before starting work.

2. **Execute one task at a time**
   - Pick the **next eligible task** (not completed, not "Run as needed", and in order).
   - Follow the **Task lifecycle** (analysis → implementation → testing → completion notes → change control).
   - Do not start another task until the current one is finished or explicitly deferred.

3. **Change control for each task**
   For every task, the agent should:
   - **Review context**: Read all referenced input/context files.
   - **Plan changes**: Summarize the planned approach in the notes section of the task file.
   - **Implement changes**: Update code, configuration, docs, etc., as required.
   - **Testing**:
     - Run any tests or commands listed in the task file’s **Testing expectations** section.
     - In this repo, that typically means:
       - `make container` – build the MongoDB Configurator API container image.
       - `make process` – call the Configure Database API endpoint (`POST /api/configurations/`) and validate the event JSON with `jq`.
   - **Packaging verification**:
     - Use `make container` as the packaging/build gate for this repo.
   - **Commit gating**:
     - Only create a commit once testing and packaging verification have passed.

4. **Completion and documentation**
   - Update the task file’s **status** and **implementation notes**.
   - Rename the task file to reflect it's new status.
   - If follow‑ups are discovered, add them as new tasks instead of over‑expanding the current one.

### Task ordering

- **Primary mechanism**: A task’s filename should start **STATUS** and a sortable prefix (e.g., `PENDING.T001_`, `PENDING.T002_`, `PENDING.T010_`).
- **Execution order**:
  - Sort all task files by filename.
  - Skip tasks explicitly marked as **Run as needed** (see below).
  - Skip tasks with status **Shipped**.
  - Process remaining tasks in sorted order.
- **Manual overrides**:
  - If a task must run earlier/later, note this in the task’s **Dependencies / Ordering** section; the agent should respect these dependencies when building its execution plan.

### Task status, categories, and filenames

Each task file should declare status and type **inside the file**, and also encode the status in the **filename prefix** so tasks are visually grouped in the IDE.

- **Lifecycle statuses (in‑file)**:
  - `Pending`: Not yet started.
  - `Running`: Work is currently being done in the active session.
  - `Blocked`: Waiting on some external dependency or decision.
  - `Shipped`: Implemented, tested, and merged/committed as per the change control process.
  - `Run as needed`: Not part of the main long‑running sequence; to be run manually or opportunistically.

- **Filename status prefixes (for grouping)**:
  - `AS_NEEDED.` – Tasks that should **not** be part of the main long‑running sequence.
  - `BLOCKED.` – Tasks currently blocked.
  - `PENDING.` – Tasks that are ready to be picked up when their turn comes.
  - `RUNNING.` – (Optional) Tasks currently being executed in this session.
  - `SHIPPED.` – Tasks that are fully implemented and completed.

- **Recommended filename pattern**:
  - `STATUS.RNNN.short_task_name.md`
  - Examples:
    - `AS_NEEDED.R900.example_add_healthcheck.md`
    - `PENDING.R010.add_healthcheck_endpoint.md`
    - `RUNNING.R050.implement_bulk_import.md`
    - `SHIPPED.R100.configure_ci_pipeline.md`

- **Task type** (in‑file, optional but helpful):
  - `Feature`, `Refactor`, `Bugfix`, `Chore`, `Docs`, etc.

### Sample task file

For a complete example of a well‑formed `Run as needed` task (including context files, testing expectations, change control checklist, and implementation notes), see:

- `AS_NEEDED.R900.example_add_healthcheck.md`

### Marking a task as completed or "Run as needed"

- **Completed task**:
  - Update `Status` to `Completed`.
  - Fill in the **Implementation notes** and **Testing results** while the work and test commands are still fresh.
  - Ensure all items in the **Change control checklist** are checked or explicitly commented if intentionally skipped (with rationale).
  - **Only after testing passes and packaging verification succeeds** (for this repo: `make container`, and where applicable `make process`), create a scoped commit referencing this task ID.

- **Run as needed task**:
  - The long‑running agent should **not** include these tasks in its default sequential run; they are to be invoked manually when appropriate.

---

With this structure, an agent (orchestrator or task executor) can:
- Discover tasks by listing markdown files in this folder.
- Determine order and eligibility based on filenames, `Status`, and `Run Mode`.
- Apply a consistent change control process (analysis, testing, packaging, commit) for each task.
