# T111 – Import Obsidian Topic Resources Test Data

**Status**: Shipped  
**Task Type**: Feature  
**Run Mode**: Sequential  

## User inputs (edit before running)

- **Dictionary file** `../configurator/dictionaries/Resource.0.1.0.yaml`
- **Enumerators file** `../configurator/enumerators/enumerations.0.yaml`
- **Target test-data file** `../configurator/test_data/Resource.0.1.0.0.json`
- **Obsidian source directory** `../Tasks/obsidian files/` (topic files only — **exclude** the `Paths/` subdirectory)
- **Number of documents to generate**: All harvestable resources (~150+ topic files; expect hundreds of individual resource links after deduplication by URL)
- **Special requirements**
  - Harvest every resource link from Mike's Obsidian topic markdown exports.
  - **Synthesize** human-readable `name` and `description` values; do not leave placeholder text.
  - Use a **variety** of enum values for `type`, `cost`, `skill_level`, `interests`, `technologies`, and `status` across the dataset.
  - Ensure **every** enum value in `resource_type`, `Costs`, `Skills`, `interests`, `technologies`, and `resource_status` appears at least once across all generated Resource documents.
  - Assign deterministic `_id` values starting at `{ "$oid": "B00000000000000000000001" }`, incrementing sequentially in harvest order (topic file name sort, then resource order within file).
  - Set most resources to `status`: `active`; include a small number (`failed`) for demo/testing of broken links.

## Goal

Parse Obsidian topic markdown files and generate schema-compliant EJSON Resource documents in `Resource.0.1.0.0.json`.

## Context / Input files

These files must be treated as **inputs** and read before implementation:

- The **Dictionary** and **Enumerators** linked in **User inputs**.
- The [type files](../configurator/types/) — especially `word.yaml` (`^[^\s]{1,40}$` for `name`).
- [Data standards](../../mentorhub/DeveloperEdition/standards/data_standards.md).
- `../Tasks/obsidian files/*.md` — **156** topic files (all markdown in the root of `obsidian files/`, not under `Paths/`).
- [SHIPPED.T103.generate_resource_test_data.md](./SHIPPED.T103.generate_resource_test_data.md) — prior harvest approach (engineerkit modules); use as a pattern reference only.
- [PENDING.T110.clear_resource_and_path_test_data.md](./PENDING.T110.clear_resource_and_path_test_data.md) — must be complete; target file should be `[]` before this task runs.

### Obsidian topic file format

Topic files follow a consistent structure. Examples:

**Standard topic** (`Collecting Logs, Errors, Metrics, and Traces.md`):

```markdown
# Topic [[Collecting Logs, Errors, Metrics, and Traces]]
With this topic, you'll learn about...

## Resources
   * [DataDog `Tool`](https://datadoghq.com/)
   * [Grafana Explained in Under 5 Minutes `Video`](https://www.youtube.com/watch?v=...)
```

**Alternate checklist format** (`FIgma.md`):

```markdown
# Topic [[FIgma]]
Figma is a popular tool for...

## Resources
- [ ] [What is Figma](https://help.figma.com/...)
```

**Resource link patterns to parse**:

1. `[Title \`TypeHint\`](url)` — type hint in backticks (e.g. `Video`, `Article`, `Tool`, `Book ($)`, `Tutorial`, `Thread`).
2. `- [ ] [Title](url)` — infer `type` from URL/title when no backtick hint is present.
3. `- [Title \`Type\`](url)` checklist variants.

**Per-topic metadata to harvest**:

- Topic title from `# Topic [[Name]]` or `# [[Name]]`.
- Topic description from the first non-heading paragraph after the title (or synthesize one sentence from the title + skills list).
- Skills bullets under `## Skills` — use to inform `description` and enum tagging.

### Type-hint → `resource_type` mapping (infer when missing)

| Obsidian hint | `resource_type` |
| --- | --- |
| `Video` | `video` |
| `Article`, `Thread` | `article` |
| `Book`, `Book ($)` | `book` |
| `Tutorial`, `Tool`, `Getting Started` | `tutorial` or `getting-started` |
| `Manual`, `Docs` | `manual` |
| `Lesson` | `lesson` |
| `Class`, `Course` | `online-class` |
| YouTube URLs | `video` |
| amazon.com / book retailers | `book` |
| Default | `article` |

### Cost inference from hints and URLs

| Signal | `cost` |
| --- | --- |
| `Book ($)` or paid book links | `$$` or `$$$` |
| Free docs, OSS tools, YouTube, blog posts | `free` |
| Paid course platforms without explicit price | `$`–`$$` |
| Subscription/membership landing pages | `S$`–`S$$$` |

Vary costs deliberately so all `Costs` enum values appear at least once.

### Interests / technologies tagging

Infer from topic title, path context, and URL keywords:

- SRE/monitoring/ops topics → `interests`: `sre`; technologies: `Other` (until expanded).
- Design/UX/Figma/Material topics → `interests`: `design`, `ux`.
- Python topics → `interests`: `data` or `api`; `technologies`: `Python`.
- React/Node/HTML/CSS/JS topics → matching `technologies` enum values.
- Default at least one interest per resource; use `Other` technology when no match.

### `skill_level` guidance

- Foundational/basics topics → `Apprentice` or `Candidate`.
- Intermediate Odin/engineering topics → `Practioneer`.
- Advanced/specialty topics → `Craftsperson` or `Master`.
- Distribute all `Skills` enum values across the dataset.

## Requirements

1. **EJSON encoding**
   - `_id` and identifier references: `{ "$oid": "<24-byte hex>" }`.
   - `last_verified`, breadcrumb `at_time`: `{ "$date": "<ISO-8601>" }`.

2. **Schema-driven generation**
   - Every document includes: `_id`, `name`, `description`, `url`, `type`, `cost`, `skill_level`, `interests`, `technologies`, `last_verified`, `status`, `created`, `saved`.
   - `name` must satisfy the `word` pattern (no spaces; max 40 chars). Derive from resource title (e.g. `GrafanaExplained`, `DataDog`, `TenUsabilityHeuristics`).
   - `description` is a single sentence synthesizing what the learner gains from the resource.
   - Deduplicate by URL; if the same URL appears in multiple topics, keep one Resource document and note both topic associations in implementation notes.

3. **Enum coverage**
   - Every value in `resource_type`, `Costs`, `Skills`, `interests`, `technologies`, and `resource_status` must appear at least once.

4. **Breadcrumbs**
   - Match style from `Identity.0.1.0.0.json` and `Plan.0.1.0.0.json` (`created`/`saved` with `at_time`, `by_user`, `correlation_id`, `from_ip`).

5. **Skip / handle edge cases**
   - Skip placeholder topics/files named `Topic Name` with no real resources.
   - Skip Obsidian wikilinks without URLs (those resolve in Path task T112).
   - Files with empty `## Resources` sections produce no resources but should be noted.

## Testing expectations

- **Processing test**
  - `curl -X DELETE "http://localhost:8385/api/database/" -H "accept: application/json"`
  - `curl -X POST "http://localhost:8385/api/configurations/" -H "accept: application/json"`
  - Validate `SUCCESS`.
- **Packaging test**
  - `make container` → SUCCESS.
  - `make process` → SUCCESS in `artifacts/process_all_configurations.json`.

## Dependencies / Ordering

- **Depends on** [PENDING.T110](./PENDING.T110.clear_resource_and_path_test_data.md).
- **Blocks** [PENDING.T112](./PENDING.T112.import_obsidian_paths_test_data.md), [PENDING.T113](./PENDING.T113.practitioner_sre_membership_path.md), and [PENDING.T114](./PENDING.T114.practitioner_uiux_path.md).

## Change control checklist

- [x] Reviewed all **Context / Input files** and sampled topic markdown formats.
- [x] Generated Resource test data from Obsidian topic files.
- [x] Verified enum coverage across the dataset.
- [x] Ran `make container` successfully.
- [x] Ran `make process` successfully.
- [ ] Created a scoped commit referencing this task ID.

## Implementation notes (to be updated by the agent)

**Summary of changes**

Generated **716** Obsidian-harvested Resource documents in `configurator/test_data/Resource.0.1.0.0.json` via `Tasks/scripts/generate_obsidian_test_data.py` (T113/T114 append 7 membership/additional resources for **723** total).

**Approach**

- Parsed **156** topic markdown files under `Tasks/obsidian files/` (excluding `Paths/`).
- Extracted links from `## Resources` sections supporting both backtick type hints and Figma-style checklist links.
- Deduplicated by URL; assigned sequential `B000…` ids.
- Inferred `type`, `cost`, `skill_level`, `interests`, and `technologies` from type hints, URLs, and topic context.
- Patched tail documents to ensure all enum values appear at least once (including `audio`, `failed` status).

**Testing results**

- `make container` → SUCCESS.
- `POST /api/configurations/` → SUCCESS.
